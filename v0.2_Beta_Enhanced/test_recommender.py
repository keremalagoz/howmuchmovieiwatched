"""
ContentBasedRecommender Sınıfı Test ve Örnek Kullanım
"""

from content_based_recommender import ContentBasedRecommender


def main():
    """Ana test fonksiyonu"""
    
    # Recommender sistemini başlat
    print("🎬 Film Önerme Sistemi Test Ediliyor...")
    print("=" * 50)
    
    try:        # CSV dosyasını yükle
        recommender = ContentBasedRecommender('processed_tmdb_movies.csv')
        
        # Sistem istatistiklerini göster
        stats = recommender.get_stats()
        print(f"\n📊 Sistem İstatistikleri:")
        print(f"   • Toplam Film: {stats['total_movies']}")
        print(f"   • Benzersiz Yönetmen: {stats['unique_directors']}")
        print(f"   • Özellik Boyutu: {stats['feature_dimensions']}")
        
        # Örnek: Kullanıcının izlediği filmler - TMDB dataset'inden
        watched_movies = [19995, 49026, 597]  # Avatar, The Dark Knight Rises, Titanic
        
        print(f"\n👤 Kullanıcının İzlediği Filmler:")
        for movie_id in watched_movies:
            movie_info = recommender.get_movie_info(movie_id)
            print(f"   • {movie_info['title']} ({movie_info['genres']})")
        
        # Film önerilerini al
        print(f"\n🎯 Önerilen Filmler:")
        recommendations = recommender.get_recommendations(watched_movies, num_recommendations=8)
        
        for i, rec in enumerate(recommendations, 1):
            print(f"   {i}. {rec['title']}")
            print(f"      Tür: {rec['genres']}")
            print(f"      Yönetmen: {rec['director']}")
            print(f"      Benzerlik Skoru: {rec['similarity_score']:.3f}")
            print()
        
        # Arama özelliğini test et
        print("🔍 Arama Testi:")
        search_results = recommender.search_movies("Matrix")
        for result in search_results:
            print(f"   • {result['title']} - {result['director']}")
        
        print("\n✅ Test başarıyla tamamlandı!")
        
    except Exception as e:
        print(f"❌ Hata oluştu: {str(e)}")


if __name__ == "__main__":
    main()
