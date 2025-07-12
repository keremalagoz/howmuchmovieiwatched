# 🎬 Wikidata Movie Recommender - v0.4 Beta
## Hızlı Başlangıç Rehberi (Quick Start Guide)

### 📋 Sistem Gereksinimleri
- Python 3.7+
- Gerekli paketler: `pip install -r requirements.txt`
- Minimum 2GB RAM (büyük veri setleri için)
- Minimum 500MB disk alanı

### ⚡ Hızlı Kurulum (3 Adım)

#### 1. Repository'yi İndir
```bash
# Git ile
git clone <repository-url>
cd "howmuchmovieiwatched.com/Releases/v0.4 - Beta"

# Veya ZIP dosyasını indir ve çıkart
```

#### 2. Bağımlılıkları Yükle
```bash
pip install -r requirements.txt
```

#### 3. Sistemi Test Et
```bash
python system_test.py
```

### 🚀 Temel Kullanım

#### A) Komut Satırından Çalıştırma
```bash
# Ana sistem
python wikidata_movie_recommender.py

# Etkileşimli kullanım - film adı girin
🔍 Film adı girin: Avatar
```

#### B) Python Scripti Olarak Kullanma
```python
from wikidata_movie_recommender import WikidataMovieRecommender

# Sistem başlatma
recommender = WikidataMovieRecommender()

# Film önerisi alma
recommendations = recommender.get_movie_recommendations("Avatar", n_recommendations=5)

# Sonuçları yazdırma
for i, rec in enumerate(recommendations, 1):
    print(f"{i}. {rec['title']} - Benzerlik: {rec['similarity_score']:.3f}")
```

### 🔧 Gelişmiş Özellikler

#### Dataset Yeniden Oluşturma
```bash
# Wikidata'dan yeni veri çekme
python enhanced_wikidata_scraper.py

# Yeni CSV dosyası: wikidata_films.csv
```

#### Sistem İstatistikleri
```python
stats = recommender.get_dataset_statistics()
print(f"Toplam film: {stats['total_movies']}")
print(f"Ortalama IMDB puanı: {stats['avg_imdb_rating']:.1f}")
```

#### Özellik Ağırlıklarını Değiştirme
```python
# Özellik ağırlıklarını görüntüleme
print(recommender.feature_weights)

# Ağırlıkları değiştirme
recommender.feature_weights['genre'] = 0.30  # Tür ağırlığını artır
recommender.feature_weights['year'] = 0.05   # Yıl ağırlığını azalt

# Sistem yeniden hesaplama
recommender.calculate_similarity_matrix()
```

### 🎯 Kullanım Senaryoları

#### 1. Film Keşfi
```python
# Sevdiğiniz filmden benzer filmler bulmak
recommendations = recommender.get_movie_recommendations("The Matrix")
recommender.print_recommendations(recommendations, "The Matrix")
```

#### 2. Tür Bazlı Analiz
```python
# Belirli türdeki filmler
action_movies = recommender.df[recommender.df['genre'].str.contains('action', case=False, na=False)]
print(f"Aksiyon filmi sayısı: {len(action_movies)}")
```

#### 3. Benzerlik Analizi
```python
# İki film arasındaki benzerlik
movie1 = "Avatar"
movie2 = "Titanic"
# Benzerlik skorları karşılaştırma
```

### 📊 Desteklenen Özellikler
- **Temel**: Tür, yönetmen, oyuncular, yıl
- **Gelişmiş**: Müzik, senaryo, yapım şirketi, ödüller
- **Coğrafi**: Ülke, dil, çekim yeri
- **Finansal**: Bütçe, hasılat kategorileri
- **Kalite**: IMDB puanı, süre kategorileri
- **İçerik**: Ana tema, açıklama anahtar kelimeleri

### 🔍 Sorun Giderme

#### Yaygın Hatalar
```bash
# Modül bulunamadı
pip install -r requirements.txt

# CSV dosyası bulunamadı
# test_wikidata_films.csv dosyasının aynı klasörde olduğundan emin olun

# Bellek hatası
# Daha küçük veri seti kullanın veya RAM'i artırın
```

#### Performans Optimizasyonu
```python
# Daha az özellik kullanma
recommender.feature_weights = {
    'genre': 0.4,
    'director': 0.3,
    'cast': 0.2,
    'year': 0.1
}

# Daha az film önerisi
recommendations = recommender.get_movie_recommendations("Film", n_recommendations=3)
```

### 📞 Destek
- **Dokümantasyon**: README.md, FEATURES.md, EXAMPLES.md
- **Testler**: test_features.py, system_test.py
- **İleri Kurulum**: INSTALLATION.md
- **Değişiklikler**: CHANGELOG.md

### 📈 Sistemin Gücü
- ✅ **16 ana özellik** kullanan kapsamlı analiz
- ✅ **TF-IDF + Cosine Similarity** ile matematiksel doğruluk
- ✅ **Açıklanabilir AI** - her önerinin nedeni belli
- ✅ **Wikidata entegrasyonu** - zengin meta veri
- ✅ **Çok dilli destek** - Türkçe/İngilizce
- ✅ **Ölçeklenebilir** - binlerce film destekler

### 🎯 Sonuç
Bu sistem, film önerilerini sadece basit benzerlik değil, **16 farklı özelliği** analiz ederek **matematiksel** ve **açıklanabilir** şekilde sunar. Wikidata'nın zengin veri kaynağı sayesinde geleneksel öneri sistemlerinden çok daha detaylı ve doğru sonuçlar alırsınız.

**Başlamak için**: `python wikidata_movie_recommender.py`
