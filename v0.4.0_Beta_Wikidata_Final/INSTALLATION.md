# 🛠️ Kurulum Kılavuzu - v0.4 Beta

## 📋 Sistem Gereksinimleri

### Minimum Gereksinimler
- **Python:** 3.8 veya üzeri
- **RAM:** 512 MB
- **Disk Alanı:** 100 MB
- **İnternet:** Yeni veri çekmek için (opsiyonel)

### Önerilen Gereksinimler
- **Python:** 3.10+
- **RAM:** 2 GB
- **Disk Alanı:** 1 GB
- **CPU:** Modern çok çekirdekli işlemci

---

## 🚀 Hızlı Kurulum

### 1. Python Kontrolü

```bash
python --version
# veya
python3 --version
```

**Çıktı:** `Python 3.8.x` veya üzeri olmalı

### 2. Dosyaları İndirin

```bash
# v0.4 Beta klasörünü bilgisayarınıza kopyalayın
# Tüm dosyalar bu kılavuzla birlikte gelir
```

### 3. Gerekli Kütüphaneleri Yükleyin

```bash
cd "v0.4 - Beta"
pip install -r requirements.txt
```

### 4. Test Edin

```bash
python test_features.py
```

**Beklenen Çıktı:** ✅ TEST TAMAMLANDI!

---

## 📦 Detaylı Kurulum

### Adım 1: Python Kurulumu

#### Windows:
1. https://python.org/downloads adresinden Python 3.10+ indirin
2. Kurulum sırasında "Add Python to PATH" seçeneğini işaretleyin
3. Kurulumu tamamlayın

#### macOS:
```bash
# Homebrew ile
brew install python3

# Veya resmi installer kullanın
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install python3 python3-pip
```

### Adım 2: Pip Güncellemesi

```bash
python -m pip install --upgrade pip
```

### Adım 3: Sanal Ortam (Önerilen)

```bash
# Sanal ortam oluştur
python -m venv wikidata_recommender_env

# Sanal ortamı aktifleştir
# Windows:
wikidata_recommender_env\Scripts\activate

# macOS/Linux:
source wikidata_recommender_env/bin/activate
```

### Adım 4: Gereksinimler

#### requirements.txt içeriği:
```
pandas>=1.3.0
numpy>=1.21.0
scikit-learn>=1.0.0
SPARQLWrapper>=2.0.0
requests>=2.25.0
tqdm>=4.60.0
```

#### Kurulum:
```bash
pip install -r requirements.txt
```

#### Manuel kurulum:
```bash
pip install pandas numpy scikit-learn SPARQLWrapper requests tqdm
```

---

## 🔧 Doğrulama Testleri

### Test 1: Python Modülleri

```python
# test_imports.py
try:
    import pandas as pd
    import numpy as np
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    from SPARQLWrapper import SPARQLWrapper
    import requests
    from tqdm import tqdm
    print("✅ Tüm modüller başarıyla yüklendi!")
except ImportError as e:
    print(f"❌ Modül hatası: {e}")
```

### Test 2: Ana Sistem

```bash
python test_features.py
```

**Beklenen Çıktı:**
```
🧪 TÜM ÖZELLİKLER TESTİ
==================================================
✅ Toplam film: 50
✅ Kullanılan özellik sayısı: 16
...
✅ TEST TAMAMLANDI!
```

### Test 3: Interaktif Mod

```bash
python wikidata_movie_recommender.py
```

**Beklenen Çıktı:**
```
🎬 WIKIDATA MATEMATİKSEL FİLM ÖNERİ SİSTEMİ
============================================================
✅ Veri seti yüklendi: 50 film
🧹 Veri temizleniyor...
🔧 TÜM özellik vektörleri hazırlanıyor...
...
🔍 Film adı girin (çıkmak için 'q'):
```

---

## 🚨 Sorun Giderme

### Yaygın Kurulum Sorunları

#### 1. Python Bulunamadı
```bash
# Çözüm: PATH kontrolü
echo $PATH  # macOS/Linux
echo %PATH%  # Windows

# Python yolu ekleme
export PATH="/usr/local/bin/python3:$PATH"  # macOS/Linux
```

#### 2. Pip Hatası
```bash
# Çözüm: Pip güncelleme
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

#### 3. Permission Denied (Linux/macOS)
```bash
# Çözüm: Kullanıcı kurulumu
pip install --user -r requirements.txt
```

#### 4. SSL Certificate Hatası
```bash
# Çözüm: Trust store güncelleme
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt
```

#### 5. Memory Error
```bash
# Çözüm: Swap artırma veya küçük veri seti kullanma
# Test veri seti zaten küçük (50 film)
```

### Windows Özel Sorunları

#### 1. Visual C++ 14.0 Hatası
```bash
# Çözüm: Visual Studio Build Tools indir
# https://visualstudio.microsoft.com/visual-cpp-build-tools/
```

#### 2. Long Path Hatası
```bash
# Çözüm: Long path desteğini aktifleştir
# Windows Registry: HKLM\SYSTEM\CurrentControlSet\Control\FileSystem
# LongPathsEnabled = 1
```

### macOS Özel Sorunları

#### 1. Command Line Tools
```bash
xcode-select --install
```

#### 2. Homebrew Sorunları
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

---

## 📁 Veri Seti Kurulumu

### Mevcut Test Veri Seti (Dahil)

- **Dosya:** `test_wikidata_films.csv`
- **Film Sayısı:** 50
- **Boyut:** ~27 KB
- **Hazır kullanım:** ✅

### Yeni Veri Seti Oluşturma

```bash
# Enhanced Wikidata Scraper ile
python enhanced_wikidata_scraper.py

