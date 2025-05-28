#!/usr/bin/env python3
"""
Weather Forecast MCP Server

Bu MCP server, OpenWeatherMap API kullanarak enlem ve boylam koordinatlarına göre
hava durumu bilgilerini sağlar.
"""

import asyncio
import json
import os


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

if __name__ == "__main__":
    # Server'ı çalıştır
    mcp.run()
