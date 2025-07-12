#!/usr/bin/env python3
"""
Wikidata Matematiksel Film Öneri Sistemi
Wikidata veri setine optimize edilmiş content-based öneri algoritması
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from typing import List, Dict, Tuple, Optional

class WikidataMovieRecommender:
    """Wikidata veri setine özel film öneri sistemi"""
    
    def __init__(self, csv_path: str = "test_wikidata_films.csv"):
        """
        Wikidata film veri seti ile öneri sistemini başlat
        
        Args:
            csv_path: Wikidata film CSV dosyasının yolu
        """
        self.df = None
        self.similarity_matrix = None
        self.tfidf_vectorizer = None
        self.feature_weights = {
            'genre': 0.25,              # Tür - en önemli
            'director': 0.20,           # Yönetmen - çok önemli
            'cast': 0.15,               # Oyuncular - önemli
            'year': 0.08,               # Yıl - orta önemli
            'country': 0.06,            # Ülke - orta önemli
            'language': 0.05,           # Dil - düşük önemli
            'composer': 0.04,           # Müzik - önemli
            'screenwriter': 0.04,       # Senarist - önemli
            'production_company': 0.03, # Yapım şirketi - orta
            'budget_range': 0.03,       # Bütçe aralığı - orta
            'box_office_range': 0.02,   # Hasılat aralığı - orta
            'imdb_rating_range': 0.02,  # IMDB puan aralığı - orta
            'duration_range': 0.02,     # Süre aralığı - düşük
            'award_received': 0.04,     # Ödüller - önemli
            'main_subject': 0.03,       # Ana konu - orta
            'description_keywords': 0.02 # Açıklama anahtar kelimeleri - düşük
        }
        
        # Veri setini yükle
        self.load_data(csv_path)
        
    def load_data(self, csv_path: str):
        """Wikidata veri setini yükle ve temizle"""
        try:
            self.df = pd.read_csv(csv_path)
            print(f"✅ Veri seti yüklendi: {len(self.df)} film")
            
            # Veri temizleme
            self.clean_data()
            
            # Özellikleri hazırla
            self.prepare_features()
            
            # Benzerlik matrisini hesapla
            self.calculate_similarity_matrix()
            
        except Exception as e:
            print(f"❌ Veri yükleme hatası: {e}")
            raise
    
    def clean_data(self):
        """Veri setini temizle ve normalize et"""
        print("🧹 Veri temizleniyor...")
        
        # Boş değerleri doldur
        self.df = self.df.fillna('')
        
        # Temel sütunları kontrol et
        required_columns = ['title_en', 'qid']
        for col in required_columns:
            if col not in self.df.columns:
                print(f"⚠️  Eksik sütun: {col}")
        
        # Sayısal sütunları temizle
        numeric_columns = ['year', 'imdb_rating_float', 'duration_minutes']
        for col in numeric_columns:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce').fillna(0)
            else:
                self.df[col] = 0
        
        # Finansal verileri temizle
        self.clean_financial_data()
        
        # Wikidata ID'lerini temizle - TÜM ÖZELLİKLER (producer, cinematographer, film_editor hariç)
        wikidata_columns = ['genre', 'director', 'cast_member', 'country', 'language',
                           'composer', 'screenwriter', 'production_company', 
                           'award_received', 'main_subject', 'narrative_location',
                           'based_on', 'part_of_series', 'based_on_work', 'distributor',
                           'filming_location', 'executive_producer', 'original_network',
                           'original_broadcaster']
        
        for col in wikidata_columns:
            if col in self.df.columns:
                self.df[col] = self.df[col].astype(str).apply(self.clean_wikidata_ids)
        
        print(f"   Temizlenen veri: {len(self.df)} film")
    
    def clean_wikidata_ids(self, text: str) -> str:
        """Wikidata ID'lerini temizle ve normalize et"""
        if pd.isna(text) or text == '' or text == 'nan':
            return ''
        
        # Q-ID'leri kaldır ve sadece sayı kısımları bırak
        text = str(text)
        
        # Çoklu değerleri ayır
        if '|' in text:
            ids = text.split('|')
        else:
            ids = [text]
        
        # Q-ID'leri temizle
        cleaned_ids = []
        for id_str in ids:
            if id_str.startswith('Q'):
                cleaned_ids.append(id_str)
            else:
                cleaned_ids.append(id_str)
        
        return '|'.join(cleaned_ids[:5])  # Maksimum 5 ID al
    
    def prepare_features(self):
        """TÜM Wikidata özelliklerini hazırla (producer, cinematographer, film_editor hariç)"""
        print("🔧 TÜM özellik vektörleri hazırlanıyor...")
        
        # Temel özellikler
        self.df['genre_features'] = self.df['genre'].apply(self.process_genre_feature)
        self.df['director_features'] = self.df['director'].apply(self.process_director_feature)
        self.df['cast_features'] = self.df['cast_member'].apply(self.process_cast_feature)
        self.df['country_features'] = self.df['country'].apply(self.process_country_feature)
        self.df['language_features'] = self.df['language'].apply(self.process_language_feature)
        
        # Teknik ekip özellikleri (producer, cinematographer, film_editor hariç)
        self.df['composer_features'] = self.df['composer'].apply(self.process_crew_feature)
        self.df['screenwriter_features'] = self.df['screenwriter'].apply(self.process_crew_feature)
        self.df['production_company_features'] = self.df['production_company'].apply(self.process_crew_feature)
        self.df['executive_producer_features'] = self.df.get('executive_producer', pd.Series([''] * len(self.df))).apply(self.process_crew_feature)
        self.df['distributor_features'] = self.df.get('distributor', pd.Series([''] * len(self.df))).apply(self.process_crew_feature)
        
        # Mekan ve kaynak özellikleri
        self.df['narrative_location_features'] = self.df.get('narrative_location', pd.Series([''] * len(self.df))).apply(self.process_location_feature)
        self.df['filming_location_features'] = self.df.get('filming_location', pd.Series([''] * len(self.df))).apply(self.process_location_feature)
        self.df['based_on_features'] = self.df.get('based_on', pd.Series([''] * len(self.df))).apply(self.process_source_feature)
        self.df['based_on_work_features'] = self.df.get('based_on_work', pd.Series([''] * len(self.df))).apply(self.process_source_feature)
        self.df['part_of_series_features'] = self.df.get('part_of_series', pd.Series([''] * len(self.df))).apply(self.process_series_feature)
        self.df['original_network_features'] = self.df.get('original_network', pd.Series([''] * len(self.df))).apply(self.process_network_feature)
        self.df['original_broadcaster_features'] = self.df.get('original_broadcaster', pd.Series([''] * len(self.df))).apply(self.process_network_feature)
        
        # Kategorik özellikler
        self.df['year_decade'] = (self.df['year'] // 10) * 10
        self.df['budget_range'] = self.df['budget_cleaned'].apply(self.categorize_budget)
        self.df['box_office_range'] = self.df['box_office_cleaned'].apply(self.categorize_box_office)
        self.df['imdb_rating_range'] = self.df['imdb_rating_float'].apply(self.categorize_imdb_rating)
        self.df['duration_range'] = self.df['duration_minutes'].apply(self.categorize_duration)
        
        # Ödül özellikleri
        self.df['award_features'] = self.df['award_received'].apply(self.process_award_feature)
        
        # Ana konu özellikleri
        self.df['main_subject_features'] = self.df['main_subject'].apply(self.process_main_subject_feature)
        
        # Açıklama anahtar kelimeleri
        self.df['description_keywords'] = self.df.apply(self.extract_description_keywords, axis=1)
        
        # Birleşik özellik metni oluştur
        self.create_comprehensive_features()
        
        print("   TÜM özellik vektörleri hazırlandı")
    
    def process_genre_feature(self, genre_text: str) -> str:
        """Tür özelliklerini işle - GELİŞTİRMİŞ"""
        if not genre_text or genre_text == '':
            return ''
        
        # Genişletilmiş genre mapping
        genre_mapping = {
            'Q130232': 'drama',
            'Q157443': 'comedy',
            'Q188473': 'action',
            'Q200092': 'horror',
            'Q471839': 'scifi',
            'Q1200678': 'romance',
            'Q182415': 'thriller',
            'Q319221': 'adventure',
            'Q157394': 'fantasy',
            'Q959790': 'crime',
            'Q842256': 'musical',
            'Q1146335': 'documentary',
            'Q2484376': 'mystery',
            'Q645928': 'biography',
            'Q1054574': 'family',
            'Q860626': 'melodrama',
            'Q496523': 'psychological',
            'Q1341051': 'zombie',
            'Q1535153': 'slasher',
            'Q1747837': 'postapocalyptic',
            'Q2297927': 'spy',
            'Q3990883': 'actionthriller',
            'Q11304653': 'survival',
            'Q590103': 'claustrophobic',
            'Q3745430': 'satire',
            'Q5778924': 'blackcomedy',
            'Q109733333': 'political',
            'Q17013749': 'historical',
            'Q25110269': 'ecological',
            'Q652256': 'militaryscifi',
            'Q904447': 'alieninvasion',
            'Q132803402': 'pandora',
            'Q468478': 'space',
            'Q2973181': 'spaceopera',
            'Q1919632': 'supernatural',
            'Q52207399': 'youngadult',
            'Q5258881': 'vampires',
            'Q2137852': 'teenfiction',
            'Q20442589': 'urbanfantasy',
            'Q1188977': 'demonhunter',
            'Q121432339': 'minimalist',
            'Q1361932': 'emotional',
            'Q3072042': 'martialarts',
            'Q2143665': 'animated',
            'Q2096633': 'adult',
            'Q185529': 'erotic',
            'Q1033891': 'epicfantasy',
            'Q3745430': 'satirical',
            'Q1535153': 'superhero',
            'Q1200678': 'romantic',
            'Q2421031': 'gangster',
            'Q185867': 'heist',
            'Q20656232': 'mindbending',
            'Q4425624': 'dreams'
        }
        
        genres = []
        for genre_id in genre_text.split('|'):
            if genre_id in genre_mapping:
                genres.append(genre_mapping[genre_id])
            else:
                # Bilinmeyen genre'ları da dahil et
                genres.append(f"genre_{genre_id}")
        
        return ' '.join(genres)
    
    def process_director_feature(self, director_text: str) -> str:
        """Yönetmen özelliklerini işle"""
        if not director_text or director_text == '':
            return ''
        
        # Yönetmen ID'lerini işle
        directors = director_text.split('|')[:3]  # Maksimum 3 yönetmen
        return ' '.join([f"director_{d}" for d in directors])
    
    def process_cast_feature(self, cast_text: str) -> str:
        """Oyuncu özelliklerini işle"""
        if not cast_text or cast_text == '':
            return ''
        
        # Oyuncu ID'lerini işle (sadece ilk 5 oyuncu)
        cast_members = cast_text.split('|')[:5]
        return ' '.join([f"actor_{c}" for c in cast_members])
    
    def process_country_feature(self, country_text: str) -> str:
        """Ülke özelliklerini işle"""
        if not country_text or country_text == '':
            return ''
        
        # Ülke mapping
        country_mapping = {
            'Q30': 'usa',
            'Q145': 'uk',
            'Q142': 'france',
            'Q183': 'germany',
            'Q38': 'italy',
            'Q29': 'spain',
            'Q668': 'india',
            'Q148': 'china',
            'Q17': 'japan',
            'Q884': 'southkorea'
        }
        
        countries = []
        for country_id in country_text.split('|'):
            if country_id in country_mapping:
                countries.append(country_mapping[country_id])
            else:
                countries.append(country_id.lower())
        
        return ' '.join(countries)
    
    def process_language_feature(self, language_text: str) -> str:
        """Dil özelliklerini işle"""
        if not language_text or language_text == '':
            return ''
        
        # Dil mapping
        language_mapping = {
            'Q1860': 'english',
            'Q150': 'french',
            'Q188': 'german',
            'Q1321': 'spanish',
            'Q652': 'italian',
            'Q9186': 'chinese',
            'Q5885': 'tamil',
            'Q1860': 'english'
        }
        
        languages = []
        for lang_id in language_text.split('|'):
            if lang_id in language_mapping:
                languages.append(language_mapping[lang_id])
            else:
                languages.append(lang_id.lower())
        
        return ' '.join(languages)
    
    def process_crew_feature(self, crew_text: str) -> str:
        """Ekip özelliklerini işle"""
        if not crew_text or crew_text == '':
            return ''
        
        # Ekip ID'lerini işle (sadece ilk 3)
        crew_members = crew_text.split('|')[:3]
        return ' '.join([f"crew_{c}" for c in crew_members])
    
    def process_award_feature(self, award_text: str) -> str:
        """Ödül özelliklerini işle"""
        if not award_text or award_text == '':
            return ''
        
        # Ödül ID'lerini işle
        awards = award_text.split('|')[:5]
        return ' '.join([f"award_{a}" for a in awards])
    
    def process_main_subject_feature(self, subject_text: str) -> str:
        """Ana konu özelliklerini işle"""
        if not subject_text or subject_text == '':
            return ''
        
        # Konu ID'lerini işle
        subjects = subject_text.split('|')[:3]
        return ' '.join([f"subject_{s}" for s in subjects])
    
    def process_location_feature(self, location_text: str) -> str:
        """Mekan özelliklerini işle"""
        if not location_text or location_text == '':
            return ''
        
        # Mekan ID'lerini işle
        locations = location_text.split('|')[:3]
        return ' '.join([f"location_{loc}" for loc in locations])
    
    def process_source_feature(self, source_text: str) -> str:
        """Kaynak eser özelliklerini işle"""
        if not source_text or source_text == '':
            return ''
        
        # Kaynak ID'lerini işle
        sources = source_text.split('|')[:2]
        return ' '.join([f"source_{src}" for src in sources])
    
    def process_series_feature(self, series_text: str) -> str:
        """Seri özelliklerini işle"""
        if not series_text or series_text == '':
            return ''
        
        # Seri ID'lerini işle
        series = series_text.split('|')[:1]  # Genellikle tek seri
        return ' '.join([f"series_{ser}" for ser in series])
    
    def process_network_feature(self, network_text: str) -> str:
        """Ağ/kanal özelliklerini işle"""
        if not network_text or network_text == '':
            return ''
        
        # Ağ ID'lerini işle
        networks = network_text.split('|')[:2]
        return ' '.join([f"network_{net}" for net in networks])
    
    def categorize_budget(self, budget: float) -> str:
        """Bütçeyi kategorize et"""
        if budget == 0:
            return 'unknown_budget'
        elif budget < 1000000:
            return 'low_budget'
        elif budget < 50000000:
            return 'medium_budget'
        else:
            return 'high_budget'
    
    def categorize_box_office(self, box_office: float) -> str:
        """Hasılatı kategorize et"""
        if box_office == 0:
            return 'unknown_box_office'
        elif box_office < 10000000:
            return 'low_box_office'
        elif box_office < 100000000:
            return 'medium_box_office'
        else:
            return 'high_box_office'
    
    def categorize_imdb_rating(self, rating: float) -> str:
        """IMDB puanını kategorize et"""
        if rating == 0:
            return 'no_rating'
        elif rating < 5.0:
            return 'low_rating'
        elif rating < 7.0:
            return 'medium_rating'
        elif rating < 8.0:
            return 'high_rating'
        else:
            return 'excellent_rating'
    
    def categorize_duration(self, duration: float) -> str:
        """Film süresini kategorize et"""
        if duration == 0:
            return 'unknown_duration'
        elif duration < 90:
            return 'short_film'
        elif duration < 120:
            return 'medium_film'
        else:
            return 'long_film'
    
    def extract_description_keywords(self, row: pd.Series) -> str:
        """Açıklama metinlerinden anahtar kelimeler çıkar"""
        keywords = []
        
        # İngilizce açıklamadan anahtar kelimeler
        if 'description_en' in row and row['description_en']:
            desc_en = str(row['description_en']).lower()
            # Basit anahtar kelime çıkarma
            common_keywords = ['war', 'love', 'family', 'death', 'crime', 'police', 'detective', 
                             'murder', 'school', 'friendship', 'revenge', 'money', 'power']
            for keyword in common_keywords:
                if keyword in desc_en:
                    keywords.append(keyword)
        
        # Türkçe açıklamadan anahtar kelimeler
        if 'description_tr' in row and row['description_tr']:
            desc_tr = str(row['description_tr']).lower()
            tr_keywords = ['savaş', 'aşk', 'aile', 'ölüm', 'suç', 'polis', 'dedektif',
                          'cinayet', 'okul', 'arkadaşlık', 'intikam', 'para', 'güç']
            for keyword in tr_keywords:
                if keyword in desc_tr:
                    keywords.append(keyword)
        
        return ' '.join(keywords)

    def create_comprehensive_features(self):
        """TÜM özelliklerden kapsamlı feature vektörü oluştur (producer, cinematographer, film_editor hariç)"""
        combined_features = []
        
        for _, row in self.df.iterrows():
            features = []
            
            # Ağırlıklı temel özellikler
            if row['genre_features']:
                features.extend([row['genre_features']] * 3)  # 3x ağırlık
            
            if row['director_features']:
                features.extend([row['director_features']] * 2)  # 2x ağırlık
            
            if row['cast_features']:
                features.append(row['cast_features'])
            
            # Teknik ekip (producer, cinematographer, film_editor hariç)
            if row['composer_features']:
                features.append(row['composer_features'])
            
            if row['screenwriter_features']:
                features.append(row['screenwriter_features'])
            
            if row['production_company_features']:
                features.append(row['production_company_features'])
            
            if row.get('executive_producer_features'):
                features.append(row['executive_producer_features'])
            
            if row.get('distributor_features'):
                features.append(row['distributor_features'])
            
            # Coğrafi ve dil
            if row['country_features']:
                features.append(row['country_features'])
            
            if row['language_features']:
                features.append(row['language_features'])
            
            # Mekan özellikleri
            if row.get('narrative_location_features'):
                features.append(row['narrative_location_features'])
            
            if row.get('filming_location_features'):
                features.append(row['filming_location_features'])
            
            # Kaynak ve seri özellikleri
            if row.get('based_on_features'):
                features.append(row['based_on_features'])
            
            if row.get('based_on_work_features'):
                features.append(row['based_on_work_features'])
            
            if row.get('part_of_series_features'):
                features.append(row['part_of_series_features'])
            
            # Ağ/kanal özellikleri
            if row.get('original_network_features'):
                features.append(row['original_network_features'])
            
            if row.get('original_broadcaster_features'):
                features.append(row['original_broadcaster_features'])
            
            # Kategorik özellikler
            if row['year_decade'] > 0:
                features.append(f"decade_{int(row['year_decade'])}")
            
            features.append(row['budget_range'])
            features.append(row['box_office_range'])
            features.append(row['imdb_rating_range'])
            features.append(row['duration_range'])
            
            # Ödül ve konu
            if row['award_features']:
                features.append(row['award_features'])
            
            if row['main_subject_features']:
                features.append(row['main_subject_features'])
            
            # Açıklama anahtar kelimeleri
            if row['description_keywords']:
                features.append(row['description_keywords'])
            
            combined_features.append(' '.join(features))
        
        self.df['combined_features'] = combined_features
    
    def calculate_similarity_matrix(self):
        """TF-IDF ve cosine similarity ile benzerlik matrisini hesapla"""
        print("🔢 Benzerlik matrisi hesaplanıyor...")
        
        # TF-IDF vektörize et
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.8
        )
        
        # Boş özellik metinlerini filtrele
        feature_texts = self.df['combined_features'].fillna('').astype(str)
        
        # TF-IDF matrisini oluştur
        tfidf_matrix = self.tfidf_vectorizer.fit_transform(feature_texts)
        
        # Cosine similarity hesapla
        self.similarity_matrix = cosine_similarity(tfidf_matrix)
        
        print(f"   Benzerlik matrisi: {self.similarity_matrix.shape}")
    
    def get_movie_recommendations(self, movie_title: str, n_recommendations: int = 10) -> List[Dict]:
        """Film önerileri al"""
        
        # Film başlığını ara
        movie_matches = self.df[
            self.df['title_en'].str.contains(movie_title, case=False, na=False) |
            self.df['title_tr'].str.contains(movie_title, case=False, na=False)
        ]
        
        if movie_matches.empty:
            print(f"❌ Film bulunamadı: {movie_title}")
            return []
        
        # İlk eşleşen filmi al
        target_movie = movie_matches.iloc[0]
        movie_idx = movie_matches.index[0]
        
        print(f"🎬 Hedef film: {target_movie['title_en']} ({target_movie['year']})")
        
        # Benzerlik skorlarını al
        similarity_scores = self.similarity_matrix[movie_idx]
        
        # Skorları sırala (kendisi hariç)
        similar_indices = np.argsort(similarity_scores)[::-1][1:n_recommendations+1]
        
        # Önerileri hazırla
        recommendations = []
        for idx in similar_indices:
            similar_movie = self.df.iloc[idx]
            similarity_score = similarity_scores[idx]
            
            # Benzerlik nedenlerini analiz et
            similarity_reasons = self.analyze_similarity_reasons(target_movie, similar_movie)
            
            recommendation = {
                'title': similar_movie['title_en'],
                'title_tr': similar_movie.get('title_tr', ''),
                'year': int(similar_movie['year']) if similar_movie['year'] > 0 else 'N/A',
                'director': similar_movie.get('director', ''),
                'genre': similar_movie.get('genre', ''),
                'imdb_rating': similar_movie.get('imdb_rating_float', 0),
                'similarity_score': float(similarity_score),
                'similarity_reasons': similarity_reasons,
                'wikidata_id': similar_movie['qid'],
                'imdb_id': similar_movie.get('imdb_id', '')
            }
            
            recommendations.append(recommendation)
        
        return recommendations
    
    def get_recommendations_by_ids(self, movie_ids: List[str], n_recommendations: int = 10) -> List[Dict]:
        """Birden fazla film ID'sine dayalı öneriler al"""
        
        if not movie_ids:
            return []
        
        # Film ID'lerini kontrol et
        valid_movies = []
        for movie_id in movie_ids:
            movie_match = self.df[self.df['qid'] == movie_id]  # 'qid' sütununu kullan
            if not movie_match.empty:
                valid_movies.append(movie_match.iloc[0])
        
        if not valid_movies:
            print("❌ Geçerli film bulunamadı")
            return []
        
        print(f"🎬 {len(valid_movies)} film için öneriler hesaplanıyor...")
        
        # Tüm seçili filmlerin benzerlik skorlarını topla
        combined_scores = np.zeros(len(self.df))
        
        for movie in valid_movies:
            movie_idx = self.df[self.df['qid'] == movie['qid']].index[0]  # 'qid' sütununu kullan
            similarity_scores = self.similarity_matrix[movie_idx]
            combined_scores += similarity_scores
        
        # Ortalama benzerlik skoru
        combined_scores = combined_scores / len(valid_movies)
        
        # Seçili filmlerin indekslerini al (bunları hariç tutmak için)
        selected_indices = set()
        for movie in valid_movies:
            movie_idx = self.df[self.df['qid'] == movie['qid']].index[0]  # 'qid' sütununu kullan
            selected_indices.add(movie_idx)
        
        # Skorları sırala (seçili filmler hariç)
        similar_indices = []
        for idx in np.argsort(combined_scores)[::-1]:
            if idx not in selected_indices:
                similar_indices.append(idx)
                if len(similar_indices) >= n_recommendations:
                    break
        
        # Önerileri hazırla
        recommendations = []
        for idx in similar_indices:
            similar_movie = self.df.iloc[idx]
            similarity_score = combined_scores[idx]
            
            # Benzerlik nedenlerini analiz et
            similarity_reasons = self.analyze_similarity_reasons(valid_movies, similar_movie)
            
            recommendation = {
                'wikidata_id': similar_movie['qid'],  # 'qid' sütununu kullan
                'title_en': similar_movie['title_en'],
                'title_tr': similar_movie.get('title_tr', ''),
                'genre': similar_movie.get('genre', ''),
                'director': similar_movie.get('director', ''),
                'cast': similar_movie.get('cast_member', ''),  # 'cast_member' sütununu kullan
                'year': similar_movie.get('year', ''),
                'publication_date': similar_movie.get('publication_date', ''),
                'country': similar_movie.get('country', ''),
                'language': similar_movie.get('language', ''),
                'imdb_rating': similar_movie.get('imdb_rating', ''),
                'imdb_id': similar_movie.get('imdb_id', ''),
                'composer': similar_movie.get('composer', ''),
                'screenwriter': similar_movie.get('screenwriter', ''),
                'production_company': similar_movie.get('production_company', ''),
                'award_received': similar_movie.get('award_received', ''),
                'main_subject': similar_movie.get('main_subject', ''),
                'description': similar_movie.get('description_en', ''),
                'duration': similar_movie.get('duration', ''),
                'budget': similar_movie.get('budget', ''),
                'box_office': similar_movie.get('box_office', ''),
                'similarity_score': similarity_score,
                'similarity_reasons': similarity_reasons
            }
            
            recommendations.append(recommendation)
        
        return recommendations
    
    def analyze_similarity_reasons(self, target_movie: pd.Series, similar_movie: pd.Series) -> List[str]:
        """Benzerlik nedenlerini analiz et - TÜM ÖZELLİKLER"""
        reasons = []
        
        # Tür benzerliği
        if target_movie['genre'] and similar_movie['genre']:
            target_genres = set(target_movie['genre'].split('|'))
            similar_genres = set(similar_movie['genre'].split('|'))
            common_genres = target_genres.intersection(similar_genres)
            if common_genres:
                reasons.append(f"Ortak tür: {len(common_genres)} benzerlik")
        
        # Yönetmen benzerliği
        if target_movie['director'] and similar_movie['director']:
            target_directors = set(target_movie['director'].split('|'))
            similar_directors = set(similar_movie['director'].split('|'))
            common_directors = target_directors.intersection(similar_directors)
            if common_directors:
                reasons.append(f"Ortak yönetmen: {len(common_directors)} benzerlik")
        
        # Oyuncu benzerliği
        if target_movie.get('cast_member') and similar_movie.get('cast_member'):
            target_cast = set(str(target_movie['cast_member']).split('|'))
            similar_cast = set(str(similar_movie['cast_member']).split('|'))
            common_cast = target_cast.intersection(similar_cast)
            if common_cast:
                reasons.append(f"Ortak oyuncu: {len(common_cast)} benzerlik")
        
        # Müzik benzerliği
        if target_movie.get('composer') and similar_movie.get('composer'):
            target_composers = set(str(target_movie['composer']).split('|'))
            similar_composers = set(str(similar_movie['composer']).split('|'))
            common_composers = target_composers.intersection(similar_composers)
            if common_composers:
                reasons.append(f"Ortak müzik: {len(common_composers)} benzerlik")
        
        # Senaryo benzerliği
        if target_movie.get('screenwriter') and similar_movie.get('screenwriter'):
            target_writers = set(str(target_movie['screenwriter']).split('|'))
            similar_writers = set(str(similar_movie['screenwriter']).split('|'))
            common_writers = target_writers.intersection(similar_writers)
            if common_writers:
                reasons.append(f"Ortak senarist: {len(common_writers)} benzerlik")
        
        # Yapım şirketi benzerliği
        if target_movie.get('production_company') and similar_movie.get('production_company'):
            target_companies = set(str(target_movie['production_company']).split('|'))
            similar_companies = set(str(similar_movie['production_company']).split('|'))
            common_companies = target_companies.intersection(similar_companies)
            if common_companies:
                reasons.append(f"Ortak yapım: {len(common_companies)} benzerlik")
        
        # Seri benzerliği
        if target_movie.get('part_of_series') and similar_movie.get('part_of_series'):
            target_series = set(str(target_movie['part_of_series']).split('|'))
            similar_series = set(str(similar_movie['part_of_series']).split('|'))
            common_series = target_series.intersection(similar_series)
            if common_series:
                reasons.append(f"Aynı seri: {len(common_series)} benzerlik")
        
        # Yıl benzerliği
        if target_movie['year'] > 0 and similar_movie['year'] > 0:
            year_diff = abs(target_movie['year'] - similar_movie['year'])
            if year_diff <= 5:
                reasons.append(f"Yakın yıl: {year_diff} yıl fark")
        
        # Ülke benzerliği
        if target_movie.get('country') and similar_movie.get('country'):
            target_countries = set(str(target_movie['country']).split('|'))
            similar_countries = set(str(similar_movie['country']).split('|'))
            common_countries = target_countries.intersection(similar_countries)
            if common_countries:
                reasons.append(f"Ortak ülke: {len(common_countries)} benzerlik")
        
        # Ödül benzerliği
        if target_movie.get('award_received') and similar_movie.get('award_received'):
            target_awards = set(str(target_movie['award_received']).split('|'))
            similar_awards = set(str(similar_movie['award_received']).split('|'))
            common_awards = target_awards.intersection(similar_awards)
            if common_awards:
                reasons.append(f"Ortak ödül: {len(common_awards)} benzerlik")
        
        # Ana konu benzerliği
        if target_movie.get('main_subject') and similar_movie.get('main_subject'):
            target_subjects = set(str(target_movie['main_subject']).split('|'))
            similar_subjects = set(str(similar_movie['main_subject']).split('|'))
            common_subjects = target_subjects.intersection(similar_subjects)
            if common_subjects:
                reasons.append(f"Ortak tema: {len(common_subjects)} benzerlik")
        
        return reasons[:5]  # Maksimum 5 neden
    
    def analyze_similarity_reasons(self, reference_movies: List, target_movie) -> List[str]:
        """Benzerlik nedenlerini analiz et"""
        reasons = []
        
        # Tür benzerliği
        target_genres = set(target_movie.get('genre', '').split('|'))
        for ref_movie in reference_movies:
            ref_genres = set(ref_movie.get('genre', '').split('|'))
            if target_genres & ref_genres:
                common_genres = target_genres & ref_genres
                reasons.append(f"Ortak tür: {', '.join(common_genres)}")
                break
        
        # Yönetmen benzerliği
        target_directors = set(target_movie.get('director', '').split('|'))
        for ref_movie in reference_movies:
            ref_directors = set(ref_movie.get('director', '').split('|'))
            if target_directors & ref_directors:
                common_directors = target_directors & ref_directors
                reasons.append(f"Ortak yönetmen: {', '.join(common_directors)}")
                break
        
        # Oyuncu benzerliği
        target_cast = set(target_movie.get('cast', '').split('|')[:3])  # İlk 3 oyuncu
        for ref_movie in reference_movies:
            ref_cast = set(ref_movie.get('cast', '').split('|')[:3])
            if target_cast & ref_cast:
                reasons.append("Ortak oyuncu kadrosu")
                break
        
        # Ülke benzerliği
        target_countries = set(target_movie.get('country', '').split('|'))
        for ref_movie in reference_movies:
            ref_countries = set(ref_movie.get('country', '').split('|'))
            if target_countries & ref_countries:
                common_countries = target_countries & ref_countries
                reasons.append(f"Ortak ülke: {', '.join(common_countries)}")
                break
        
        # Yıl benzerliği
        target_year = target_movie.get('year', 0)
        for ref_movie in reference_movies:
            ref_year = ref_movie.get('year', 0)
            if abs(target_year - ref_year) <= 5:
                reasons.append(f"Benzer dönem ({target_year})")
                break
        
        return reasons[:3]  # En fazla 3 neden
    
    def get_dataset_statistics(self) -> Dict:
        """Veri seti istatistikleri - TÜM ÖZELLİKLER"""
        stats = {
            'total_movies': len(self.df),
            'years_range': f"{int(self.df['year'].min())}-{int(self.df['year'].max())}" if self.df['year'].max() > 0 else "N/A",
            'avg_imdb_rating': self.df['imdb_rating_float'].mean(),
            'movies_with_imdb': (self.df['imdb_rating_float'] > 0).sum(),
            'movies_with_genre': (self.df['genre'] != '').sum(),
            'movies_with_director': (self.df['director'] != '').sum(),
            'movies_with_cast': (self.df['cast_member'] != '').sum(),
            'movies_with_composer': (self.df['composer'] != '').sum(),
            'movies_with_screenwriter': (self.df['screenwriter'] != '').sum(),
            'movies_with_production_company': (self.df['production_company'] != '').sum(),
            'movies_with_awards': (self.df['award_received'] != '').sum(),
            'movies_with_main_subject': (self.df['main_subject'] != '').sum(),
            'unique_genres': len(set('|'.join(self.df['genre'].fillna('').astype(str)).split('|'))),
            'unique_directors': len(set('|'.join(self.df['director'].fillna('').astype(str)).split('|'))),
            'unique_countries': len(set('|'.join(self.df['country'].fillna('').astype(str)).split('|'))),
            'unique_languages': len(set('|'.join(self.df['language'].fillna('').astype(str)).split('|')))
        }
        
        return stats
    
    def print_recommendations(self, recommendations: List[Dict], target_movie: str):
        """Önerileri formatla ve yazdır"""
        print(f"\n🎯 '{target_movie}' için öneriler:")
        print("=" * 80)
        
        for i, rec in enumerate(recommendations, 1):
            print(f"\n{i}. {rec['title']} ({rec['year']})")
            if rec['title_tr']:
                print(f"   TR: {rec['title_tr']}")
            
            if rec['imdb_rating'] > 0:
                print(f"   IMDB: {rec['imdb_rating']:.1f}")
            
            print(f"   Benzerlik: {rec['similarity_score']:.3f}")
            
            if rec['similarity_reasons']:
                print(f"   Nedenler: {', '.join(rec['similarity_reasons'])}")
            
            if rec['imdb_id']:
                print(f"   IMDB: https://www.imdb.com/title/{rec['imdb_id']}")
                
            print(f"   Wikidata: https://www.wikidata.org/wiki/{rec['wikidata_id']}")

    def clean_financial_data(self):
        """Finansal verileri temizle (bütçe, hasılat)"""
        # Bütçe temizleme
        if 'budget' in self.df.columns:
            self.df['budget_cleaned'] = self.df['budget'].apply(self.parse_financial_value)
        else:
            self.df['budget_cleaned'] = 0
            
        # Hasılat temizleme
        if 'box_office' in self.df.columns:
            self.df['box_office_cleaned'] = self.df['box_office'].apply(self.parse_financial_value)
        else:
            self.df['box_office_cleaned'] = 0
    
    def parse_financial_value(self, value: str) -> float:
        """Finansal değerleri parse et"""
        if pd.isna(value) or value == '' or value == 'nan':
            return 0.0
        
        value = str(value).replace('+', '').replace(',', '')
        
        # Çoklu değer varsa ilkini al
        if '|' in value:
            value = value.split('|')[0]
        
        # Sadece sayıları al
        numbers = re.findall(r'\d+', value)
        if numbers:
            return float(numbers[0])
        
        return 0.0
    
