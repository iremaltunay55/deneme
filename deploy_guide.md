# Weather Forecast MCP - Deployment Guide

Bu rehber, Weather Forecast MCP projenizi Smithery platformunda nasıl deploy edeceğinizi açıklar.

## 📋 Ön Gereksinimler

1. **GitHub Hesabı**: Projeyi GitHub'da barındırmak için
2. **Smithery Hesabı**: MCP server'ı deploy etmek için
3. **OpenWeatherMap API Key**: Hava durumu verilerine erişim için (mevcut: `6b2e97b1b6559436aee37b83b71412b3`)

## 🚀 Deployment Adımları

### 1. GitHub'a Yükleme

1. **GitHub'da yeni repository oluşturun:**
   - Repository adı: `weather-forecast-mcp`
   - Açıklama: `Weather forecast MCP server using OpenWeatherMap API`
   - Public olarak ayarlayın

2. **Projeyi GitHub'a push edin:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Weather Forecast MCP Server"
   git branch -M main
   git remote add origin https://github.com/KULLANICI_ADINIZ/weather-forecast-mcp.git
   git push -u origin main
   ```

### 2. Smithery'de Deployment

1. **Smithery'ye giriş yapın:**
   - [Smithery](https://smithery.ai) sitesine gidin
   - Hesabınızla giriş yapın

2. **Yeni MCP Server oluşturun:**
   - "New MCP Server" butonuna tıklayın
   - Server adı: `Weather Forecast`
   - Açıklama: `Get weather information by coordinates or city name`

3. **GitHub Repository'yi bağlayın:**
   - Source olarak "GitHub" seçin
   - Repository URL'nizi girin: `https://github.com/KULLANICI_ADINIZ/weather-forecast-mcp`
   - Branch: `main`

4. **Konfigürasyon:**
   - Smithery otomatik olarak `smithery.yaml` dosyasını tanıyacak
   - Gerekirse API key'i güncelleyin

5. **Deploy edin:**
   - "Deploy" butonuna tıklayın
   - Deployment işleminin tamamlanmasını bekleyin

## ⚙️ Konfigürasyon Seçenekleri

### Smithery.yaml Parametreleri

```yaml
api_key: "6b2e97b1b6559436aee37b83b71412b3"  # OpenWeatherMap API key
units: "metric"                                # Ölçü birimi (metric/imperial/standard)
language: "tr"                                 # Dil kodu
```

### Çevre Değişkenleri

Smithery'de aşağıdaki çevre değişkenlerini ayarlayabilirsiniz:

- `OPENWEATHER_API_KEY`: OpenWeatherMap API anahtarı
- `DEFAULT_UNITS`: Varsayılan ölçü birimi
- `LANGUAGE`: Dil kodu

## 🧪 Test Etme

Deploy edildikten sonra MCP server'ınızı test etmek için:

### 1. Claude Desktop ile Test

1. Claude Desktop'ta MCP server'ınızı ekleyin
2. Aşağıdaki komutları deneyin:
   - "İstanbul'un hava durumunu göster"
   - "41.0082, 28.9784 koordinatlarındaki hava durumu nedir?"

### 2. MCP Inspector ile Test

```bash
mcp dev https://smithery.ai/YOUR_USERNAME/weather-forecast
```

## 📊 Kullanım Örnekleri

### Koordinat ile Hava Durumu

```json
{
  "tool": "get_weather_by_coordinates",
  "parameters": {
    "latitude": 41.0082,
    "longitude": 28.9784,
    "units": "metric"
  }
}
```

### Şehir ile Hava Durumu

```json
{
  "tool": "get_weather_by_city",
  "parameters": {
    "city_name": "Istanbul",
    "country_code": "TR",
    "units": "metric"
  }
}
```

### Resource Kullanımı

```
weather://coordinates/41.0082/28.9784
```

## 🔧 Sorun Giderme

### Yaygın Sorunlar

1. **API Key Hatası:**
   - OpenWeatherMap API key'inizin geçerli olduğundan emin olun
   - API key'in doğru şekilde konfigüre edildiğini kontrol edin

2. **Koordinat Hataları:**
   - Enlem: -90 ile 90 arasında olmalı
   - Boylam: -180 ile 180 arasında olmalı

3. **Şehir Bulunamadı:**
   - Şehir adının doğru yazıldığından emin olun
   - Ülke kodunu eklemeyi deneyin (örn: "Istanbul, TR")

### Log Kontrolü

Smithery dashboard'unda server loglarını kontrol edebilirsiniz:
- Deployment logs
- Runtime logs
- Error logs

## 📈 Monitoring

### Metrics

Smithery'de aşağıdaki metrikleri izleyebilirsiniz:
- Request count
- Response time
- Error rate
- API usage

### Alerts

Önemli olaylar için alert kurabilirsiniz:
- High error rate
- API quota exceeded
- Server downtime

## 🔄 Güncelleme

Projenizi güncellemek için:

1. GitHub'da değişiklikleri push edin
2. Smithery otomatik olarak yeni deployment başlatacak
3. Deployment tamamlandığında yeni versiyon aktif olacak

## 📞 Destek

Sorun yaşarsanız:
- GitHub Issues bölümünde konu açın
- Smithery support ile iletişime geçin
- OpenWeatherMap API dokümantasyonunu kontrol edin

## 🎉 Tebrikler!

Weather Forecast MCP server'ınız artık canlıda! Artık Claude ve diğer MCP uyumlu uygulamalarda hava durumu bilgilerini kullanabilirsiniz.
