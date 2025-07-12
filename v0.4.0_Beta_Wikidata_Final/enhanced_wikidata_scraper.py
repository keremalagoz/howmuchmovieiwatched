#!/usr/bin/env python3
"""
Geliştirilmiş Wikidata Film Veri Çekme Sistemi
Orijinal kodunuza eklenen iyileştirmeler ile.
"""

from SPARQLWrapper import SPARQLWrapper, JSON
import requests
import time
import csv
from tqdm import tqdm
import json

# --------------------------
# FİLM ÖNERİ SİSTEMİ İÇİN ÖNEMLİ PROPERTY'LER
# Producer, cinematographer ve film_editor HARİÇ TÜM ÖZELLİKLER
# --------------------------
IMPORTANT_PROPERTIES = {
    'P31': 'instance_of',           # Film olduğunu doğrula
    'P345': 'imdb_id',             # IMDB ID (çok önemli)
    'P577': 'publication_date',     # Yayın tarihi
    'P57': 'director',             # Yönetmen (çok önemli)
    'P161': 'cast_member',         # Oyuncular (önemli)
    'P136': 'genre',               # Tür (en önemli)
    'P495': 'country',             # Yapım ülkesi
    'P364': 'language',            # Dil
    'P2047': 'duration',           # Süre
    'P2130': 'budget',             # Bütçe
    'P2142': 'box_office',         # Gişe hasılatı
    'P444': 'imdb_rating',         # IMDB puanı (çok önemli)
    'P1258': 'rotten_tomatoes_id', # Rotten Tomatoes
    'P166': 'award_received',      # Ödüller
    'P921': 'main_subject',        # Ana konu/tema
    'P272': 'production_company',  # Yapımcı şirket
    'P86': 'composer',             # Müzik
    'P58': 'screenwriter',         # Senaryo
    # P344: cinematographer - HARİÇ TUTULDU
    # P1040: film_editor - HARİÇ TUTULDU  
    # P162: producer - HARİÇ TUTULDU
    'P18': 'image',                # Poster/resim
    'P856': 'official_website',    # Resmi web sitesi
    'P840': 'narrative_location',  # Hikaye geçtiği yer
    'P1434': 'based_on',           # Temel aldığı eser
    'P179': 'part_of_series',      # Serinin parçası
    'P144': 'based_on_work',       # Dayandığı eser
    'P750': 'distributor',         # Dağıtımcı
    'P915': 'filming_location',    # Çekim yeri
    'P1431': 'executive_producer', # Yürütücü yapımcı
    'P3306': 'original_network',   # Orijinal kanal
    'P449': 'original_broadcaster' # Orijinal yayıncı
}

# --------------------------
# 1. Gelişmiş Film Q-ID Çekme (Filtrelenmiş)
# --------------------------
def get_filtered_film_qids(batch_size=5000, max_batches=2, min_year=1950):
    """Filtrelenmiş film Q-ID'leri al"""
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setReturnFormat(JSON)
    qids = []

    for batch in range(max_batches):
        offset = batch * batch_size
        print(f"[+] Batch {batch+1}/{max_batches}: Q-IDs {offset} → {offset + batch_size}")
        
        # Filtrelenmiş sorgu: IMDB ID'si olan, belirli yıldan sonraki filmler
        query = f"""
        SELECT DISTINCT ?film WHERE {{
          ?film wdt:P31 wd:Q11424 .          # Film olmalı
          ?film wdt:P345 ?imdbId .           # IMDB ID olmalı
          ?film wdt:P577 ?pubDate .          # Yayın tarihi olmalı
          
          # Yıl filtresi
          FILTER(YEAR(?pubDate) >= {min_year})
          FILTER(YEAR(?pubDate) <= 2024)
        }}
        LIMIT {batch_size}
        OFFSET {offset}
        """
        
        sparql.setQuery(query)
        try:
            results = sparql.query().convert()
            batch_qids = []
            for result in results["results"]["bindings"]:
                qid = result["film"]["value"].split("/")[-1]
                batch_qids.append(qid)
                qids.append(qid)
            
            print(f"    → {len(batch_qids)} film bulundu")
            
        except Exception as e:
            print(f"[!] SPARQL Hatası: {e}")
            time.sleep(10)
            continue

        time.sleep(1.5)  # Rate limit uyumu

    print(f"[✓] Toplam {len(qids)} film Q-ID'si toplandı")
    return qids

