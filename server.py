#!/usr/bin/env python3
"""
Weather Forecast MCP Server

Bu MCP server, OpenWeatherMap API kullanarak enlem ve boylam koordinatlarına göre
hava durumu bilgilerini sağlar. Ayrıca kullanıcı dostu asistan fonksiyonları içerir.
"""

import asyncio
import json
import os
import re

import httpx
from mcp.server.fastmcp import FastMCP

# OpenWeatherMap API anahtarı - çevre değişkeninden al, yoksa varsayılan kullan
API_KEY = os.getenv("OPENWEATHER_API_KEY", "6b2e97b1b6559436aee37b83b71412b3")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
DEFAULT_UNITS = os.getenv("DEFAULT_UNITS", "metric")
LANGUAGE = os.getenv("LANGUAGE", "tr")

# MCP server oluştur
mcp = FastMCP("Weather Forecast")

@mcp.tool()
async def get_weather_by_coordinates(latitude: float, longitude: float, units: str = None) -> str:
    """
    Enlem ve boylam koordinatlarına göre hava durumu bilgilerini getirir.

    Args:
        latitude: Enlem (-90 ile 90 arasında)
        longitude: Boylam (-180 ile 180 arasında)
        units: Ölçü birimi (metric, imperial, standard)

    Returns:
        JSON formatında hava durumu bilgileri
    """

    # Varsayılan units değerini ayarla
    if units is None:
        units = DEFAULT_UNITS

    # Koordinat doğrulaması
    if not (-90 <= latitude <= 90):
        return json.dumps({
            "error": "Geçersiz enlem değeri. -90 ile 90 arasında olmalıdır.",
            "latitude": latitude
        }, ensure_ascii=False, indent=2)

    if not (-180 <= longitude <= 180):
        return json.dumps({
            "error": "Geçersiz boylam değeri. -180 ile 180 arasında olmalıdır.",
            "longitude": longitude
        }, ensure_ascii=False, indent=2)

    # API parametreleri
    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": API_KEY,
        "units": units,
        "lang": LANGUAGE  # Dil ayarı
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(BASE_URL, params=params)
            response.raise_for_status()

            data = response.json()

            # Hava durumu bilgilerini düzenle
            weather_info = {
                "konum": {
                    "enlem": data["coord"]["lat"],
                    "boylam": data["coord"]["lon"],
                    "şehir": data.get("name", "Bilinmiyor"),
                    "ülke": data["sys"].get("country", "Bilinmiyor")
                },
                "hava_durumu": {
                    "ana_durum": data["weather"][0]["main"],
                    "açıklama": data["weather"][0]["description"],
                    "ikon": data["weather"][0]["icon"]
                },
                "sıcaklık": {
                    "mevcut": data["main"]["temp"],
                    "hissedilen": data["main"]["feels_like"],
                    "minimum": data["main"]["temp_min"],
                    "maksimum": data["main"]["temp_max"],
                    "birim": "°C" if units == "metric" else ("°F" if units == "imperial" else "K")
                },
                "atmosfer": {
                    "basınç": data["main"]["pressure"],
                    "nem": data["main"]["humidity"],
                    "görüş_mesafesi": data.get("visibility", "Bilinmiyor")
                },
                "rüzgar": {
                    "hız": data["wind"].get("speed", 0),
                    "yön": data["wind"].get("deg", 0),
                    "birim": "m/s" if units != "imperial" else "mph"
                },
                "bulutluluk": {
                    "yüzde": data["clouds"]["all"]
                },
                "güneş": {
                    "doğuş": data["sys"]["sunrise"],
                    "batış": data["sys"]["sunset"]
                },
                "zaman": {
                    "veri_zamanı": data["dt"],
                    "saat_dilimi": data["timezone"]
                }
            }

            # Yağış bilgisi varsa ekle
            if "rain" in data:
                weather_info["yağış"] = {
                    "son_1_saat": data["rain"].get("1h", 0),
                    "birim": "mm"
                }

            if "snow" in data:
                weather_info["kar"] = {
                    "son_1_saat": data["snow"].get("1h", 0),
                    "birim": "mm"
                }

            return json.dumps(weather_info, ensure_ascii=False, indent=2)

    except httpx.HTTPStatusError as e:
        error_msg = {
            "error": f"API hatası: {e.response.status_code}",
            "mesaj": "Hava durumu bilgisi alınamadı. Koordinatları kontrol edin.",
            "latitude": latitude,
            "longitude": longitude
        }
        return json.dumps(error_msg, ensure_ascii=False, indent=2)

    except Exception as e:
        error_msg = {
            "error": f"Beklenmeyen hata: {str(e)}",
            "latitude": latitude,
            "longitude": longitude
        }
        return json.dumps(error_msg, ensure_ascii=False, indent=2)

