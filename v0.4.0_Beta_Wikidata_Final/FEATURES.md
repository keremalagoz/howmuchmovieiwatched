# 🎯 Özellik Detayları - v0.4 Beta

## 📋 Genel Bakış

Wikidata Film Öneri Sistemi v0.4, **16 farklı özellik** kullanarak kapsamlı content-based film önerileri sunar. Bu dosyada her özelliğin detaylı açıklaması, kullanım şekli ve önemi açıklanmaktadır.

---

## 🏆 Özellik Ağırlık Sistemi

### Ağırlık Dağılımı Mantığı

```python
feature_weights = {
    # TEMEL ÖZELLİKLER (Toplam: 0.79)
    'genre': 0.25,              # En kritik - Film türü
    'director': 0.20,           # Çok önemli - Yönetmen tarzı
    'cast': 0.15,               # Önemli - Oyuncu tercihleri
    'year': 0.08,               # Orta - Dönem tercihi
    'country': 0.06,            # Orta - Kültürel tercih
    'language': 0.05,           # Düşük - Dil tercihi
    
    # TEKNİK EKİP (Toplam: 0.11)
    'composer': 0.04,           # Müzik tarzı
    'screenwriter': 0.04,       # Hikaye tarzı
    'production_company': 0.03, # Yapım kalitesi
    
    # FİNANSAL/TEKNİK (Toplam: 0.09)
    'budget_range': 0.03,       # Prodüksiyon seviyesi
    'box_office_range': 0.02,   # Popülerlik
    'imdb_rating_range': 0.02,  # Kalite göstergesi
    'duration_range': 0.02,     # İzleme süresi tercihi
    
    # İÇERİK (Toplam: 0.09)
    'award_received': 0.04,     # Kalite onayı
    'main_subject': 0.03,       # Tema tercihi
    'description_keywords': 0.02 # İçerik ipuçları
}
```

