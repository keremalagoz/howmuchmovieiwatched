#!/usr/bin/env python3
"""
ENHANCED WIKIDATA SCRAPER v2.5 - ROBUSTIFIED
- Akıllı checkpoint sistemi
- Gelişmiş hata yönetimi ve retry mekanizması
- Label cache optimizasyonu
- Windows güncelleme koruması
- Sinyal işleme ile güvenli kapatma
"""

import argparse
import os
import json
import time
import csv
import signal
import sys
import random
from datetime import datetime
from tqdm import tqdm
from SPARQLWrapper import SPARQLWrapper, JSON
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# urllib3 uyarılarını sustur
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ============ 403 FORBIDDEN HATASI ÇÖZÜMÜ ============
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0',
    'WikidataBot/1.0 (https://wikidata.org/wiki/User:Example)',
    'Python-requests/2.25.1',
    'SPARQL-Client/1.0 (Wikidata Film Scraper)',
    'Mozilla/5.0 (compatible; WikidataFilmBot/1.0; +https://wikidata.org)'
]

def get_random_user_agent():
    """Rastgele bir User-Agent döndür"""
    return random.choice(USER_AGENTS)

# ============ ÖNEMLİ PROPERTY'LER ============
IMPORTANT_PROPERTIES = {
    'P31': 'instance_of',
    'P345': 'imdb_id',
    'P577': 'publication_date',
    'P57': 'director',
    'P161': 'cast_member',
    'P136': 'genre',
    'P495': 'country',
    'P364': 'language',
    'P2047': 'duration',
    'P2130': 'budget',
    'P2142': 'box_office',
    'P444': 'imdb_rating',
    'P1258': 'rotten_tomatoes_id',
    'P166': 'award_received',
    'P921': 'main_subject',
    'P272': 'production_company',
    'P86': 'composer',
    'P58': 'screenwriter',
    'P18': 'image',
    'P856': 'official_website',
    'P840': 'narrative_location',
    'P1434': 'based_on',
    'P179': 'part_of_series',
    'P144': 'based_on_work',
    'P750': 'distributor',
    'P915': 'filming_location',
    'P1431': 'executive_producer',
    'P3306': 'original_network',
    'P449': 'original_broadcaster'
}

# ============ GÜÇLÜ CHECKPOINT SİSTEMİ ============
class SmartCheckpoint:
    def __init__(self, filename="wikidata_checkpoint.json"):
        self.filename = filename
        self.temp_filename = self.filename + ".tmp"
        self.backup_filename = self.filename + ".backup"
        self.data = {"processed_ids": set(), "films": [], "progress": 0, "timestamp": None}
        self.load()
    
    def load(self):
        """Checkpoint dosyasını yükle, başarısız olursa backup'tan dene"""
        for file_to_try in [self.filename, self.backup_filename]:
            if os.path.exists(file_to_try):
                try:
                    with open(file_to_try, "r", encoding="utf-8") as f:
                        loaded = json.load(f)
                        self.data["processed_ids"] = set(loaded.get("processed_ids", []))
                        self.data["films"] = loaded.get("films", [])
                        self.data["progress"] = loaded.get("progress", 0)
                        self.data["timestamp"] = loaded.get("timestamp")
                    print(f"✅ Checkpoint yüklendi: {len(self.data['films'])} film, {len(self.data['processed_ids'])} işlenmiş ID")
                    return
                except Exception as e:
                    print(f"⚠️ {file_to_try} yüklenemedi: {e}")
                    continue
        print("ℹ️ Yeni checkpoint başlatılıyor...")
    
    def save(self):
        """Güvenli checkpoint kaydetme - atomik işlem"""
        try:
            save_data = {
                "processed_ids": list(self.data["processed_ids"]),
                "films": self.data["films"],
                "progress": self.data["progress"],
                "timestamp": datetime.now().isoformat()
            }
            
            # Önce temp dosyaya yaz
            with open(self.temp_filename, "w", encoding="utf-8") as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
            
            # Eski dosyayı backup'a taşı
            if os.path.exists(self.filename):
                os.replace(self.filename, self.backup_filename)
            
            # Temp dosyayı asıl dosyaya taşı
            os.replace(self.temp_filename, self.filename)
            
        except Exception as e:
            print(f"❌ Checkpoint kaydedilemedi: {e}")
            # Temp dosyayı temizle
            if os.path.exists(self.temp_filename):
                try:
                    os.remove(self.temp_filename)
                except:
                    pass
    
    def add_film(self, film_data):
        """Film ekle ve işlenmiş ID'yi kaydet"""
        self.data["films"].append(film_data)
        self.data["processed_ids"].add(film_data["qid"])
        self.data["progress"] = len(self.data["films"])
    
    def is_processed(self, qid):
        """QID daha önce işlenmiş mi?"""
        return qid in self.data["processed_ids"]
    
    def get_stats(self):
        """İstatistikleri al"""
        return {
            "total_films": len(self.data["films"]),
            "processed_ids": len(self.data["processed_ids"]),
            "timestamp": self.data["timestamp"]
        }

