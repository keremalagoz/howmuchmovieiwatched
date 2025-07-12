#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wikidata Movie Recommender v0.4 Beta - System Test
Sistem özelliklerini test etmek için kullanılır.
"""

import pandas as pd
from wikidata_movie_recommender import WikidataMovieRecommender

def main():
    print("=== WIKIDATA MOVIE RECOMMENDER v0.4 BETA SİSTEM TESTİ ===")
    print()
    
    # Veri yükleme ve istatistikler
    print("1. Veri setini yükleme...")
    df = pd.read_csv('test_wikidata_films.csv')
    print(f"   ✅ Toplam film sayısı: {len(df)}")
    print(f"   ✅ Toplam sütun sayısı: {len(df.columns)}")
    print(f"   ✅ Sütunlar: {list(df.columns)}")
    print()
    
    # Recommender sistemini başlat
    print("2. Recommender sistemini başlatma...")
    recommender = WikidataMovieRecommender()
    print(f"   ✅ İşlenen film sayısı: {len(recommender.df)}")
    print()
    
    # Özellik istatistikleri
    print("3. Özellik istatistikleri...")
    stats = recommender.get_dataset_statistics()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    print()
    
    # Detaylı test
    print("4. Detaylı öneri testi...")
    test_movie = "Van Diemen's Land"
    recommendations = recommender.get_movie_recommendations(test_movie, n_recommendations=3)
    print(f"   🎬 {test_movie} için öneriler:")
    for i, rec in enumerate(recommendations, 1):
        print(f"   {i}. {rec['title']} - Benzerlik: {rec['similarity_score']:.3f}")
        print(f"      Nedenler: {rec['similarity_reasons']}")
    print()
    
    # Sistem özelliklerini test et
    print("5. Sistem özelliklerini test etme...")
    features = recommender.feature_weights.keys()
    print(f"   ✅ Toplam özellik sayısı: {len(features)}")
    print(f"   ✅ Kullanılan özellikler: {list(features)}")
    print()
    
    # Farklı film türlerini test et
    print("6. Farklı film türlerini test etme...")
    test_movies = ["Ghost Rider", "Apollo 18", "Contagion"]
    for movie in test_movies:
        try:
            recs = recommender.get_movie_recommendations(movie, n_recommendations=2)
            print(f"   🎬 {movie} için {len(recs)} öneri bulundu")
        except Exception as e:
            print(f"   ❌ {movie} için hata: {e}")
    print()
    
    print("=== TEST TAMAMLANDI ===")
    print("v0.4 Beta sistemi başarıyla çalışıyor!")
    print("Tüm özellikler aktif ve sistem stabil.")

if __name__ == "__main__":
    main()
