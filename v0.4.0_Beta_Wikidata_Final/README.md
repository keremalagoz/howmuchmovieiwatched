# 🎬 Wikidata Film Öneri Sistemi v0.4 Beta

## 📖 Genel Bakış

**Wikidata Film Öneri Sistemi**, Wikidata'dan elde edilen zengin film verileri kullanarak **matematiksel content-based** film önerileri sunan gelişmiş bir sistemdir. 

### 🌟 Temel Özellikler

- **16 farklı özellik** kullanarak kapsamlı benzerlik analizi
- **Producer, cinematographer, film_editor** özellikle hariç tutulan temiz sistem
- **Açıklanabilir öneriler** - Her önerinin nedenini gösterir
- **Çoklu dil desteği** - İngilizce ve Türkçe
- **Matematiksel yaklaşım** - TF-IDF ve Cosine Similarity
- **Zengin Wikidata** entegrasyonu

---

## 🚀 Hızlı Başlangıç

### 1. Gereksinimler

```bash
pip install -r requirements.txt
```

### 2. Temel Kullanım

```python
from wikidata_movie_recommender import WikidataMovieRecommender

# Öneri sistemini başlat
recommender = WikidataMovieRecommender()

# Film önerileri al
recommendations = recommender.get_movie_recommendations("Avatar", 5)

# Önerileri yazdır
recommender.print_recommendations(recommendations, "Avatar")
```

### 3. İnteraktif Mod

```bash
python wikidata_movie_recommender.py
```

---

## 📊 Kullanılan Özellikler

### 🎯 **Temel Özellikler (Ağırlıklı)**

| Özellik | Ağırlık | Açıklama |
|---------|---------|----------|
| **genre** | 0.25 | Film türü (en önemli) |
| **director** | 0.20 | Yönetmen (çok önemli) |
| **cast** | 0.15 | Oyuncular (önemli) |
| **year** | 0.08 | Yıl (orta önemli) |
| **country** | 0.06 | Ülke (orta önemli) |
| **language** | 0.05 | Dil (düşük önemli) |

### 🎵 **Teknik Ekip Özellikleri**

| Özellik | Ağırlık | Açıklama |
|---------|---------|----------|
| **composer** | 0.04 | Müzik |
| **screenwriter** | 0.04 | Senarist |
| **production_company** | 0.03 | Yapım şirketi |

### 💰 **Finansal Özellikler**

| Özellik | Ağırlık | Açıklama |
|---------|---------|----------|
| **budget_range** | 0.03 | Bütçe aralığı |
| **box_office_range** | 0.02 | Hasılat aralığı |
| **imdb_rating_range** | 0.02 | IMDB puan aralığı |
| **duration_range** | 0.02 | Süre aralığı |

### 🏆 **İçerik Özellikleri**

| Özellik | Ağırlık | Açıklama |
|---------|---------|----------|
| **award_received** | 0.04 | Ödüller |
| **main_subject** | 0.03 | Ana konu/tema |
| **description_keywords** | 0.02 | Açıklama anahtar kelimeleri |

### 📍 **Ek Özellikler**

- **narrative_location** - Hikaye geçtiği yer
- **filming_location** - Çekim yeri
- **based_on** - Dayandığı eser
- **based_on_work** - Temel aldığı eser
- **part_of_series** - Serinin parçası
- **distributor** - Dağıtımcı
- **executive_producer** - Yürütücü yapımcı
- **original_network** - Orijinal kanal
- **original_broadcaster** - Orijinal yayıncı

---

## 🚫 Kullanılmayan Özellikler

Aşağıdaki özellikler **kasıtlı olarak** kullanılmaz:

- **producer** (P162) - Yapımcı
- **cinematographer** (P344) - Görüntü yönetmeni
- **film_editor** (P1040) - Kurgucu

**Neden?** Bu özellikler teknik prodüksiyon detaylarıyla ilgili olup, content-based önerilerde etkili değildir.

---

## 🔧 Kurulum

### 1. Depoyu Klonlayın

```bash
git clone [repository-url]
cd wikidata-movie-recommender
```

### 2. Gerekli Kütüphaneleri Yükleyin

```bash
pip install -r requirements.txt
```

### 3. Veri Setini Hazırlayın

#### Mevcut Test Veri Seti:
```bash
# test_wikidata_films.csv dosyası hazır olarak gelir
python wikidata_movie_recommender.py
```

#### Yeni Veri Seti Oluşturma:
```bash
# Enhanced Wikidata Scraper ile yeni veri çekin
python enhanced_wikidata_scraper.py
```

---

## 💻 Kullanım Örnekleri

### Örnek 1: Temel Öneri

```python
from wikidata_movie_recommender import WikidataMovieRecommender

# Sistem başlat
recommender = WikidataMovieRecommender("test_wikidata_films.csv")

# Avatar için 8 öneri al
recommendations = recommender.get_movie_recommendations("Avatar", 8)

# Sonuçları görüntüle
for i, rec in enumerate(recommendations, 1):
    print(f"{i}. {rec['title']} ({rec['year']}) - Benzerlik: {rec['similarity_score']:.3f}")
    print(f"   Nedenler: {', '.join(rec['similarity_reasons'])}")
```

### Örnek 2: Detaylı Analiz

```python
# Veri seti istatistikleri
stats = recommender.get_dataset_statistics()
print(f"Toplam film: {stats['total_movies']}")
print(f"IMDB puanı olan: {stats['movies_with_imdb']}")
print(f"Benzersiz tür: {stats['unique_genres']}")

# Benzerlik nedenlerini analiz et
target_movie = recommender.df.iloc[0]
similar_movie = recommender.df.iloc[1]
reasons = recommender.analyze_similarity_reasons(target_movie, similar_movie)
print(f"Benzerlik nedenleri: {reasons}")
```

