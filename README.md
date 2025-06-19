# Film İzleme Sayacı - İçerik Bazlı Film Önerme Sistemi

Bu modül, kullanıcının izlediği filmlere dayanarak benzer içerikli filmler önerir. Sistem, filmlerin tür, yönetmen, oyuncular ve konu özetlerini analiz ederek kullanıcının zevk profilini oluşturur.

## Özellikler

✅ **İçerik Bazlı Filtreleme**: Filmler arasındaki benzerliği metadata'ya göre hesaplar  
✅ **Sürekli Öğrenme**: Her yeni film eklendikinde kullanıcı profilini günceller  
✅ **Esnek Veri Yapısı**: CSV formatındaki film verilerini destekler  
✅ **Performanslı Algoritma**: TF-IDF ve cosine similarity kullanır  
✅ **Kolay Entegrasyon**: Basit Python API'si  

## Kurulum

### 1. Gerekli Kütüphaneleri Kurun
```bash
pip install -r requirements.txt
```

### 2. Veri Dosyasını Hazırlayın
`movies.csv` dosyasında şu sütunlar bulunmalıdır:
- `movie_id`: Benzersiz film kimliği
- `title`: Film başlığı
- `genres`: Türler (virgülle ayrılmış)
- `director`: Yönetmen adı
- `actors`: Oyuncular (virgülle ayrılmış)
- `plot_summary`: Konu özeti

## Kullanım

### Temel Kullanım

```python
from content_based_recommender import ContentBasedRecommender

# Sistem başlatma
recommender = ContentBasedRecommender('movies.csv')

# Kullanıcının izlediği filmler
watched_movies = [101, 102, 108]  # Film ID'leri

# Önerileri al
recommendations = recommender.get_recommendations(
    watched_movie_ids=watched_movies,
    num_recommendations=10
)

# Sonuçları görüntüle
for rec in recommendations:
    print(f"{rec['title']} - Benzerlik: {rec['similarity_score']:.3f}")
```

### Film Arama

```python
# Başlıkta arama
results = recommender.search_movies("Matrix", max_results=5)
for movie in results:
    print(f"{movie['title']} ({movie['director']})")
```

### Film Bilgisi Alma

```python
# Belirli bir filmin detaylarını al
movie_info = recommender.get_movie_info(101)
print(f"Film: {movie_info['title']}")
print(f"Tür: {movie_info['genres']}")
print(f"Yönetmen: {movie_info['director']}")
```

### Sistem İstatistikleri

```python
stats = recommender.get_stats()
print(f"Toplam Film: {stats['total_movies']}")
print(f"Benzersiz Yönetmen: {stats['unique_directors']}")
```

## API Referansı

### `ContentBasedRecommender` Sınıfı

#### `__init__(movie_data_path: str)`
Sistem başlatma ve veri yükleme.

**Parametreler:**
- `movie_data_path`: CSV dosyasının yolu

#### `get_recommendations(watched_movie_ids: List[int], num_recommendations: int = 10)`
Film önerilerini getirir.

**Parametreler:**
- `watched_movie_ids`: İzlenen filmlerin ID listesi
- `num_recommendations`: Önerilecek film sayısı

**Dönen Değer:**
```python
[
    {
        'movie_id': 105,
        'title': 'The Matrix',
        'genres': 'Action,Sci-Fi',
        'director': 'The Wachowskis',
        'similarity_score': 0.789
    },
    ...
]
```

#### `search_movies(query: str, max_results: int = 10)`
Film başlığında arama yapar.

#### `get_movie_info(movie_id: int)`
Belirli bir filmin detaylarını getirir.

#### `get_stats()`
Sistem istatistiklerini döndürür.

## Algoritma Detayları

### 1. Veri Ön İşleme
- Eksik değerler boş string ile doldurulur
- Tüm metin alanları birleştirilerek tek bir `features` sütunu oluşturulur

### 2. TF-IDF Vektörleştirme
- Stop words (anlamsız kelimeler) filtrelenir
- Unigram ve bigram n-gramları kullanılır
- Maksimum 5000 özellik ile performans optimize edilir

### 3. Kullanıcı Profili Oluşturma
- İzlenen filmlerin TF-IDF vektörlerinin ortalaması alınır
- Bu ortalama vektör kullanıcının zevk profilini temsil eder

### 4. Benzerlik Hesaplama
- Cosine similarity kullanılarak profil ile tüm filmler karşılaştırılır
- Benzerlik skorlarına göre sıralama yapılır

### 5. Filtreleme ve Sıralama
- İzlenen filmler sonuçlardan çıkarılır
- En yüksek benzerlik skoruna sahip filmler önerilir

## Performans Optimizasyonları

- **Özellik Sınırlaması**: Maksimum 5000 TF-IDF özelliği
- **Sparse Matrix**: Bellek tasarrufu için sparse matris kullanımı
- **Batch Processing**: Toplu benzerlik hesaplama
- **Caching**: Vektörleştirici ve matris önbellekleme

## Gelişmiş Kullanım

### Özel Parametre Ayarları

```python
# TF-IDF parametrelerini özelleştirmek için sınıfı genişletin
class CustomRecommender(ContentBasedRecommender):
    def __init__(self, movie_data_path):
        # TF-IDF ayarlarını değiştirin
        self.tfidf_vectorizer = TfidfVectorizer(
            stop_words='english',
            max_features=10000,  # Daha fazla özellik
            ngram_range=(1, 3),  # Trigram da dahil et
            min_df=2,           # Minimum doküman frekansı
            max_df=0.8          # Maksimum doküman frekansı
        )
        super().__init__(movie_data_path)
```

### Hibrit Önerme Sistemi

Bu content-based yaklaşımı collaborative filtering ile birleştirerek hibrit bir sistem oluşturabilirsiniz:

```python
# Content-based skorları al
content_recs = recommender.get_recommendations(watched_movies)

# Collaborative filtering skorları ile birleştir
# final_score = alpha * content_score + (1-alpha) * collab_score
```

## Sorun Giderme

### Yaygın Hatalar

1. **"CSV dosyası bulunamadı"**
   - Dosya yolunu kontrol edin
   - Dosyanın var olduğundan emin olun

2. **"Eksik sütunlar"**
   - CSV dosyasının gerekli sütunları içerdiğini doğrulayın
   - Sütun isimlerinin doğru olduğunu kontrol edin

3. **"İzlenen film ID listesi boş"**
   - En az bir film ID'si sağlayın
   - ID'lerin veri setinde bulunduğundan emin olun

### Performans İpuçları

- Büyük veri setleri için `max_features` parametresini artırın
- Bellek kullanımını azaltmak için veri setini parçalara bölün
- GPU desteği için cupy kütüphanesini kullanabilirsiniz

## Test

Sistemi test etmek için:

```bash
python test_recommender.py
```

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır.
