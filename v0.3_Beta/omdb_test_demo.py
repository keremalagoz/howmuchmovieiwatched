"""
OMDB API Test ve Demo Script
Bu script OMDB API'yi test eder ve örnek bir zenginleştirme işlemi yapar.
"""

import os
import sys
from omdb_data_enricher import OMDBDataEnricher
from omdb_enhanced_recommender import OMDBEnhancedRecommender
from omdb_config import OMDBConfig


def test_omdb_api():
    """OMDB API bağlantısını test et"""
    print("OMDB API Test Basliyor...")
    print("=" * 50)
    
    # API anahtarını config'den al
    config = OMDBConfig()
    api_key = config.get_api_key()
    
    if not api_key:
        print("API anahtari alinamadi!")
        return False
    
    try:
        # Enricher'ı başlat
        enricher = OMDBDataEnricher(api_key=api_key)
        print("OMDB API baglantisi basarili!")
        
        # Test arama yap
        print("\nTest Aramalari:")
        print("-" * 30)
        
        test_movies = [
            ("The Matrix", "1999"),
            ("Inception", "2010"),
            ("Pulp Fiction", "1994")
        ]
        
        for title, year in test_movies:
            print(f"\n🔍 Araniyor: {title} ({year})")
            movie_data = enricher.search_movie_by_title(title, year)
            
            if movie_data:
                print(f"✅ Bulundu: {movie_data.get('Title', 'N/A')}")
                print(f"   📅 Yıl: {movie_data.get('Year', 'N/A')}")
                print(f"   🎭 Türler: {movie_data.get('Genre', 'N/A')}")
                print(f"   ⭐ IMDB: {movie_data.get('imdbRating', 'N/A')}")
                print(f"   Yonetmen: {movie_data.get('Director', 'N/A')}")
            else:
                print(f"Film bulunamadi!")
        
        return True
        
    except Exception as e:
        print(f"OMDB API Test Hatasi: {str(e)}")
        return False


def create_sample_dataset():
    """Örnek bir veriset oluştur ve zenginleştir"""
    print("\nOrnek Veriset Olusturuluyor...")
    print("=" * 50)
    
    # API anahtarını config'den al
    config = OMDBConfig()
    api_key = config.get_api_key()
    
    if not api_key:
        print("API anahtari alinamadi!")
        return
    
    try:
        enricher = OMDBDataEnricher(api_key=api_key)
        
        # Örnek veriset oluştur
        print("100 populer filmle ornek veriset olusturuluyor...")
        enricher.create_sample_enriched_dataset(sample_size=100000)
        
        print("Ornek veriset olusturuldu: omdb_enriched_sample_movies.csv")
        
        # Oluşturulan veriseti test et
        print("\nYeni Oneri Sistemi Test Ediliyor...")
        test_enhanced_recommender()
        
    except Exception as e:
        print(f"❌ Örnek veriset oluşturma hatası: {str(e)}")


def test_enhanced_recommender():
    """Gelişmiş öneri sistemini test et"""
    print("\n🤖 Gelişmiş Öneri Sistemi Testi")
    print("=" * 50)
    
    try:
        # Zenginleştirilmiş verisetini yükle
        if not os.path.exists('omdb_enriched_sample_movies.csv'):
            print("❌ Zenginleştirilmiş veriset bulunamadı!")
            print("   Önce 'create_sample_dataset()' fonksiyonunu çalıştırın.")
            return
        
        # Gelişmiş recommender'ı başlat
        recommender = OMDBEnhancedRecommender('omdb_enriched_sample_movies.csv')
        
        # İstatistikleri göster
        print("\n📊 Veriset İstatistikleri:")
        stats = recommender.get_stats()
        for key, value in stats.items():
            print(f"   • {key}: {value}")
        
        # Film arama testi
        print("\n🔍 Film Arama Testi:")
        search_results = recommender.search_movies("Matrix", max_results=3)
        for i, movie in enumerate(search_results, 1):
            print(f"   {i}. {movie['title']} - {movie.get('imdb_rating', 'N/A')} ⭐")
        
        # Öneri testi
        if search_results:
            print(f"\n🎯 '{search_results[0]['title']}' Filmine Dayalı Öneriler:")
            test_movie_id = search_results[0]['movie_id']
            
            recommendations = recommender.get_recommendations(
                watched_movie_ids=[test_movie_id],
                num_recommendations=5
            )
            
            for i, rec in enumerate(recommendations, 1):
                print(f"   {i}. {rec['title']}")
                print(f"      🎭 Türler: {rec['genres']}")
                print(f"      🎬 Yönetmen: {rec['director']}")
                print(f"      ⭐ Benzerlik: {rec['similarity_score']:.1%}")
                if 'imdb_rating' in rec:
                    print(f"      📊 IMDB: {rec['imdb_rating']}")
                print()
        
        print("✅ Gelişmiş öneri sistemi test başarılı!")
        
    except Exception as e:
        print(f"❌ Gelişmiş öneri sistemi test hatası: {str(e)}")