@mcp.tool()
async def get_weather_by_city(city_name: str, country_code: str = "", units: str = None) -> str:
    """
    Şehir adına göre hava durumu bilgilerini getirir.

    Args:
        city_name: Şehir adı
        country_code: Ülke kodu (opsiyonel, örn: TR, US)
        units: Ölçü birimi (metric, imperial, standard)

    Returns:
        JSON formatında hava durumu bilgileri
    """

    # Varsayılan units değerini ayarla
    if units is None:
        units = DEFAULT_UNITS

    # Şehir adı parametresi
    if country_code:
        q = f"{city_name},{country_code}"
    else:
        q = city_name

    params = {
        "q": q,
        "appid": API_KEY,
        "units": units,
        "lang": LANGUAGE
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(BASE_URL, params=params)
            response.raise_for_status()

            data = response.json()

            # Koordinatları al ve get_weather_by_coordinates fonksiyonunu kullan
            lat = data["coord"]["lat"]
            lon = data["coord"]["lon"]

            return await get_weather_by_coordinates(lat, lon, units)

    except httpx.HTTPStatusError as e:
        error_msg = {
            "error": f"API hatası: {e.response.status_code}",
            "mesaj": "Şehir bulunamadı. Şehir adını kontrol edin.",
            "şehir": city_name,
            "ülke_kodu": country_code
        }
        return json.dumps(error_msg, ensure_ascii=False, indent=2)

    except Exception as e:
        error_msg = {
            "error": f"Beklenmeyen hata: {str(e)}",
            "şehir": city_name,
            "ülke_kodu": country_code
        }
        return json.dumps(error_msg, ensure_ascii=False, indent=2)

@mcp.resource("weather://coordinates/{latitude}/{longitude}")
def get_weather_resource(latitude: str, longitude: str) -> str:
    """
    Koordinatlara göre hava durumu kaynağı.

    Args:
        latitude: Enlem değeri (string)
        longitude: Boylam değeri (string)

    Returns:
        Hava durumu bilgileri
    """
    try:
        lat = float(latitude)
        lon = float(longitude)

        # Senkron çağrı için asyncio kullan
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(get_weather_by_coordinates(lat, lon))
        loop.close()

        return result
    except ValueError:
        error_msg = {
            "error": "Geçersiz koordinat formatı",
            "latitude": latitude,
            "longitude": longitude
        }
        return json.dumps(error_msg, ensure_ascii=False, indent=2)

@mcp.prompt()
def weather_analysis_prompt(location: str) -> str:
    """
    Hava durumu analizi için prompt şablonu.

    Args:
        location: Konum bilgisi

    Returns:
        Analiz prompt'u
    """
    return f"""
{location} konumu için hava durumu analizi yapın. Aşağıdaki konuları ele alın:

1. Mevcut hava koşulları
2. Sıcaklık durumu ve hissedilen sıcaklık
3. Rüzgar ve nem oranı
4. Görüş mesafesi
5. Genel hava durumu değerlendirmesi
6. Günlük aktiviteler için öneriler

Analizi Türkçe olarak yapın ve kullanıcı dostu bir dille sunun.
"""

# ============================================================================
# HAVA DURUMU ASİSTANI FONKSİYONLARI
# ============================================================================

class WeatherAssistant:
    """Kullanıcı dostu hava durumu asistanı sınıfı"""

    def __init__(self):
        self.conversation_state = {}

    def format_weather_response(self, weather_data: dict) -> str:
        """Hava durumu verisini kullanıcı dostu formatta sunar"""
        try:
            data = json.loads(weather_data) if isinstance(weather_data, str) else weather_data

            if "error" in data:
                return f"😔 Üzgünüm, bir hata oluştu: {data['error']}"

            # Temel bilgileri çıkar
            konum = data.get("konum", {})
            hava = data.get("hava_durumu", {})
            sicaklik = data.get("sıcaklık", {})
            atmosfer = data.get("atmosfer", {})
            ruzgar = data.get("rüzgar", {})

            # Dostane yanıt oluştur
            response = f"🌍 **{konum.get('şehir', 'Bilinmeyen konum')}, {konum.get('ülke', '')}** için hava durumu:\n\n"

            # Ana hava durumu
            response += f"🌤️ **Genel Durum:** {hava.get('açıklama', 'Bilinmiyor').title()}\n"

            # Sıcaklık bilgileri
            mevcut_sicaklik = sicaklik.get('mevcut', 'N/A')
            hissedilen = sicaklik.get('hissedilen', 'N/A')
            birim = sicaklik.get('birim', '°C')

            response += f"🌡️ **Sıcaklık:** {mevcut_sicaklik}{birim}"
            if hissedilen != 'N/A':
                response += f" (Hissedilen: {hissedilen}{birim})"
            response += "\n"

            # Min-Max sıcaklık
            min_temp = sicaklik.get('minimum', 'N/A')
            max_temp = sicaklik.get('maksimum', 'N/A')
            if min_temp != 'N/A' and max_temp != 'N/A':
                response += f"📊 **Günlük Aralık:** {min_temp}{birim} - {max_temp}{birim}\n"

            # Nem ve basınç
            nem = atmosfer.get('nem', 'N/A')
            basinc = atmosfer.get('basınç', 'N/A')
            response += f"💧 **Nem:** %{nem}\n"
            response += f"🔽 **Basınç:** {basinc} hPa\n"

            # Rüzgar
            ruzgar_hiz = ruzgar.get('hız', 0)
            ruzgar_birim = ruzgar.get('birim', 'm/s')
            response += f"💨 **Rüzgar:** {ruzgar_hiz} {ruzgar_birim}\n"

            # Yağış bilgisi varsa
            if "yağış" in data:
                yagis = data["yağış"].get("son_1_saat", 0)
                response += f"🌧️ **Yağış (Son 1 saat):** {yagis} mm\n"

            if "kar" in data:
                kar = data["kar"].get("son_1_saat", 0)
                response += f"❄️ **Kar (Son 1 saat):** {kar} mm\n"

            # Tavsiye ekle
            response += "\n" + self._get_weather_advice(data)

            return response

        except Exception as e:
            return f"😔 Hava durumu bilgilerini işlerken bir hata oluştu: {str(e)}"

    def _get_weather_advice(self, data: dict) -> str:
        """Hava durumuna göre tavsiye verir"""
        try:
            sicaklik = data.get("sıcaklık", {}).get("mevcut", 20)
            nem = data.get("atmosfer", {}).get("nem", 50)
            ruzgar = data.get("rüzgar", {}).get("hız", 0)
            hava_durumu = data.get("hava_durumu", {}).get("ana_durum", "").lower()

            advice = "💡 **Tavsiyelerim:**\n"

            # Sıcaklık tavsiyeleri
            if sicaklik < 0:
                advice += "🧥 Çok soğuk! Kalın kıyafetler giyin ve sıcak tutun.\n"
            elif sicaklik < 10:
                advice += "🧥 Soğuk hava, mont almayı unutmayın!\n"
            elif sicaklik < 20:
                advice += "👕 Serin hava, hafif bir ceket yeterli.\n"
            elif sicaklik < 30:
                advice += "👕 Güzel hava! Rahat kıyafetler tercih edin.\n"
            else:
                advice += "🌞 Çok sıcak! Bol su için ve gölgede kalın.\n"

            # Hava durumu tavsiyeleri
            if "rain" in hava_durumu or "drizzle" in hava_durumu:
                advice += "☂️ Yağmur var, şemsiye almayı unutmayın!\n"
            elif "snow" in hava_durumu:
                advice += "❄️ Kar yağıyor, dikkatli yürüyün!\n"
            elif "clear" in hava_durumu:
                advice += "☀️ Açık hava! Dışarıda vakit geçirmek için harika!\n"

            # Rüzgar tavsiyeleri
            if ruzgar > 10:
                advice += "💨 Rüzgarlı hava, saçınızı bağlamayı unutmayın!\n"

            # Nem tavsiyeleri
            if nem > 80:
                advice += "💧 Yüksek nem, serinletici içecekler tercih edin!\n"

            return advice

        except:
            return "💡 **Tavsiye:** Hava durumuna uygun kıyafet seçin ve güzel bir gün geçirin! 😊"

# Global asistan instance
weather_assistant = WeatherAssistant()

# ============================================================================
# ASİSTAN MCP ARAÇLARI
# ============================================================================

@mcp.tool()
async def get_weather(latitude: float, longitude: float) -> str:
    """
    Kullanıcı dostu hava durumu asistanı - koordinatlara göre hava durumu getirir.

    Bu araç, kullanıcıyla dostane iletişim kurar ve hava durumu bilgilerini
    anlaşılır şekilde sunar.

    Args:
        latitude: Enlem (-90 ile 90 arasında)
        longitude: Boylam (-180 ile 180 arasında)

    Returns:
        Kullanıcı dostu formatta hava durumu bilgileri
    """
    # Mevcut hava durumu verisini al
    weather_data = await get_weather_by_coordinates(latitude, longitude)

    # Asistan formatında sun
    return weather_assistant.format_weather_response(weather_data)

@mcp.tool()
async def chat_weather_assistant(message: str) -> str:
    """
    Hava durumu asistanı ile sohbet et.

    Bu araç kullanıcının mesajlarını analiz eder ve uygun yanıtlar verir.
    Koordinat bilgilerini toplar ve hava durumu sorgular.

    Args:
        message: Kullanıcının mesajı

    Returns:
        Asistan yanıtı
    """
    message = message.lower().strip()

    # Koordinat arama regex'leri
    coord_patterns = [
        r'enlem[:\s]*(-?\d+\.?\d*)[,\s]*boylam[:\s]*(-?\d+\.?\d*)',
        r'lat[:\s]*(-?\d+\.?\d*)[,\s]*lon[:\s]*(-?\d+\.?\d*)',
        r'latitude[:\s]*(-?\d+\.?\d*)[,\s]*longitude[:\s]*(-?\d+\.?\d*)',
        r'(-?\d+\.?\d*)[,\s]+(-?\d+\.?\d*)'  # Sadece sayılar
    ]

    # Koordinat arama
    for pattern in coord_patterns:
        match = re.search(pattern, message)
        if match:
            try:
                lat = float(match.group(1))
                lon = float(match.group(2))

                # Koordinat doğrulaması
                if -90 <= lat <= 90 and -180 <= lon <= 180:
                    # Hava durumu bilgisini al ve formatla
                    weather_data = await get_weather_by_coordinates(lat, lon)
                    formatted_response = weather_assistant.format_weather_response(weather_data)

                    return f"Harika! Koordinatlarınızı aldım. İşte hava durumu bilginiz:\n\n{formatted_response}"
                else:
                    return "😅 Koordinatlar geçerli aralıkta değil. Enlem -90 ile 90, boylam -180 ile 180 arasında olmalı."
            except ValueError:
                continue

    # Şehir adı arama
    city_patterns = [
        r'(?:şehir|city|konum|location)[:\s]*([a-zA-ZğüşıöçĞÜŞİÖÇ]+)',
        r'([a-zA-ZğüşıöçĞÜŞİÖÇ]+)(?:\s+için\s+hava|\s+hava)',
        r'([a-zA-ZğüşıöçĞÜŞİÖÇ]+)(?:\s+için)',
    ]

    for pattern in city_patterns:
        match = re.search(pattern, message)
        if match:
            city_name = match.group(1).strip()
            if len(city_name) > 2:  # En az 3 karakter
                try:
                    weather_data = await get_weather_by_city(city_name)
                    formatted_response = weather_assistant.format_weather_response(weather_data)
                    return f"Buldum! {city_name.title()} için hava durumu:\n\n{formatted_response}"
                except:
                    return f"😔 Üzgünüm, '{city_name}' şehrini bulamadım. Koordinatlarınızı verebilir misiniz?"

    # Genel yanıtlar
    if any(word in message for word in ['merhaba', 'selam', 'hello', 'hi']):
        return """🌤️ Merhaba! Ben hava durumu asistanınızım! 😊

Size hava durumu bilgisi verebilmek için şunlardan birini paylaşabilirsiniz:

📍 **Koordinatlar:**
   • Enlem: 41.0082, Boylam: 28.9784
   • Veya: 41.0082, 28.9784

🏙️ **Şehir adı:**
   • İstanbul için hava durumu
   • Ankara hava durumu

Hangi konum için hava durumu öğrenmek istiyorsunuz? 🌍"""

    elif any(word in message for word in ['teşekkür', 'sağol', 'thanks', 'thank you']):
        return "😊 Rica ederim! Başka bir konumun hava durumunu öğrenmek isterseniz, koordinatlarını veya şehir adını söylemeniz yeterli! 🌤️"

    elif any(word in message for word in ['yardım', 'help', 'nasıl']):
        return """🆘 **Nasıl kullanılır:**

1️⃣ **Koordinat ile:**
   • "Enlem: 41.0082, Boylam: 28.9784"
   • "41.0082, 28.9784"

2️⃣ **Şehir adı ile:**
   • "İstanbul için hava durumu"
   • "Ankara hava"

3️⃣ **Doğal dil ile:**
   • "İstanbul'da hava nasıl?"
   • "Ankara'nın hava durumu nedir?"

Koordinatlarınızı bilmiyorsanız, şehir adınızı söylemeniz yeterli! 😊"""

    else:
        return """🤔 Anlayamadım. Size yardımcı olabilmek için lütfen:

📍 **Koordinatlarınızı** (enlem, boylam) veya
🏙️ **Şehir adınızı** paylaşın

Örnek:
• "Enlem: 41.0082, Boylam: 28.9784"
• "İstanbul için hava durumu"
• "41.0082, 28.9784"

Nasıl yardımcı olabilirim? 😊"""

@mcp.tool()
async def weather_greeting() -> str:
    """
    Hava durumu asistanının karşılama mesajı.

    Returns:
        Dostane karşılama mesajı
    """
    return """🌤️ **Merhaba! Hava Durumu Asistanınızım!** 😊

Size güncel hava durumu bilgileri sağlamak için buradayım!

**Nasıl kullanabilirsiniz:**

📍 **Koordinat ile:**
   • Enlem: 41.0082, Boylam: 28.9784
   • Veya kısaca: 41.0082, 28.9784

🏙️ **Şehir adı ile:**
   • İstanbul için hava durumu
   • Ankara hava durumu

🗣️ **Doğal konuşma ile:**
   • "İstanbul'da hava nasıl?"
   • "Bugün Ankara'da yağmur var mı?"

Hangi konum için hava durumu öğrenmek istiyorsunuz? 🌍✨"""

if __name__ == "__main__":
    # Server'ı çalıştır
    mcp.run()
