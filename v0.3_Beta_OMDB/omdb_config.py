"""
OMDB API Configuration Manager
API anahtarı yönetimi ve yapılandırma
"""

import os
import json
from pathlib import Path


class OMDBConfig:
    """OMDB API yapılandırma yöneticisi"""
    
    def __init__(self):
        self.config_file = "omdb_config.json"
        self.env_file = ".env"
        
    def get_api_key(self) -> str:
        """API anahtarını farklı kaynaklardan al"""
        
        # 1. Environment variable'dan kontrol et
        api_key = os.getenv('OMDB_API_KEY')
        if api_key and api_key != 'your_api_key_here':
            print("✅ API anahtarı environment variable'dan alındı")
            return api_key
        
        # 2. Config dosyasından kontrol et
        api_key = self._load_from_config()
        if api_key:
            print("✅ API anahtarı config dosyasından alındı")
            return api_key
        
        # 3. .env dosyasından kontrol et
        api_key = self._load_from_env()
        if api_key:
            print("✅ API anahtarı .env dosyasından alındı")
            return api_key
        
        # 4. Kullanıcıdan iste
        return self._get_from_user()
    
    def _load_from_config(self) -> str:
        """Config JSON dosyasından API anahtarını yükle"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    return config.get('omdb_api_key', '')
        except:
            pass
        return ''
    
    def _load_from_env(self) -> str:
        """Env dosyasından API anahtarını yükle"""
        try:
            if os.path.exists(self.env_file):
                with open(self.env_file, 'r') as f:
                    for line in f:
                        if line.startswith('OMDB_API_KEY='):
                            key = line.split('=', 1)[1].strip()
                            if key and key != 'your_api_key_here':
                                return key
        except:
            pass
        return ''
    
    def _get_from_user(self) -> str:
        """Kullanıcıdan API anahtarını al"""
        print("\n🔑 OMDB API Anahtarı Gerekli")
        print("=" * 40)
        print("OMDB API anahtarı bulunamadı. Lütfen API anahtarınızı girin.")
        print("📝 Ücretsiz API anahtarı için: http://www.omdbapi.com/apikey.aspx")
        print()
        
        while True:
            api_key = input("🗝️  OMDB API anahtarınızı girin: ").strip()
            
            if not api_key:
                print("❌ Lütfen geçerli bir API anahtarı girin!")
                continue
            
            # Kaydetmek isteyip istemediğini sor
            save_choice = input("\n💾 Bu API anahtarını kaydetmek istiyor musunuz? (e/h): ").lower()
            
            if save_choice in ['e', 'evet', 'y', 'yes']:
                self._save_api_key(api_key)
            
            return api_key
    
    def _save_api_key(self, api_key: str):
        """API anahtarını dosyaya kaydet"""
        try:
            # Config dosyasına kaydet
            config = {'omdb_api_key': api_key}
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            print(f"✅ API anahtarı kaydedildi: {self.config_file}")
            
        except Exception as e:
            print(f"⚠️  API anahtarı kaydedilemedi: {str(e)}")
    
    def setup_api_key(self):
        """API anahtarı kurulum wizard'ı"""
        print("🔧 OMDB API Anahtarı Kurulumu")
        print("=" * 40)
        print()
        print("1. Ücretsiz API anahtarı al: http://www.omdbapi.com/apikey.aspx")
        print("2. Email adresinizi girin ve aktivasyon linkini tıklayın")
        print("3. Aldığınız API anahtarını buraya girin")
        print()
        
        api_key = input("🗝️  OMDB API anahtarınızı girin: ").strip()
        
        if api_key:
            # Test et
            print("🔍 API anahtarı test ediliyor...")
            if self._test_api_key(api_key):
                print("✅ API anahtarı geçerli!")
                
                # Kaydet
                self._save_api_key(api_key)
                return api_key
            else:
                print("❌ API anahtarı geçersiz veya API'ye erişim sorunu!")
                return None
        
        return None
    
    def _test_api_key(self, api_key: str) -> bool:
        """API anahtarını test et"""
        try:
            import requests
            
            response = requests.get(
                "http://www.omdbapi.com/",
                params={
                    'apikey': api_key,
                    't': 'The Matrix',
                    'type': 'movie'
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('Response') == 'True'
            
        except Exception as e:
            print(f"API test hatası: {str(e)}")
        
        return False


def main():
    """API anahtarı yapılandırma test"""
    config = OMDBConfig()
    
    print("🔑 OMDB API Yapılandırma Test")
    print("=" * 40)
    
    # Mevcut API anahtarını kontrol et
    api_key = config.get_api_key()
    
    if api_key:
        print(f"✅ API anahtarı bulundu: {api_key[:8]}...")
        
        # Test et
        if config._test_api_key(api_key):
            print("✅ API anahtarı çalışıyor!")
        else:
            print("❌ API anahtarı çalışmıyor!")
    else:
        print("❌ API anahtarı bulunamadı!")
        
        # Kurulum yap
        setup_choice = input("\nAPI anahtarı kurmak istiyor musunuz? (e/h): ").lower()
        if setup_choice in ['e', 'evet', 'y', 'yes']:
            config.setup_api_key()


if __name__ == "__main__":
    main()
