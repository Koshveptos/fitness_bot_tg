import httpx
from typing import Optional
from bot.config import settings


async def get_city_temperature(city: str) -> Optional[float]:
    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": settings.OPENWEATHER_API_KEY,
        "units": "metric",
        "lang": "ru",
    }

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(url, params=params)

    if response.status_code != 200:
        return None

    data = response.json()
    return data.get("main", {}).get("temp")