def enrich_existing_dataset():
    """Mevcut verisetini zenginleştir"""
    print("\n📈 Mevcut Veriset Zenginleştirme")
    print("=" * 50)
    
    # API anahtarını config'den al
    config = OMDBConfig()
    api_key = config.get_api_key()
    
    if not api_key:
        print("❌ API anahtarı alınamadı!")
        return
    
    # Mevcut verisetleri listele
    csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
    
    if not csv_files:
        print("❌ Mevcut dizinde CSV dosyası bulunamadı!")
        return
    
    print("📁 Mevcut CSV dosyaları:")
    for i, file in enumerate(csv_files, 1):
        print(f"   {i}. {file}")
    
    try:
        choice = int(input(f"\nHangi dosyayı zenginleştirmek istiyorsunuz? (1-{len(csv_files)}): "))
        
        if 1 <= choice <= len(csv_files):
            input_file = csv_files[choice - 1]
            output_file = input_file.replace('.csv', '_omdb_enriched.csv')
            
            print(f"\n🔄 Zenginleştiriliyor: {input_file} -> {output_file}")
            
            # Sütun adlarını sor
            title_col = input("Film başlığı sütunu adı (varsayılan: title): ").strip() or "title"
            year_col = input("Film yılı sütunu adı (opsiyonel): ").strip() or None
            
            # Maksimum film sayısı
            max_req = input("Maksimum kaç film işlensin? (boş = tümü): ").strip()
            max_requests = int(max_req) if max_req.isdigit() else None
            
            # Zenginleştirme işlemini başlat
            enricher = OMDBDataEnricher(api_key=api_key)
            enricher.enrich_dataset(
                input_csv_path=input_file,
                output_csv_path=output_file,
                title_column=title_col,
                year_column=year_col,
                max_requests=max_requests
            )
            
            print(f"\n✅ Zenginleştirme tamamlandı: {output_file}")
            
            # Test et
            test_choice = input("\nYeni verisetini test etmek istiyor musunuz? (e/h): ").lower()
            if test_choice in ['e', 'evet', 'y', 'yes']:
                test_enhanced_with_file(output_file)
                
        else:
            print("❌ Geçersiz seçim!")
            
    except (ValueError, IndexError):
        print("❌ Geçersiz giriş!")
    except Exception as e:
        print(f"❌ Zenginleştirme hatası: {str(e)}")


def test_enhanced_with_file(csv_file: str):
    """Belirtilen dosya ile gelişmiş öneri sistemini test et"""
    try:
        print(f"\n🧪 Test Ediliyor: {csv_file}")
        
        # Gelişmiş recommender'ı başlat
        recommender = OMDBEnhancedRecommender(csv_file)
        
        # İstatistikleri göster
        print("\n📊 Veriset İstatistikleri:")
        stats = recommender.get_stats()
        for key, value in stats.items():
            print(f"   • {key}: {value}")
        
        # Birkaç film önerisi göster
        print("\n🎯 Rastgele Film Önerisi Testi:")
        
        # İlk filmi seç
        first_movie_id = recommender.df.iloc[0]['movie_id']
        first_movie_info = recommender.get_movie_info(first_movie_id)
        
        print(f"   🎬 Temel Film: {first_movie_info['title']}")
        
        recommendations = recommender.get_recommendations(
            watched_movie_ids=[first_movie_id],
            num_recommendations=3
        )
        
        print("   📝 Öneriler:")
        for i, rec in enumerate(recommendations, 1):
            print(f"      {i}. {rec['title']} (Benzerlik: {rec['similarity_score']:.1%})")
        
        print(f"\n✅ Test başarılı!")
        
    except Exception as e:
        print(f"❌ Test hatası: {str(e)}")


def main():
    """Ana menü"""
    print("OMDB Film Veriset Zenginlestirici")
    print("=" * 50)
    print("1. OMDB API Test Et")
    print("2. Ornek Zenginlestirilmis Veriset Olustur")
    print("3. Mevcut Verisetimi Zenginlestir")
    print("4. Gelismis Oneri Sistemi Test Et")
    print("5. API Anahtari Yapilandir")
    print("6. Cikis")
    
    while True:
        try:
            choice = input("\nSeciminiz (1-6): ").strip()
            
            if choice == "1":
                test_omdb_api()
            elif choice == "2":
                create_sample_dataset()
            elif choice == "3":
                enrich_existing_dataset()
            elif choice == "4":
                test_enhanced_recommender()
            elif choice == "5":
                config = OMDBConfig()
                config.setup_api_key()
            elif choice == "6":
                print("Hosca kalin!")
                break
            else:
                print("Gecersiz secim! Lutfen 1-6 arasi bir sayi girin.")
                
        except KeyboardInterrupt:
            print("\nProgram sonlandiriliyor...")
            break
        except Exception as e:
            print(f"Beklenmeyen hata: {str(e)}")


if __name__ == "__main__":
    main()
