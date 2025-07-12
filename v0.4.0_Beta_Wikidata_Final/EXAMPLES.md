# 💡 Kullanım Örnekleri - v0.4 Beta

## 📖 Giriş

Bu dokümanda Wikidata Film Öneri Sistemi v0.4'ün farklı kullanım senaryolarını ve örneklerini bulacaksınız. Her örnek pratik ve test edilebilir kodlarla açıklanmıştır.

---

## 🚀 Temel Kullanım

### Örnek 1: İlk Öneriler

```python
from wikidata_movie_recommender import WikidataMovieRecommender

# Sistem başlat
recommender = WikidataMovieRecommender()

# Avatar için 5 öneri al
recommendations = recommender.get_movie_recommendations("Avatar", 5)

# Basit yazdırma
for i, rec in enumerate(recommendations, 1):
    print(f"{i}. {rec['title']} ({rec['year']}) - Benzerlik: {rec['similarity_score']:.3f}")

# Beklenen çıktı:
# 1. Inception (2010) - Benzerlik: 0.142
# 2. Interstellar (2014) - Benzerlik: 0.128
# 3. The Matrix (1999) - Benzerlik: 0.115
# ...
```

### Örnek 2: Detaylı Öneri Analizi

```python
# Film önerileri al
recommendations = recommender.get_movie_recommendations("Moon", 3)

# Detaylı analiz
for rec in recommendations:
    print(f"\n🎬 {rec['title']} ({rec['year']})")
    print(f"   TR Adı: {rec['title_tr']}")
    print(f"   IMDB: {rec['imdb_rating']}")
    print(f"   Benzerlik: {rec['similarity_score']:.4f}")
    print(f"   Nedenler: {', '.join(rec['similarity_reasons'])}")
    print(f"   Wikidata: https://www.wikidata.org/wiki/{rec['wikidata_id']}")
    if rec['imdb_id']:
        print(f"   IMDB: https://www.imdb.com/title/{rec['imdb_id']}")
```

---

## 📊 Veri Analizi Örnekleri

### Örnek 3: Veri Seti İstatistikleri

```python
# Kapsamlı istatistikler
stats = recommender.get_dataset_statistics()

print("📊 VERİ SETİ İSTATİSTİKLERİ")
print("=" * 40)
print(f"Toplam film: {stats['total_movies']}")
print(f"Yıl aralığı: {stats['years_range']}")
print(f"Ortalama IMDB puanı: {stats['avg_imdb_rating']:.1f}")

# Özellik kapsamı
print(f"\n🎯 ÖZELLİK KAPSAMI:")
print(f"Tür bilgisi olan: {stats['movies_with_genre']}")
print(f"Yönetmen bilgisi olan: {stats['movies_with_director']}")
print(f"Oyuncu bilgisi olan: {stats['movies_with_cast']}")
print(f"Müzik bilgisi olan: {stats['movies_with_composer']}")
print(f"Ödül bilgisi olan: {stats['movies_with_awards']}")

# Çeşitlilik
print(f"\n🌍 ÇEŞİTLİLİK:")
print(f"Benzersiz tür: {stats['unique_genres']}")
print(f"Benzersiz yönetmen: {stats['unique_directors']}")
print(f"Benzersiz ülke: {stats['unique_countries']}")
print(f"Benzersiz dil: {stats['unique_languages']}")
```

### Örnek 4: En Popüler Türler Analizi

```python
import pandas as pd
from collections import Counter

# Tüm türleri topla
all_genres = []
for _, movie in recommender.df.iterrows():
    if movie['genre']:
        genres = movie['genre'].split('|')
        all_genres.extend(genres)

# En popüler türler
genre_counts = Counter(all_genres)
top_genres = genre_counts.most_common(10)

print("🎭 EN POPÜLER TÜRLER:")
for genre, count in top_genres:
    percentage = (count / len(recommender.df)) * 100
    print(f"  {genre}: {count} film (%{percentage:.1f})")
```

---

## 🔧 Gelişmiş Kullanım

### Örnek 5: Özel Ağırlık Ayarlama

