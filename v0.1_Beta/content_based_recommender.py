"""
Film İzleme Sayacı - İçerik Bazlı Film Önerme Sistemi
Bu modül, kullanıcının izlediği filmlere dayanarak benzer filmleri önerir.
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Union, Dict, Any


class ContentBasedRecommender:
    """
    İçerik bazlı film önerme sistemi.
    
    Bu sınıf, filmlerin metadata'sını (tür, yönetmen, oyuncular, özet) kullanarak
    kullanıcının izlediği filmlere benzer filmler önerir.
    """
    
    def __init__(self, movie_data_path: str):
        """
        ContentBasedRecommender sınıfını başlatır.
        
        Args:
            movie_data_path (str): Film verilerini içeren CSV dosyasının yolu
        """
        try:
            # CSV dosyasını DataFrame'e yükle
            self.df = pd.read_csv(movie_data_path)
            
            # Gerekli sütunların varlığını kontrol et
            required_columns = ['movie_id', 'title', 'genres', 'director', 'actors', 'plot_summary']
            missing_columns = [col for col in required_columns if col not in self.df.columns]
            if missing_columns:
                raise ValueError(f"CSV dosyasında eksik sütunlar: {missing_columns}")
            
            # Eksik değerleri boş string ile doldur
            feature_columns = ['genres', 'director', 'actors', 'plot_summary']
            for col in feature_columns:
                self.df[col] = self.df[col].fillna('')
            
            # Tüm önemli metin verilerini birleştirerek features sütunu oluştur
            self.df['features'] = (
                self.df['genres'] + ' ' +
                self.df['director'] + ' ' +
                self.df['actors'] + ' ' +
                self.df['plot_summary']
            )
            
            # TF-IDF vektörleştirici oluştur
            self.tfidf_vectorizer = TfidfVectorizer(
                stop_words='english',
                max_features=5000,  # Performans için özellik sayısını sınırla
                ngram_range=(1, 2)  # Unigram ve bigram kullan
            )
            
            # Features sütununu TF-IDF matrisine dönüştür
            self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.df['features'])
            
            print(f"✅ Başarıyla yüklendi: {len(self.df)} film, {self.tfidf_matrix.shape[1]} özellik")
            
        except FileNotFoundError:
            raise FileNotFoundError(f"CSV dosyası bulunamadı: {movie_data_path}")
        except Exception as e:
            raise Exception(f"Başlatma hatası: {str(e)}")
    
    def _get_user_profile(self, watched_movie_indices: List[int]) -> np.ndarray:
        """
        Kullanıcının izlediği filmlere dayanarak kullanıcı profil vektörü oluşturur.
        
        Args:
            watched_movie_indices (List[int]): İzlenen filmlerin DataFrame indeksleri
            
        Returns:
            np.ndarray: Kullanıcının zevk profilini temsil eden vektör
        """
        if not watched_movie_indices:
            raise ValueError("İzlenen film listesi boş olamaz")
        
        # İzlenen filmlerin TF-IDF vektörlerini al
        watched_vectors = self.tfidf_matrix[watched_movie_indices]
        
        # Vektörlerin ortalamasını al (kullanıcı profili)
        user_profile_vector = np.mean(watched_vectors.toarray(), axis=0)
        
        return user_profile_vector
    
    def get_recommendations(self, watched_movie_ids: List[int], num_recommendations: int = 10) -> List[Dict[str, Any]]:
        """
        Kullanıcının izlediği filmlere dayanarak film önerileri üretir.
        
        Args:
            watched_movie_ids (List[int]): Kullanıcının izlediği filmlerin ID'leri
            num_recommendations (int): Önerilecek film sayısı (varsayılan: 10)
            
        Returns:
            List[Dict[str, Any]]: Önerilen filmlerin bilgilerini içeren liste
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
        
        print(f"📊 Profil oluşturuluyor: {len(found_movies)} film kullanılıyor")
        
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
                recommendation = {
                    'movie_id': int(movie_id),
                    'title': self.df.iloc[movie_index]['title'],
                    'genres': self.df.iloc[movie_index]['genres'],
                    'director': self.df.iloc[movie_index]['director'],
                    'similarity_score': float(similarity_score)
                }
                recommendations.append(recommendation)
                
                # İstenen sayıya ulaştıysak dur
                if len(recommendations) >= num_recommendations:
                    break
        
        print(f"🎬 {len(recommendations)} film önerisi oluşturuldu")
        return recommendations
    
    def get_movie_info(self, movie_id: int) -> Dict[str, Any]:
        """
        Belirli bir filmin bilgilerini getirir.
        
        Args:
            movie_id (int): Film ID'si
            
        Returns:
            Dict[str, Any]: Film bilgileri
        """
        movie_row = self.df[self.df['movie_id'] == movie_id]
        
        if movie_row.empty:
            raise ValueError(f"Film ID {movie_id} bulunamadı")
        
        movie_info = {
            'movie_id': int(movie_row.iloc[0]['movie_id']),
            'title': movie_row.iloc[0]['title'],
            'genres': movie_row.iloc[0]['genres'],
            'director': movie_row.iloc[0]['director'],
            'actors': movie_row.iloc[0]['actors'],
            'plot_summary': movie_row.iloc[0]['plot_summary']
        }
        
        return movie_info
    
    def search_movies(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Film başlığında arama yapar.
        
        Args:
            query (str): Arama terimi
            max_results (int): Maksimum sonuç sayısı
            
        Returns:
            List[Dict[str, Any]]: Bulunan filmlerin listesi
        """
        if not query.strip():
            raise ValueError("Arama terimi boş olamaz")
        
        # Başlıkta arama yap (büyük/küçük harf duyarsız)
        matches = self.df[self.df['title'].str.contains(query, case=False, na=False)]
        
        results = []
        for _, row in matches.head(max_results).iterrows():
            result = {
                'movie_id': int(row['movie_id']),
                'title': row['title'],
                'genres': row['genres'],
                'director': row['director']
            }
            results.append(result)
        
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Veri seti istatistiklerini döndürür.
        
        Returns:
            Dict[str, Any]: İstatistik bilgileri
        """
        stats = {
            'total_movies': len(self.df),
            'unique_directors': self.df['director'].nunique(),
            'feature_dimensions': self.tfidf_matrix.shape[1],
            'genres_distribution': self.df['genres'].value_counts().head().to_dict()
        }
        
        return stats
