#!/usr/bin/env python3
"""
Weather Forecast MCP Server Test

Bu dosya, weather forecast MCP server'ının temel fonksiyonlarını test eder.
"""

import asyncio
import json
import sys
import os

# Server modülünü import et
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from server import get_weather_by_coordinates, get_weather_by_city

async def test_coordinates():
    """Koordinat tabanlı hava durumu testini çalıştır."""
    print("🌍 Koordinat tabanlı hava durumu testi...")
    
    # İstanbul koordinatları
    latitude = 41.0082
    longitude = 28.9784
    
    try:
        result = await get_weather_by_coordinates(latitude, longitude)
        data = json.loads(result)
        
        if "error" in data:
            print(f"❌ Hata: {data['error']}")
            return False
        
        print(f"✅ Başarılı! Konum: {data['konum']['şehir']}, {data['konum']['ülke']}")
        print(f"🌡️ Sıcaklık: {data['sıcaklık']['mevcut']}{data['sıcaklık']['birim']}")
        print(f"☁️ Durum: {data['hava_durumu']['açıklama']}")
        return True
        
    except Exception as e:
        print(f"❌ Test hatası: {str(e)}")
        return False

async def test_city():
    """Şehir tabanlı hava durumu testini çalıştır."""
    print("\n🏙️ Şehir tabanlı hava durumu testi...")
    
    try:
        result = await get_weather_by_city("Istanbul", "TR")
        data = json.loads(result)
        
        if "error" in data:
            print(f"❌ Hata: {data['error']}")
            return False
        
        print(f"✅ Başarılı! Konum: {data['konum']['şehir']}, {data['konum']['ülke']}")
        print(f"🌡️ Sıcaklık: {data['sıcaklık']['mevcut']}{data['sıcaklık']['birim']}")
        print(f"☁️ Durum: {data['hava_durumu']['açıklama']}")
        return True
        
    except Exception as e:
        print(f"❌ Test hatası: {str(e)}")
        return False

async def test_invalid_coordinates():
    """Geçersiz koordinat testini çalıştır."""
    print("\n⚠️ Geçersiz koordinat testi...")
    
    try:
        result = await get_weather_by_coordinates(999, 999)  # Geçersiz koordinatlar
        data = json.loads(result)
        
        if "error" in data:
            print(f"✅ Beklenen hata yakalandı: {data['error']}")
            return True
        else:
            print("❌ Hata yakalanmadı!")
            return False
        
    except Exception as e:
        print(f"❌ Test hatası: {str(e)}")
        return False

async def test_different_units():
    """Farklı ölçü birimleri testini çalıştır."""
    print("\n📏 Farklı ölçü birimleri testi...")
    
    latitude = 41.0082
    longitude = 28.9784
    
    units_list = ["metric", "imperial", "standard"]
    
    for units in units_list:
        try:
            result = await get_weather_by_coordinates(latitude, longitude, units)
            data = json.loads(result)
            
            if "error" in data:
                print(f"❌ {units} için hata: {data['error']}")
                return False
            
            temp_unit = data['sıcaklık']['birim']
            temp_value = data['sıcaklık']['mevcut']
            
            print(f"✅ {units}: {temp_value}{temp_unit}")
            
        except Exception as e:
            print(f"❌ {units} test hatası: {str(e)}")
            return False
    
    return True

async def main():
    """Ana test fonksiyonu."""
    print("🧪 Weather Forecast MCP Server Test Başlıyor...\n")
    
    tests = [
        ("Koordinat Testi", test_coordinates),
        ("Şehir Testi", test_city),
        ("Geçersiz Koordinat Testi", test_invalid_coordinates),
        ("Ölçü Birimleri Testi", test_different_units)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"🔄 {test_name} çalışıyor...")
        try:
            if await test_func():
                passed += 1
                print(f"✅ {test_name} başarılı!")
            else:
                print(f"❌ {test_name} başarısız!")
        except Exception as e:
            print(f"❌ {test_name} hata: {str(e)}")
        
        print("-" * 50)
    
    print(f"\n📊 Test Sonuçları: {passed}/{total} test başarılı")
    
    if passed == total:
        print("🎉 Tüm testler başarılı!")
        return 0
    else:
        print("⚠️ Bazı testler başarısız!")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
