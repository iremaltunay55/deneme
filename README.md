# Weather Forecast MCP Server

[![smithery badge](https://smithery.ai/badge/@iremaltunay55/deneme1)](https://smithery.ai/server/@iremaltunay55/deneme1)

Bu proje, OpenWeatherMap API kullanarak hava durumu bilgilerini sağlayan bir Model Context Protocol (MCP) server'ıdır. Enlem ve boylam koordinatları veya şehir adı ile hava durumu bilgilerini alabilirsiniz.

## Özellikler

- 🌍 Enlem/boylam koordinatlarına göre hava durumu
- 🏙️ Şehir adına göre hava durumu  
- 🌡️ Detaylı sıcaklık bilgileri (mevcut, hissedilen, min/max)
- 💨 Rüzgar hızı ve yönü
- 💧 Nem oranı ve atmosfer basıncı
- ☁️ Bulutluluk yüzdesi
- 🌅 Güneş doğuş/batış saatleri
- 🌧️ Yağış bilgileri (varsa)
- 🇹🇷 Türkçe açıklamalar

## Kurulum

### Gereksinimler

- Python 3.8+
- OpenWeatherMap API anahtarı

### Yerel Kurulum

1. Projeyi klonlayın:
```bash
git clone <repository-url>
cd weather-forecast-mcp
```

2. Bağımlılıkları yükleyin:
```bash
pip install -r requirements.txt
```

3. Server'ı çalıştırın:
```bash
python server.py
```

### Smithery Deployment

Bu proje Smithery platformunda deploy edilmek üzere tasarlanmıştır.

1. Projeyi GitHub'a yükleyin
2. Smithery'de yeni bir MCP server oluşturun
3. GitHub repository'nizi bağlayın
4. `smithery.yaml` dosyası otomatik olarak tanınacaktır

## Kullanım

### Tools (Araçlar)

#### 1. `get_weather_by_coordinates`
Enlem ve boylam koordinatlarına göre hava durumu bilgilerini getirir.

**Parametreler:**
- `latitude` (float): Enlem (-90 ile 90 arasında)
- `longitude` (float): Boylam (-180 ile 180 arasında)
- `units` (string, opsiyonel): Ölçü birimi ("metric", "imperial", "standard")

**Örnek:**
```json
{
  "latitude": 41.0082,
  "longitude": 28.9784,
  "units": "metric"
}
```

#### 2. `get_weather_by_city`
Şehir adına göre hava durumu bilgilerini getirir.

**Parametreler:**
- `city_name` (string): Şehir adı
- `country_code` (string, opsiyonel): Ülke kodu (örn: "TR", "US")
- `units` (string, opsiyonel): Ölçü birimi

**Örnek:**
```json
{
  "city_name": "Istanbul",
  "country_code": "TR",
  "units": "metric"
}
```

### Resources (Kaynaklar)

#### `weather://coordinates/{latitude}/{longitude}`
Koordinatlara göre hava durumu kaynağı.

**Örnek:**
```
weather://coordinates/41.0082/28.9784
```

### Prompts (Şablonlar)

#### `weather_analysis_prompt`
Hava durumu analizi için prompt şablonu.

**Parametre:**
- `location` (string): Konum bilgisi

## API Yanıt Formatı

```json
{
  "konum": {
    "enlem": 41.0082,
    "boylam": 28.9784,
    "şehir": "Istanbul",
    "ülke": "TR"
  },
  "hava_durumu": {
    "ana_durum": "Clear",
    "açıklama": "açık",
    "ikon": "01d"
  },
  "sıcaklık": {
    "mevcut": 22.5,
    "hissedilen": 23.1,
    "minimum": 20.0,
    "maksimum": 25.0,
    "birim": "°C"
  },
  "atmosfer": {
    "basınç": 1013,
    "nem": 65,
    "görüş_mesafesi": 10000
  },
  "rüzgar": {
    "hız": 3.5,
    "yön": 180,
    "birim": "m/s"
  },
  "bulutluluk": {
    "yüzde": 10
  },
  "güneş": {
    "doğuş": 1640234567,
    "batış": 1640267890
  }
}
```

## Konfigürasyon

### Smithery Konfigürasyonu

`smithery.yaml` dosyasında aşağıdaki parametreleri ayarlayabilirsiniz:

- `api_key`: OpenWeatherMap API anahtarınız
- `units`: Varsayılan ölçü birimi (metric/imperial/standard)
- `language`: Dil kodu (tr, en, vb.)

### Çevre Değişkenleri

- `OPENWEATHER_API_KEY`: OpenWeatherMap API anahtarı
- `DEFAULT_UNITS`: Varsayılan ölçü birimi
- `LANGUAGE`: Dil kodu

## Hata Yönetimi

Server, aşağıdaki durumlarda uygun hata mesajları döndürür:

- Geçersiz koordinatlar
- API erişim hataları
- Şehir bulunamadığında
- Ağ bağlantı sorunları

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## Destek

Herhangi bir sorun yaşarsanız, lütfen GitHub Issues bölümünde bir konu açın.
