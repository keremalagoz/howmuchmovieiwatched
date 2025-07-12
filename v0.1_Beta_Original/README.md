# Film Öneri Sistemi v0.1 Beta

Bu, film öneri sistemimizin ilk beta versiyonudur. Basit ve etkili içerik bazlı filtreleme kullanır.

## 🎬 Özellikler

### ✨ Temel Film Önerisi
- **İçerik Bazlı Filtreleme**: Film türlerine dayalı öneri sistemi
- **Basit CSV Veriset**: 25 popüler film ile başlangıç
- **Cosine Similarity**: Matematiksel benzerlik hesaplama
- **Hızlı ve Etkili**: Anında sonuç

### 🛠️ Araçlar
- `main.py` - Ana çalıştırılabilir dosya
- `content_based_recommender.py` - Temel öneri algoritması
- `interactive_movie_app.py` - Basit interaktif uygulama
- `demo_app.py` - Demo ve test uygulaması
- `test_recommender.py` - Sistem testi

## 📋 Gereksinimler

```bash
pip install -r requirements.txt
```

**Bağımlılıklar:**
- pandas
- scikit-learn
- numpy

## 🚀 Kullanım

### 1. Hızlı Başlangıç
```bash
python main.py
```

### 2. İnteraktif Uygulama
```bash
python interactive_movie_app.py
```

### 3. Demo ve Test
```bash
python demo_app.py
python test_recommender.py
```

## 📊 Veriset

**movies.csv** - 25 popüler film:
- Film ID, başlık, tür, yıl
- Basit metadata
- Manuel olarak seçilmiş kaliteli filmler

## 🎯 Algoritma

### Content-Based Filtering
```python
# Film özellik vektörleri oluşturma
tfidf = TfidfVectorizer(stop_words='english')
feature_matrix = tfidf.fit_transform(movie_features)

# Benzerlik hesaplama
similarity_matrix = cosine_similarity(feature_matrix)

# Öneri üretme
recommendations = get_similar_movies(user_preferences, similarity_matrix)
```

### Çalışma Prensibi
1. **Özellik Çıkarma**: Film türleri ve açıklamalarından özellik vektörleri
2. **TF-IDF**: Metin madenciliği ile özellik ağırlıklandırma
3. **Cosine Similarity**: Vektörler arası benzerlik ölçümü
4. **Sıralama**: En benzer filmleri sıralayarak öneri

## 📁 Dosya Yapısı

```
v0.1_Beta/
├── main.py                          # Ana program
├── content_based_recommender.py     # Öneri algoritması
├── interactive_movie_app.py         # İnteraktif arayüz
├── demo_app.py                      # Demo uygulaması
├── test_recommender.py              # Test scriptleri
├── movies.csv                       # Film veriset
├── requirements.txt                 # Python bağımlılıkları
└── README.md                        # Bu dosya
```

## 🎯 Özellikler

### Güçlü Yanlar
- ✅ **Basit ve Anlaşılır**: Temiz kod yapısı
- ✅ **Hızlı**: Anında sonuç üretir
- ✅ **Stabil**: Minimal bağımlılık
- ✅ **Test Edilmiş**: Çalışan demo örnekleri

### Sınırlamalar
- ❌ **Küçük Veriset**: Sadece 25 film
- ❌ **Basit Metadata**: Sınırlı film bilgisi
- ❌ **No User Profiling**: Kullanıcı geçmişi yok
- ❌ **No Rating System**: Puanlama sistemi yok

## 🚀 Performans

- **Film Sayısı**: 25
- **Özellik Boyutu**: ~100 TF-IDF özelliği
- **Yanıt Süresi**: <1 saniye
- **Bellek Kullanımı**: <10 MB

## 🔄 Gelecek Sürümler

### v0.2 Planları
- Daha büyük veriset (1000+ film)
- Gelişmiş metadata
- Kullanıcı profilleri
- Rating sistemi

### v0.3 Planları
- OMDB API entegrasyonu
- Gerçek zamanlı veri
- Gelişmiş algoritma
- Web arayüzü

## 📞 Sorun Giderme

### Yaygın Sorunlar

**1. Import Hataları**
```bash
pip install pandas scikit-learn numpy
```

**2. CSV Dosya Hatası**
- `movies.csv` dosyasının aynı klasörde olduğundan emin olun

**3. Encoding Sorunları**
```python
# CSV dosyasını UTF-8 ile açın
pd.read_csv('movies.csv', encoding='utf-8')
```

## 💡 Kullanım Örnekleri

### Basit Öneri
```python
from content_based_recommender import ContentBasedRecommender

# Sistem başlat
recommender = ContentBasedRecommender('movies.csv')

# Film öner
movies = ['The Matrix', 'Inception']
recommendations = recommender.get_recommendations(movies, num_recommendations=5)

print("Önerilen filmler:")
for movie in recommendations:
    print(f"- {movie}")
```

### İnteraktif Kullanım
```bash
python interactive_movie_app.py
# İzlediğiniz filmleri seçin
# Sistem otomatik olarak öneri verecek
```

---

**Not**: Bu ilk beta versiyonudur. Basit ama etkili! 🎬
