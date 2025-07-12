# 🎬 Wikidata Movie Recommender v0.4 Beta - Sürüm Notları

## 📋 Genel Bilgiler
- **Sürüm**: v0.4 Beta
- **Tarih**: 8 Temmuz 2025
- **Dil**: Python 3.7+
- **Lisans**: MIT
- **Geliştirici**: Film İzleme Sayacı Projesi

## 🎯 Bu Sürümde Neler Var?

### 🔥 Ana Özellikler
- **16 Farklı Özellik** ile kapsamlı film analizi
- **TF-IDF + Cosine Similarity** ile matematiksel doğruluk
- **Açıklanabilir AI** - her önerinin nedeni açık
- **Wikidata entegrasyonu** - zengin meta veri
- **Çok dilli destek** - Türkçe/İngilizce
- **Ölçeklenebilir** - binlerce film destekler

### 📊 Kullanılan Özellikler (16 Adet)
1. **Tür** (Genre) - %25 ağırlık
2. **Yönetmen** (Director) - %20 ağırlık
3. **Oyuncular** (Cast) - %15 ağırlık
4. **Yıl** (Year) - %8 ağırlık
5. **Ülke** (Country) - %6 ağırlık
6. **Dil** (Language) - %5 ağırlık
7. **Müzik** (Composer) - %4 ağırlık
8. **Senarist** (Screenwriter) - %4 ağırlık
9. **Yapım Şirketi** (Production Company) - %3 ağırlık
10. **Bütçe Kategorisi** (Budget Range) - %3 ağırlık
11. **Hasılat Kategorisi** (Box Office Range) - %2 ağırlık
12. **IMDB Puan Kategorisi** (IMDB Rating Range) - %2 ağırlık
13. **Süre Kategorisi** (Duration Range) - %2 ağırlık
14. **Ödüller** (Awards) - %4 ağırlık
15. **Ana Tema** (Main Subject) - %3 ağırlık
16. **Açıklama Anahtar Kelimeleri** (Keywords) - %2 ağırlık

### 🚀 Dahil Edilen Dosyalar
```
v0.4 - Beta/
├── wikidata_movie_recommender.py    # Ana öneri sistemi
├── enhanced_wikidata_scraper.py     # Veri çekme aracı
├── test_features.py                 # Özellik testleri
├── system_test.py                   # Sistem testleri
├── test_wikidata_films.csv          # Test veri seti
├── requirements.txt                 # Python bağımlılıkları
├── README.md                        # Genel dokümantasyon
├── QUICKSTART.md                    # Hızlı başlangıç rehberi
├── INSTALLATION.md                  # Kurulum rehberi
├── FEATURES.md                      # Özellik açıklamaları
├── EXAMPLES.md                      # Kullanım örnekleri
├── CHANGELOG.md                     # Bu dosya
└── VERSION_NOTES.md                 # Sürüm notları
```

## 🛠️ Teknik Detaylar

### Algoritma
- **TF-IDF (Term Frequency-Inverse Document Frequency)**: Özellik vektörlerini oluşturur
- **Cosine Similarity**: Filmler arası benzerlik hesaplar
- **Ağırlıklı Özellik Birleştirme**: Her özelliğin önemi farklıdır
- **Normalizasyon**: Farklı veri tiplerini standartlaştırır

### Veri Kaynağı
- **Wikidata**: Açık kaynak yapılandırılmış veri
- **SPARQL Sorguları**: Otomatik veri çekme
- **CSV Format**: Yerel işleme ve hız
- **Çok Dilli**: İngilizce/Türkçe başlıklar

### Performans
- **Bellek**: ~2GB RAM önerilir
- **Hesaplama**: ~10-30 saniye başlangıç (veri setine bağlı)
- **Öneri Hızı**: ~1-2 saniye per film
- **Ölçeklenebilirlik**: 10,000+ film destekler

## 🔧 Kurulum

### Gereksinimler
```bash
pip install -r requirements.txt
```

### Temel Kullanım
```python
from wikidata_movie_recommender import WikidataMovieRecommender

# Sistem başlatma
recommender = WikidataMovieRecommender()

# Film önerisi alma
recommendations = recommender.get_movie_recommendations("Avatar", n_recommendations=5)

# Sonuçları yazdırma
recommender.print_recommendations(recommendations, "Avatar")
```

## 📈 Önceki Sürümlerden Farklar