# --------------------------
# 2. Gelişmiş Veri Çekme ve İşleme
# --------------------------
def get_enhanced_film_data(qid):
    """Gelişmiş film verisi çek ve işle"""
    url = f"https://www.wikidata.org/wiki/Special:EntityData/{qid}.json"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return None

        entity = response.json()["entities"][qid]
        claims = entity.get("claims", {})
        labels = entity.get("labels", {})
        descriptions = entity.get("descriptions", {})
        
        # Temel bilgiler
        film_data = {
            "qid": qid,
            "title_en": labels.get("en", {}).get("value", ""),
            "title_tr": labels.get("tr", {}).get("value", ""),
            "description_en": descriptions.get("en", {}).get("value", ""),
            "description_tr": descriptions.get("tr", {}).get("value", "")
        }

        # Önemli property'leri işle
        for prop_id, prop_name in IMPORTANT_PROPERTIES.items():
            if prop_id in claims:
                values = extract_property_values(claims[prop_id])
                if values:
                    film_data[prop_name] = "|".join(values)  # Çoklu değerleri | ile ayır
                    
                    # Özel işlemler
                    if prop_name == "publication_date" and values:
                        film_data["year"] = extract_year(values[0])
                    elif prop_name == "duration" and values:
                        film_data["duration_minutes"] = parse_duration(values[0])
                    elif prop_name == "imdb_rating" and values:
                        try:
                            film_data["imdb_rating_float"] = float(values[0])
                        except:
                            pass

        return film_data

    except Exception as e:
        print(f"[!] {qid} parse hatası: {e}")
        return None

def extract_property_values(property_claims):
    """Property claim'lerinden değerleri çıkar"""
    values = []
    
    for claim in property_claims:
        mainsnak = claim.get("mainsnak", {})
        datavalue = mainsnak.get("datavalue", {})
        
        if not datavalue:
            continue
            
        value = datavalue.get("value")
        if isinstance(value, dict):
            if "id" in value:  # Wikidata entity
                values.append(value["id"])
            elif "time" in value:  # Tarih
                values.append(value["time"])
            elif "amount" in value:  # Sayı
                values.append(value["amount"])
            else:
                values.append(str(value))
        else:
            values.append(str(value))
    
    return values

def extract_year(date_string):
    """Tarih string'inden yılı çıkar"""
    try:
        if date_string.startswith("+"):
            return int(date_string[1:5])
        elif date_string.startswith("-"):
            return int(date_string[1:5]) * -1
        else:
            return int(date_string[:4])
    except:
        return None

def parse_duration(duration_string):
    """Süre string'ini dakikaya çevir"""
    try:
        if "+" in duration_string:
            duration_string = duration_string.replace("+", "")
        return int(float(duration_string))
    except:
        return None

