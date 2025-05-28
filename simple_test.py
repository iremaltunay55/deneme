import httpx
import asyncio

async def test_api():
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": 41.0082,
        "lon": 28.9784,
        "appid": "6b2e97b1b6559436aee37b83b71412b3",
        "units": "metric",
        "lang": "tr"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"City: {data.get('name', 'Unknown')}")
                print(f"Temperature: {data['main']['temp']}°C")
                print("✅ API test successful!")
            else:
                print(f"❌ API error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_api())
