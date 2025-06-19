"""
Film İzleme Sayacı - Otomatik Demo Uygulaması

Bu uygulama, sistem özelliklerini otomatik olarak gösterir.
"""

import time
from content_based_recommender import ContentBasedRecommender


class DemoRecommenderApp:
    """Demo film önerme uygulaması"""
    
    def __init__(self, movie_data_path: str):
        """Demo uygulamasını başlat"""
        self.recommender = ContentBasedRecommender(movie_data_path)
        
    def print_section(self, title: str):
        """Bölüm başlığı yazdır"""
        print("\n" + "🎬" * 50)
        print(f"🎯 {title}")
        print("🎬" * 50)
        
    def simulate_typing(self, text: str, delay: float = 0.03):
        """Yazma efekti simüle et"""
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()
        
    def demo_initial_selection(self):
        """İlk seçim demosunu göster"""
        self.print_section("DEMO: İlk Film Seçimleri")
        
        # Örnek ilk seçimler
        initial_movies = [
            (101, "Inception"),
            (105, "The Matrix"), 
            (103, "Pulp Fiction")
        ]
        
        print("👤 Kullanıcı ilk 3 filmini seçiyor...\n")
        
        user_movies = []
        for i, (movie_id, title) in enumerate(initial_movies, 1):
            self.simulate_typing(f"🔍 {i}. Film Aranıyor: '{title}'")
            time.sleep(1)
            
            movie_info = self.recommender.get_movie_info(movie_id)
            print(f"✅ Seçildi: {movie_info['title']} ({movie_info['genres']})")
            user_movies.append(movie_id)
            time.sleep(1)
            
        return user_movies
        
    def demo_recommendation_round(self, user_movies: list, round_num: int):
        """Öneri turu demosunu göster"""
        self.print_section(f"DEMO: {round_num}. Öneri Turu")
        
        print(f"🧠 AI sistemi kullanıcının {len(user_movies)} filmini analiz ediyor...")
        time.sleep(2)
        
        # Önerileri al
        recommendations = self.recommender.get_recommendations(
            watched_movie_ids=user_movies,
            num_recommendations=4
        )
        
        print(f"\n🎯 {round_num}. Tur AI Önerileri:")
        print("─" * 60)
        
        for i, rec in enumerate(recommendations, 1):
            print(f"   {i}. 🎬 {rec['title']}")
            print(f"      📁 {rec['genres']}")
            print(f"      🎭 {rec['director']}")
            print(f"      ⭐ Benzerlik Skoru: {rec['similarity_score']:.1%}")
            print()
            
        # Otomatik seçim (ilk öneriyi seç)
        selected = recommendations[0]
        print(f"👤 Kullanıcı seçimi: {selected['title']}")
        user_movies.append(selected['movie_id'])
        
        time.sleep(2)
        return user_movies
        
    def demo_learning_analysis(self, user_movies: list):
        """Öğrenme analizi demosunu göster"""
        self.print_section("DEMO: AI Öğrenme Analizi")
        
        print("🔬 Kullanıcı profili analiz ediliyor...\n")
        time.sleep(1)
        
        # Tür analizi
        genres_count = {}
        directors_count = {}
        
        for movie_id in user_movies:
            movie_info = self.recommender.get_movie_info(movie_id)
            
            # Türleri say
            genres = movie_info['genres'].split(',')
            for genre in genres:
                genre = genre.strip()
                genres_count[genre] = genres_count.get(genre, 0) + 1
                
            # Yönetmenleri say
            director = movie_info['director']
            directors_count[director] = directors_count.get(director, 0) + 1
            
        # Sonuçları göster
        print("📊 Kullanıcı Tercihi Analizi:")
        
        # En popüler türler
        sorted_genres = sorted(genres_count.items(), key=lambda x: x[1], reverse=True)
        print("\n🎭 En Sevilen Türler:")
        for genre, count in sorted_genres[:5]:
            percentage = (count / len(user_movies)) * 100
            print(f"   • {genre}: {count} film (%{percentage:.1f})")
            
        # En popüler yönetmenler
        popular_directors = [(d, c) for d, c in directors_count.items() if c > 1]
        if popular_directors:
            print("\n🎬 Favori Yönetmenler:")
            for director, count in popular_directors:
                print(f"   • {director}: {count} film")
                
        time.sleep(3)
        
    def demo_improvement_over_time(self, initial_movies: list):
        """Zamanla iyileşme demosunu göster"""
        self.print_section("DEMO: Sürekli Öğrenme Karşılaştırması")
        
        print("📈 AI önerilerinin kalitesi nasıl artıyor?\n")
        
        # İlk 3 filmle yapılan öneri
        print("1️⃣ BAŞLANGIÇ (3 film ile):")
        initial_recs = self.recommender.get_recommendations(initial_movies[:3], 3)
        for i, rec in enumerate(initial_recs, 1):
            print(f"   {i}. {rec['title']} (Skor: {rec['similarity_score']:.3f})")
            
        time.sleep(2)
        
        # 6 filmle yapılan öneri
        print("\n2️⃣ ORTA AŞAMA (6 film ile):")
        mid_recs = self.recommender.get_recommendations(initial_movies[:6], 3)
        for i, rec in enumerate(mid_recs, 1):
            print(f"   {i}. {rec['title']} (Skor: {rec['similarity_score']:.3f})")
            
        time.sleep(2)
        
        # Tam liste ile yapılan öneri
        print(f"\n3️⃣ GELİŞMİŞ AŞAMA ({len(initial_movies)} film ile):")
        final_recs = self.recommender.get_recommendations(initial_movies, 3)
        for i, rec in enumerate(final_recs, 1):
            print(f"   {i}. {rec['title']} (Skor: {rec['similarity_score']:.3f})")
            
        # Karşılaştırma
        print(f"\n📊 SONUÇ:")
        print(f"   • Başlangıç ortalama skor: {sum(r['similarity_score'] for r in initial_recs)/len(initial_recs):.3f}")
        print(f"   • Gelişmiş ortalama skor: {sum(r['similarity_score'] for r in final_recs)/len(final_recs):.3f}")
        
        improvement = ((sum(r['similarity_score'] for r in final_recs)/len(final_recs)) - 
                      (sum(r['similarity_score'] for r in initial_recs)/len(initial_recs))) * 100
        print(f"   • İyileşme oranı: %{improvement:.1f}")
        
        time.sleep(3)
        
    def run_demo(self):
        """Ana demo akışı"""
        try:
            print("🎬" + "=" * 60 + "🎬")
            print("    Film İzleme Sayacı - AI Önerme Sistemi DEMO")
            print("🎬" + "=" * 60 + "🎬")
            
            # Sistem bilgileri
            stats = self.recommender.get_stats()
            print(f"\n📊 Sistem Özellikleri:")
            print(f"   • Film Veritabanı: {stats['total_movies']} film")
            print(f"   • AI Özellik Boyutu: {stats['feature_dimensions']} özellik")
            print(f"   • Benzersiz Yönetmen: {stats['unique_directors']}")
            
            time.sleep(3)
            
            # İlk seçimler
            user_movies = self.demo_initial_selection()
            
            # 3 tur öneri
            for round_num in range(1, 4):
                user_movies = self.demo_recommendation_round(user_movies, round_num)
                
            # Öğrenme analizi
            self.demo_learning_analysis(user_movies)
            
            # İyileşme karşılaştırması
            self.demo_improvement_over_time(user_movies)
            
            # Final
            self.print_section("DEMO TAMAMLANDI")
            print("🎉 AI Önerme Sistemi başarıyla çalışıyor!")
            print("📱 Kullanıcılar artık kişiselleştirilmiş film önerileri alabilir.")
            print("🧠 Sistem her yeni filmle birlikte daha da akıllı hale geliyor.")
            
        except KeyboardInterrupt:
            print("\n\n👋 Demo durduruldu...")
        except Exception as e:
            print(f"\n❌ Demo hatası: {str(e)}")


def main():
    """Ana fonksiyon"""
    print("🚀 Film İzleme Sayacı - AI Demo başlatılıyor...\n")
    time.sleep(2)
    
    demo = DemoRecommenderApp('movies.csv')
    demo.run_demo()


if __name__ == "__main__":
    main()
