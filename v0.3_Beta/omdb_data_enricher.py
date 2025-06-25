"""
OMDB API Data Enricher - Film Verisetini Zenginleştirme Aracı

Bu script mevcut film verisetini OMDB API kullanarak daha detaylı
bilgilerle zenginleştirir ve yeni bir CSV dosyası oluşturur.

OMDB API: http://www.omdbapi.com/
"""

import pandas as pd
import requests
import time
import json
from typing import Dict, Optional, List
import logging

# Logging ayarları
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('omdb_enrichment.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)


class OMDBDataEnricher:
    """OMDB API kullanarak film verilerini zenginleştiren sınıf"""
    
    def __init__(self, api_key: str):
        """
        OMDB Data Enricher'ı başlat
        
        Args:
            api_key (str): OMDB API anahtarınız
        """
        self.api_key = api_key
        # Farklı endpoint'leri dene
        self.base_urls = [
            "https://www.omdbapi.com/",
            "https://omdbapi.com/",
            "http://www.omdbapi.com/",
            "http://omdbapi.com/"
        ]
        self.current_base_url = None
        self.session = requests.Session()
        self.session.timeout = 30  # Timeout ayarla
        self.rate_limit_delay = 0.2  # API rate limit için bekleme süresi (saniye)
        
        # Session ayarları - DNS ve bağlantı sorunları için
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # API anahtarını test et
        if not self._test_api_key():
            raise ValueError("Geçersiz API anahtarı veya API erişim sorunu!")
            
        logging.info(f"OMDB API bağlantısı başarılı! Kullanılan URL: {self.current_base_url}")
    
    def _test_api_key(self) -> bool:
        """API anahtarını test et ve çalışan endpoint'i bul"""
        print("🔍 OMDB API bağlantısı test ediliyor...")
        
        for url in self.base_urls:
            try:
                print(f"   Deneniyor: {url}")
                response = self.session.get(
                    url,
                    params={
                        'apikey': self.api_key,
                        't': 'The Matrix',
                        'type': 'movie'
                    },
                    timeout=15
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('Response') == 'True':
                        print(f"✅ Başarılı bağlantı: {url}")
                        self.current_base_url = url
                        return True
                    elif 'Invalid API key' in data.get('Error', ''):
                        print(f"❌ Geçersiz API anahtarı!")
                        return False
                
            except requests.exceptions.DNSError:
                print(f"   ❌ DNS hatası: {url}")
                continue
            except requests.exceptions.ConnectTimeout:
                print(f"   ❌ Bağlantı zaman aşımı: {url}")
                continue
            except requests.exceptions.ConnectionError as e:
                print(f"   ❌ Bağlantı hatası: {url} - {str(e)}")
                continue
            except Exception as e:
                print(f"   ❌ Genel hata: {url} - {str(e)}")
                continue
        
        print("❌ Hiçbir OMDB endpoint'ine bağlanılamadı!")
        return False
    
    def search_movie_by_title(self, title: str, year: Optional[str] = None) -> Optional[Dict]:
        """
        Film başlığına göre OMDB'den film ara
        
        Args:
            title (str): Film başlığı
            year (str, optional): Film yılı (daha doğru sonuç için)
            
        Returns:
            Dict: Film bilgileri veya None
        """
        try:
            params = {
                'apikey': self.api_key,
                't': title,
                'type': 'movie',
                'plot': 'full'  # Detaylı özet al
            }
            
            if year:
                params['y'] = year
            
            response = self.session.get(self.current_base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('Response') == 'True':
                    return data
                else:
                    logging.warning(f"Film bulunamadı: {title} ({year if year else 'Yıl belirtilmedi'})")
                    return None
            else:
                logging.error(f"API hatası: HTTP {response.status_code}")
                return None
                
        except Exception as e:
            logging.error(f"Film arama hatası ({title}): {str(e)}")
            return None
    
    def search_movie_by_imdb_id(self, imdb_id: str) -> Optional[Dict]:
        """
        IMDB ID'sine göre film ara
        
        Args:
            imdb_id (str): IMDB ID (örn: tt0133093)
            
        Returns:
            Dict: Film bilgileri veya None
        """
        try:
            params = {
                'apikey': self.api_key,
                'i': imdb_id,
                'plot': 'full'
            }
            
            response = self.session.get(self.current_base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('Response') == 'True':
                    return data
                else:
                    logging.warning(f"IMDB ID ile film bulunamadı: {imdb_id}")
                    return None
            else:
                logging.error(f"API hatası: HTTP {response.status_code}")
                return None
                
        except Exception as e:
            logging.error(f"IMDB ID arama hatası ({imdb_id}): {str(e)}")
            return None
    
    def extract_movie_data(self, omdb_data: Dict) -> Dict:
        """
        OMDB API yanıtından gerekli film bilgilerini çıkar
        
        Args:
            omdb_data (Dict): OMDB API yanıtı
            
        Returns:
            Dict: İşlenmiş film bilgileri
        """
        return {
            'omdb_title': omdb_data.get('Title', ''),
            'omdb_year': omdb_data.get('Year', ''),
            'omdb_rated': omdb_data.get('Rated', ''),
            'omdb_released': omdb_data.get('Released', ''),
            'omdb_runtime': omdb_data.get('Runtime', ''),
            'omdb_genre': omdb_data.get('Genre', ''),
            'omdb_director': omdb_data.get('Director', ''),
            'omdb_writer': omdb_data.get('Writer', ''),
            'omdb_actors': omdb_data.get('Actors', ''),
            'omdb_plot': omdb_data.get('Plot', ''),
            'omdb_language': omdb_data.get('Language', ''),
            'omdb_country': omdb_data.get('Country', ''),
            'omdb_awards': omdb_data.get('Awards', ''),
            'omdb_poster': omdb_data.get('Poster', ''),
            'omdb_metascore': omdb_data.get('Metascore', ''),
            'omdb_imdb_rating': omdb_data.get('imdbRating', ''),
            'omdb_imdb_votes': omdb_data.get('imdbVotes', ''),
            'omdb_imdb_id': omdb_data.get('imdbID', ''),
            'omdb_type': omdb_data.get('Type', ''),
            'omdb_dvd': omdb_data.get('DVD', ''),
            'omdb_box_office': omdb_data.get('BoxOffice', ''),
            'omdb_production': omdb_data.get('Production', ''),
            'omdb_website': omdb_data.get('Website', ''),
        }
    
    def enrich_dataset(self, input_csv_path: str, output_csv_path: str, 
                      title_column: str = 'title', year_column: str = None,
                      imdb_id_column: str = None, max_requests: int = None) -> None:
        """
        Mevcut verisetini OMDB API ile zenginleştir
        
        Args:
            input_csv_path (str): Girdi CSV dosyası yolu
            output_csv_path (str): Çıktı CSV dosyası yolu
            title_column (str): Film başlığı sütunu adı
            year_column (str, optional): Film yılı sütunu adı
            imdb_id_column (str, optional): IMDB ID sütunu adı
            max_requests (int, optional): Maksimum API isteği sayısı
        """
        logging.info(f"Verisetini yüklüyor: {input_csv_path}")
        
        try:
            # CSV dosyasını yükle
            df = pd.read_csv(input_csv_path)
            logging.info(f"Toplam {len(df)} film yüklendi")
            
            if max_requests and max_requests < len(df):
                df = df.head(max_requests)
                logging.info(f"İşlem {max_requests} film ile sınırlandırıldı")
            
            # OMDB verilerini saklamak için sütunlar ekle
            omdb_columns = [
                'omdb_title', 'omdb_year', 'omdb_rated', 'omdb_released', 'omdb_runtime',
                'omdb_genre', 'omdb_director', 'omdb_writer', 'omdb_actors', 'omdb_plot',
                'omdb_language', 'omdb_country', 'omdb_awards', 'omdb_poster',
                'omdb_metascore', 'omdb_imdb_rating', 'omdb_imdb_votes', 'omdb_imdb_id',
                'omdb_type', 'omdb_dvd', 'omdb_box_office', 'omdb_production', 'omdb_website',
                'omdb_enriched'  # Zenginleştirilme durumu
            ]
            
            for col in omdb_columns:
                df[col] = ''
            
            # Her film için OMDB verilerini al
            successful_enrichments = 0
            failed_enrichments = 0
            
            for index, row in df.iterrows():
                logging.info(f"İşleniyor ({index + 1}/{len(df)}): {row[title_column]}")
                
                omdb_data = None
                
                # Önce IMDB ID ile arama yap (varsa)
                if imdb_id_column and pd.notna(row.get(imdb_id_column, '')):
                    imdb_id = str(row[imdb_id_column]).strip()
                    if imdb_id and imdb_id != 'nan':
                        omdb_data = self.search_movie_by_imdb_id(imdb_id)
                
                # IMDB ID ile bulunamadıysa başlık ile ara
                if not omdb_data:
                    title = str(row[title_column]).strip()
                    year = None
                    
                    if year_column and pd.notna(row.get(year_column, '')):
                        year = str(row[year_column]).strip()
                        # Yıldan sadece sayısal kısmı al
                        import re
                        year_match = re.search(r'\d{4}', year)
                        if year_match:
                            year = year_match.group()
                    
                    omdb_data = self.search_movie_by_title(title, year)
                
                # OMDB verilerini işle ve ekle
                if omdb_data:
                    extracted_data = self.extract_movie_data(omdb_data)
                    
                    for col, value in extracted_data.items():
                        df.at[index, col] = value
                    
                    df.at[index, 'omdb_enriched'] = 'True'
                    successful_enrichments += 1
                    logging.info(f"Basarili: {row[title_column]}")
                else:
                    df.at[index, 'omdb_enriched'] = 'False'
                    failed_enrichments += 1
                    logging.warning(f"Basarisiz: {row[title_column]}")
                
                # Rate limiting
                time.sleep(self.rate_limit_delay)
                
                # Her 50 filmde bir durumu kaydet
                if (index + 1) % 50 == 0:
                    temp_output_path = output_csv_path.replace('.csv', f'_temp_{index + 1}.csv')
                    df.to_csv(temp_output_path, index=False, encoding='utf-8')
                    logging.info(f"Geçici kayıt: {temp_output_path}")
            
            # Final CSV'yi kaydet
            df.to_csv(output_csv_path, index=False, encoding='utf-8')
            
            logging.info(f"""
            Zenginlestirme tamamlandi!
            
            Istatistikler:
            • Toplam film: {len(df)}
            • Basarili zenginlestirme: {successful_enrichments}
            • Basarisiz zenginlestirme: {failed_enrichments}
            • Basari orani: {(successful_enrichments / len(df) * 100):.1f}%
            
            Cikti dosyasi: {output_csv_path}
            """)
            
        except Exception as e:
            logging.error(f"Zenginleştirme hatası: {str(e)}")
            raise
    
    def create_sample_enriched_dataset(self, sample_size: int = 100) -> None:
        """
        Popüler filmlerle örnek bir zenginleştirilmiş veriset oluştur
        
        Args:
            sample_size (int): Örnek veriset boyutu
        """
        popular_movies = [
            # IMDB Top 250 filmleri
            ("The Shawshank Redemption", "1994"),
            ("The Godfather", "1972"),
            ("The Dark Knight", "2008"),
            ("The Godfather Part II", "1974"),
            ("12 Angry Men", "1957"),
            ("Schindler's List", "1993"),
            ("The Lord of the Rings: The Return of the King", "2003"),
            ("Pulp Fiction", "1994"),
            ("The Lord of the Rings: The Fellowship of the Ring", "2001"),
            ("The Good, the Bad and the Ugly", "1966"),
            ("Forrest Gump", "1994"),
            ("The Lord of the Rings: The Two Towers", "2002"),
            ("Fight Club", "1999"),
            ("Inception", "2010"),
            ("Star Wars: Episode V - The Empire Strikes Back", "1980"),
            ("The Matrix", "1999"),
            ("Goodfellas", "1990"),
            ("One Flew Over the Cuckoo's Nest", "1975"),
            ("Se7en", "1995"),
            ("Seven Samurai", "1954"),
            ("The Silence of the Lambs", "1991"),
            ("It's a Wonderful Life", "1946"),
            ("Life Is Beautiful", "1997"),
            ("The Usual Suspects", "1995"),
            ("Léon: The Professional", "1994"),
            ("Spirited Away", "2001"),
            ("Saving Private Ryan", "1998"),
            ("Once Upon a Time in the West", "1968"),
            ("American History X", "1998"),
            ("Interstellar", "2014"),
            
            # Daha fazla popüler filmler
            ("City of God", "2002"),
            ("Casablanca", "1942"),
            ("The Pianist", "2002"),
            ("The Departed", "2006"),
            ("The Prestige", "2006"),
            ("Gladiator", "2000"),
            ("Apocalypse Now", "1979"),
            ("Alien", "1979"),
            ("Sunset Boulevard", "1950"),
            ("Dr. Strangelove", "1964"),
            ("The Great Dictator", "1940"),
            ("Cinema Paradiso", "1988"),
            ("The Lives of Others", "2006"),
            ("Grave of the Fireflies", "1988"),
            ("Paths of Glory", "1957"),
            ("Django Unchained", "2012"),
            ("WALL·E", "2008"),
            ("The Shining", "1980"),
            ("3 Idiots", "2009"),
            ("Inglourious Basterds", "2009"),
            
            # Aksiyon Filmleri
            ("Terminator 2: Judgment Day", "1991"),
            ("Back to the Future", "1985"),
            ("Aliens", "1986"),
            ("The Avengers", "2012"),
            ("Mad Max: Fury Road", "2015"),
            ("Die Hard", "1988"),
            ("Raiders of the Lost Ark", "1981"),
            ("Heat", "1995"),
            ("The Bourne Identity", "2002"),
            ("John Wick", "2014"),
            
            # Komedi Filmleri
            ("The Grand Budapest Hotel", "2014"),
            ("Some Like It Hot", "1959"),
            ("Toy Story", "1995"),
            ("Monty Python and the Holy Grail", "1975"),
            ("The Big Lebowski", "1998"),
            ("Groundhog Day", "1993"),
            ("Life of Brian", "1979"),
            ("The Princess Bride", "1987"),
            ("Airplane!", "1980"),
            ("Young Frankenstein", "1974"),
            
            # Bilim Kurgu
            ("2001: A Space Odyssey", "1968"),
            ("Blade Runner", "1982"),
            ("Star Wars", "1977"),
            ("E.T. the Extra-Terrestrial", "1982"),
            ("The Thing", "1982"),
            ("Minority Report", "2002"),
            ("District 9", "2009"),
            ("Ex Machina", "2014"),
            ("Arrival", "2016"),
            ("The Martian", "2015"),
            
            # Korku Filmleri
            ("The Exorcist", "1973"),
            ("Psycho", "1960"),
            ("Halloween", "1978"),
            ("A Nightmare on Elm Street", "1984"),
            ("The Texas Chain Saw Massacre", "1974"),
            ("Rosemary's Baby", "1968"),
            ("Get Out", "2017"),
            ("Hereditary", "2018"),
            ("The Babadook", "2014"),
            ("It Follows", "2014"),
            
            # Romantik Filmler
            ("Titanic", "1997"),
            ("The Notebook", "2004"),
            ("Eternal Sunshine of the Spotless Mind", "2004"),
            ("Roman Holiday", "1953"),
            ("Before Sunrise", "1995"),
            ("Her", "2013"),
            ("La La Land", "2016"),
            ("Lost in Translation", "2003"),
            ("The Shape of Water", "2017"),
            ("Amelie", "2001"),
            
            # Türk Filmleri (OMDB'de bulunanlar)
            ("Vizontele", "2001"),
            ("G.O.R.A.", "2004"),
            ("Gemide", "1998"),
            ("Eşkıya", "1996"),
            ("Düğün Dernek", "2013"),
            ("Organize İşler", "2005"),
            
            # Animasyon Filmleri
            ("The Lion King", "1994"),
            ("Finding Nemo", "2003"),
            ("Shrek", "2001"),
            ("Up", "2009"),
            ("Inside Out", "2015"),
            ("Coco", "2017"),
            ("Zootopia", "2016"),
            ("Frozen", "2013"),
            ("Moana", "2016"),
            ("The Incredibles", "2004"),
            
            # Klasik Filmler
            ("Gone with the Wind", "1939"),
            ("Lawrence of Arabia", "1962"),
            ("Vertigo", "1958"),
            ("Citizen Kane", "1941"),
            ("Singin' in the Rain", "1952"),
            ("North by Northwest", "1959"),
            ("Rear Window", "1954"),
            ("On the Waterfront", "1954"),
            ("The Wizard of Oz", "1939"),
            ("Modern Times", "1936"),
            
            # Gerilim Filmleri
            ("Zodiac", "2007"),
            ("Prisoners", "2013"),
            ("Gone Girl", "2014"),
            ("Shutter Island", "2010"),
            ("The Sixth Sense", "1999"),
            ("No Country for Old Men", "2007"),
            ("Sicario", "2015"),
            ("Drive", "2011"),
            ("Nightcrawler", "2014"),
            ("Parasite", "2019"),
            
            # Müzik Filmleri
            ("Whiplash", "2014"),
            ("A Star Is Born", "2018"),
            ("Bohemian Rhapsody", "2018"),
            ("8 Mile", "2002"),
            ("Almost Famous", "2000"),
            ("School of Rock", "2003"),
            ("Mamma Mia!", "2008"),
            ("Chicago", "2002"),
            ("The Greatest Showman", "2017"),
            ("Rocketman", "2019"),
        ]
        
        # Sample size'a göre filmleri sınırla
        popular_movies = popular_movies[:sample_size]
        
        # CSV formatında örnek veriset oluştur
        sample_data = []
        for i, (title, year) in enumerate(popular_movies):
            sample_data.append({
                'movie_id': i + 1,
                'title': title,
                'release_date': year,
                'original_title': title
            })
        
        # Geçici CSV dosyası oluştur
        temp_csv = 'temp_sample_movies.csv'
        sample_df = pd.DataFrame(sample_data)
        sample_df.to_csv(temp_csv, index=False, encoding='utf-8')
        
        # Zenginleştir
        self.enrich_dataset(
            input_csv_path=temp_csv,
            output_csv_path='omdb_enriched_sample_movies.csv',
            title_column='title',
            year_column='release_date'
        )
        
        # Geçici dosyayı sil
        import os
        os.remove(temp_csv)
        
        logging.info("Örnek zenginleştirilmiş veriset oluşturuldu: omdb_enriched_sample_movies.csv")


def main():
    """Ana fonksiyon - Örnek kullanım"""
    
    # API anahtarınızı buraya girin
    API_KEY = input("OMDB API anahtarınızı girin: ").strip()
    
    if not API_KEY:
        print("❌ API anahtarı gereklidir!")
        return
    
    try:
        # OMDB Enricher'ı başlat
        enricher = OMDBDataEnricher(api_key=API_KEY)
        
        print("\n🎬 OMDB Film Veriset Zenginleştirici")
        print("=" * 50)
        print("1. Mevcut verisetimi zenginleştir")
        print("2. Örnek zenginleştirilmiş veriset oluştur")
        
        choice = input("\nSeçiminiz (1-2): ").strip()
        
        if choice == "1":
            # Mevcut verisetini zenginleştir
            input_file = input("Girdi CSV dosyası yolu: ").strip()
            output_file = input("Çıktı CSV dosyası yolu: ").strip()
            title_col = input("Film başlığı sütunu adı (varsayılan: title): ").strip() or "title"
            year_col = input("Film yılı sütunu adı (boş bırakabilirsiniz): ").strip() or None
            
            max_req = input("Maksimum film sayısı (boş = tümü): ").strip()
            max_requests = int(max_req) if max_req.isdigit() else None
            
            enricher.enrich_dataset(
                input_csv_path=input_file,
                output_csv_path=output_file,
                title_column=title_col,
                year_column=year_col,
                max_requests=max_requests
            )
            
        elif choice == "2":
            # Örnek veriset oluştur
            sample_size = input("Örnek veriset boyutu (varsayılan: 50): ").strip()
            sample_size = int(sample_size) if sample_size.isdigit() else 50
            
            enricher.create_sample_enriched_dataset(sample_size=sample_size)
            
        else:
            print("❌ Geçersiz seçim!")
            
    except Exception as e:
        logging.error(f"Program hatası: {str(e)}")
        print(f"\n❌ Hata: {str(e)}")


if __name__ == "__main__":
    main()