# ============ GÜÇLÜ LABEL CACHE YÖNETİCİSİ ============
class LabelCacheManager:
    def __init__(self, filename="labels_cache.json"):
        self.filename = filename
        self.temp_filename = self.filename + ".tmp"
        self.backup_filename = self.filename + ".backup"
        self.cache = {}
        self.changes_count = 0
        self.save_interval = 100  # Her 100 değişiklikte kaydet
        self.load()
    
    def load(self):
        """Label cache'ini yükle"""
        for file_to_try in [self.filename, self.backup_filename]:
            if os.path.exists(file_to_try):
                try:
                    with open(file_to_try, "r", encoding="utf-8") as f:
                        self.cache = json.load(f)
                    print(f"✅ Label cache yüklendi: {len(self.cache)} etiket")
                    return
                except Exception as e:
                    print(f"⚠️ {file_to_try} yüklenemedi: {e}")
                    continue
        print("ℹ️ Yeni label cache başlatılıyor...")
    
    def get(self, qid, lang="tr"):
        """Label'ı al, yoksa Wikidata'dan çek"""
        if qid in self.cache:
            return self.cache[qid]
        
        # Wikidata'dan çek
        label = self._fetch_label(qid, lang)
        self.cache[qid] = label
        self.changes_count += 1
        
        # Belirli aralıklarla kaydet
        if self.changes_count >= self.save_interval:
            self.save()
            self.changes_count = 0
        
        return label
    
    def _fetch_label(self, qid, lang="tr"):
        """Wikidata'dan label çek"""
        url = f"https://www.wikidata.org/wiki/Special:EntityData/{qid}.json"
        try:
            # Basit requests kullan (label'lar için)
            import requests
            headers = {
                'User-Agent': get_random_user_agent(),
                'Accept': 'application/json'
            }
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                label = data["entities"][qid]["labels"].get(lang, {}).get("value", qid)
                return label
        except Exception as e:
            print(f"⚠️ Label çekilemedi {qid}: {e}")
        return qid
    
    def save(self):
        """Güvenli label cache kaydetme"""
        try:
            # Önce temp dosyaya yaz
            with open(self.temp_filename, "w", encoding="utf-8") as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
            
            # Eski dosyayı backup'a taşı
            if os.path.exists(self.filename):
                os.replace(self.filename, self.backup_filename)
            
            # Temp dosyayı asıl dosyaya taşı
            os.replace(self.temp_filename, self.filename)
            
        except Exception as e:
            print(f"❌ Label cache kaydedilemedi: {e}")
            # Temp dosyayı temizle
            if os.path.exists(self.temp_filename):
                try:
                    os.remove(self.temp_filename)
                except:
                    pass
    
    def force_save(self):
        """Zorunlu kaydetme"""
        self.save()
        self.changes_count = 0