```python
# Mevcut ağırlıkları görüntüle
print("🎯 MEVCUT AĞIRLIKLAR:")
for feature, weight in recommender.feature_weights.items():
    print(f"  {feature}: {weight}")

# Tür odaklı öneriler için ayarlama
print("\n🔄 TÜR ODAKLI AYARLAMA...")
recommender.feature_weights['genre'] = 0.35      # Türü artır
recommender.feature_weights['director'] = 0.15   # Yönetmeni azalt
recommender.feature_weights['cast'] = 0.10       # Oyuncuları azalt

# Benzerlik matrisini yeniden hesapla
recommender.calculate_similarity_matrix()

# Yeni ayarlarla öneri al
new_recommendations = recommender.get_movie_recommendations("Avatar", 5)
print("Yeni öneriler (tür odaklı):")
for i, rec in enumerate(new_recommendations, 1):
    print(f"{i}. {rec['title']} - Benzerlik: {rec['similarity_score']:.3f}")
```

### Örnek 6: Kalite Odaklı Öneriler

```python
# Kalite odaklı sistem ayarları
recommender.feature_weights['award_received'] = 0.08      # Ödülleri artır
recommender.feature_weights['imdb_rating_range'] = 0.06   # IMDB puanını artır
recommender.feature_weights['production_company'] = 0.05  # Yapım şirketini artır

# Benzerlik matrisini güncelle
recommender.calculate_similarity_matrix()

# Kalite odaklı öneriler
quality_recs = recommender.get_movie_recommendations("Inception", 5)
print("🏆 KALİTE ODAKLI ÖNERİLER:")
for rec in quality_recs:
    print(f"  {rec['title']} - IMDB: {rec['imdb_rating']} - Benzerlik: {rec['similarity_score']:.3f}")
```

---

## 🔍 Benzerlik Analizi Örnekleri

### Örnek 7: Film Karşılaştırması

```python
# İki filmi karşılaştır
movie1 = recommender.df[recommender.df['title_en'].str.contains('Avatar', case=False)].iloc[0]
movie2 = recommender.df[recommender.df['title_en'].str.contains('Inception', case=False)].iloc[0]

# Benzerlik nedenlerini analiz et
reasons = recommender.analyze_similarity_reasons(movie1, movie2)

print(f"🔍 {movie1['title_en']} vs {movie2['title_en']}")
print("Ortak özellikler:")
for reason in reasons:
    print(f"  • {reason}")

# Manuel benzerlik hesapla
if len(reasons) > 0:
    print(f"\nToplam ortak özellik: {len(reasons)}")
else:
    print("\nHiç ortak özellik bulunamadı")
```

### Örnek 8: Benzerlik Matrisi Analizi

```python
import numpy as np

# En yüksek benzerlik skorlarını bul
similarity_matrix = recommender.similarity_matrix
max_similarity = np.max(similarity_matrix[similarity_matrix < 1.0])  # Kendisiyle benzerlik hariç

# En yüksek benzerliğe sahip film çiftini bul
max_indices = np.where(similarity_matrix == max_similarity)
movie1_idx = max_indices[0][0]
movie2_idx = max_indices[1][0]

movie1 = recommender.df.iloc[movie1_idx]
movie2 = recommender.df.iloc[movie2_idx]

print(f"🎯 EN YÜKSEK BENZERLİK: {max_similarity:.4f}")
print(f"Film 1: {movie1['title_en']} ({movie1['year']})")
print(f"Film 2: {movie2['title_en']} ({movie2['year']})")

# Benzerlik nedenlerini analiz et
reasons = recommender.analyze_similarity_reasons(movie1, movie2)
print(f"Nedenler: {', '.join(reasons)}")
```

---

## 📁 Veri İşleme Örnekleri

### Örnek 9: Özel Veri Seti ile Çalışma

```python
# Kendi CSV dosyanızla çalışın
custom_recommender = WikidataMovieRecommender("my_custom_films.csv")

# Veri setini inceleyin
print(f"Özel veri seti: {len(custom_recommender.df)} film")

# Eksik sütunları kontrol edin
required_columns = ['qid', 'title_en', 'genre', 'director']
missing_columns = [col for col in required_columns if col not in custom_recommender.df.columns]

if missing_columns:
    print(f"⚠️ Eksik sütunlar: {missing_columns}")
else:
    print("✅ Tüm gerekli sütunlar mevcut")
```

### Örnek 10: Veri Seti Filtreleme