### v0.3'ten v0.4'e Geçiş
- ✅ **5 özellik** → **16 özellik** (3x artış)
- ✅ **Basit benzerlik** → **Matematiksel analiz**
- ✅ **Açıklanamayan** → **Açıklanabilir AI**
- ✅ **Sınırlı veri** → **Wikidata entegrasyonu**
- ✅ **Tek dil** → **Çok dilli destek**

### Yeni Özellikler
- 🆕 **Müzik Benzerliği**: Aynı besteci filmleri
- 🆕 **Coğrafi Benzerlik**: Ülke/dil bazlı
- 🆕 **Finansal Kategori**: Bütçe/hasılat seviyeleri
- 🆕 **Kalite Kategori**: IMDB/süre seviyeleri
- 🆕 **Tema Analizi**: Ana konu benzerliği
- 🆕 **Anahtar Kelime**: Açıklama analizi

## 🎯 Kullanım Senaryoları

### 1. Film Keşfi
"Bu filmi sevdim, benzer ne var?" sorusuna matematiksel cevap.

### 2. Tür Analizi
Belirli türlerin derinlemesine analizi.

### 3. Yönetmen/Oyuncu Takibi
Sevdiğiniz artistlerin diğer işlerini keşfetme.

### 4. Kalite Kontrolü
Yüksek puanlı filmleri filtreleme.

### 5. Coğrafi Keşif
Belirli ülkelerin sinemasını keşfetme.

## 🔍 Test Sonuçları

### Sistem Testleri
```bash
python system_test.py
```

### Özellik Testleri
```bash
python test_features.py
```

### Performans
- ✅ **1000+ film** başarıyla işlendi
- ✅ **16 özellik** aktif ve test edildi
- ✅ **10+ test senaryosu** başarıyla geçti
- ✅ **Benzerlik nedenleri** doğrulandı

## 🐛 Bilinen Sorunlar

### Sınırlamalar
- 🔸 **Büyük veri setleri**: 10,000+ film için yavaşlama
- 🔸 **Bellek kullanımı**: Çok fazla özellik RAM kullanır
- 🔸 **Wikidata bağımlılığı**: İnternet bağlantısı gerekli (scraping için)
- 🔸 **Dil desteği**: Sadece İngilizce/Türkçe optimize

### Çözümler
- 💡 **Performans**: Özellik sayısını azaltın
- 💡 **Bellek**: Daha küçük veri seti kullanın
- 💡 **Bağlantı**: Mevcut CSV dosyasını kullanın
- 💡 **Dil**: Ek dil desteği için katkıda bulunun

## 🔮 Gelecek Planlar

### v0.5 Hedefleri
- 🎯 **Daha fazla özellik**: 20+ özellik
- 🎯 **Makine öğrenmesi**: Neural networks
- 🎯 **Web arayüzü**: Flask/Django
- 🎯 **API desteği**: RESTful API
- 🎯 **Veritabanı**: PostgreSQL/MongoDB

### v1.0 Hedefleri
- 🎯 **Üretim hazır**: Production-ready
- 🎯 **Çok dilli**: 10+ dil desteği
- 🎯 **Bulut desteği**: AWS/GCP deployment
- 🎯 **Mobil uygulama**: React Native/Flutter
- 🎯 **Sosyal özellikler**: Kullanıcı profilleri

## 🤝 Katkıda Bulunma

### Geliştirici Rehberi
1. Repository fork edin
2. Yeni özellik dalı oluşturun
3. Testlerinizi yazın
4. Pull request gönderin

### Hangi Alanlarda Yardım?
- 🔹 **Yeni özellikler**: Daha fazla film verisi
- 🔹 **Performans**: Optimizasyon
- 🔹 **Dil desteği**: Çeviri
- 🔹 **Dokümantasyon**: Rehberler
- 🔹 **Test**: Daha fazla test senaryosu

## 📞 Destek

### Dokümantasyon
- 📖 **README.md**: Genel bilgiler
- 📖 **QUICKSTART.md**: Hızlı başlangıç
- 📖 **INSTALLATION.md**: Kurulum rehberi
- 📖 **FEATURES.md**: Özellik açıklamaları
- 📖 **EXAMPLES.md**: Kullanım örnekleri

### İletişim
- 💬 **Issues**: GitHub issues
- 💬 **Discussions**: GitHub discussions
- 💬 **Email**: Proje e-postası

## 🎉 Teşekkürler

Bu sürüm, film önerme sistemlerinin yeni bir seviyesini temsil ediyor. Wikidata'nın zengin veri kaynağı ve 16 farklı özelliğin matematik analizi sayesinde, sadece "benzer" değil, **neden benzer** olduğunu da söylüyoruz.

**Keyifli filmler! 🍿**
