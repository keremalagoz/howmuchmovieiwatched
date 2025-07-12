"""
Film İzleme Sayacı - OMDB Destekli İnteraktif Film Önerme Uygulaması

Bu uygulama kullanıcıdan film seçimlerini alır ve OMDB API ile zenginleştirilmiş
veriler kullanarak daha iyi öneriler sunar.
"""

import os
from content_based_recommender import ContentBasedRecommender
from omdb_enhanced_recommender import OMDBEnhancedRecommender


class AdvancedInteractiveMovieRecommender:
    """OMDB destekli gelişmiş interaktif film önerme uygulaması"""
    
    def __init__(self, movie_data_path: str):
        """Uygulamayı başlat"""
        self.movie_data_path = movie_data_path
        self.user_movies = []  # Kullanıcının seçtiği filmler
        self.round_number = 0
        self.shown_recommendations = set()  # Gösterilen önerileri takip et
        
        # Verisetinin OMDB zenginleştirilmiş olup olmadığını kontrol et
        self._initialize_recommender()
        
    def _initialize_recommender(self):
        """Verisetine göre uygun recommender'ı başlat"""
        try:
            # Önce OMDB zenginleştirilmiş verisetiyle dene
            self.recommender = OMDBEnhancedRecommender(self.movie_data_path)
            self.is_omdb_enhanced = True
            print("✅ OMDB zenginleştirilmiş öneri sistemi yüklendi!")
        except:
            try:
                # OMDB başarısızsa standart sistemi kullan
                self.recommender = ContentBasedRecommender(self.movie_data_path)
                self.is_omdb_enhanced = False
                print("✅ Standart öneri sistemi yüklendi!")
            except Exception as e:
                raise Exception(f"Öneri sistemi başlatılamadı: {str(e)}")
        
    def clear_screen(self):
        """Ekranı temizle"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def display_header(self):
        """Başlık göster"""
        system_type = "OMDB Destekli" if self.is_omdb_enhanced else "Standart"
        print("🎬" + "=" * 60 + "🎬")
        print(f"     Film İzleme Sayacı - {system_type} AI Önerme Sistemi")
        print("🎬" + "=" * 60 + "🎬")
        print()
        
    def display_user_profile(self):
        """Kullanıcının mevcut film listesini göster"""
        if self.user_movies:
            print(f"📚 Şu ana kadar seçtiğiniz filmler ({len(self.user_movies)} adet):")
            for i, movie_id in enumerate(self.user_movies, 1):
                movie_info = self.recommender.get_movie_info(movie_id)
                
                # OMDB verisi varsa daha detaylı göster
                if self.is_omdb_enhanced and 'imdb_rating' in movie_info:
                    rating_info = f" - ⭐{movie_info['imdb_rating']}"
                    year_info = f" ({movie_info.get('year', 'N/A')})" if 'year' in movie_info else ""
                    print(f"   {i}. {movie_info['title']}{year_info} ({movie_info['genres']}){rating_info}")
                else:
                    print(f"   {i}. {movie_info['title']} ({movie_info['genres']})")
            print()
    
    def search_and_select_movie(self, prompt_text: str):
        """Film arama ve seçme"""
        while True:
            print(f"\n{prompt_text}")
            if self.is_omdb_enhanced:
                print("💡 İpucu: OMDB verisi ile zenginleştirilmiş arama - daha doğru sonuçlar!")
            else:
                print("💡 İpucu: Film adının bir kısmını yazarak arama yapabilirsiniz")
            
            search_query = input("🔍 Film adı girin: ").strip()
            
            if not search_query:
                print("❌ Lütfen bir film adı girin!")
                continue
                
            # Arama yap
            search_results = self.recommender.search_movies(search_query, max_results=10)
            
            if not search_results:
                print(f"❌ '{search_query}' ile eşleşen film bulunamadı. Tekrar deneyin.")
                continue
                
            # Sonuçları göster
            print(f"\n🎯 '{search_query}' için bulunan filmler:")
            for i, movie in enumerate(search_results, 1):
                # OMDB verisi varsa daha detaylı göster
                if self.is_omdb_enhanced and 'imdb_rating' in movie:
                    rating_info = f" - ⭐{movie['imdb_rating']}"
                    year_info = f" ({movie.get('year', 'N/A')})" if 'year' in movie else ""
                    print(f"   {i}. {movie['title']}{year_info} ({movie['genres']}) - {movie['director']}{rating_info}")
                else:
                    print(f"   {i}. {movie['title']} ({movie['genres']}) - {movie['director']}")
                
            # Seçim yap
            try:
                choice = input(f"\n✅ Hangi filmi seçiyorsunuz? (1-{len(search_results)}) veya 'tekrar' yazın: ").strip()
                
                if choice.lower() == 'tekrar':
                    continue
                    
                choice_num = int(choice)
                if 1 <= choice_num <= len(search_results):
                    selected_movie = search_results[choice_num - 1]
                    
                    # Daha önce seçilmiş mi kontrol et
                    if selected_movie['movie_id'] in self.user_movies:
                        print("⚠️  Bu filmi zaten seçmişsiniz! Başka bir film seçin.")
                        continue
                        
                    return selected_movie['movie_id']
                else:
                    print("❌ Geçersiz seçim! Lütfen listeden bir numara seçin.")
                    
            except ValueError:
                print("❌ Lütfen geçerli bir numara girin!")
                
    def display_recommendations(self, recommendations, round_num):
        """Önerileri güzel bir şekilde göster"""
        print(f"\n🎯 {round_num}. Tur Önerilerimiz:")
        print("─" * 50)
        
        for i, rec in enumerate(recommendations, 1):
            print(f"   {i}. 🎬 {rec['title']}")
            print(f"      📁 Tür: {rec['genres']}")
            print(f"      🎭 Yönetmen: {rec['director']}")
            print(f"      ⭐ Benzerlik: {rec['similarity_score']:.1%}")
            
            # OMDB verisi varsa ek bilgiler göster
            if self.is_omdb_enhanced:
                if 'imdb_rating' in rec:
                    print(f"      📊 IMDB: {rec['imdb_rating']}")
                if 'year' in rec:
                    print(f"      📅 Yıl: {rec['year']}")
                if 'runtime' in rec:
                    print(f"      ⏱️ Süre: {rec['runtime']}")
            print()
            
        # Gösterilen önerileri takip et
        for rec in recommendations:
            self.shown_recommendations.add(rec['movie_id'])
            
    def get_more_recommendations(self):
        """Daha fazla öneri al (daha önce gösterilmemiş filmler)"""
        try:
            print("🔄 Sistem daha geniş arama yapıyor...")
            
            # Daha fazla öneri al
            all_recommendations = self.recommender.get_recommendations(
                watched_movie_ids=self.user_movies,
                num_recommendations=100  # Çok geniş pool
            )
            
            # Daha önce gösterilmemiş önerileri filtrele
            new_recommendations = []
            for rec in all_recommendations:
                if rec['movie_id'] not in self.shown_recommendations:
                    new_recommendations.append(rec)
                    
                    # 4 tane bulduğumuzda dur
                    if len(new_recommendations) >= 4:
                        break
            
            if new_recommendations:
                print(f"✅ {len(new_recommendations)} yeni öneri bulundu!")
                # Yeni önerileri gösterilen listesine ekle
                for rec in new_recommendations:
                    self.shown_recommendations.add(rec['movie_id'])
            else:
                print("❌ Daha fazla yeni öneri bulunamadı.")
                
            return new_recommendations
                
        except Exception as e:
            print(f"❌ Yeni öneriler alınırken hata: {str(e)}")
            return []
            
    def reset_shown_recommendations(self):
        """Her yeni tur başında gösterilen önerileri sıfırla"""
        self.shown_recommendations.clear()
            
    def select_from_recommendations(self, recommendations):
        """Önerilerden film seçme veya alternatif seçenekler"""
        while True:
            print("\n🎯 Seçenekleriniz:")
            print(f"   1-{len(recommendations)}: Yukarıdaki filmlerden birini seçin")
            print(f"   {len(recommendations)+1}: 🔄 Yeni öneriler al (farklı filmler)")
            print(f"   {len(recommendations)+2}: 🔍 Manuel film arama")
            print(f"   {len(recommendations)+3}: ❌ Bu turu atla")
            
            try:
                choice = input(f"\n✅ Seçiminiz (1-{len(recommendations)+3}): ").strip()
                choice_num = int(choice)
                
                if 1 <= choice_num <= len(recommendations):
                    # Normal öneri seçimi
                    selected_rec = recommendations[choice_num - 1]
                    return selected_rec['movie_id']
                elif choice_num == len(recommendations) + 1:
                    # Yeni öneriler al
                    print("\n🔄 Daha fazla öneri getiriliyor...")
                    new_recommendations = self.get_more_recommendations()
                    if new_recommendations:
                        self.display_recommendations(new_recommendations, "Alternatif")
                        return self.select_from_recommendations(new_recommendations)
                    else:
                        print("❌ Daha fazla öneri bulunamadı. Lütfen başka bir seçenek deneyin.")
                        continue
                elif choice_num == len(recommendations) + 2:
                    # Manuel arama
                    movie_id = self.search_and_select_movie("🔍 Hangi filmi aramak istiyorsunuz?")
                    return movie_id
                elif choice_num == len(recommendations) + 3:
                    # Turu atla
                    print("⏭️ Bu tur atlanıyor...")
                    return None
                else:
                    print(f"❌ Lütfen 1-{len(recommendations)+3} arasında bir numara girin!")
                    
            except ValueError:
                print("❌ Lütfen geçerli bir numara girin!")
                
    def run_initial_setup(self):
        """İlk 3 film seçimini yap"""
        self.clear_screen()
        self.display_header()
        
        print("🚀 Film İzleme Sayacı'na Hoş Geldiniz!")
        if self.is_omdb_enhanced:
            print("\n🌟 OMDB API ile zenginleştirilmiş veriset kullanılıyor!")
            print("   • Daha doğru IMDB puanları")
            print("   • Detaylı film bilgileri")
            print("   • Gelişmiş öneri algoritması")
        
        print("\nSistemimiz sizin zevkinizi öğrenmek için 3 film seçmenizi istiyor.")
        print("Bu filmler, size önerilecek filmlerin temelini oluşturacak.\n")
        
        # İlk 3 filmi seç
        for i in range(3):
            movie_id = self.search_and_select_movie(f"📝 {i+1}. filminizi seçin:")
            self.user_movies.append(movie_id)
            
            # Seçilen filmi göster
            movie_info = self.recommender.get_movie_info(movie_id)
            if self.is_omdb_enhanced and 'imdb_rating' in movie_info:
                print(f"✅ Seçtiniz: {movie_info['title']} (⭐{movie_info['imdb_rating']})")
            else:
                print(f"✅ Seçtiniz: {movie_info['title']}")
            
            if i < 2:  # Son filmde profil gösterme
                self.display_user_profile()
                
    def run_recommendation_round(self):
        """Bir öneri turu çalıştır"""
        self.round_number += 1
        
        # Her yeni turda gösterilen önerileri sıfırla
        self.reset_shown_recommendations()
        
        print(f"\n🔄 {self.round_number}. Tur Başlıyor...")
        if self.is_omdb_enhanced:
            print("OMDB verileri ile gelişmiş zevk profili oluşturuluyor...")
        else:
            print("Zevk profiliniz güncelleniyor...")
        print()
        
        # Önerileri al
        recommendations = self.recommender.get_recommendations(
            watched_movie_ids=self.user_movies,
            num_recommendations=4
        )
        
        if not recommendations:
            print("❌ Öneri üretilemedi. Sistemi yeniden başlatın.")
            return False
            
        # Önerileri göster
        self.display_recommendations(recommendations, self.round_number)
        
        # Kullanıcıdan seçim al
        selected_movie_id = self.select_from_recommendations(recommendations)
        
        # Tur atlandı mı kontrol et
        if selected_movie_id is None:
            print("⏭️ Tur atlandı, devam ediliyor...")
            return True
            
        self.user_movies.append(selected_movie_id)
        
        # Seçimi onayla
        movie_info = self.recommender.get_movie_info(selected_movie_id)
        if self.is_omdb_enhanced and 'imdb_rating' in movie_info:
            print(f"\n✅ Seçtiniz: {movie_info['title']} (⭐{movie_info['imdb_rating']})")
        else:
            print(f"\n✅ Seçtiniz: {movie_info['title']}")
        print(f"🎯 Toplam film sayınız: {len(self.user_movies)}")
        
        return True
        
    def ask_continue(self):
        """Devam etmek isteyip istemediğini sor"""
        while True:
            choice = input("\n🤔 Devam etmek istiyor musunuz? (e/h): ").strip().lower()
            if choice in ['e', 'evet', 'y', 'yes']:
                return True
            elif choice in ['h', 'hayır', 'n', 'no']:
                return False
            else:
                print("❌ Lütfen 'e' (evet) veya 'h' (hayır) yazın!")
                
    def show_final_summary(self):
        """Final özeti göster"""
        print("\n" + "🎬" * 20)
        print("             FİNAL ÖZETİ")
        print("🎬" * 20)
        
        print(f"\n📊 Toplam seçilen film: {len(self.user_movies)}")
        print(f"🔄 Öneri turu sayısı: {self.round_number}")
        if self.is_omdb_enhanced:
            print("🌟 OMDB zenginleştirilmiş veriset kullanıldı!")
        
        print(f"\n🎬 Film listeniz:")
        total_rating = 0
        rated_count = 0
        
        for i, movie_id in enumerate(self.user_movies, 1):
            movie_info = self.recommender.get_movie_info(movie_id)
            phase = "İlk seçim" if i <= 3 else f"{i-3}. tur"
            
            if self.is_omdb_enhanced and 'imdb_rating' in movie_info:
                rating_str = f" - ⭐{movie_info['imdb_rating']}"
                try:
                    rating_val = float(movie_info['imdb_rating'])
                    total_rating += rating_val
                    rated_count += 1
                except:
                    rating_str = ""
                print(f"   {i}. {movie_info['title']} ({phase}){rating_str}")
            else:
                print(f"   {i}. {movie_info['title']} ({phase})")
            
        # Ortalama rating göster
        if self.is_omdb_enhanced and rated_count > 0:
            avg_rating = total_rating / rated_count
            print(f"\n⭐ Ortalama IMDB puanınız: {avg_rating:.1f}/10")
            
            if avg_rating >= 8.0:
                print("🏆 Mükemmel zevk! Kaliteli filmleri tercih ediyorsunuz.")
            elif avg_rating >= 7.0:
                print("👍 Güzel seçimler! İyi filmleri seviyorsunuz.")
            elif avg_rating >= 6.0:
                print("👌 Dengeli seçimler yapıyorsunuz.")
            
        # Tür analizi yap
        genres_count = {}
        directors_count = {}
        
        for movie_id in self.user_movies:
            movie_info = self.recommender.get_movie_info(movie_id)
            
            # Türleri say
            genres = movie_info['genres'].split(',')
            for genre in genres:
                genre = genre.strip()
                if genre:  # Boş değilse
                    genres_count[genre] = genres_count.get(genre, 0) + 1
                
            # Yönetmenleri say
            director = movie_info['director']
            if director:  # Boş değilse
                directors_count[director] = directors_count.get(director, 0) + 1
            
        # En çok tercih edilen türleri göster
        if genres_count:
            sorted_genres = sorted(genres_count.items(), key=lambda x: x[1], reverse=True)
            print(f"\n🎭 En çok tercih ettiğiniz türler:")
            for genre, count in sorted_genres[:3]:
                print(f"   • {genre}: {count} film")
                
        # En çok tercih edilen yönetmenler
        if directors_count:
            popular_directors = [(d, c) for d, c in directors_count.items() if c > 1]
            if popular_directors:
                print(f"\n🎬 Birden fazla filmini seçtiğiniz yönetmenler:")
                for director, count in popular_directors:
                    print(f"   • {director}: {count} film")
                    
        print(f"\n🙏 Film İzleme Sayacı'nı kullandığınız için teşekkürler!")
        if self.is_omdb_enhanced:
            print("🌟 OMDB API sayesinde daha zengin bir deneyim yaşadınız!")
        print("📱 Uygulamamız sürekli öğrenerek daha iyi öneriler sunmaya devam edecek!")
        
    def run(self):
        """Ana uygulama döngüsü"""
        try:
            # İlk kurulum
            self.run_initial_setup()
            
            # Profil özeti göster
            self.clear_screen()
            self.display_header()
            self.display_user_profile()
            
            print("🎉 Harika! İlk profiliniz oluşturuldu.")
            print("Şimdi size öneriler sunmaya başlayabiliriz.\n")
            
            input("⏳ Devam etmek için Enter'a basın...")
            
            # Öneri turları
            while True:
                self.clear_screen()
                self.display_header()
                self.display_user_profile()
                
                # Öneri turunu çalıştır
                if not self.run_recommendation_round():
                    break
                    
                # Devam etmek isteyip istemediğini sor
                if not self.ask_continue():
                    break
                    
            # Final özeti
            self.clear_screen()
            self.display_header()
            self.show_final_summary()
            
        except KeyboardInterrupt:
            print("\n\n👋 Uygulamadan çıkılıyor...")
        except Exception as e:
            print(f"\n❌ Bir hata oluştu: {str(e)}")


def select_dataset():
    """Kullanıcının veriset seçmesini sağla"""
    import os
    
    print("📊 Veriset Seçimi")
    print("=" * 30)
    
    # Mevcut CSV dosyalarını listele
    csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
    
    if not csv_files:
        print("❌ Mevcut dizinde CSV dosyası bulunamadı!")
        return None
    
    print("📁 Mevcut verisetleri:")
    for i, file in enumerate(csv_files, 1):
        # OMDB zenginleştirilmiş mi kontrol et
        if 'omdb' in file.lower() or 'enriched' in file.lower():
            print(f"   {i}. {file} 🌟 (OMDB Zenginleştirilmiş)")
        else:
            print(f"   {i}. {file}")
    
    print(f"   {len(csv_files)+1}. Varsayılan veriset (processed_tmdb_movies.csv)")
    
    try:
        choice = input(f"\nHangi veriseti kullanmak istiyorsunuz? (1-{len(csv_files)+1}): ").strip()
        choice_num = int(choice)
        
        if 1 <= choice_num <= len(csv_files):
            return csv_files[choice_num - 1]
        elif choice_num == len(csv_files) + 1:
            return 'processed_tmdb_movies.csv'
        else:
            print("❌ Geçersiz seçim!")
            return None
            
    except ValueError:
        print("❌ Geçersiz giriş!")
        return None


def main():
    """Ana fonksiyon"""
    print("🎬 Film İzleme Sayacı - Gelişmiş Versiyon")
    print("=" * 50)
    
    # Veriset seçimi
    dataset_path = select_dataset()
    
    if not dataset_path:
        print("❌ Veriset seçilemedi!")
        return
    
    if not os.path.exists(dataset_path):
        print(f"❌ Veriset dosyası bulunamadı: {dataset_path}")
        return
    
    print(f"\n✅ Seçilen veriset: {dataset_path}")
    input("⏳ Başlamak için Enter'a basın...")
    
    # Uygulamayı başlat
    app = AdvancedInteractiveMovieRecommender(dataset_path)
    app.run()


if __name__ == "__main__":
    main()