# Seçenekler:
# 1. Hızlı test (50 film)      - 2-3 dakika
# 2. Orta ölçek (1000 film)    - 15-20 dakika  
# 3. Büyük ölçek (10000 film)  - 2-3 saat
```

### Özel Veri Seti

```python
# Kendi CSV dosyanızı kullanın
recommender = WikidataMovieRecommender("my_custom_dataset.csv")

# Gerekli sütunlar:
# - qid, title_en, genre, director, cast_member, year, ...
```

---

## 🔧 Gelişmiş Konfigürasyon

### IDE Kurulumu (Opsiyonel)

#### Visual Studio Code:
```bash
# Python extension yükle
code --install-extension ms-python.python
```

#### PyCharm:
- Python interpreter olarak sanal ortamı seçin

#### Jupyter Notebook:
```bash
pip install jupyter
jupyter notebook
```

### Git Kurulumu (Opsiyonel)

```bash
# Proje versiyonlama için
git init
git add .
git commit -m "v0.4 Beta kurulumu"
```

---

## 🧪 Test Senaryoları

### Tam Test Paketi

```bash
# 1. Modül testleri
python -c "import wikidata_movie_recommender; print('✅ Ana modül OK')"

# 2. Özellik testleri  
python test_features.py

# 3. Öneri testleri
python -c "
from wikidata_movie_recommender import WikidataMovieRecommender
r = WikidataMovieRecommender()
recs = r.get_movie_recommendations('Avatar', 3)
print(f'✅ {len(recs)} öneri alındı')
"

# 4. Scraper testi (opsiyonel - internet gerekli)
python enhanced_wikidata_scraper.py  # Seçenek 1 - Hızlı test
```

### Performans Testi

```python
# performance_test.py
import time
from wikidata_movie_recommender import WikidataMovieRecommender

start_time = time.time()
recommender = WikidataMovieRecommender()
load_time = time.time() - start_time

start_time = time.time()
recs = recommender.get_movie_recommendations("Avatar", 5)
recommend_time = time.time() - start_time

print(f"Yükleme süresi: {load_time:.2f} saniye")
print(f"Öneri süresi: {recommend_time:.2f} saniye")
print(f"Toplam: {load_time + recommend_time:.2f} saniye")
```

---

## 📱 Platform Özel Notlar

### Windows
- **PowerShell** önerilen terminal
- **Antivirus** yazılımı Python dosyalarını tarayabilir
- **Windows Defender** bazen yavaşlatabilir

### macOS
- **Terminal.app** veya **iTerm2** kullanın
- **Gatekeeper** uyarıları normal
- **Homebrew** package manager önerilen

### Linux
- **bash** veya **zsh** shell kullanın
- **Package manager** (apt, yum, dnf) kullanın
- **Python3-dev** paketi gerekebilir

---

## 🎯 Kurulum Doğrulama Checklist

- [ ] **Python 3.8+** kurulu
- [ ] **pip** çalışıyor
- [ ] **Sanal ortam** aktif (önerilen)
- [ ] **requirements.txt** yüklendi
- [ ] **test_features.py** başarılı
- [ ] **wikidata_movie_recommender.py** çalışıyor
- [ ] **test_wikidata_films.csv** okunuyor
- [ ] **Öneri sistemi** çalışıyor
- [ ] **Interaktif mod** çalışıyor

---

## 🔄 Güncelleme

### Minor Update (v0.4.1, v0.4.2, ...)

```bash
# Yeni dosyaları kopyalayın
# pip gereksinimlerini güncelleyin
pip install -r requirements.txt --upgrade
```

### Major Update (v0.5, v1.0, ...)

```bash
# Tam yeni kurulum önerilen
# Eski veri setlerini yedekleyin
# Yeni sürümü kurun
```

---

## 📞 Destek

### Kurulum başarısız olursa:

1. **Python sürümünü** kontrol edin
2. **requirements.txt** tam yüklenmiş mi kontrol edin  
3. **test_features.py** çıktısını inceleyin
4. **Hata mesajlarını** kaydedin
5. **Sistem bilgilerini** (OS, Python version) not alın

### Başarılı kurulum çıktısı:

```
✅ Veri seti yüklendi: 50 film
🧹 Veri temizleniyor...
   Temizlenen veri: 50 film
🔧 TÜM özellik vektörleri hazırlanıyor...
   TÜM özellik vektörleri hazırlandı
🔢 Benzerlik matrisi hesaplanıyor...
   Benzerlik matrisi: (50, 50)
📊 Veri Seti İstatistikleri:
   Toplam film: 50
   ...
✅ Sistem hazır!
```

---

**🎬 Kurulum tamamlandı! Film önerileriniz hazır!**
