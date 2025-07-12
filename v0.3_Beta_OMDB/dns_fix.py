"""
DNS Sorun Giderici - İnternet Bağlantı Sorunları İçin Yardımcı Script

Bu script DNS sorunlarını çözmek için çeşitli yöntemler dener.
"""

import socket
import subprocess
import sys
import requests
from typing import List, Tuple

def test_dns_resolution(hostnames: List[str]) -> List[Tuple[str, bool]]:
    """DNS çözümlemesini test et"""
    results = []
    
    for hostname in hostnames:
        try:
            socket.gethostbyname(hostname)
            results.append((hostname, True))
            print(f"✅ {hostname} - DNS çözümlemesi başarılı")
        except socket.gaierror:
            results.append((hostname, False))
            print(f"❌ {hostname} - DNS çözümlemesi başarısız")
    
    return results

def flush_dns():
    """DNS cache'ini temizle"""
    try:
        print("🔄 DNS cache temizleniyor...")
        subprocess.run(['ipconfig', '/flushdns'], check=True, capture_output=True)
        print("✅ DNS cache temizlendi")
        return True
    except Exception as e:
        print(f"❌ DNS cache temizleme başarısız: {e}")
        return False

def test_internet_connectivity():
    """İnternet bağlantısını test et"""
    test_urls = [
        "https://www.google.com",
        "https://www.cloudflare.com",
        "https://1.1.1.1",
        "https://8.8.8.8"
    ]
    
    print("🌐 İnternet bağlantısı test ediliyor...")
    
    for url in test_urls:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {url} - Bağlantı başarılı")
                return True
        except Exception as e:
            print(f"❌ {url} - Bağlantı başarısız: {e}")
            continue
    
    print("❌ İnternet bağlantısı tespit edilemedi!")
    return False

def suggest_dns_servers():
    """Alternatif DNS sunucuları öner"""
    print("\n🔧 Önerilen DNS Sunucuları:")
    print("1. Google DNS: 8.8.8.8, 8.8.4.4")
    print("2. Cloudflare DNS: 1.1.1.1, 1.0.0.1")
    print("3. OpenDNS: 208.67.222.222, 208.67.220.220")
    print("4. Quad9 DNS: 9.9.9.9, 149.112.112.112")
    print("\nDNS değiştirme talimatları:")
    print("1. Denetim Masası > Ağ ve İnternet > Ağ ve Paylaşım Merkezi")
    print("2. Bağlantınıza tıklayın > Özellikler")
    print("3. Internet Protocol Version 4 (TCP/IPv4) > Özellikler")
    print("4. 'Aşağıdaki DNS sunucu adreslerini kullan' seçeneğini işaretleyin")
    print("5. Yukarıdaki DNS adreslerini girin")

def test_omdb_endpoints():
    """OMDB API endpoint'lerini test et"""
    endpoints = [
        "https://www.omdbapi.com/",
        "https://omdbapi.com/",
        "http://www.omdbapi.com/",
        "http://omdbapi.com/"
    ]
    
    print("\n🎬 OMDB API endpoint'leri test ediliyor...")
    
    working_endpoints = []
    
    for endpoint in endpoints:
        try:
            response = requests.get(endpoint, timeout=10)
            if response.status_code == 200:
                print(f"✅ {endpoint} - Erişilebilir")
                working_endpoints.append(endpoint)
            else:
                print(f"❌ {endpoint} - HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint} - Hata: {e}")
    
    return working_endpoints

def main():
    """Ana fonksiyon"""
    print("🔧 DNS ve İnternet Bağlantısı Sorun Giderici")
    print("=" * 50)
    
    # İnternet bağlantısını test et
    internet_ok = test_internet_connectivity()
    
    if not internet_ok:
        print("\n❌ İnternet bağlantısı sorunu tespit edildi!")
        suggest_dns_servers()
        return
    
    # DNS çözümlemesini test et
    print("\n🔍 DNS çözümlemesi test ediliyor...")
    dns_hosts = [
        "www.omdbapi.com",
        "omdbapi.com",
        "www.google.com",
        "www.github.com"
    ]
    
    dns_results = test_dns_resolution(dns_hosts)
    
    # OMDB host'ları başarısızsa DNS temizlemeyi dene
    omdb_dns_ok = any(result[1] for result in dns_results if 'omdb' in result[0])
    
    if not omdb_dns_ok:
        print("\n⚠️ OMDB DNS çözümlemesi başarısız!")
        flush_dns()
        
        print("\n🔍 DNS temizleme sonrası tekrar test ediliyor...")
        dns_results = test_dns_resolution(dns_hosts)
        omdb_dns_ok = any(result[1] for result in dns_results if 'omdb' in result[0])
    
    # OMDB endpoint'lerini test et
    working_endpoints = test_omdb_endpoints()
    
    # Sonuç raporu
    print("\n📊 Sonuç Raporu:")
    print("=" * 30)
    
    if internet_ok:
        print("✅ İnternet bağlantısı: Çalışıyor")
    else:
        print("❌ İnternet bağlantısı: Sorunlu")
    
    if omdb_dns_ok:
        print("✅ OMDB DNS çözümlemesi: Çalışıyor")
    else:
        print("❌ OMDB DNS çözümlemesi: Sorunlu")
    
    if working_endpoints:
        print(f"✅ Çalışan OMDB endpoint'leri: {len(working_endpoints)}")
        for endpoint in working_endpoints:
            print(f"   • {endpoint}")
    else:
        print("❌ Hiçbir OMDB endpoint'i erişilebilir değil")
    
    # Öneriler
    print("\n💡 Öneriler:")
    
    if not omdb_dns_ok and not working_endpoints:
        print("1. 🌐 İnternet bağlantınızı kontrol edin")
        print("2. 🔧 DNS sunucularınızı değiştirin (öneriler yukarıda)")
        print("3. 🔄 Modeminizi/router'ınızı yeniden başlatın")
        print("4. 🛡️ Güvenlik duvarı ayarlarınızı kontrol edin")
        print("5. 📱 Mobil hotspot ile test edin")
        print("6. 💾 Offline veriset kullanın: python offline_omdb_creator.py")
    elif working_endpoints:
        print("✅ OMDB API kullanılabilir, projenizi çalıştırabilirsiniz!")
    
    input("\nDevam etmek için Enter'a basın...")

if __name__ == "__main__":
    main()