```python
# Sadece belirli yılları kullan
filtered_df = recommender.df[
    (recommender.df['year'] >= 2000) & 
    (recommender.df['year'] <= 2020)
].copy()

print(f"Filtrelenmiş veri seti: {len(filtered_df)} film")

# IMDB puanı yüksek filmleri filtrele
high_rated_df = recommender.df[
    recommender.df['imdb_rating_float'] >= 7.0
].copy()

print(f"Yüksek puanlı filmler: {len(high_rated_df)} film")

# Belirli türleri filtrele
sci_fi_df = recommender.df[
    recommender.df['genre'].str.contains('Q471839', na=False)  # Sci-fi genre ID
].copy()

print(f"Bilim kurgu filmleri: {len(sci_fi_df)} film")
```

---

## 🤖 Otomatik Analiz Örnekleri

### Örnek 11: Toplu Film Analizi

```python
# Test için film listesi
test_movies = ["Avatar", "Inception", "Matrix", "Pulp Fiction", "Godfather"]

print("🎬 TOPLU FİLM ANALİZİ")
print("=" * 50)

for movie_name in test_movies:
    try:
        # Her film için 3 öneri al
        recs = recommender.get_movie_recommendations(movie_name, 3)
        
        print(f"\n🎯 {movie_name}:")
        if recs:
            for i, rec in enumerate(recs, 1):
                print(f"  {i}. {rec['title']} ({rec['similarity_score']:.3f})")
        else:
            print("  ❌ Öneri bulunamadı")
            
    except Exception as e:
        print(f"  ⚠️ Hata: {e}")
```

### Örnek 12: Performans Testi

```python
import time

# Performans testi
print("⚡ PERFORMANS TESTİ")
print("=" * 30)

# Sistem yükleme süresi
start_time = time.time()
test_recommender = WikidataMovieRecommender()
load_time = time.time() - start_time
print(f"Sistem yükleme: {load_time:.2f} saniye")

# Öneri hızı testi
test_queries = ["Avatar", "Inception", "Matrix"]
total_recommendation_time = 0

for query in test_queries:
    start_time = time.time()
    recs = test_recommender.get_movie_recommendations(query, 5)
    rec_time = time.time() - start_time
    total_recommendation_time += rec_time
    print(f"{query} önerileri: {rec_time:.3f} saniye")

avg_time = total_recommendation_time / len(test_queries)
print(f"Ortalama öneri süresi: {avg_time:.3f} saniye")
```

---

## 📊 Görselleştirme Örnekleri

### Örnek 13: Tür Dağılımı Görselleştirme

```python
import matplotlib.pyplot as plt
from collections import Counter

# Tür dağılımını hesapla
all_genres = []
for _, movie in recommender.df.iterrows():
    if movie['genre']:
        # Genre mapping uygula
        genre_features = recommender.process_genre_feature(movie['genre'])
        if genre_features:
            genres = genre_features.split()
            all_genres.extend(genres)

# En popüler 10 türü al
genre_counts = Counter(all_genres)
top_genres = dict(genre_counts.most_common(10))

# Grafik oluştur
plt.figure(figsize=(12, 6))
plt.bar(top_genres.keys(), top_genres.values())
plt.title('En Popüler Film Türleri')
plt.xlabel('Tür')
plt.ylabel('Film Sayısı')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

### Örnek 14: Yıl Dağılımı Analizi

```python
# Yıl dağılımını analiz et
year_data = recommender.df[recommender.df['year'] > 0]['year']

# İstatistikler
print("📅 YIL DAĞILIMI:")
print(f"En eski film: {year_data.min()}")
print(f"En yeni film: {year_data.max()}")
print(f"Ortalama yıl: {year_data.mean():.1f}")
print(f"Medyan yıl: {year_data.median():.0f}")