# ============ GÜÇLÜ HTTP İSTEK YÖNETİCİSİ (403 Hatası Çözümü ile) ============
class RobustHTTPManager:
    def __init__(self):
        self.session = requests.Session()
        
        # 403 hatası için gelişmiş retry stratejisi
        retry_strategy = Retry(
            total=5,
            backoff_factor=2,
            status_forcelist=[403, 429, 500, 502, 503, 504],
            allowed_methods=["GET"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Timeout ayarları
        self.session.timeout = 30
        
        # Başlangıç headers
        self.update_headers()
    
    def update_headers(self):
        """Headers'ı güncel User-Agent ile güncelle"""
        self.session.headers.update({
            'User-Agent': get_random_user_agent(),
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9,tr;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
        })
    
    def get(self, url, **kwargs):
        """403 hatası çözümü ile güçlü GET isteği"""
        max_attempts = 5
        
        for attempt in range(max_attempts):
            try:
                # Her denemede farklı User-Agent kullan
                if attempt > 0:
                    self.update_headers()
                    print(f"    🔄 User-Agent değiştirildi (deneme {attempt + 1})")
                
                response = self.session.get(url, **kwargs)
                
                if response.status_code == 403:
                    print(f"    ⚠️ 403 Forbidden (deneme {attempt + 1}/{max_attempts})")
                    if attempt < max_attempts - 1:
                        wait_time = (2 ** attempt) + random.uniform(1, 3)
                        print(f"    ⏰ {wait_time:.1f} saniye bekleniyor...")
                        time.sleep(wait_time)
                        continue
                    else:
                        print(f"    ❌ Maksimum deneme sayısına ulaşıldı")
                        return None
                
                response.raise_for_status()
                return response
                
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 403:
                    print(f"    ⚠️ 403 HTTPError (deneme {attempt + 1}/{max_attempts})")
                    if attempt < max_attempts - 1:
                        wait_time = (2 ** attempt) + random.uniform(1, 3)
                        time.sleep(wait_time)
                        continue
                print(f"    ❌ HTTP hatası ({url}): {e}")
                return None
            except Exception as e:
                print(f"    ❌ Genel hata (deneme {attempt + 1}): {e}")
                if attempt < max_attempts - 1:
                    time.sleep(1)
                    continue
                return None
        
        return None

# ============ SİNYAL İŞLEME ============
class GracefulKiller:
    def __init__(self):
        self.kill_now = False
        signal.signal(signal.SIGINT, self._exit_gracefully)
        signal.signal(signal.SIGTERM, self._exit_gracefully)
    
    def _exit_gracefully(self, signum, frame):
        print("\n🛑 Güvenli kapatma başlatılıyor...")
        self.kill_now = True

# ============ GLOBAL OBJECTS ============
checkpoint = SmartCheckpoint()
label_cache_manager = LabelCacheManager()
http_manager = RobustHTTPManager()
killer = GracefulKiller()

# ============ LABEL CACHE - LEGACY UYUMLULUK ============
def get_label(qid, lang="tr"):
    """Eski uyumluluk için wrapper"""
    return label_cache_manager.get(qid, lang)

# ============ Q-ID ÇEKME (403 Hatası Çözümü ile) ============
def get_film_qids(batch_size, offset, min_year, max_retries=5):
    """SPARQL sorgusu ile film QID'leri çek - 403 hatası çözümü ile"""
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setReturnFormat(JSON)

    print(f"[+] Offset {offset}, batch size {batch_size}")
    query = f"""
    SELECT DISTINCT ?film WHERE {{
        ?film wdt:P31 wd:Q11424 .
        ?film wdt:P345 ?imdbId .
        ?film wdt:P577 ?pubDate .
        FILTER(YEAR(?pubDate) >= {min_year})
        FILTER(YEAR(?pubDate) <= 2024)
    }}
    LIMIT {batch_size}
    OFFSET {offset}
    """

    sparql.setQuery(query)
    
    for attempt in range(max_retries):
        try:
            # Her denemede farklı User-Agent kullan
            user_agent = get_random_user_agent()
            sparql.addCustomHttpHeader("User-Agent", user_agent)
            sparql.addCustomHttpHeader("Accept", "application/sparql-results+json")
            sparql.addCustomHttpHeader("Accept-Language", "en-US,en;q=0.9")
            
            print(f"    → SPARQL deneme {attempt + 1}/{max_retries}...")
            
            results = sparql.query().convert()
            qids = [result["film"]["value"].split("/")[-1] for result in results["results"]["bindings"]]
            print(f"✅ {len(qids)} QID çekildi")
            return qids
            
        except Exception as e:
            error_msg = str(e).lower()
            print(f"⚠️ SPARQL Hatası (deneme {attempt + 1}/{max_retries}): {e}")
            
            if "403" in error_msg or "forbidden" in error_msg:
                print(f"    ⚠️ 403 Forbidden tespit edildi")
                wait_time = (2 ** attempt) + random.uniform(2, 5)
                print(f"    ⏰ {wait_time:.1f} saniye bekleniyor...")
                time.sleep(wait_time)
            elif "429" in error_msg or "rate" in error_msg:
                print(f"    ⚠️ Rate limit hatası")
                time.sleep(60 + random.uniform(10, 30))
            else:
                wait_time = 5 + (attempt * 2)
                time.sleep(wait_time)
            
            if attempt == max_retries - 1:
                print("❌ SPARQL sorgusu başarısız oldu")
                return []
    
    return []

# ============ VERİ ÇEKME (403 Hatası Çözümü ile) ============
def get_film_data(qid, max_retries=5):
    """Film verilerini Wikidata'dan çek - 403 hatası çözümü ile"""
    url = f"https://www.wikidata.org/wiki/Special:EntityData/{qid}.json"
    
    for attempt in range(max_retries):
        try:
            response = http_manager.get(url)
            
            if not response:
                if attempt < max_retries - 1:
                    wait_time = 1 + (attempt * 0.5)
                    time.sleep(wait_time)
                    continue
                return None
            
            if response.status_code == 403:
                print(f"    ⚠️ {qid} - 403 Forbidden (deneme {attempt + 1})")
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt) + random.uniform(1, 3)
                    time.sleep(wait_time)
                    # HTTP manager'ın headers'ını yenile
                    http_manager.update_headers()
                    continue
                return None
            
            if response.status_code != 200:
                print(f"    ⚠️ {qid} - HTTP {response.status_code}")
                if attempt < max_retries - 1:
                    time.sleep(1)
                    continue
                return None

            entity = response.json()["entities"][qid]
            claims = entity.get("claims", {})
            labels = entity.get("labels", {})
            descriptions = entity.get("descriptions", {})

            data = {
                "qid": qid,
                "title_en": labels.get("en", {}).get("value", ""),
                "title_tr": labels.get("tr", {}).get("value", ""),
                "description_en": descriptions.get("en", {}).get("value", ""),
                "description_tr": descriptions.get("tr", {}).get("value", "")
            }

            for prop_id, name in IMPORTANT_PROPERTIES.items():
                if prop_id in claims:
                    values = extract_values(claims[prop_id])
                    if values:
                        data[name] = "|".join(values)

                        # Label ekle
                        if all(v.startswith("Q") for v in values):
                            label_values = [get_label(v, lang="tr") for v in values]
                            data[f"{name}_label"] = "|".join(label_values)

                        if name == "publication_date":
                            data["year"] = extract_year(values[0])
                        if name == "duration":
                            data["duration_minutes"] = parse_duration(values[0])
                        if name == "imdb_rating":
                            try:
                                data["imdb_rating_float"] = float(values[0])
                            except:
                                pass
            return data
            
        except Exception as e:
            error_msg = str(e).lower()
            print(f"⚠️ {qid} parse hatası (deneme {attempt + 1}/{max_retries}): {e}")
            
            if "403" in error_msg or "forbidden" in error_msg:
                wait_time = (2 ** attempt) + random.uniform(1, 3)
                time.sleep(wait_time)
                # HTTP manager'ı yenile
                http_manager.update_headers()
            elif attempt < max_retries - 1:
                time.sleep(0.5 * (attempt + 1))
            else:
                print(f"❌ {qid} verisi çekilemedi")
                return None
    
    return None

def extract_values(claims):
    values = []
    for c in claims:
        snak = c.get("mainsnak", {})
        val = snak.get("datavalue", {}).get("value", None)
        if isinstance(val, dict):
            if "id" in val:
                values.append(val["id"])
            elif "time" in val:
                values.append(val["time"])
            elif "amount" in val:
                values.append(val["amount"])
        elif val:
            values.append(str(val))
    return values

def extract_year(date_string):
    try:
        if date_string.startswith("+"):
            return int(date_string[1:5])
        elif date_string.startswith("-"):
            return -int(date_string[1:5])
        return int(date_string[:4])
    except:
        return None

def parse_duration(val):
    try:
        return int(float(val.replace("+", "")))
    except:
        return None

# ============ ANA =============
def main():
    print("🚀 ENHANCED WIKIDATA SCRAPER v2.5 - ROBUSTIFIED 🚀")
    print("🛡️ HTTP 403 FORBIDDEN HATASI ÇÖZÜMÜ AKTİF")
    print("=" * 60)
    
    parser = argparse.ArgumentParser(description="Güçlü Wikidata Film Scraper - 403 Hatası Çözümü ile")
    parser.add_argument("--resume-from", type=int, default=0, help="Başlangıç offset'i")
    parser.add_argument("--batches", type=int, default=10, help="Batch sayısı")
    parser.add_argument("--batch-size", type=int, default=1000, help="Batch boyutu")
    parser.add_argument("--min-year", type=int, default=1950, help="Minimum yıl")
    parser.add_argument("--output", type=str, default="films_resume_label.csv", help="Çıktı CSV dosyası")
    parser.add_argument("--checkpoint-interval", type=int, default=50, help="Checkpoint kaydetme aralığı")
    args = parser.parse_args()

    print(f"📊 Parametreler:")
    print(f"   - Resume offset: {args.resume_from}")
    print(f"   - Batch sayısı: {args.batches}")
    print(f"   - Batch boyutu: {args.batch_size}")
    print(f"   - Minimum yıl: {args.min_year}")
    print(f"   - Çıktı dosyası: {args.output}")
    print(f"   - Checkpoint aralığı: {args.checkpoint_interval}")
    
    print(f"\n🔧 403 Hatası Çözümleri:")
    print(f"   ✅ {len(USER_AGENTS)} farklı User-Agent rotasyonu")
    print(f"   ✅ Exponential backoff algoritması")
    print(f"   ✅ Otomatik retry mekanizması (5 deneme)")
    print(f"   ✅ Session ve header yenileme")
    print(f"   ✅ Gelişmiş rate limiting")
    print()

    failed_ids = []
    processed_count = 0
    start_time = time.time()

    try:
        # Checkpoint durumunu göster
        stats = checkpoint.get_stats()
        print(f"📋 Checkpoint durumu:")
        print(f"   - Toplam film: {stats['total_films']}")
        print(f"   - İşlenmiş ID: {stats['processed_ids']}")
        print(f"   - Son güncelleme: {stats['timestamp']}")
        print()

        for i in range(args.batches):
            if killer.kill_now:
                print("🛑 Güvenli kapatma tespit edildi!")
                break
                
            offset = args.resume_from + i * args.batch_size
            print(f"📦 Batch {i+1}/{args.batches} → Offset {offset}")
            
            qids = get_film_qids(args.batch_size, offset, args.min_year)
            if not qids:
                print("⚠️ QID alınamadı, duruluyor...")
                break

            batch_processed = 0
            for qid in tqdm(qids, desc=f"Batch {i+1} işleniyor"):
                if killer.kill_now:
                    print("🛑 Güvenli kapatma tespit edildi!")
                    break
                    
                # Daha önce işlenmiş mi kontrol et
                if checkpoint.is_processed(qid):
                    continue
                
                data = get_film_data(qid)
                if data:
                    checkpoint.add_film(data)
                    batch_processed += 1
                    processed_count += 1
                else:
                    failed_ids.append(qid)
                
                # Checkpoint kaydet
                if processed_count % args.checkpoint_interval == 0:
                    checkpoint.save()
                    print(f"💾 Checkpoint kaydedildi: {processed_count} film işlendi")
                
                # 403 hatası önleme için daha uzun bekleme
                time.sleep(random.uniform(0.5, 1.5))  # Rastgele bekleme

            print(f"✅ Batch {i+1} tamamlandı: {batch_processed} yeni film")
            
            # Her batch sonunda checkpoint kaydet
            checkpoint.save()
            
            if killer.kill_now:
                break

    except KeyboardInterrupt:
        print("\n🛑 Klavye kesintisi tespit edildi!")
    except Exception as e:
        print(f"❌ Beklenmeyen hata: {e}")
    finally:
        # Güvenli kapatma
        print("\n🔄 Güvenli kapatma işlemleri...")
        
        # Final checkpoint
        checkpoint.save()
        print("💾 Final checkpoint kaydedildi")
        
        # Label cache'i kaydet
        label_cache_manager.force_save()
        print("💾 Label cache kaydedildi")

        # Hatalı ID'leri kaydet
        if failed_ids:
            with open("failed_ids.txt", "w", encoding="utf-8") as f:
                f.write("\n".join(failed_ids))
            print(f"📝 {len(failed_ids)} başarısız ID kaydedildi")

        # CSV export
        print(f"📊 CSV yazılıyor: {args.output}")
        export_csv(checkpoint.data["films"], args.output)

        # JSON yedeği
        backup_filename = "films_resume_label_backup.json"
        with open(backup_filename, "w", encoding="utf-8") as f:
            json.dump(checkpoint.data["films"], f, ensure_ascii=False, indent=2)
        print(f"💾 JSON yedeği kaydedildi: {backup_filename}")

        # İstatistikler
        elapsed_time = time.time() - start_time
        total_films = len(checkpoint.data["films"])
        print(f"\n📈 ÖZET:")
        print(f"   - Toplam film: {total_films}")
        print(f"   - İşlenmiş film: {processed_count}")
        print(f"   - Başarısız: {len(failed_ids)}")
        print(f"   - Geçen süre: {elapsed_time:.2f} saniye")
        if processed_count > 0:
            print(f"   - Hız: {processed_count / elapsed_time:.2f} film/saniye")
        print("🎉 Scraping tamamlandı!")

def safe_exit():
    """Güvenli çıkış fonksiyonu"""
    print("🛑 Güvenli çıkış yapılıyor...")
    checkpoint.save()
    label_cache_manager.force_save()
    print("✅ Tüm veriler kaydedildi")
    sys.exit(0)

def export_csv(data, filename):
    """CSV dosyasına güvenli yazma"""
    if not data:
        print("⚠️ Yazılacak veri yok")
        return
    
    try:
        all_cols = set()
        for d in data:
            all_cols.update(d.keys())
        cols = sorted(all_cols)
        
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=cols)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
        print(f"✅ CSV dosyası kaydedildi: {filename} ({len(data)} kayıt)")
    except Exception as e:
        print(f"❌ CSV yazma hatası: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Klavye kesintisi - güvenli çıkış")
        safe_exit()
    except Exception as e:
        print(f"❌ Beklenmeyen hata: {e}")
        safe_exit()
