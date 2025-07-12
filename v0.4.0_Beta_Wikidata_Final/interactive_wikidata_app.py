#!/usr/bin/env python3
"""
Film İzleme Sayacı - Wikidata Destekli İnteraktif Film Önerme Uygulaması v0.4 Beta

Bu uygulama kullanıcıdan film seçimlerini alır ve Wikidata'dan zenginleştirilmiş
veriler kullanarak gelişmiş öneriler sunar.
"""

import os
import pandas as pd
from typing import List, Dict, Optional
from wikidata_movie_recommender import WikidataMovieRecommender


class InteractiveWikidataMovieApp:
    """Wikidata destekli interaktif film önerme uygulaması"""
    
    def __init__(self, dataset_path: str = "test_wikidata_films.csv"):
        """Uygulamayı başlat"""
        self.dataset_path = dataset_path
        self.user_movies = []  # Kullanıcının seçtiği film ID'leri
        self.user_movie_details = []  # Kullanıcının seçtiği film detayları
        self.round_number = 0
        self.shown_recommendations = set()  # Gösterilen önerileri takip et
        
        # Wikidata öneri sistemini başlat
        self._initialize_recommender()
        
    def _initialize_recommender(self):
        """Wikidata öneri sistemini başlat"""
        try:
            self.recommender = WikidataMovieRecommender(self.dataset_path)
            print("✅ Wikidata öneri sistemi başarıyla yüklendi!")
            
            # Veri seti istatistikleri
            stats = self.recommender.get_dataset_statistics()
            print(f"📊 {stats['total_movies']} film yüklendi")
            print(f"📅 Yıl aralığı: {stats['years_range']}")
            
        except Exception as e:
            raise Exception(f"Wikidata öneri sistemi başlatılamadı: {str(e)}")
        
    def clear_screen(self):
        """Ekranı temizle"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def display_header(self):
        """Başlık göster"""
        print("🎬" + "=" * 65 + "🎬")
        print("     Film İzleme Sayacı - Wikidata AI Önerme Sistemi v0.4 Beta")
        print("🎬" + "=" * 65 + "🎬")
        
    def display_user_profile(self):
        """Kullanıcı profilini göster"""
        if not self.user_movie_details:
            print("👤 Henüz film seçilmedi")
            return
            
        print(f"👤 Profiliniz ({len(self.user_movie_details)} film):")
        print("─" * 50)
        
        for i, movie in enumerate(self.user_movie_details, 1):
            print(f"   {i}. 🎬 {movie['title_en']}")
            if movie.get('genre'):
                print(f"      📁 Tür: {movie['genre']}")
            if movie.get('director'):
                print(f"      🎭 Yönetmen: {movie['director']}")
            if movie.get('publication_date'):
                print(f"      📅 Yıl: {movie['publication_date']}")
            if movie.get('imdb_rating'):
                print(f"      ⭐ IMDB: {movie['imdb_rating']}")
            print()
        
    def run_initial_setup(self):
        """İlk kurulum: Kullanıcıdan 3-5 film seçmesini iste"""
        self.clear_screen()
        self.display_header()
        
        print("🚀 BAŞLANGIÇ KURULUMU")
        print("=" * 30)
        print("Sizin için daha iyi öneriler sunabilmek için")
        print("lütfen beğendiğiniz 3-5 film seçin.\n")
        
        target_movies = 3
        selected_count = 0
        
        while selected_count < target_movies:
            remaining = target_movies - selected_count
            print(f"📍 {remaining} film daha seçmeniz gerekiyor...")
            
            # Film ara ve seç
            movie_id = self.search_and_select_movie()
            if movie_id:
                # Film detaylarını al
                movie_details = self.get_movie_details(movie_id)
                if movie_details:
                    self.user_movies.append(movie_id)
                    self.user_movie_details.append(movie_details)
                    selected_count += 1
                    print(f"✅ '{movie_details['title_en']}' profilinize eklendi!")
                    
                    # Profili göster
                    self.clear_screen()
                    self.display_header()
                    self.display_user_profile()
                    
                    # Devam seçeneği sun
                    if selected_count >= target_movies:
                        if selected_count < 5:
                            continue_choice = input(f"\n🎯 İsteğe bağlı: Daha fazla film eklemek ister misiniz? (y/n): ").strip().lower()
                            if continue_choice == 'y':
                                target_movies = min(target_movies + 1, 5)
                                continue
                        break
                    else:
                        input(f"\n⏳ Devam etmek için Enter'a basın...")
                        
    def search_and_select_movie(self) -> Optional[str]:
        """Film arama ve seçim"""
        while True:
            print(f"\n🔍 Film Arama")
            print("─" * 20)
            
            search_query = input("Film adını girin (Türkçe veya İngilizce): ").strip()
            
            if not search_query:
                continue
                
            # Arama yap
            search_results = self.search_movies(search_query)
            
            if not search_results:
                print("❌ Film bulunamadı! Başka bir isim deneyin.")
                continue
                
            # Sonuçları göster
            print(f"\n📋 Bulunan filmler ({len(search_results)} sonuç):")
            print("─" * 40)
            
            for i, movie in enumerate(search_results, 1):
                print(f"   {i}. 🎬 {movie['title_en']}")
                if movie.get('genre'):
                    print(f"      📁 {movie['genre']}")
                if movie.get('director'):
                    print(f"      🎭 {movie['director']}")
                if movie.get('publication_date'):
                    print(f"      📅 {movie['publication_date']}")
                if movie.get('imdb_rating'):
                    print(f"      ⭐ {movie['imdb_rating']}")
                print()
                
            # Seçim yap
            try:
                choice = input(f"\n✅ Hangi filmi seçiyorsunuz? (1-{len(search_results)}) veya 'tekrar' yazın: ").strip()
                
                if choice.lower() == 'tekrar':
                    continue
                    
                choice_num = int(choice)
                if 1 <= choice_num <= len(search_results):
                    selected_movie = search_results[choice_num - 1]
                    
                    # Daha önce seçilmiş mi kontrol et
                    if selected_movie['wikidata_id'] in self.user_movies:
                        print("⚠️  Bu filmi zaten seçmişsiniz! Başka bir film seçin.")
                        continue
                        
                    return selected_movie['wikidata_id']
                else:
                    print("❌ Geçersiz seçim! Lütfen listeden bir numara seçin.")
                    
            except ValueError:
                print("❌ Lütfen geçerli bir numara girin!")
                
    def search_movies(self, query: str) -> List[Dict]:
        """Film arama"""
        # Hem İngilizce hem de Türkçe başlıklarda ara
        df = self.recommender.df
        
        # Arama sonuçları
        results = []
        
        # İngilizce başlıkta ara
        en_matches = df[df['title_en'].str.contains(query, case=False, na=False)]
        
        # Türkçe başlıkta ara (varsa)
        if 'title_tr' in df.columns:
            tr_matches = df[df['title_tr'].str.contains(query, case=False, na=False)]
            matches = pd.concat([en_matches, tr_matches]).drop_duplicates()
        else:
            matches = en_matches
            
        # İlk 10 sonucu al
        for _, row in matches.head(10).iterrows():
            results.append({
                'wikidata_id': row['qid'],  # 'qid' sütununu kullan
                'title_en': row['title_en'],
                'title_tr': row.get('title_tr', ''),
                'genre': row.get('genre', ''),
                'director': row.get('director', ''),
                'publication_date': row.get('publication_date', ''),
                'imdb_rating': row.get('imdb_rating', ''),
                'country': row.get('country', ''),
                'language': row.get('language', '')
            })
            
        return results
    
    def get_movie_details(self, wikidata_id: str) -> Optional[Dict]:
        """Film detaylarını al"""
        df = self.recommender.df
        movie_row = df[df['qid'] == wikidata_id]  # 'qid' sütununu kullan
        
        if movie_row.empty:
            return None
            
        row = movie_row.iloc[0]
        return {
            'wikidata_id': row['qid'],  # 'qid' sütununu kullan
            'title_en': row['title_en'],
            'title_tr': row.get('title_tr', ''),
            'genre': row.get('genre', ''),
            'director': row.get('director', ''),
            'cast': row.get('cast_member', ''),  # 'cast_member' sütununu kullan
            'publication_date': row.get('publication_date', ''),
            'imdb_rating': row.get('imdb_rating', ''),
            'country': row.get('country', ''),
            'language': row.get('language', ''),
            'composer': row.get('composer', ''),
            'screenwriter': row.get('screenwriter', ''),
            'production_company': row.get('production_company', ''),
            'award_received': row.get('award_received', ''),
            'main_subject': row.get('main_subject', ''),
            'description': row.get('description_en', ''),
            'imdb_id': row.get('imdb_id', ''),
            'duration': row.get('duration', ''),
            'budget': row.get('budget', ''),
            'box_office': row.get('box_office', '')
        }
    
    def run_recommendation_round(self) -> bool:
        """Öneri turu çalıştır"""
        self.round_number += 1
        
        print(f"\n🎯 {self.round_number}. ÖNERİ TURU")
        print("=" * 30)
        
        # Önerileri al
        recommendations = self.get_recommendations()
        
        if not recommendations:
            print("❌ Öneri oluşturulamadı. Lütfen daha sonra tekrar deneyin.")
            return False
            
        # Önerileri göster
        self.display_recommendations(recommendations)
        
        # Kullanıcıdan seçim al
        selected_movie = self.select_from_recommendations(recommendations)
        
        if selected_movie:
            # Seçilen filmi profile ekle
            movie_details = self.get_movie_details(selected_movie)
            if movie_details:
                self.user_movies.append(selected_movie)
                self.user_movie_details.append(movie_details)
                print(f"✅ '{movie_details['title_en']}' profilinize eklendi!")
                
                # Profili güncelle
                input("⏳ Devam etmek için Enter'a basın...")
                
        return True
    
    def get_recommendations(self) -> List[Dict]:
        """Kullanıcı profiline göre öneriler al"""
        if not self.user_movies:
            return []
            
        # Wikidata öneri sisteminden öneriler al
        # Sistem get_recommendations_by_ids metodunu kullanacak
        try:
            recommendations = self.recommender.get_recommendations_by_ids(
                movie_ids=self.user_movies,
                n_recommendations=6
            )
            
            # Daha önce gösterilen önerileri filtrele
            filtered_recommendations = []
            for rec in recommendations:
                if rec['wikidata_id'] not in self.shown_recommendations:
                    filtered_recommendations.append(rec)
                    
            return filtered_recommendations[:4]  # İlk 4 tanesini al
            
        except Exception as e:
            print(f"⚠️ Öneri sistemi hatası: {str(e)}")
            return []
    
    def display_recommendations(self, recommendations: List[Dict]):
        """Önerileri göster"""
        print(f"\n🎬 Size Özel Önerilerimiz:")
        print("─" * 50)
        
        for i, rec in enumerate(recommendations, 1):
            print(f"   {i}. 🎬 {rec['title_en']}")
            if rec.get('genre'):
                print(f"      📁 Tür: {rec['genre']}")
            if rec.get('director'):
                print(f"      🎭 Yönetmen: {rec['director']}")
            if rec.get('publication_date'):
                print(f"      📅 Yıl: {rec['publication_date']}")
            if rec.get('imdb_rating'):
                print(f"      ⭐ IMDB: {rec['imdb_rating']}")
            if rec.get('similarity_score'):
                print(f"      🎯 Benzerlik: {rec['similarity_score']:.1%}")
            if rec.get('country'):
                print(f"      🌍 Ülke: {rec['country']}")
            print()
            
        # Gösterilen önerileri takip et
        for rec in recommendations:
            self.shown_recommendations.add(rec['wikidata_id'])
    
    def select_from_recommendations(self, recommendations: List[Dict]) -> Optional[str]:
        """Önerilerden film seçme"""
        while True:
            print("\n🎯 Seçenekleriniz:")
            print(f"   1-{len(recommendations)}: Yukarıdaki filmlerden birini seçin")
            print(f"   {len(recommendations)+1}: 🔄 Yeni öneriler al")
            print(f"   {len(recommendations)+2}: 🔍 Manuel film arama")
            print(f"   {len(recommendations)+3}: ❌ Bu turu atla")
            
            try:
                choice = input(f"\n✅ Seçiminiz (1-{len(recommendations)+3}): ").strip()
                choice_num = int(choice)
                
                if 1 <= choice_num <= len(recommendations):
                    # Öneri seçildi
                    selected_rec = recommendations[choice_num - 1]
                    return selected_rec['wikidata_id']
                    
                elif choice_num == len(recommendations) + 1:
                    # Yeni öneriler
                    new_recommendations = self.get_more_recommendations()
                    if new_recommendations:
                        self.display_recommendations(new_recommendations)
                        return self.select_from_recommendations(new_recommendations)
                    else:
                        print("❌ Yeni öneri bulunamadı.")
                        
                elif choice_num == len(recommendations) + 2:
                    # Manuel arama
                    return self.search_and_select_movie()
                    
                elif choice_num == len(recommendations) + 3:
                    # Turu atla
                    return None
                    
                else:
                    print("❌ Geçersiz seçim!")
                    
            except ValueError:
                print("❌ Lütfen geçerli bir numara girin!")
    
    def get_more_recommendations(self) -> List[Dict]:
        """Daha fazla öneri al"""
        try:
            # Daha geniş öneri havuzu
            all_recommendations = self.recommender.get_recommendations_by_ids(
                movie_ids=self.user_movies,
                n_recommendations=20
            )
            
            # Daha önce gösterilmemiş önerileri filtrele
            new_recommendations = []
            for rec in all_recommendations:
                if rec['wikidata_id'] not in self.shown_recommendations:
                    new_recommendations.append(rec)
                    
                    if len(new_recommendations) >= 4:
                        break
                        
            return new_recommendations
            
        except Exception as e:
            print(f"⚠️ Yeni öneriler alınırken hata: {str(e)}")
            return []
    
    def ask_continue(self) -> bool:
        """Devam etmek isteyip istemediğini sor"""
        while True:
            print("\n🎯 Devam etmek istiyor musunuz?")
            print("   1. ✅ Evet, daha fazla öneri al")
            print("   2. ❌ Hayır, çıkış yap")
            
            try:
                choice = input("Seçiminiz (1-2): ").strip()
                if choice == '1':
                    return True
                elif choice == '2':
                    return False
                else:
                    print("❌ Lütfen 1 veya 2 seçin!")
            except ValueError:
                print("❌ Geçersiz giriş!")
    
    def show_final_summary(self):
        """Final özeti göster"""
        print("\n📊 FINAL ÖZETİ")
        print("=" * 30)
        
        print(f"🎬 Toplam seçilen film: {len(self.user_movie_details)}")
        print(f"🎯 Tamamlanan tur: {self.round_number}")
        
        if self.user_movie_details:
            print(f"\n👤 Film profiliniz:")
            for i, movie in enumerate(self.user_movie_details, 1):
                print(f"   {i}. {movie['title_en']}")
                if movie.get('genre'):
                    print(f"      📁 {movie['genre']}")
                    
        print(f"\n🎉 Teşekkürler! Film deneyiminiz kaydedildi.")
        print(f"💾 Toplam {len(self.user_movies)} film profilinizde.")
        
    def run(self):
        """Ana uygulama döngüsü"""
        try:
            # İlk kurulum
            self.run_initial_setup()
            
            # Profil özeti göster
            self.clear_screen()
            self.display_header()
            self.display_user_profile()
            
            print("🎉 Harika! İlk profiliniz oluşturuldu.")
            print("Şimdi size özel öneriler sunmaya başlayabiliriz.\n")
            
            input("⏳ Devam etmek için Enter'a basın...")
            
            # Öneri turları
            while True:
                self.clear_screen()
                self.display_header()
                self.display_user_profile()
                
                # Öneri turunu çalıştır
                if not self.run_recommendation_round():
                    break
                    
                # Devam etmek isteyip istemediğini sor
                if not self.ask_continue():
                    break
                    
            # Final özeti
            self.clear_screen()
            self.display_header()
            self.show_final_summary()
            
        except KeyboardInterrupt:
            print("\n\n👋 Uygulamadan çıkılıyor...")
        except Exception as e:
            print(f"\n❌ Bir hata oluştu: {str(e)}")
            import traceback
            traceback.print_exc()


def select_dataset():
    """Kullanıcının veriset seçmesini sağla"""
    print("📊 Veriset Seçimi")
    print("=" * 30)
    
    # Mevcut CSV dosyalarını listele
    csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
    
    if not csv_files:
        print("❌ Mevcut dizinde CSV dosyası bulunamadı!")
        return None
    
    print("📁 Mevcut verisetleri:")
    for i, file in enumerate(csv_files, 1):
        # Wikidata dosyası mı kontrol et
        if 'wikidata' in file.lower() or 'wiki' in file.lower():
            print(f"   {i}. {file} 🌟 (Wikidata)")
        else:
            print(f"   {i}. {file}")
    
    print(f"   {len(csv_files)+1}. Varsayılan veriset (test_wikidata_films.csv)")
    
    try:
        choice = input(f"\nHangi veriseti kullanmak istiyorsunuz? (1-{len(csv_files)+1}): ").strip()
        choice_num = int(choice)
        
        if 1 <= choice_num <= len(csv_files):
            return csv_files[choice_num - 1]
        elif choice_num == len(csv_files) + 1:
            return 'test_wikidata_films.csv'
        else:
            print("❌ Geçersiz seçim!")
            return None
            
    except ValueError:
        print("❌ Geçersiz giriş!")
        return None


def main():
    """Ana fonksiyon"""
    print("🎬 Film İzleme Sayacı - Wikidata Gelişmiş Versiyon v0.4 Beta")
    print("=" * 65)
    
    # Veriset seçimi
    dataset_path = select_dataset()
    
    if not dataset_path:
        print("❌ Veriset seçilemedi!")
        return
    
    if not os.path.exists(dataset_path):
        print(f"❌ Veriset dosyası bulunamadı: {dataset_path}")
        return
    
    print(f"\n✅ Seçilen veriset: {dataset_path}")
    input("⏳ Başlamak için Enter'a basın...")
    
    # Uygulamayı başlat
    app = InteractiveWikidataMovieApp(dataset_path)
    app.run()


if __name__ == "__main__":
    main()