# Onluk bazında dağılım
decade_data = (year_data // 10) * 10
decade_counts = decade_data.value_counts().sort_index()

print("\n📊 ONLUK DAĞILIMI:")
for decade, count in decade_counts.items():
    print(f"{decade}s: {count} film")
```

---

## 🎛️ Özelleştirme Örnekleri

### Örnek 15: Özel Tür Mapping

```python
# Kendi tür mapping'inizi ekleyin
custom_genre_mapping = {
    'Q1535153': 'superhero',      # Süper kahraman
    'Q2484376': 'mystery',        # Gizem
    'Q200092': 'horror',          # Korku
    'Q21590660': 'documentary'    # Belgesel
}

# Mevcut mapping'i güncelle
original_mapping = recommender.process_genre_feature.__defaults__
print("Özel tür mapping eklendi")

# Test edin
test_genre = "Q1535153|Q200092"
processed = recommender.process_genre_feature(test_genre)
print(f"Input: {test_genre}")
print(f"Output: {processed}")
```

### Örnek 16: Özel Benzerlik Fonksiyonu

```python
def custom_similarity_analyzer(target_movie, similar_movie):
    """Özel benzerlik analizi fonksiyonu"""
    reasons = []
    
    # Özel mantık: Aynı yönetmen varsa çok önemli
    if target_movie.get('director') and similar_movie.get('director'):
        target_dirs = set(str(target_movie['director']).split('|'))
        similar_dirs = set(str(similar_movie['director']).split('|'))
        common_dirs = target_dirs.intersection(similar_dirs)
        
        if common_dirs:
            reasons.append(f"⭐ AYNI YÖNETMEN: {len(common_dirs)} ortak")
    
    # Özel mantık: Aynı seri varsa çok önemli
    if target_movie.get('part_of_series') and similar_movie.get('part_of_series'):
        target_series = set(str(target_movie['part_of_series']).split('|'))
        similar_series = set(str(similar_movie['part_of_series']).split('|'))
        common_series = target_series.intersection(similar_series)
        
        if common_series:
            reasons.append(f"🎬 AYNI SERİ: {len(common_series)} ortak")
    
    # Diğer standart analizler...
    standard_reasons = recommender.analyze_similarity_reasons(target_movie, similar_movie)
    reasons.extend(standard_reasons)
    
    return reasons[:3]  # En önemli 3 neden

# Özel fonksiyonu test et
movie1 = recommender.df.iloc[0]
movie2 = recommender.df.iloc[1]
custom_reasons = custom_similarity_analyzer(movie1, movie2)
print(f"Özel analiz sonucu: {custom_reasons}")
```

---

## 🔄 İnteraktif Örnekler

### Örnek 17: Film Keşif Uygulaması

```python
def film_discovery_app():
    """İnteraktif film keşif uygulaması"""
    print("🎬 FİLM KEŞİF UYGULAMASI")
    print("=" * 40)
    
    while True:
        print("\n📋 SEÇENEKLER:")
        print("1. Film önerisi al")
        print("2. Tür bazlı filtreleme")
        print("3. Yıl bazlı filtreleme")
        print("4. IMDB puanı bazlı filtreleme")
        print("5. Çıkış")
        
        choice = input("\nSeçiminiz (1-5): ").strip()
        
        if choice == '1':
            movie_name = input("Film adı: ").strip()
            count = int(input("Kaç öneri? (varsayılan 5): ") or "5")
            
            recs = recommender.get_movie_recommendations(movie_name, count)
            if recs:
                print(f"\n🎯 '{movie_name}' için öneriler:")
                for i, rec in enumerate(recs, 1):
                    print(f"{i}. {rec['title']} ({rec['year']}) - {rec['similarity_score']:.3f}")
            else:
                print("❌ Öneri bulunamadı")
                
        elif choice == '2':
            print("Mevcut türler:", ", ".join(['drama', 'comedy', 'action', 'horror', 'scifi']))
            genre_filter = input("Tür seçin: ").strip().lower()
            
            filtered_movies = recommender.df[
                recommender.df['genre_features'].str.contains(genre_filter, na=False)
            ]
            
            print(f"\n{genre_filter.title()} türünde {len(filtered_movies)} film bulundu:")
            for _, movie in filtered_movies.head(10).iterrows():
                print(f"  • {movie['title_en']} ({movie['year']})")
                
        elif choice == '5':
            print("Görüşmek üzere! 🎬")
            break
        else:
            print("Geçersiz seçim!")

# Uygulamayı başlat
# film_discovery_app()  # Yorum satırını kaldırarak çalıştırın
```

### Örnek 18: Öneri Karşılaştırma

```python
def compare_recommendations():
    """Farklı ayarlarla öneri karşılaştırması"""
    test_movie = "Avatar"
    
    # Orijinal ayarlarla
    original_recs = recommender.get_movie_recommendations(test_movie, 5)
    
    # Tür odaklı ayarlar
    recommender.feature_weights['genre'] = 0.40
    recommender.feature_weights['director'] = 0.10
    recommender.calculate_similarity_matrix()
    genre_focused_recs = recommender.get_movie_recommendations(test_movie, 5)
    
    # Yönetmen odaklı ayarlar
    recommender.feature_weights['genre'] = 0.15
    recommender.feature_weights['director'] = 0.35
    recommender.calculate_similarity_matrix()
    director_focused_recs = recommender.get_movie_recommendations(test_movie, 5)
    
    # Karşılaştırma
    print(f"🔍 '{test_movie}' için öneri karşılaştırması:")
    print("\n📊 ORİJİNAL AYARLAR:")
    for i, rec in enumerate(original_recs, 1):
        print(f"  {i}. {rec['title']} ({rec['similarity_score']:.3f})")
    
    print("\n🎭 TÜR ODAKLI:")
    for i, rec in enumerate(genre_focused_recs, 1):
        print(f"  {i}. {rec['title']} ({rec['similarity_score']:.3f})")
    
    print("\n🎬 YÖNETMEN ODAKLI:")
    for i, rec in enumerate(director_focused_recs, 1):
        print(f"  {i}. {rec['title']} ({rec['similarity_score']:.3f})")

# Karşılaştırmayı çalıştır
# compare_recommendations()  # Yorum satırını kaldırarak çalıştırın
```

---

## 🧪 Test ve Debug Örnekleri

### Örnek 19: Sistem Testi

```python
def comprehensive_system_test():
    """Kapsamlı sistem testi"""
    print("🧪 KAPSAMLI SİSTEM TESTİ")
    print("=" * 40)
    
    # Test 1: Modül yükleme
    try:
        test_recommender = WikidataMovieRecommender()
        print("✅ Test 1: Modül yükleme - BAŞARILI")
    except Exception as e:
        print(f"❌ Test 1: Modül yükleme - BAŞARISIZ: {e}")
        return
    
    # Test 2: Özellik sayısı
    expected_features = 16
    actual_features = len(test_recommender.feature_weights)
    if actual_features == expected_features:
        print(f"✅ Test 2: Özellik sayısı ({actual_features}) - BAŞARILI")
    else:
        print(f"❌ Test 2: Özellik sayısı beklenen {expected_features}, actual {actual_features}")
    
    # Test 3: Veri seti boyutu
    if len(test_recommender.df) > 0:
        print(f"✅ Test 3: Veri seti ({len(test_recommender.df)} film) - BAŞARILI")
    else:
        print("❌ Test 3: Veri seti boş")
    
    # Test 4: Öneri sistemi
    try:
        test_recs = test_recommender.get_movie_recommendations("Avatar", 3)
        if len(test_recs) > 0:
            print(f"✅ Test 4: Öneri sistemi ({len(test_recs)} öneri) - BAŞARILI")
        else:
            print("❌ Test 4: Öneri sistemi - öneri üretilmedi")
    except Exception as e:
        print(f"❌ Test 4: Öneri sistemi - BAŞARISIZ: {e}")
    
    # Test 5: Benzerlik matrisi
    if test_recommender.similarity_matrix is not None:
        matrix_shape = test_recommender.similarity_matrix.shape
        print(f"✅ Test 5: Benzerlik matrisi {matrix_shape} - BAŞARILI")
    else:
        print("❌ Test 5: Benzerlik matrisi oluşturulamadı")
    
    print("\n🎯 TÜM TESTLER TAMAMLANDI")

# Testi çalıştır
comprehensive_system_test()
```

### Örnek 20: Debug ve Troubleshooting

```python
def debug_recommendation(movie_name):
    """Öneri debug fonksiyonu"""
    print(f"🔍 '{movie_name}' için debug analizi:")
    print("=" * 50)
    
    # Film bulma
    movie_matches = recommender.df[
        recommender.df['title_en'].str.contains(movie_name, case=False, na=False)
    ]
    
    if movie_matches.empty:
        print("❌ Film bulunamadı!")
        # Benzer isimli filmleri öner
        similar_names = recommender.df[
            recommender.df['title_en'].str.contains(movie_name.split()[0], case=False, na=False)
        ]['title_en'].head(5)
        print("💡 Benzer filmler:")
        for name in similar_names:
            print(f"  • {name}")
        return
    
    target_movie = movie_matches.iloc[0]
    print(f"✅ Film bulundu: {target_movie['title_en']} ({target_movie['year']})")
    
    # Özellik analizi
    print(f"\n🎯 ÖZELLİK ANALİZİ:")
    print(f"Genre: {target_movie.get('genre', 'N/A')}")
    print(f"Director: {target_movie.get('director', 'N/A')}")
    print(f"Cast: {target_movie.get('cast_member', 'N/A')[:100]}...")  # İlk 100 karakter
    print(f"Year: {target_movie.get('year', 'N/A')}")
    print(f"Country: {target_movie.get('country', 'N/A')}")
    
    # Feature vector analizi
    combined_features = target_movie.get('combined_features', '')
    print(f"\n🔧 FEATURE VECTOR:")
    print(f"Uzunluk: {len(combined_features.split())} kelime")
    print(f"İlk 150 karakter: {combined_features[:150]}...")
    
    # Benzerlik skorları
    movie_idx = movie_matches.index[0]
    similarity_scores = recommender.similarity_matrix[movie_idx]
    
    print(f"\n📊 BENZERLİK SKORLARI:")
    print(f"Maksimum skor: {similarity_scores.max():.4f}")
    print(f"Ortalama skor: {similarity_scores.mean():.4f}")
    print(f"Minimum skor: {similarity_scores.min():.4f}")
    
    # En yüksek 5 benzerlik
    top_indices = similarity_scores.argsort()[::-1][1:6]  # Kendisi hariç
    print(f"\n🎯 EN YÜKSEK 5 BENZERLİK:")
    for i, idx in enumerate(top_indices, 1):
        similar_movie = recommender.df.iloc[idx]
        score = similarity_scores[idx]
        print(f"  {i}. {similar_movie['title_en']} - {score:.4f}")

# Debug fonksiyonunu test et
debug_recommendation("Avatar")
```

---

## 🎓 İleri Düzey Örnekler

### Örnek 21: Özel Scoring Sistemi

```python
def custom_scoring_system(recommendations, user_preferences):
    """
    Kullanıcı tercihlerine göre özel skorlama
    
    user_preferences = {
        'preferred_genres': ['action', 'scifi'],
        'min_year': 2000,
        'min_imdb_rating': 7.0,
        'preferred_directors': ['Q42574']  # James Cameron
    }
    """
    scored_recs = []
    
    for rec in recommendations:
        base_score = rec['similarity_score']
        bonus_score = 0
        
        # Tercih edilen tür bonusu
        if 'preferred_genres' in user_preferences:
            # Bu kısım daha detaylı implementasyon gerektirir
            # Şimdilik basit örnek
            bonus_score += 0.1
        
        # Yıl bonusu
        if 'min_year' in user_preferences:
            if rec['year'] >= user_preferences['min_year']:
                bonus_score += 0.05
        
        # IMDB rating bonusu
        if 'min_imdb_rating' in user_preferences:
            if rec['imdb_rating'] >= user_preferences['min_imdb_rating']:
                bonus_score += 0.1
        
        # Final skor
        final_score = base_score + bonus_score
        
        rec_copy = rec.copy()
        rec_copy['custom_score'] = final_score
        rec_copy['bonus_applied'] = bonus_score
        scored_recs.append(rec_copy)
    
    # Özel skora göre sırala
    scored_recs.sort(key=lambda x: x['custom_score'], reverse=True)
    return scored_recs

# Kullanım örneği
user_prefs = {
    'preferred_genres': ['action', 'scifi'],
    'min_year': 2000,
    'min_imdb_rating': 6.0
}

basic_recs = recommender.get_movie_recommendations("Avatar", 5)
custom_recs = custom_scoring_system(basic_recs, user_prefs)

print("🎯 ÖZEL SKORLAMA SİSTEMİ:")
for i, rec in enumerate(custom_recs, 1):
    print(f"{i}. {rec['title']} - Orijinal: {rec['similarity_score']:.3f}, "
          f"Özel: {rec['custom_score']:.3f} (+{rec['bonus_applied']:.3f})")
```

---

**🎬 Bu örnekler ile Wikidata Film Öneri Sistemi v0.4'ün tüm potansiyelini keşfedin!**

**💡 İpucu:** Her örneği test ederek sistemi daha iyi anlayabilir ve kendi ihtiyaçlarınıza göre özelleştirebilirsiniz.