**Toplam:** 1.08 (normalização sırasında 1.0'a ayarlanır)

---

## 🎬 Temel Özellikler

### 1. **Genre (Tür) - 0.25**

**En önemli özellik.** Film türü kullanıcı tercihlerinin temel belirleyicisidir.

#### Desteklenen Türler:
- **Ana Türler:** drama, comedy, action, horror, scifi, romance, thriller
- **Alt Türler:** adventure, fantasy, crime, musical, documentary, mystery
- **Özel Türler:** biography, family, psychological, zombie, spy, historical
- **Teknük Türler:** animated, martialarts, superhero, spaceopera

#### Örnek İşleme:
```python
# Input: "Q130232|Q157443|Q188473"
# Output: "drama comedy action"
# TF-IDF'de: "drama drama drama comedy action"  # 3x ağırlık
```

#### Wikidata Mapping:
```python
genre_mapping = {
    'Q130232': 'drama',         # En yaygın
    'Q157443': 'comedy',        # Popüler
    'Q188473': 'action',        # Geniş çekici
    'Q200092': 'horror',        # Özel kitle
    'Q471839': 'scifi',         # Teknoloji meraklıları
    # ... 40+ tür daha
}
```

---

### 2. **Director (Yönetmen) - 0.20**

**Çok önemli.** Yönetmen tarzı film kalitesi ve tarzının güçlü göstergesidir.

#### İşleme Şekli:
```python
# Input: "Q42574|Q102124|Q56094"
# Output: "director_Q42574 director_Q102124 director_Q56094"
# Maksimum: 3 yönetmen
```

#### Benzerlik Mantığı:
- **Aynı yönetmen:** %100 benzerlik
- **Ortak yönetmen:** Çok yüksek benzerlik 
- **Farklı yönetmen:** Tarz analizi devreye girer

#### Örnekler:
- **James Cameron** → Avatar, Terminator, Titanic
- **Christopher Nolan** → Inception, Interstellar, Dark Knight
- **Quentin Tarantino** → Pulp Fiction, Kill Bill, Django

---

### 3. **Cast (Oyuncular) - 0.15**

**Önemli.** Oyuncu tercihleri ve chemistry faktörü.

#### İşleme Şekli:
```python
# Input: "Q82085|Q190162|Q312902|Q184219|Q371786"
# Output: "actor_Q82085 actor_Q190162 actor_Q312902 actor_Q184219 actor_Q371786"
# Maksimum: 5 oyuncu (en önemliler)
```

#### Benzerlik Faktörleri:
- **Ortak oyuncu sayısı**
- **Ana karakter vs yan karakter**
- **Oyuncu türü (aksiyon, komedi, dram)**

---

### 4. **Year (Yıl) - 0.08**

**Orta önemli.** Dönem tercihi ve teknolojik seviye.

#### İşleme Şekli:
```python
# Input: 2009
# Output: "decade_2000"
# Kategoriler: 1950, 1960, 1970, ..., 2020
```

#### Benzerlik Hesabı:
```python
if year_diff <= 5:
    reasons.append(f"Yakın yıl: {year_diff} yıl fark")
```

---

### 5. **Country (Ülke) - 0.06**

**Orta önemli.** Kültürel tercih ve prodüksiyon tarzı.

#### Ülke Mapping:
```python
country_mapping = {
    'Q30': 'usa',           # Hollywood
    'Q145': 'uk',           # British cinema
    'Q142': 'france',       # Auteur cinema
    'Q183': 'germany',      # Expressionist tradition
    'Q38': 'italy',         # Neorealism
    'Q17': 'japan',         # Anime & art films
    'Q884': 'southkorea',   # K-cinema boom
    # ... daha fazlası
}
```

---

### 6. **Language (Dil) - 0.05**

**Düşük önemli.** Dil tercihi ve kültürel bağlam.

#### Dil Mapping:
```python
language_mapping = {
    'Q1860': 'english',     # Global dominance
    'Q150': 'french',       # Art cinema
    'Q188': 'german',       # Philosophical cinema
    'Q1321': 'spanish',     # Growing market
    'Q9186': 'chinese',     # Massive market
    # ... daha fazlası
}
```

---

## 🎵 Teknik Ekip Özellikleri

### 7. **Composer (Müzik) - 0.04**

**Önemli.** Müzik tarzı ve atmosfer.

#### Örnekler:
- **Hans Zimmer:** Epic, orchestral (Inception, Interstellar)
- **John Williams:** Classic, heroic (Star Wars, Superman)
- **Trent Reznor:** Electronic, dark (Social Network, Gone Girl)

#### İşleme:
```python
# Input: "Q484726|Q106221"
# Output: "crew_Q484726 crew_Q106221"
# Maksimum: 3 besteci
```

---

### 8. **Screenwriter (Senarist) - 0.04**

**Önemli.** Hikaye tarzı ve karakter gelişimi.

#### Faktörler:
- **Dialogue style**
- **Narrative structure**
- **Character development**
- **Genre expertise**

---

### 9. **Production Company (Yapım Şirketi) - 0.03**

**Orta önemli.** Kalite standardı ve tarz.

#### Örnekler:
- **Marvel Studios:** Superhero universe
- **Pixar:** High-quality animation
- **A24:** Independent art films
- **Warner Bros:** Blockbuster tradition

---

## 💰 Finansal/Teknik Özellikler

### 10. **Budget Range (Bütçe Aralığı) - 0.03**

Prodüksiyon seviyesi göstergesi.

#### Kategoriler:
```python
def categorize_budget(budget):
    if budget < 1_000_000:
        return 'low_budget'      # Indie, experimental
    elif budget < 50_000_000:
        return 'medium_budget'   # Studio films
    else:
        return 'high_budget'     # Blockbusters
```

---

### 11. **Box Office Range (Hasılat Aralığı) - 0.02**

Popülerlik ve çekicilik göstergesi.

#### Kategoriler:
```python
def categorize_box_office(box_office):
    if box_office < 10_000_000:
        return 'low_box_office'     # Niche appeal
    elif box_office < 100_000_000:
        return 'medium_box_office'  # Moderate success
    else:
        return 'high_box_office'    # Blockbuster hit
```

---

### 12. **IMDB Rating Range (IMDB Puan Aralığı) - 0.02**

Kalite ve genel beğeni göstergesi.

#### Kategoriler:
```python
def categorize_imdb_rating(rating):
    if rating < 5.0:
        return 'low_rating'         # Poor quality
    elif rating < 7.0:
        return 'medium_rating'      # Average
    elif rating < 8.0:
        return 'high_rating'        # Good
    else:
        return 'excellent_rating'   # Masterpiece
```

---

### 13. **Duration Range (Süre Aralığı) - 0.02**

İzleme süresi tercihi.

#### Kategoriler:
```python
def categorize_duration(duration):
    if duration < 90:
        return 'short_film'    # Quick watch
    elif duration < 120:
        return 'medium_film'   # Standard length
    else:
        return 'long_film'     # Epic length
```

---

## 🏆 İçerik Özellikleri

### 14. **Award Received (Ödüller) - 0.04**

**Önemli.** Kalite onayı ve prestij göstergesi.

#### Önemli Ödüller:
- **Oscar (Academy Awards)**
- **Golden Globe**
- **BAFTA**
- **Cannes Film Festival**
- **Venice Film Festival**

#### İşleme:
```python
# Input: "Q131520|Q277751|Q1011509"
# Output: "award_Q131520 award_Q277751 award_Q1011509"
# Maksimum: 5 ödül
```

---

### 15. **Main Subject (Ana Konu) - 0.03**

**Orta önemli.** Tema ve içerik odağı.

#### Konu Kategorileri:
- **İnsan ilişkileri:** Aşk, aile, arkadaşlık
- **Sosyal konular:** Savaş, politik, adalet
- **Felsefik:** Ölüm, anlamlandırma, varoluş
- **Teknolojik:** AI, space exploration, future

#### İşleme:
```python
# Input: "Q544830|Q120877|Q7150"
# Output: "subject_Q544830 subject_Q120877 subject_Q7150"
# Maksimum: 3 konu
```

---

### 16. **Description Keywords (Açıklama Anahtar Kelimeleri) - 0.02**

**Düşük önemli.** İçerik ipuçları ve detaylar.

#### Anahtar Kelime Kategorileri:

**İngilizce:**
```python
common_keywords = [
    'war', 'love', 'family', 'death', 'crime', 
    'police', 'detective', 'murder', 'school', 
    'friendship', 'revenge', 'money', 'power'
]
```

**Türkçe:**
```python
tr_keywords = [
    'savaş', 'aşk', 'aile', 'ölüm', 'suç', 
    'polis', 'dedektif', 'cinayet', 'okul', 
    'arkadaşlık', 'intikam', 'para', 'güç'
]
```

---

## 📍 Ek Özellikler (Ağırlıksız)

Bu özellikler feature vektörüne dahil edilir ancak özel ağırlıkları yoktur:

### **Mekan Özellikleri:**
- **narrative_location:** Hikayenin geçtiği yer
- **filming_location:** Çekim yapılan yer

### **Kaynak Özellikleri:**
- **based_on:** Dayandığı eser
- **based_on_work:** Temel aldığı çalışma
- **part_of_series:** Serinin parçası

### **Prodüksiyon Özellikleri:**
- **distributor:** Dağıtımcı şirket
- **executive_producer:** Yürütücü yapımcı
- **original_network:** Orijinal yayın kanalı
- **original_broadcaster:** Orijinal yayıncı

---

## 🚫 Bilinçli Olarak Kullanılmayan Özellikler

### **Neden Hariç Tutuldular?**

#### 1. **Producer (Yapımcı)**
- **Sebep:** Content-based önerilerde çok etkili değil
- **Alternatif:** Production company daha değerli
- **Mantık:** Yapımcı kişisel tarz; şirket kurumsal tarz

#### 2. **Cinematographer (Görüntü Yönetmeni)**
- **Sebep:** Teknik detay, genel kullanıcı için az önemli
- **Alternatif:** Genre ve director daha kapsamlı
- **Mantık:** Görsel tarz çoğunlukla yönetmen tarzıyla örtüşür

#### 3. **Film Editor (Kurgucu)**
- **Sebep:** En teknik özellik, son kullanıcı fark etmez
- **Alternatif:** Director ve genre daha etkili
- **Mantık:** Kurgu tarzı genelde yönetmen vizyonuyla şekillenir

---

## 🔧 Özellik İşleme Algoritması

### 1. **Veri Temizleme**
```python
def clean_wikidata_ids(text):
    # Pipe ile ayrılmış değerleri işle
    # Maksimum ID sınırı uygula
    # Q-ID formatını kontrol et
    return cleaned_ids
```

### 2. **Feature Vector Oluşturma**
```python
def create_comprehensive_features():
    # Her özellik için processing fonksiyonu çağır
    # Ağırlıklı kombinasyon yap
    # TF-IDF için tek string oluştur
    return combined_features
```

### 3. **TF-IDF Vektörizasyonu**
```python
TfidfVectorizer(
    max_features=5000,      # Maksimum özellik
    stop_words='english',   # Stop word filtreleme
    ngram_range=(1, 2),     # Unigram + Bigram
    min_df=1,               # Minimum doküman frekansı
    max_df=0.8              # Maksimum doküman frekansı
)
```

---

## 📊 Özellik Performans Analizi

### **En Etkili Özellikler (Benzerlik İçin):**
1. **Genre** → %85 önerilerde ortak
2. **Director** → %60 önerilerde ortak
3. **Cast** → %40 önerilerde ortak
4. **Year** → %75 5 yıl içinde
5. **Country** → %55 önerilerde ortak

### **En Az Etkili Özellikler:**
1. **Description Keywords** → Çok genel
2. **Duration Range** → Tercih çeşitliliği yüksek
3. **Box Office Range** → Kalite ile ilişkisiz

### **Dengeleyici Özellikler:**
1. **Award Received** → Kalite filtresi
2. **Main Subject** → İçerik derinliği
3. **Production Company** → Tutarlılık

---

## 🎯 Özellik Optimizasyonu İpuçları

### **Ağırlık Ayarlama:**
```python
# Tür odaklı öneriler için
feature_weights['genre'] = 0.35
feature_weights['director'] = 0.15

# Yönetmen odaklı öneriler için  
feature_weights['director'] = 0.30
feature_weights['genre'] = 0.20

# Kalite odaklı öneriler için
feature_weights['award_received'] = 0.08
feature_weights['imdb_rating_range'] = 0.06
```

### **Yeni Özellik Ekleme:**
1. **Wikidata property** seç
2. **Processing fonksiyonu** yaz
3. **Feature weight** belirle
4. **Test et** ve optimize et

### **Özellik Kaldırma:**
```python
# Kullanmak istemediğiniz özelliği 0 yapın
feature_weights['duration_range'] = 0.0

# Veya wikidata_columns'dan çıkarın
wikidata_columns.remove('duration_range')
```

---

**🎬 Özellik sistemi sayesinde kişiselleştirilmiş ve açıklanabilir film önerileri alın!**