# --------------------------
# 3. Gelişmiş CSV Export + JSON Backup
# --------------------------
def collect_enhanced_data(qid_list, output_csv="enhanced_wikidata_films.csv", output_json="films_backup.json"):
    """Gelişmiş veri toplama ve kaydetme"""
    
    all_data = []
    successful_count = 0
    failed_count = 0

    print(f"[*] {len(qid_list)} film için veri toplanıyor...")
    
    for i, qid in enumerate(tqdm(qid_list), 1):
        film_data = get_enhanced_film_data(qid)
        
        if film_data:
            all_data.append(film_data)
            successful_count += 1
        else:
            failed_count += 1
        
        # Progress raporu
        if i % 100 == 0:
            print(f"    Progress: {i}/{len(qid_list)} - Success: {successful_count}, Failed: {failed_count}")
        
        time.sleep(0.5)  # Rate limit

    # JSON backup kaydet
    print(f"[*] JSON backup kaydediliyor: {output_json}")
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

    # CSV kaydet
    if all_data:
        print(f"[*] CSV kaydediliyor: {output_csv}")
        
        # Tüm sütunları topla
        all_columns = set()
        for film in all_data:
            all_columns.update(film.keys())
        
        # Sütun sıralaması - Producer, cinematographer, film_editor hariç
        priority_columns = [
            'qid', 'title_en', 'title_tr', 'year', 'imdb_id', 'imdb_rating_float',
            'director', 'genre', 'cast_member', 'duration_minutes', 'country',
            'language', 'budget', 'box_office', 'award_received', 'main_subject',
            'production_company', 'composer', 'screenwriter', 'narrative_location',
            'based_on', 'part_of_series', 'based_on_work', 'distributor',
            'filming_location', 'executive_producer', 'original_network',
            'original_broadcaster', 'description_en', 'description_tr'
        ]
        
        ordered_columns = []
        for col in priority_columns:
            if col in all_columns:
                ordered_columns.append(col)
                all_columns.remove(col)
        ordered_columns.extend(sorted(all_columns))
        
        # CSV yaz
        with open(output_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=ordered_columns)
            writer.writeheader()
            for film in all_data:
                writer.writerow(film)

    print(f"[✓] Tamamlandı!")
    print(f"    Başarılı: {successful_count}")
    print(f"    Başarısız: {failed_count}")
    print(f"    CSV: {output_csv}")
    print(f"    JSON Backup: {output_json}")
    
    return all_data

# --------------------------
# 4. Ana Fonksiyon + Kullanıcı Seçenekleri
# --------------------------
def main():
    print("🎬 GELİŞMİŞ WIKIDATA FİLM VERİ ÇEKME SİSTEMİ")
    print("=" * 60)
    
    print("📋 Seçenekler:")
    print("   1. Hızlı test (50 film)")
    print("   2. Orta ölçek (1000 film)")  
    print("   3. Büyük ölçek (10000 film)")
    print("   4. Özel ayarlar")
    
    choice = input("Seçiminiz (1-4): ").strip()
    
    if choice == "1":
        batch_size, max_batches = 50, 1
        output_csv = "test_wikidata_films.csv"
    elif choice == "2":
        batch_size, max_batches = 1000, 1
        output_csv = "medium_wikidata_films.csv"
    elif choice == "3":
        batch_size, max_batches = 5000, 2
        output_csv = "large_wikidata_films.csv"
    elif choice == "4":
        batch_size = int(input("Batch size: "))
        max_batches = int(input("Max batches: "))
        output_csv = input("Output CSV adı: ")
    else:
        print("❌ Geçersiz seçim!")
        return
    
    min_year = int(input("Minimum yıl (örn: 1950): ") or "1950")
    
    print(f"\n🚀 İşlem başlıyor...")
    print(f"   Batch size: {batch_size}")
    print(f"   Max batches: {max_batches}")
    print(f"   Total target: {batch_size * max_batches}")
    print(f"   Min year: {min_year}")
    print(f"   Output: {output_csv}")
    
    # Q-ID'leri topla
    qid_list = get_filtered_film_qids(batch_size, max_batches, min_year)
    
    if not qid_list:
        print("❌ Hiç film Q-ID'si bulunamadı!")
        return
    
    # Veri çek ve kaydet
    films_data = collect_enhanced_data(qid_list, output_csv)
    
    # Özet istatistik
    if films_data:
        print(f"\n📊 VERİSET ÖZETİ:")
        print(f"   Toplam film: {len(films_data)}")
        
        # IMDB ID'si olanlar
        imdb_count = sum(1 for f in films_data if f.get('imdb_id'))
        print(f"   IMDB ID'li: {imdb_count}")
        
        # Rating olanlar
        rating_count = sum(1 for f in films_data if f.get('imdb_rating_float'))
        if rating_count > 0:
            avg_rating = sum(f.get('imdb_rating_float', 0) for f in films_data if f.get('imdb_rating_float')) / rating_count
            print(f"   IMDB rating'li: {rating_count} (ortalama: {avg_rating:.1f})")
        
        # Yıl dağılımı
        years = [f.get('year') for f in films_data if f.get('year')]
        if years:
            print(f"   Yıl aralığı: {min(years)}-{max(years)}")

if __name__ == "__main__":
    main()
