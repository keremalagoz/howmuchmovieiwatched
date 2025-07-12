#!/usr/bin/env python3
"""
Tüm özelliklerin kullanıldığını test et
"""

from wikidata_movie_recommender import WikidataMovieRecommender

def test_all_features():
    """Tüm özelliklerin kullanıldığını test et"""
    print("🧪 TÜM ÖZELLİKLER TESTİ")
    print("=" * 50)
    
    # Recommender'ı yükle
    recommender = WikidataMovieRecommender()
    
    # Özellik sayısını kontrol et
    print(f"✅ Toplam film: {len(recommender.df)}")
    print(f"✅ Kullanılan özellik sayısı: {len(recommender.feature_weights)}")
    
    # Özellik listesini yazdır
    print("\n🎯 KULLANILAN ÖZELLİKLER:")
    for feature, weight in recommender.feature_weights.items():
        print(f"   {feature}: {weight}")
    
    # Veri setindeki sütunları kontrol et
    print(f"\n📊 Veri setindeki sütun sayısı: {len(recommender.df.columns)}")
    
    # Örnek bir film için özellik vektörü kontrolü
    if len(recommender.df) > 0:
        sample_movie = recommender.df.iloc[0]
        print(f"\n🎬 Örnek Film: {sample_movie['title_en']}")
        print(f"   Combined Features Uzunluğu: {len(sample_movie['combined_features'].split())}")
        print(f"   İlk 100 karakter: {sample_movie['combined_features'][:100]}...")
    
    # Hızlı öneri testi
    print("\n🔍 HIZLI ÖNERİ TESTİ:")
    first_movie = recommender.df.iloc[0]['title_en']
    recs = recommender.get_movie_recommendations(first_movie, 3)
    
    if recs:
        print(f"✅ {first_movie} için {len(recs)} öneri bulundu")
        for i, rec in enumerate(recs):
            print(f"   {i+1}. {rec['title']} - Benzerlik: {rec['similarity_score']:.3f}")
            if rec['similarity_reasons']:
                print(f"      Nedenler: {', '.join(rec['similarity_reasons'])}")
    else:
        print("❌ Öneri bulunamadı")
    
    print("\n✅ TEST TAMAMLANDI!")

if __name__ == "__main__":
    test_all_features()
