#!/usr/bin/env python3
"""
Hava Durumu Asistanı Örnek Kullanım

Bu dosya, yeni entegre edilen hava durumu asistanının nasıl kullanılacağını gösterir.
"""

import asyncio
from server import (
    get_weather, 
    chat_weather_assistant, 
    weather_greeting,
    get_weather_by_coordinates,
    get_weather_by_city
)

async def main():
    """Ana örnek kullanım fonksiyonu"""
    
    print("🌤️ HAVA DURUMU ASİSTANI ÖRNEK KULLANIM")
    print("=" * 50)
    
    # 1. Karşılama mesajı
    print("\n1️⃣ Karşılama Mesajı:")
    print("-" * 25)
    greeting = await weather_greeting()
    print(greeting)
    
    # 2. Koordinat ile hava durumu (Asistan formatı)
    print("\n2️⃣ Koordinat ile Hava Durumu (Asistan Formatı):")
    print("-" * 50)
    print("📍 İstanbul koordinatları: 41.0082, 28.9784")
    weather = await get_weather(41.0082, 28.9784)
    print(weather)
    
    # 3. Chat asistanı ile farklı mesajlar
    print("\n3️⃣ Chat Asistanı Örnekleri:")
    print("-" * 30)
    
    messages = [
        "Merhaba",
        "İstanbul için hava durumu", 
        "Enlem: 39.9334, Boylam: 32.8597",  # Ankara
        "41.0082, 28.9784",  # İstanbul
        "Yardım",
        "Teşekkürler"
    ]
    
    for i, message in enumerate(messages, 1):
        print(f"\n📝 Örnek {i}: '{message}'")
        print("Asistan Yanıtı:")
        response = await chat_weather_assistant(message)
        print(response)
        print("-" * 40)
    
    # 4. Ham veri formatı (Mevcut API)
    print("\n4️⃣ Ham Veri Formatı (JSON):")
    print("-" * 30)
    print("🔧 Geliştiriciler için ham JSON verisi:")
    raw_data = await get_weather_by_coordinates(41.0082, 28.9784)
    print(raw_data[:500] + "..." if len(raw_data) > 500 else raw_data)
    
    # 5. Şehir adı ile ham veri
    print("\n5️⃣ Şehir Adı ile Ham Veri:")
    print("-" * 30)
    print("🏙️ İstanbul için ham veri:")
    city_data = await get_weather_by_city("Istanbul", "TR")
    print(city_data[:500] + "..." if len(city_data) > 500 else city_data)
    
    print("\n" + "=" * 50)
    print("✅ TÜM ÖRNEKLER TAMAMLANDI!")
    print("\n💡 İpucu: Bu fonksiyonları kendi uygulamanızda kullanabilirsiniz!")

async def interactive_demo():
    """İnteraktif demo"""
    
    print("\n🎮 İNTERAKTİF DEMO")
    print("-" * 20)
    print("Asistanla konuşmak için mesajınızı yazın (çıkmak için 'quit'):")
    
    while True:
        try:
            user_input = input("\n👤 Siz: ").strip()
            if user_input.lower() in ['quit', 'çık', 'exit']:
                print("👋 Demo tamamlandı!")
                break
            
            response = await chat_weather_assistant(user_input)
            print(f"\n🤖 Asistan: {response}")
            
        except KeyboardInterrupt:
            print("\n👋 Demo tamamlandı!")
            break
        except Exception as e:
            print(f"❌ Hata: {e}")

if __name__ == "__main__":
    # Ana örnekleri çalıştır
    asyncio.run(main())
    
    # İnteraktif demo seçeneği
    choice = input("\n🎮 İnteraktif demo yapmak ister misiniz? (e/h): ").lower()
    if choice in ['e', 'evet', 'y', 'yes']:
        asyncio.run(interactive_demo())
    
    print("\n🎉 Örnek kullanım tamamlandı!")
    print("\n📚 Daha fazla bilgi için README.md dosyasını inceleyin.")
