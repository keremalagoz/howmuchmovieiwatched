# Film Öneri Sistemi - Değişiklik Günlüğü

## v0.2 Beta (Büyük Veriset Güncellemesi)

### 🆕 Yeni Özellikler
- **Büyük Veriset Desteği**: 5000 film içeren TMDb veriseti entegrasyonu
- **Gelişmiş Interactive Apps**: İki yeni enhanced versiyon eklendi
- **TMDb Data Processor**: Veriset işleme ve optimizasyon araçları
- **Advanced Filtering**: Yıl, tür, puan bazlı gelişmiş filtreleme
- **Rich Metadata**: Yönetmen, oyuncular, bütçe, hasılat bilgileri

### 🛠️ Yeni Modüller
- `interactive_movie_app_enhanced.py` - Gelişmiş kullanıcı arayüzü
- `interactive_movie_app_enhanced_v2.py` - En gelişmiş versiyon
- `tmdb_data_processor.py` - TMDb veriset işleyici

### 📊 Veriset Geliştirmeleri
- **tmdb_5000_movies.csv**: Orijinal TMDb veriseti (5000 film)
- **processed_tmdb_movies.csv**: İşlenmiş ve optimize edilmiş veriset
- **Zengin Metadata**: 
  - Film başlığı, tür, yıl, açıklama
  - Yönetmen ve ana oyuncular
  - Bütçe ve hasılat bilgileri
  - IMDB puanı ve oy sayısı
  - Çalışma süresi
- **movies.csv**: Orijinal küçük veriset (geriye uyumluluk)

### 🎯 Algoritma Geliştirmeleri
- **Improved TF-IDF**: Büyük veriset için optimize edilmiş
- **Multi-Feature Analysis**: Tür, açıklama, oyuncu analizi
- **Better Similarity Calculation**: Daha hassas benzerlik hesaplama
- **Performance Optimization**: 5000 film için hızlı işlem

### 🚀 Kullanıcı Deneyimi
- **Enhanced CLI Interface**: Daha kullanıcı dostu menüler
- **Smart Filtering**: Akıllı film filtreleme seçenekleri
- **Better Recommendations**: Daha kaliteli öneri sonuçları
- **Input Validation**: Gelişmiş kullanıcı girdisi kontrolü

### 🔧 Teknik İyileştirmeler
- **Data Processing Pipeline**: Veriset işleme hattı
- **Memory Optimization**: Büyük veriset için bellek optimizasyonu
- **Error Handling**: Gelişmiş hata yönetimi
- **Code Structure**: Daha modüler kod yapısı

### 📦 Sistem Gereksinimleri
- **Python 3.7+**
- **pandas >= 1.3.0**
- **scikit-learn >= 1.0.0**
- **numpy >= 1.21.0**
- **matplotlib >= 3.4.0** (yeni eklenen)

### 🔄 Geriye Uyumluluk
- Eski v0.1 dosyaları korundu
- `movies.csv` orijinal küçük veriset hala mevcut
- Temel `interactive_movie_app.py` değişmedi
- Ana API ve işlevler korundu

### 📈 Performans İyileştirmeleri
- **5000x Veriset**: 25 filmden 5000 filme çıkış
- **Faster Processing**: Optimize edilmiş işlem hızı
- **Better Memory Usage**: Daha verimli bellek kullanımı
- **Scalable Architecture**: Büyük verisetler için hazır altyapı

### 🐛 Düzeltilen Hatalar
- Büyük veriset yükleme sorunları
- Unicode karakter işleme
- Memory overflow koruması
- Input sanitization

### 🎬 Yeni Film Veriseti Özellikleri
- **Popular Movies**: TMDb'nin en popüler 5000 filmi
- **Diverse Genres**: Geniş tür yelpazesi
- **Recent & Classic**: Klasik ve modern filmler
- **Rich Information**: Detaylı film bilgileri

### 📚 Dokümantasyon
- README güncellemeleri
- Kullanım kılavuzu genişletildi
- Kod örnekleri eklendi
- API dokümantasyonu

---

## v0.1 Beta (İlk Sürüm)

### 🆕 İlk Özellikler
- **Content-Based Recommendation System**: İçerik bazlı film önerme sistemi
- **TF-IDF Vectorization**: Metin madenciliği ile özellik çıkarma
- **Cosine Similarity**: Matematiksel benzerlik hesaplama
- **Interactive CLI App**: Komut satırı arayüzü

### 🛠️ Ana Modüller
- `main.py` - Ana program giriş noktası
- `content_based_recommender.py` - Temel öneri algoritması
- `interactive_movie_app.py` - Kullanıcı etkileşim arayüzü
- `demo_app.py` - Demo ve örnek kullanım
- `test_recommender.py` - Sistem test araçları

### 📊 İlk Veriset
- **movies.csv**: 25 popüler film
- **Manuel Seçim**: El ile seçilmiş kaliteli filmler
- **Temel Metadata**: ID, başlık, tür, yıl, açıklama
