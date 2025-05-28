#!/usr/bin/env python3
"""
Hava Durumu Asistanı Test Dosyası

Bu dosya, yeni entegre edilen hava durumu asistanının fonksiyonlarını test eder.
"""

import asyncio
import json
from server import (
    get_weather, 
    chat_weather_assistant, 
    weather_greeting,
    get_weather_by_coordinates,
    weather_assistant
)

async def test_assistant():
    """Asistan fonksiyonlarını test et"""
    
    print("🧪 HAVA DURUMU ASİSTANI TEST BAŞLADI\n")
    print("=" * 60)
    
    # 1. Karşılama mesajı testi
    print("\n1️⃣ KARŞILAMA MESAJI TESTİ:")
    print("-" * 30)
    greeting = await weather_greeting()
    print(greeting)
    
    # 2. Chat asistanı testleri
    print("\n2️⃣ CHAT ASİSTANI TESTLERİ:")
    print("-" * 30)
    
    test_messages = [
        "Merhaba",
        "Yardım",
        "İstanbul için hava durumu",
        "Enlem: 41.0082, Boylam: 28.9784",
        "39.9334, 32.8597",  # Ankara koordinatları
        "Teşekkürler"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n📝 Test {i}: '{message}'")
        print("Yanıt:")
        response = await chat_weather_assistant(message)
        print(response)
        print("-" * 50)
    
    # 3. Direkt hava durumu testi
    print("\n3️⃣ DİREKT HAVA DURUMU TESTİ:")
    print("-" * 30)
    print("📍 İstanbul koordinatları (41.0082, 28.9784) için hava durumu:")
    weather_response = await get_weather(41.0082, 28.9784)
    print(weather_response)
    
    # 4. Ham veri formatı testi
    print("\n4️⃣ HAM VERİ FORMAT TESTİ:")
    print("-" * 30)
    print("🔧 Ham API verisinin asistan formatına dönüştürülmesi:")
    raw_data = await get_weather_by_coordinates(41.0082, 28.9784)
    formatted_data = weather_assistant.format_weather_response(raw_data)
    print(formatted_data)
    
    print("\n" + "=" * 60)
    print("✅ TÜM TESTLER TAMAMLANDI!")

async def test_error_handling():
    """Hata yönetimi testleri"""
    
    print("\n🚨 HATA YÖNETİMİ TESTLERİ:")
    print("-" * 30)
    
    # Geçersiz koordinatlar
    print("\n❌ Geçersiz koordinat testi:")
    try:
        response = await get_weather(999, 999)  # Geçersiz koordinatlar
        print(response)
    except Exception as e:
        print(f"Hata yakalandı: {e}")
    
    # Geçersiz şehir adı
    print("\n❌ Geçersiz şehir testi:")
    response = await chat_weather_assistant("XYZ123 şehri için hava durumu")
    print(response)

def interactive_test():
    """İnteraktif test modu"""
    
    print("\n🎮 İNTERAKTİF TEST MODU")
    print("-" * 30)
    print("Asistanla konuşmak için mesajınızı yazın (çıkmak için 'quit'):")
    
    async def chat_loop():
        while True:
            try:
                user_input = input("\n👤 Siz: ").strip()
                if user_input.lower() in ['quit', 'çık', 'exit']:
                    print("👋 Görüşürüz!")
                    break
                
                response = await chat_weather_assistant(user_input)
                print(f"\n🤖 Asistan: {response}")
                
            except KeyboardInterrupt:
                print("\n👋 Görüşürüz!")
                break
            except Exception as e:
                print(f"❌ Hata: {e}")
    
    asyncio.run(chat_loop())

if __name__ == "__main__":
    print("🌤️ HAVA DURUMU ASİSTANI TEST SÜİTİ")
    print("=" * 60)
    
    # Ana testleri çalıştır
    asyncio.run(test_assistant())
    
    # Hata testleri
    asyncio.run(test_error_handling())
    
    # İnteraktif mod seçeneği
    choice = input("\n🎮 İnteraktif test modunu başlatmak ister misiniz? (e/h): ").lower()
    if choice in ['e', 'evet', 'y', 'yes']:
        interactive_test()
    
    print("\n🎉 Test süreci tamamlandı!")
