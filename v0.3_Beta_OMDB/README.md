# Film Öneri Sistemi v0.3 Beta

Bu versiyon OMDB API entegrasyonu ile geliştirilmiş film öneri sistemidir.

## 🆕 Yeni Özellikler (v0.3)

### ✨ OMDB API Entegrasyonu
- **Gelişmiş Film Bilgileri**: IMDB puanları, yönetmen, oyuncular, türler
- **Zenginleştirilmiş Veriset**: 100+ popüler film ile önceden hazırlanmış veriset
- **Otomatik API Yönetimi**: API anahtarı yapılandırma ve test araçları

### 🛠️ Yeni Araçlar
- `omdb_test_demo.py` - OMDB API test ve demo uygulaması
- `interactive_movie_app_omdb.py` - OMDB destekli interaktif film uygulaması
- `offline_omdb_creator.py` - İnternet olmadan demo veriset oluşturucu
- `dns_fix.py` - DNS ve bağlantı sorunları için yardımcı araç

### 🎯 Gelişmiş Öneri Algoritması
- **Çoklu Özellik Analizi**: Tür, yönetmen, IMDB puanı bazlı öneriler
- **Akıllı Benzerlik Hesaplama**: TF-IDF ve cosine similarity
- **IMDB Puan Entegrasyonu**: Kaliteli film önerileri

## 📋 Gereksinimler

```bash
pip install -r requirements.txt
```

## 🚀 Kurulum

1. **OMDB API Anahtarı Alın**: https://www.omdbapi.com/apikey.aspx
2. **API Anahtarını Yapılandırın**:
   ```bash
   python omdb_test_demo.py
   # Seçenek 5: API Anahtarı Yapılandır
   ```

## 🎬 Kullanım

### 1. Hızlı Başlangıç
```bash
python omdb_test_demo.py
```
**Menü Seçenekleri:**
- `1` - OMDB API Test Et
- `2` - Örnek Zenginleştirilmiş Veriset Oluştur (100 film)
- `3` - Mevcut Verisetimi Zenginleştir
- `4` - Gelişmiş Öneri Sistemi Test Et

### 2. İnteraktif Film Uygulaması
```bash
python interactive_movie_app_omdb.py
```
- Otomatik veriset algılama
- IMDB puanları ile film önerileri
- Gelişmiş filtreleme seçenekleri

### 3. Offline Kullanım
İnternet bağlantısı yoksa:
```bash
python offline_omdb_creator.py
```
- 25-100 film arası demo veriset
- İnternet gerektirmez
- Anlık kullanıma hazır

## 🔧 Sorun Giderme

### DNS/Bağlantı Sorunları
```bash
python dns_fix.py
```
Bu araç:
- İnternet bağlantısını test eder
- DNS ayarlarını kontrol eder
- OMDB API erişimini doğrular
- Çözüm önerileri sunar

### API Sorunları
1. **API Anahtarı Kontrolü**: `python omdb_test_demo.py` → Seçenek 5
2. **Bağlantı Testi**: `python omdb_test_demo.py` → Seçenek 1
3. **Offline Alternatif**: `python offline_omdb_creator.py`

## 📁 Dosya Yapısı

```
v0.3_Beta/
├── omdb_data_enricher.py          # OMDB API ile veriset zenginleştirme
├── omdb_enhanced_recommender.py   # Gelişmiş öneri algoritması
├── omdb_config.py                 # API anahtarı yönetimi
├── omdb_test_demo.py              # Test ve demo uygulaması
├── interactive_movie_app_omdb.py  # İnteraktif film uygulaması
├── offline_omdb_creator.py        # Offline veriset oluşturucu
├── dns_fix.py                     # DNS sorun giderici
├── requirements.txt               # Python bağımlılıkları
├── omdb_enriched_sample_movies_offline.csv  # Hazır demo veriset
└── README.md                      # Bu dosya
```

## 🎯 Özellikler

### Veriset Özellikleri
- **100+ Popüler Film**: IMDB Top listeleri
- **Zengin Metadata**: 25+ film bilgisi sütunu
- **IMDB Entegrasyonu**: Puanlar, oylar, ödüller
- **Çoklu Dil Desteği**: Orijinal ve çevrilmiş başlıklar

### Öneri Sistemi
- **Akıllı Algoritma**: Tür, yönetmen, puan bazlı benzerlik
- **Özelleştirilebilir**: Film sayısı, filtreleme seçenekleri
- **Hızlı**: Optimize edilmiş vektör hesaplamaları
- **Doğru**: IMDB verisi ile desteklenmiş öneriler

### API Yönetimi
- **Güvenli**: .env dosyası ile API anahtarı saklama
- **Esnek**: Farklı endpoint'ler otomatik deneme
- **Hata Toleranslı**: DNS sorunları için çoklu çözüm
- **Test Edilebilir**: Otomatik API bağlantı kontrolü

## 🔄 Versiyon Geçmişi

- **v0.3 Beta**: OMDB API entegrasyonu, gelişmiş öneriler, DNS düzeltmeleri
- **v0.2**: Interaktif uygulama, gelişmiş filtreleme
- **v0.1**: Temel öneri sistemi, CSV destegi

## ⚡ Performans

- **Hızlı Başlangıç**: Hazır veriset ile anında kullanım
- **Ölçeklenebilir**: 1000+ film desteği
- **Düşük Bellek**: Optimize edilmiş DataFrame işlemleri
- **API Verimli**: Rate limiting ve cache desteği

## 📞 Destek

Sorun yaşarsanız:
1. `dns_fix.py` çalıştırın
2. `omdb_test_demo.py` ile sistem testi yapın
3. Offline modda `offline_omdb_creator.py` deneyin

---

**Not**: Bu beta versiyonudur. Önerilerinizi bekliyoruz! 🚀
