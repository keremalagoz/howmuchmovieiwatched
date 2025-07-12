"""
Film İzleme Sayacı - İnteraktif Film Önerme Uygulaması

Bu uygulama kullanıcıdan film seçimlerini alır ve sürekli öğrenerek
daha iyi öneriler sunar.
"""

import os
from content_based_recommender import ContentBasedRecommender


class InteractiveMovieRecommender:
    """İnteraktif film önerme uygulaması"""
    
    def __init__(self, movie_data_path: str):
        """Uygulamayı başlat"""
        self.recommender = ContentBasedRecommender(movie_data_path)
        self.user_movies = []  # Kullanıcının seçtiği filmler
        self.round_number = 0
        
    def clear_screen(self):
        """Ekranı temizle"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def display_header(self):
        """Başlık göster"""
        print("🎬" + "=" * 60 + "🎬")
        print("           Film İzleme Sayacı - AI Önerme Sistemi")
        print("🎬" + "=" * 60 + "🎬")
        print()
        
    def display_user_profile(self):
        """Kullanıcının mevcut film listesini göster"""
        if self.user_movies:
            print(f"📚 Şu ana kadar seçtiğiniz filmler ({len(self.user_movies)} adet):")
            for i, movie_id in enumerate(self.user_movies, 1):
                movie_info = self.recommender.get_movie_info(movie_id)
                print(f"   {i}. {movie_info['title']} ({movie_info['genres']})")
            print()
    
    def search_and_select_movie(self, prompt_text: str):
        """Film arama ve seçme"""
        while True:
            print(f"\n{prompt_text}")
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
            print()
            
    def select_from_recommendations(self, recommendations):
        """Önerilerden film seçme"""
        while True:
            try:
                choice = input(f"✅ Hangi filmi seçiyorsunuz? (1-{len(recommendations)}): ").strip()
                choice_num = int(choice)
                
                if 1 <= choice_num <= len(recommendations):
                    selected_rec = recommendations[choice_num - 1]
                    return selected_rec['movie_id']
                else:
                    print(f"❌ Lütfen 1-{len(recommendations)} arasında bir numara girin!")
                    
            except ValueError:
                print("❌ Lütfen geçerli bir numara girin!")
                
    def run_initial_setup(self):
        """İlk 3 film seçimini yap"""
        self.clear_screen()
        self.display_header()
        
        print("🚀 Film İzleme Sayacı'na Hoş Geldiniz!")
        print("\nSistemimiz sizin zevkinizi öğrenmek için 3 film seçmenizi istiyor.")
        print("Bu filmler, size önerilecek filmlerin temelini oluşturacak.\n")
        
        # İlk 3 filmi seç
        for i in range(3):
            movie_id = self.search_and_select_movie(f"📝 {i+1}. filminizi seçin:")
            self.user_movies.append(movie_id)
            
            # Seçilen filmi göster
            movie_info = self.recommender.get_movie_info(movie_id)
            print(f"✅ Seçtiniz: {movie_info['title']}")
            
            if i < 2:  # Son filmde profil gösterme
                self.display_user_profile()
                
    def run_recommendation_round(self):
        """Bir öneri turu çalıştır"""
        self.round_number += 1
        
        print(f"\n🔄 {self.round_number}. Tur Başlıyor...")
        print("Zevk profiliniz güncelleniyor...\n")
        
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
        self.user_movies.append(selected_movie_id)
        
        # Seçimi onayla
        movie_info = self.recommender.get_movie_info(selected_movie_id)
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
        
        print(f"\n🎬 Film listeniz:")
        for i, movie_id in enumerate(self.user_movies, 1):
            movie_info = self.recommender.get_movie_info(movie_id)
            phase = "İlk seçim" if i <= 3 else f"{i-3}. tur"
            print(f"   {i}. {movie_info['title']} ({phase})")
            
        # Tür analizi yap
        genres_count = {}
        directors_count = {}
        
        for movie_id in self.user_movies:
            movie_info = self.recommender.get_movie_info(movie_id)
            
            # Türleri say
            genres = movie_info['genres'].split(',')
            for genre in genres:
                genre = genre.strip()
                genres_count[genre] = genres_count.get(genre, 0) + 1
                
            # Yönetmenleri say
            director = movie_info['director']
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


def main():
    """Ana fonksiyon"""
    app = InteractiveMovieRecommender('movies.csv')
    app.run()


if __name__ == "__main__":
    main()
