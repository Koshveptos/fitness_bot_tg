import httpx
from typing import Optional


async def get_food_calories_per_100g(product_name: str) -> Optional[int]:
    url = "https://world.openfoodfacts.org/cgi/search.pl"
    params = {
        "action": "process",
        "search_terms": product_name,
        "json": 1,
        "page_size": 1,
    }

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
    except httpx.HTTPError:
        return None

    data = response.json()
    products = data.get("products") or []

    if not products:
        return None

    nutriments = products[0].get("nutriments") or {}

    calories = nutriments.get("energy-kcal_100g") or nutriments.get("energy_100g")

    if calories is None:
        return None

    try:
        return int(float(calories))
    except (ValueError, TypeError):
        return None