def main():
    """Ana demo fonksiyonu"""
    print("🎬 WIKIDATA MATEMATİKSEL FİLM ÖNERİ SİSTEMİ")
    print("=" * 60)
    
    # Öneri sistemini başlat
    try:
        recommender = WikidataMovieRecommender()
        
        # Veri seti istatistikleri
        stats = recommender.get_dataset_statistics()
        print(f"\n📊 Veri Seti İstatistikleri:")
        print(f"   Toplam film: {stats['total_movies']}")
        print(f"   Yıl aralığı: {stats['years_range']}")
        print(f"   IMDB puanı olan: {stats['movies_with_imdb']}")
        print(f"   Tür bilgisi olan: {stats['movies_with_genre']}")
        print(f"   Yönetmen bilgisi olan: {stats['movies_with_director']}")
        print(f"   Oyuncu bilgisi olan: {stats['movies_with_cast']}")
        print(f"   Müzik bilgisi olan: {stats['movies_with_composer']}")
        print(f"   Senarist bilgisi olan: {stats['movies_with_screenwriter']}")
        print(f"   Yapım şirketi olan: {stats['movies_with_production_company']}")
        print(f"   Ödül bilgisi olan: {stats['movies_with_awards']}")
        print(f"   Ana konu olan: {stats['movies_with_main_subject']}")
        print(f"   Benzersiz tür: {stats['unique_genres']}")
        print(f"   Benzersiz yönetmen: {stats['unique_directors']}")
        print(f"   Benzersiz ülke: {stats['unique_countries']}")
        print(f"   Benzersiz dil: {stats['unique_languages']}")
        
        # Etkileşimli öneri döngüsü
        while True:
            print("\n" + "─" * 50)
            movie_title = input("\n🔍 Film adı girin (çıkmak için 'q'): ").strip()
            
            if movie_title.lower() in ['q', 'quit', 'exit']:
                break
            
            if not movie_title:
                continue
            
            # Önerileri al
            recommendations = recommender.get_movie_recommendations(movie_title, n_recommendations=8)
            
            if recommendations:
                recommender.print_recommendations(recommendations, movie_title)
            else:
                print("❌ Bu film için öneri bulunamadı.")
                
                # Benzer film isimlerini öner
                similar_titles = recommender.df[
                    recommender.df['title_en'].str.contains(movie_title.split()[0], case=False, na=False)
                ]['title_en'].head(5).tolist()
                
                if similar_titles:
                    print(f"\n💡 Benzer film isimleri:")
                    for title in similar_titles:
                        print(f"   - {title}")
    
    except Exception as e:
        print(f"❌ Sistem hatası: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
