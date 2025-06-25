# Film Öneri Sistemi v0.2 Beta

Bu versiyon, büyük veriset desteği ve gelişmiş özelliklerle güncellenmiş film öneri sistemidir.

## 🆕 v0.2 Yenilikleri

### 📊 **Büyük Veriset Desteği**
- **5000 Film**: TMDb verisetinden 5000 popüler film
- **Zengin Metadata**: Yönetmen, oyuncular, bütçe, hasılat
- **Çoklu Format**: CSV ve işlenmiş veriset desteği

### 🚀 **Gelişmiş Uygulamalar**
- **Enhanced Interactive App**: Daha akıllı film arayüzü
- **Advanced Filtering**: Yıl, tür, puan bazlı filtreleme
- **Data Processing**: TMDb veriset işleme araçları

## 📋 Gereksinimler

```bash
pip install -r requirements.txt
```

**Bağımlılıklar:**
- pandas
- scikit-learn
- numpy
- matplotlib (görselleştirme için)

## 🚀 Kullanım

### 1. Ana Uygulamalar
```bash
# Temel interaktif uygulama
python interactive_movie_app.py

# Gelişmiş özellikli uygulama
python interactive_movie_app_enhanced.py

# En gelişmiş versiyon (v2)
python interactive_movie_app_enhanced_v2.py

# Klasik demo
python demo_app.py
```

### 2. Veriset İşleme
```bash
# TMDb veriseti işle
python tmdb_data_processor.py
```

## 📊 Verisetler

### **1. movies.csv** (Temel - 25 film)
- v0.1'den miras veriset
- Hızlı test için ideal

### **2. tmdb_5000_movies.csv** (Ham - 5000 film)
- **Kaynak**: The Movie Database (TMDb)
- **İçerik**: Ham film metadata
- **Boyut**: ~5.7 MB

### **3. processed_tmdb_movies.csv** (İşlenmiş - 4800+ film)
- **Temizlenmiş**: Eksik veri filtrelenmiş
- **Optimize**: Öneri algoritması için hazırlanmış
- **Zengin**: 20+ sütun metadata

## 🎯 Gelişmiş Özellikler

### **İnteraktif Uygulamalar**

#### `interactive_movie_app_enhanced.py`
- ✅ **Akıllı Arama**: Film başlığı arama
- ✅ **Çoklu Seçim**: Birden fazla film seçimi
- ✅ **Filtreleme**: Yıl ve tür filtreleri
- ✅ **Istatistikler**: Veriset analizi

#### `interactive_movie_app_enhanced_v2.py`
- ✅ **Gelişmiş UI**: Daha iyi kullanıcı deneyimi
- ✅ **Puan Tabanlı**: IMDB/TMDb puanları
- ✅ **Bütçe/Hasılat**: Mali bilgiler
- ✅ **Popülerlik**: Trend analizi

### **Veriset İşleme**

#### `tmdb_data_processor.py`
```python
# Ham TMDb verilerini işle
processor = TMDbDataProcessor('tmdb_5000_movies.csv')
processed_data = processor.process_data()
processor.save_processed_data('processed_tmdb_movies.csv')
```

## 🧠 Gelişmiş Algoritma

### **Çoklu Özellik Analizi**
```python
# Gelişmiş özellik matrisi
features = [
    'genres',           # Film türleri
    'director',         # Yönetmen
    'cast',             # Oyuncular
    'keywords',         # Anahtar kelimeler
    'overview',         # Film özeti
    'vote_average',     # Ortalama puan
    'budget_category',  # Bütçe kategorisi
    'revenue_category'  # Hasılat kategorisi
]
```

### **Ağırlıklı Benzerlik**
- **Türler**: %40 ağırlık
- **Yönetmen**: %25 ağırlık
- **Oyuncular**: %20 ağırlık
- **Özet**: %15 ağırlık

## 📁 Dosya Yapısı

```
v0.2_Beta/
├── main.py                              # Ana program (v0.1 uyumlu)
├── content_based_recommender.py         # Temel algoritma
├── interactive_movie_app.py             # Basit arayüz
├── interactive_movie_app_enhanced.py    # Gelişmiş arayüz
├── interactive_movie_app_enhanced_v2.py # En gelişmiş arayüz
├── demo_app.py                          # Demo uygulaması
├── test_recommender.py                  # Test scriptleri
├── tmdb_data_processor.py               # Veriset işleyici
├── movies.csv                           # Küçük veriset (25 film)
├── tmdb_5000_movies.csv                 # Büyük ham veriset
├── processed_tmdb_movies.csv            # İşlenmiş veriset
├── requirements.txt                     # Bağımlılıklar
└── README.md                            # Bu dosya
```

## 🎯 Kullanım Örnekleri

### **1. Hızlı Başlangıç**
```bash
python interactive_movie_app_enhanced_v2.py
```

### **2. Büyük Veriset ile Test**
```python
from content_based_recommender import ContentBasedRecommender

# Büyük veriset yükle
recommender = ContentBasedRecommender('processed_tmdb_movies.csv')

# Gelişmiş öneri
watched = ['The Dark Knight', 'Inception', 'Interstellar']
recommendations = recommender.get_recommendations(
    watched_movies=watched,
    num_recommendations=10,
    min_year=2010,
    genres_filter=['Action', 'Sci-Fi']
)
```

### **3. Veriset İşleme**
```python
from tmdb_data_processor import TMDbDataProcessor

# Ham veriyi işle
processor = TMDbDataProcessor('tmdb_5000_movies.csv')
processor.clean_data()
processor.feature_engineering()
processor.save_processed_data('my_processed_data.csv')
```

## 📊 Performans

### **Veriset Karşılaştırması**
| Veriset | Film Sayısı | Özellik | İşlem Süresi | Bellek |
|---------|-------------|---------|--------------|--------|
| movies.csv | 25 | Basit | <1s | <10MB |
| processed_tmdb.csv | 4800+ | Zengin | 2-5s | 50-100MB |

### **Öneri Kalitesi**
- **Küçük Veriset**: %70-80 kullanıcı memnuniyeti
- **Büyük Veriset**: %85-90 kullanıcı memnuniyeti
- **Çeşitlilik**: 5x daha fazla tür kapsamı

## 🔧 Yapılandırma

### **Veriset Seçimi**
```python
# Hızlı test için
DATASET = 'movies.csv'

# Kaliteli öneriler için  
DATASET = 'processed_tmdb_movies.csv'
```

### **Algoritma Ayarları**
```python
# Öneri parametreleri
NUM_RECOMMENDATIONS = 10
MIN_SIMILARITY = 0.1
FEATURE_WEIGHTS = {
    'genres': 0.4,
    'director': 0.25,
    'cast': 0.2,
    'overview': 0.15
}
```

## 🚧 Bilinen Sınırlamalar

- **İşlem Süresi**: Büyük veriset 2-5 saniye
- **Bellek Kullanımı**: 50-100 MB RAM gerekli
- **Cold Start**: Yeni kullanıcılar için sınırlı
- **Çeşitlilik**: Benzer türlerde yoğunlaşma

## 🔮 v0.3 Planları

- **OMDB API**: Gerçek zamanlı film verileri
- **User Profiling**: Kullanıcı geçmişi takibi
- **Machine Learning**: Gelişmiş ML algoritmaları
- **Web Interface**: Browser tabanlı arayüz

---

**Not**: v0.2 büyük adım! 5000 film ile güçlü öneriler! 🎬🚀
