"""
Film İzleme Sayacı - OMDB Zenginleştirilmiş İçerik Bazlı Film Önerme Sistemi
Bu modül, OMDB API ile zenginleştirilmiş film verilerini kullanarak gelişmiş öneriler sunar.
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Union, Dict, Any
import re


class OMDBEnhancedRecommender:
    """
    OMDB API ile zenginleştirilmiş içerik bazlı film önerme sistemi.
    
    Bu sınıf, OMDB API'den alınan detaylı film metadata'sını (tür, yönetmen, 
    oyuncular, özet, ödüller, dil, ülke) kullanarak daha gelişmiş öneriler sunar.
    """
    
    def __init__(self, movie_data_path: str):
        """
        OMDBEnhancedRecommender sınıfını başlatır.
        
        Args:
            movie_data_path (str): OMDB ile zenginleştirilmiş film verilerini içeren CSV dosyasının yolu
        """
        try:
            # CSV dosyasını DataFrame'e yükle
            self.df = pd.read_csv(movie_data_path)
            print(f"📊 Veriset yüklendi: {len(self.df)} film")
            
            # Temel sütunları kontrol et
            required_columns = ['movie_id', 'title']
            missing_columns = [col for col in required_columns if col not in self.df.columns]
            if missing_columns:
                raise ValueError(f"CSV dosyasında eksik temel sütunlar: {missing_columns}")
            
            # OMDB sütunlarını kontrol et ve eksik olanları ekle
            omdb_columns = {
                'omdb_genre': 'genres',
                'omdb_director': 'director', 
                'omdb_actors': 'actors',
                'omdb_plot': 'plot_summary',
                'omdb_language': 'language',
                'omdb_country': 'country',
                'omdb_awards': 'awards',
                'omdb_imdb_rating': 'imdb_rating',
                'omdb_metascore': 'metascore',
                'omdb_runtime': 'runtime',
                'omdb_year': 'year'
            }
            
            # Fallback sütunları tanımla (eski format desteği için)
            fallback_columns = {
                'genres': 'genres',
                'director': 'director',
                'actors': 'actors', 
                'plot_summary': 'plot_summary'
            }
            
            # Her OMDB sütunu için kontrol yap
            for omdb_col, standard_col in omdb_columns.items():
                if omdb_col in self.df.columns:
                    # OMDB sütunu varsa onu kullan
                    self.df[standard_col] = self.df[omdb_col].fillna('')
                elif standard_col in self.df.columns:
                    # OMDB sütunu yoksa fallback kullan
                    self.df[standard_col] = self.df[standard_col].fillna('')
                elif standard_col in fallback_columns and fallback_columns[standard_col] in self.df.columns:
                    # Fallback sütunu varsa onu kullan
                    self.df[standard_col] = self.df[fallback_columns[standard_col]].fillna('')
                else:
                    # Hiçbiri yoksa boş sütun oluştur
                    self.df[standard_col] = ''
            
            # Sayısal sütunları temizle
            self._clean_numeric_columns()
            
            # Özellik vektörlerini oluştur
            self._create_feature_vectors()
            
            print(f"✅ Başarıyla hazırlandı: {self.tfidf_matrix.shape[1]} özellik")
            
        except FileNotFoundError:
            raise FileNotFoundError(f"CSV dosyası bulunamadı: {movie_data_path}")
        except Exception as e:
            raise Exception(f"Başlatma hatası: {str(e)}")
    
    def _clean_numeric_columns(self):
        """Sayısal sütunları temizle ve dönüştür"""
        
        # IMDB rating temizle
        if 'imdb_rating' in self.df.columns:
            self.df['imdb_rating_numeric'] = pd.to_numeric(
                self.df['imdb_rating'].astype(str).str.replace('N/A', '0'), 
                errors='coerce'
            ).fillna(0)
        
        # Metascore temizle
        if 'metascore' in self.df.columns:
            self.df['metascore_numeric'] = pd.to_numeric(
                self.df['metascore'].astype(str).str.replace('N/A', '0'), 
                errors='coerce'
            ).fillna(0)
        
        # Runtime temizle (sadece dakika değeri)
        if 'runtime' in self.df.columns:
            self.df['runtime_numeric'] = self.df['runtime'].astype(str).apply(
                lambda x: self._extract_minutes(x)
            )
        
        # Year temizle
        if 'year' in self.df.columns:
            self.df['year_numeric'] = pd.to_numeric(
                self.df['year'].astype(str).str.extract(r'(\d{4})')[0], 
                errors='coerce'
            ).fillna(0)
    
    def _extract_minutes(self, runtime_str: str) -> int:
        """Runtime string'inden dakika değerini çıkar"""
        try:
            # "120 min" formatındaki değerleri çıkar
            match = re.search(r'(\d+)', str(runtime_str))
            return int(match.group(1)) if match else 0
        except:
            return 0
    
    def _create_feature_vectors(self):
        """Gelişmiş özellik vektörleri oluştur"""
        
        # Temel metin özelliklerini birleştir
        text_features = []
        
        for _, row in self.df.iterrows():
            # Ana özellikler
            features_text = []
            
            # Türler (ağırlıklı)
            genres = str(row['genres']).replace(',', ' ')
            features_text.append(genres + ' ' + genres)  # Türleri 2 kez ekle (ağırlık için)
            
            # Yönetmen (ağırlıklı)
            director = str(row['director'])
            features_text.append(director + ' ' + director)  # Yönetmeni 2 kez ekle
            
            # Ana oyuncular
            actors = str(row['actors'])
            features_text.append(actors)
            
            # Özet
            plot = str(row['plot_summary'])
            features_text.append(plot)
            
            # Dil (önemli özellik)
            if 'language' in row and pd.notna(row['language']):
                language = str(row['language'])
                features_text.append(language)
            
            # Ülke
            if 'country' in row and pd.notna(row['country']):
                country = str(row['country'])
                features_text.append(country)
            
            # Ödüller (varsa ağırlık ver)
            if 'awards' in row and pd.notna(row['awards']):
                awards = str(row['awards'])
                if 'Oscar' in awards or 'Emmy' in awards or 'Golden Globe' in awards:
                    features_text.append(awards + ' ' + awards)  # Önemli ödülleri 2 kez ekle
                else:
                    features_text.append(awards)
            
            # Rating kategorisi ekle
            if hasattr(self, 'imdb_rating_numeric') and 'imdb_rating_numeric' in row:
                rating = row['imdb_rating_numeric']
                if rating >= 8.0:
                    features_text.append('excellent_rating')
                elif rating >= 7.0:
                    features_text.append('good_rating')
                elif rating >= 6.0:
                    features_text.append('average_rating')
            
            # Süre kategorisi ekle
            if hasattr(self, 'runtime_numeric') and 'runtime_numeric' in row:
                runtime = row['runtime_numeric']
                if runtime >= 150:
                    features_text.append('long_movie')
                elif runtime >= 90:
                    features_text.append('standard_movie')
                elif runtime > 0:
                    features_text.append('short_movie')
            
            # Dekad bilgisi ekle
            if hasattr(self, 'year_numeric') and 'year_numeric' in row:
                year = row['year_numeric']
                if year >= 2020:
                    features_text.append('decade_2020s')
                elif year >= 2010:
                    features_text.append('decade_2010s')
                elif year >= 2000:
                    features_text.append('decade_2000s')
                elif year >= 1990:
                    features_text.append('decade_1990s')
                elif year >= 1980:
                    features_text.append('decade_1980s')
                elif year > 0:
                    features_text.append('classic_era')
            
            # Tüm özellikleri birleştir
            combined_features = ' '.join(features_text)
            text_features.append(combined_features)
        
        # Features sütununu DataFrame'e ekle
        self.df['features'] = text_features
        
        # TF-IDF vektörleştirici oluştur
        self.tfidf_vectorizer = TfidfVectorizer(
            stop_words='english',
            max_features=8000,  # Daha fazla özellik (OMDB verisi zengin)
            ngram_range=(1, 2),  # Unigram ve bigram
            min_df=2,  # En az 2 filmde geçen terimler
            max_df=0.8   # Çok yaygın terimleri filtrele
        )
        
        # Features sütununu TF-IDF matrisine dönüştür
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.df['features'])
    
    def _get_user_profile(self, watched_movie_indices: List[int]) -> np.ndarray:
        """
        Kullanıcının izlediği filmlere dayanarak gelişmiş kullanıcı profili oluşturur.
        
        Args:
            watched_movie_indices (List[int]): İzlenen filmlerin DataFrame indeksleri
            
        Returns:
            np.ndarray: Kullanıcının zevk profilini temsil eden ağırlıklı vektör
        """
        if not watched_movie_indices:
            raise ValueError("İzlenen film listesi boş olamaz")
        
        # İzlenen filmlerin TF-IDF vektörlerini al
        watched_vectors = self.tfidf_matrix[watched_movie_indices]
        
        # Ağırlıklı ortalama hesapla (yüksek rating'li filmlere daha fazla ağırlık ver)
        weights = []
        for idx in watched_movie_indices:
            # IMDB rating'e göre ağırlık hesapla
            if hasattr(self.df.iloc[idx], 'imdb_rating_numeric'):
                rating = self.df.iloc[idx]['imdb_rating_numeric']
                weight = max(0.5, rating / 10.0)  # 0.5-1.0 arası ağırlık
            else:
                weight = 1.0
            weights.append(weight)
        
        # Ağırlıkları normalize et
        weights = np.array(weights)
        weights = weights / weights.sum()
        
        # Ağırlıklı ortalama al
        user_profile_vector = np.average(watched_vectors.toarray(), axis=0, weights=weights)
        
        return user_profile_vector
    
    def get_recommendations(self, watched_movie_ids: List[int], num_recommendations: int = 10) -> List[Dict[str, Any]]:
        """
        Kullanıcının izlediği filmlere dayanarak gelişmiş film önerileri üretir.
        
        Args:
            watched_movie_ids (List[int]): Kullanıcının izlediği filmlerin ID'leri
            num_recommendations (int): Önerilecek film sayısı (varsayılan: 10)
            
        Returns:
            List[Dict[str, Any]]: Önerilen filmlerin detaylı bilgilerini içeren liste
        """
        if not watched_movie_ids:
            raise ValueError("İzlenen film ID listesi boş olamaz")
        
        if num_recommendations <= 0:
            raise ValueError("Öneri sayısı pozitif olmalıdır")
        
        # İzlenen film ID'lerinin DataFrame'deki indekslerini bul
        watched_movie_indices = []
        found_movies = []
        
        for movie_id in watched_movie_ids:
            indices = self.df[self.df['movie_id'] == movie_id].index.tolist()
            if indices:
                watched_movie_indices.extend(indices)
                found_movies.append(movie_id)
            else:
                print(f"⚠️  Film ID {movie_id} veri setinde bulunamadı")
        
        if not watched_movie_indices:
            raise ValueError("Hiçbir izlenen film veri setinde bulunamadı")
        
        print(f"📊 OMDB profil oluşturuluyor: {len(found_movies)} film kullanılıyor")
        
        # Kullanıcı profil vektörünü hesapla
        user_profile_vector = self._get_user_profile(watched_movie_indices)
        
        # Tüm filmlerle benzerlik skorlarını hesapla
        similarity_scores = cosine_similarity([user_profile_vector], self.tfidf_matrix)[0]
        
        # Film indeksleri ile benzerlik skorlarını eşleştir
        movie_similarities = list(enumerate(similarity_scores))
        
        # Benzerlik skoruna göre sırala (en yüksekten en düşüğe)
        movie_similarities.sort(key=lambda x: x[1], reverse=True)
        
        # İzlenen filmleri çıkar ve önerileri topla
        recommendations = []
        seen_movie_ids = set(watched_movie_ids)
        
        for movie_index, similarity_score in movie_similarities:
            movie_id = self.df.iloc[movie_index]['movie_id']
            
            # İzlenen filmler listesinde değilse ve skor 0'dan büyükse ekle
            if movie_id not in seen_movie_ids and similarity_score > 0:
                row = self.df.iloc[movie_index]
                
                recommendation = {
                    'movie_id': int(movie_id),
                    'title': row['title'],
                    'genres': row['genres'],
                    'director': row['director'],
                    'actors': row['actors'],
                    'similarity_score': float(similarity_score)
                }
                
                # OMDB verileri varsa ekle
                if 'imdb_rating' in row and pd.notna(row['imdb_rating']):
                    recommendation['imdb_rating'] = row['imdb_rating']
                
                if 'year' in row and pd.notna(row['year']):
                    recommendation['year'] = row['year']
                
                if 'runtime' in row and pd.notna(row['runtime']):
                    recommendation['runtime'] = row['runtime']
                
                recommendations.append(recommendation)
                
                # İstenen sayıya ulaştıysak dur
                if len(recommendations) >= num_recommendations:
                    break
        
        print(f"🎬 {len(recommendations)} gelişmiş film önerisi oluşturuldu")
        return recommendations
    
    def get_movie_info(self, movie_id: int) -> Dict[str, Any]:
        """
        Belirli bir filmin detaylı bilgilerini getirir.
        
        Args:
            movie_id (int): Film ID'si
            
        Returns:
            Dict[str, Any]: Film bilgileri (OMDB verileri dahil)
        """
        movie_row = self.df[self.df['movie_id'] == movie_id]
        
        if movie_row.empty:
            raise ValueError(f"Film ID {movie_id} bulunamadı")
        
        row = movie_row.iloc[0]
        
        # Temel bilgiler
        movie_info = {
            'movie_id': int(row['movie_id']),
            'title': row['title'],
            'genres': row['genres'],
            'director': row['director'],
            'actors': row['actors'],
            'plot_summary': row['plot_summary']
        }
        
        # OMDB verileri varsa ekle
        omdb_fields = {
            'year': 'year',
            'runtime': 'runtime',
            'language': 'language',
            'country': 'country',
            'awards': 'awards',
            'imdb_rating': 'imdb_rating',
            'metascore': 'metascore',
            'box_office': 'box_office'
        }
        
        for field, key in omdb_fields.items():
            if field in row and pd.notna(row[field]) and str(row[field]) != 'N/A':
                movie_info[key] = row[field]
        
        return movie_info
    
    def search_movies(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Film başlığında gelişmiş arama yapar.
        
        Args:
            query (str): Arama terimi
            max_results (int): Maksimum sonuç sayısı
            
        Returns:
            List[Dict[str, Any]]: Bulunan filmlerin listesi (OMDB verileri dahil)
        """
        if not query.strip():
            raise ValueError("Arama terimi boş olamaz")
        
        # Başlıkta arama yap (büyük/küçük harf duyarsız)
        matches = self.df[self.df['title'].str.contains(query, case=False, na=False)]
        
        # IMDB rating'e göre sırala (varsa)
        if 'imdb_rating_numeric' in self.df.columns:
            matches = matches.sort_values('imdb_rating_numeric', ascending=False)
        
        results = []
        for _, row in matches.head(max_results).iterrows():
            result = {
                'movie_id': int(row['movie_id']),
                'title': row['title'],
                'genres': row['genres'],
                'director': row['director']
            }
            
            # OMDB verileri varsa ekle
            if 'imdb_rating' in row and pd.notna(row['imdb_rating']) and str(row['imdb_rating']) != 'N/A':
                result['imdb_rating'] = row['imdb_rating']
            
            if 'year' in row and pd.notna(row['year']):
                result['year'] = row['year']
            
            results.append(result)
        
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Gelişmiş veri seti istatistiklerini döndürür.
        
        Returns:
            Dict[str, Any]: İstatistik bilgileri (OMDB verileri dahil)
        """
        stats = {
            'total_movies': len(self.df),
            'unique_directors': self.df['director'].nunique(),
            'feature_dimensions': self.tfidf_matrix.shape[1],
            'genres_distribution': self.df['genres'].value_counts().head().to_dict()
        }
        
        # OMDB verileri varsa ekle
        if 'omdb_enriched' in self.df.columns:
            enriched_count = len(self.df[self.df['omdb_enriched'] == 'True'])
            stats['omdb_enriched_count'] = enriched_count
            stats['omdb_enrichment_rate'] = f"{(enriched_count / len(self.df) * 100):.1f}%"
        
        if 'imdb_rating_numeric' in self.df.columns:
            ratings = self.df['imdb_rating_numeric']
            ratings = ratings[ratings > 0]  # 0'ları filtrele
            if len(ratings) > 0:
                stats['avg_imdb_rating'] = f"{ratings.mean():.1f}"
                stats['movies_with_rating'] = len(ratings)
        
        if 'year_numeric' in self.df.columns:
            years = self.df['year_numeric']
            years = years[years > 0]  # 0'ları filtrele
            if len(years) > 0:
                stats['year_range'] = f"{int(years.min())}-{int(years.max())}"
        
        return stats
