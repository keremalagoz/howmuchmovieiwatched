"""
TMDB Dataset İşleyici - JSON formatındaki TMDB verilerini işler
"""

import pandas as pd
import json
import ast
from typing import List, Dict, Any


class TMDBDataProcessor:
    """TMDB dataset'ini işlemek için yardımcı sınıf"""
    
    @staticmethod
    def extract_names_from_json(json_str: str, key: str = 'name') -> str:
        """
        JSON string'den name değerlerini çıkarır
        
        Args:
            json_str (str): JSON formatındaki string
            key (str): Çıkarılacak anahtar (varsayılan: 'name')
            
        Returns:
            str: Virgülle ayrılmış name değerleri
        """
        if pd.isna(json_str) or json_str == '[]':
            return ''
        
        try:
            # JSON string'i parse et
            data = ast.literal_eval(json_str)
            if isinstance(data, list):
                names = [item.get(key, '') for item in data if isinstance(item, dict)]
                return ', '.join(names)
            return ''
        except (ValueError, SyntaxError):
            return ''
    
    @staticmethod
    def get_director_from_crew(crew_json: str) -> str:
        """
        Crew JSON'undan yönetmeni çıkarır
        
        Args:
            crew_json (str): Crew bilgilerini içeren JSON string
            
        Returns:
            str: Yönetmen adı
        """
        if pd.isna(crew_json) or crew_json == '[]':
            return ''
        
        try:
            crew_data = ast.literal_eval(crew_json)
            if isinstance(crew_data, list):
                for person in crew_data:
                    if isinstance(person, dict) and person.get('job') == 'Director':
                        return person.get('name', '')
            return ''
        except (ValueError, SyntaxError):
            return ''
    
    @staticmethod
    def get_main_actors_from_cast(cast_json: str, max_actors: int = 5) -> str:
        """
        Cast JSON'undan ana oyuncuları çıkarır
        
        Args:
            cast_json (str): Cast bilgilerini içeren JSON string
            max_actors (int): Maksimum oyuncu sayısı
            
        Returns:
            str: Virgülle ayrılmış oyuncu adları
        """
        if pd.isna(cast_json) or cast_json == '[]':
            return ''
        
        try:
            cast_data = ast.literal_eval(cast_json)
            if isinstance(cast_data, list):
                # İlk N oyuncuyu al (genelde en önemli oyuncular ilk sıralarda)
                actors = []
                for person in cast_data[:max_actors]:
                    if isinstance(person, dict):
                        actors.append(person.get('name', ''))
                return ', '.join(actors)
            return ''
        except (ValueError, SyntaxError):
            return ''
    
    @staticmethod
    def process_tmdb_dataset(movies_path: str, credits_path: str = None) -> pd.DataFrame:
        """
        TMDB dataset'ini işleyerek content_based_recommender için uygun format oluşturur
        
        Args:
            movies_path (str): TMDB movies CSV dosyası yolu
            credits_path (str): TMDB credits CSV dosyası yolu (opsiyonel)
            
        Returns:
            pd.DataFrame: İşlenmiş dataset
        """
        # Movies dosyasını yükle
        print("📁 TMDB movies dataset'i yükleniyor...")
        movies_df = pd.read_csv(movies_path)
        
        # Credits dosyası varsa yükle
        crew_data = {}
        cast_data = {}
        
        if credits_path:
            try:
                print("📁 TMDB credits dataset'i yükleniyor...")
                credits_df = pd.read_csv(credits_path)
                
                # Crew ve cast verilerini dictionary'e dönüştür
                for _, row in credits_df.iterrows():
                    movie_id = row['movie_id']
                    crew_data[movie_id] = row.get('crew', '[]')
                    cast_data[movie_id] = row.get('cast', '[]')
                    
            except FileNotFoundError:
                print("⚠️  Credits dosyası bulunamadı, sadece movies verileri kullanılacak")
        
        print("🔄 Dataset işleniyor...")
        
        # Yeni DataFrame oluştur
        processed_data = []
        
        for _, row in movies_df.iterrows():
            movie_id = row['id']
            
            # Temel bilgiler
            title = row.get('title', '')
            overview = row.get('overview', '')
            
            # Genres JSON'unu işle
            genres = TMDBDataProcessor.extract_names_from_json(row.get('genres', '[]'))
            
            # Keywords JSON'unu işle
            keywords = TMDBDataProcessor.extract_names_from_json(row.get('keywords', '[]'))
            
            # Production companies
            companies = TMDBDataProcessor.extract_names_from_json(row.get('production_companies', '[]'))
              # Director ve actors - credits dosyasından veya movies'den
            if credits_path and movie_id in crew_data:
                director = TMDBDataProcessor.get_director_from_crew(crew_data[movie_id])
                actors = TMDBDataProcessor.get_main_actors_from_cast(cast_data[movie_id])
            else:
                # Credits yoksa boş bırak, genre ve plot summary daha önemli
                director = ''
                actors = ''
            
            # Plot summary - overview kullan
            plot_summary = overview if pd.notna(overview) else ''
            
            # Kayıt oluştur
            record = {
                'movie_id': int(movie_id),
                'title': title,
                'genres': genres,
                'director': director,
                'actors': actors,
                'plot_summary': plot_summary,
                'keywords': keywords,
                'companies': companies,
                'release_date': row.get('release_date', ''),
                'vote_average': row.get('vote_average', 0),
                'vote_count': row.get('vote_count', 0),
                'popularity': row.get('popularity', 0)
            }
            
            processed_data.append(record)
        
        # DataFrame oluştur
        df = pd.DataFrame(processed_data)
        
        # Boş değerleri temizle
        df = df.fillna('')
        
        # Başarı mesajı
        print(f"✅ {len(df)} film başarıyla işlendi!")
        print(f"📊 Benzersiz tür sayısı: {len(set([g for genres in df['genres'] for g in genres.split(', ') if g]))}")
        print(f"📊 Benzersiz yönetmen sayısı: {df['director'].nunique()}")
        
        return df
    
    @staticmethod
    def save_processed_dataset(df: pd.DataFrame, output_path: str):
        """
        İşlenmiş dataset'i CSV olarak kaydet
        
        Args:
            df (pd.DataFrame): İşlenmiş dataset
            output_path (str): Çıktı dosyası yolu
        """
        # Sadece gerekli sütunları kaydet
        columns_to_save = ['movie_id', 'title', 'genres', 'director', 'actors', 'plot_summary']
        df_to_save = df[columns_to_save].copy()
        
        df_to_save.to_csv(output_path, index=False, encoding='utf-8')
        print(f"💾 İşlenmiş dataset kaydedildi: {output_path}")


def main():
    """Ana işlem fonksiyonu"""
    try:
        # TMDB dataset'ini işle
        processor = TMDBDataProcessor()
        
        # Movies dosyasını işle
        df = processor.process_tmdb_dataset('tmdb_5000_movies.csv')
        
        # İşlenmiş veriyi kaydet
        processor.save_processed_dataset(df, 'processed_tmdb_movies.csv')
        
        # İstatistikleri göster
        print("\n📈 Dataset İstatistikleri:")
        print(f"   • Toplam Film: {len(df)}")
        print(f"   • Benzersiz Yönetmen: {df['director'].nunique()}")
        print(f"   • Ortalama Oylama: {df['vote_average'].mean():.1f}")
        print(f"   • En Popüler Film: {df.loc[df['popularity'].idxmax(), 'title']}")
        
        # Örnek veri göster
        print("\n🎬 Örnek Filmler:")
        sample_movies = df.head(3)
        for _, movie in sample_movies.iterrows():
            print(f"   • {movie['title']} ({movie['genres']}) - {movie['director']}")
        
    except Exception as e:
        print(f"❌ Hata: {str(e)}")


if __name__ == "__main__":
    main()