### Örnek 3: Özellik Testleri

```python
# Özellik testleri çalıştır
python test_features.py
```

---

## 📁 Dosya Yapısı

```
v0.4 - Beta/
├── wikidata_movie_recommender.py    # Ana öneri sistemi
├── enhanced_wikidata_scraper.py     # Veri çekme sistemi
├── test_features.py                 # Özellik test sistemi
├── test_wikidata_films.csv         # Test veri seti (50 film)
├── requirements.txt                 # Python gereksinimleri
├── README.md                        # Bu dosya
├── CHANGELOG.md                     # Sürüm değişiklikleri
├── INSTALLATION.md                  # Kurulum kılavuzu
├── FEATURES.md                      # Özellik detayları
└── EXAMPLES.md                      # Kullanım örnekleri
```

---

## ⚙️ Konfigürasyon

### Feature Weights Değiştirme

```python
recommender = WikidataMovieRecommender()

# Özellik ağırlıklarını güncelle
recommender.feature_weights['genre'] = 0.30  # Türü daha önemli yap
recommender.feature_weights['director'] = 0.15  # Yönetmeni daha az önemli yap

# Sistem yeniden hesaplasın
recommender.calculate_similarity_matrix()
```

### TF-IDF Parametreleri

```python
# TF-IDF vektörize ayarları
self.tfidf_vectorizer = TfidfVectorizer(
    max_features=5000,      # Maksimum özellik sayısı
    stop_words='english',   # Stop words
    ngram_range=(1, 2),     # Unigram ve bigram
    min_df=1,               # Minimum doküman frekansı
    max_df=0.8              # Maksimum doküman frekansı
)
```

---

## 📈 Performans

### Test Sonuçları (v0.4 Beta)

- **Veri Seti:** 50 film
- **Özellik Sayısı:** 16
- **Benzerlik Hesaplama:** <1 saniye
- **Memory Kullanımı:** ~50MB
- **Öneri Kalitesi:** Yüksek (açıklanabilir nedenler)

### Sistem Gereksinimleri

- **Python:** 3.8+
- **RAM:** Minimum 512MB
- **CPU:** Herhangi bir modern CPU
- **Disk:** 100MB boş alan

---

## 🔍 Algoritma Detayları

### 1. Veri Temizleme
- Boş değer temizleme
- Wikidata ID normalizasyonu
- Finansal veri parse etme
- Kategorik özellik oluşturma

### 2. Özellik Vektörü Oluşturma
- Genre mapping (60+ tür)
- Crew/cast ID işleme
- Mekan/kaynak özellik işleme
- Anahtar kelime çıkarma

### 3. Benzerlik Hesaplama
- TF-IDF vektörizasyonu
- Cosine similarity matrisi
- Ağırlıklı özellik kombinasyonu

### 4. Öneri Oluşturma
- En yüksek benzerlik skorları
- Benzerlik nedeni analizi
- Sonuç formatlaması

---

## 🐛 Sorun Giderme

### Yaygın Sorunlar

#### 1. "Film bulunamadı" Hatası
```python
# Çözüm: Film adını kontrol edin
similar_titles = recommender.df[
    recommender.df['title_en'].str.contains('partial_name', case=False)
]['title_en'].head(5)
print(similar_titles.tolist())
```

#### 2. Düşük Benzerlik Skorları
```python
# Çözüm: Özellik ağırlıklarını ayarlayın
recommender.feature_weights['genre'] = 0.35
recommender.calculate_similarity_matrix()
```

#### 3. Yavaş Performans
```python
# Çözüm: TF-IDF parametrelerini azaltın
max_features=3000  # 5000 yerine
```

### Debug Modu

```python
# Debug bilgileri için
print(f"Özellik vektörü: {recommender.df.iloc[0]['combined_features'][:200]}...")
print(f"Benzerlik matrisi boyutu: {recommender.similarity_matrix.shape}")
```

---

## 🤝 Katkıda Bulunma

### Özellik Eklemek İçin

1. **Yeni Property** ekleyin `enhanced_wikidata_scraper.py`'e
2. **Processing fonksiyonu** yazın `wikidata_movie_recommender.py`'de
3. **Feature weight** ekleyin `feature_weights` sözlüğüne
4. **Test** edin `test_features.py` ile

### Hata Raporları

- Detaylı hata açıklaması
- Kullanılan veri seti
- Python ve kütüphane sürümleri
- Hata reproduce etme adımları

---

## 📚 Referanslar

- **Wikidata:** https://www.wikidata.org/
- **Scikit-learn:** https://scikit-learn.org/
- **Pandas:** https://pandas.pydata.org/
- **TF-IDF:** https://en.wikipedia.org/wiki/Tf%E2%80%93idf

---

## 📄 Lisans

Bu proje açık kaynak olarak geliştirilmiştir. Kullanım için uygun lisans koşullarına uyunuz.

---

## 🎯 Gelecek Sürümler

### v0.5 Planları
- **Büyük veri seti** desteği (10,000+ film)
- **Hibrit sistem** (collaborative filtering)
- **API interface** 
- **Gelişmiş NLP** özellikleri

### v1.0 Hedefleri
- **Production-ready** sistem
- **Full documentation**
- **Performance optimization**
- **Multi-language** tam desteği

---

**🎬 Wikidata Film Öneri Sistemi v0.4 Beta ile gelişmiş film keşfi deneyimi yaşayın!**

---

## 📞 İletişim

Sorularınız ve önerileriniz için dokümantasyonu inceleyin veya test örneklerini kullanın.

**Happy Movie Watching! 🍿**
