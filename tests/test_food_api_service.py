import pytest
import httpx

from bot.services.food_api_service import get_food_info, FoodInfo


@pytest.mark.asyncio
async def test_get_food_info_success(monkeypatch):
    async def mock_get(self, url, params):
        class MockResponse:
            status_code = 200

            def json(self):
                return {
                    "products": [
                        {
                            "product_name": "Banana",
                            "nutriments": {"energy-kcal_100g": 89},
                        }
                    ]
                }

        return MockResponse()

    monkeypatch.setattr(httpx.AsyncClient, "get", mock_get)

    food = await get_food_info("banana")

    assert isinstance(food, FoodInfo)
    assert food.name == "Banana"
    assert food.calories_per_100g == 89


@pytest.mark.asyncio
async def test_get_food_info_not_found(monkeypatch):
    async def mock_get(self, url, params):
        class MockResponse:
            status_code = 200

            def json(self):
                return {"products": []}

        return MockResponse()

    monkeypatch.setattr(httpx.AsyncClient, "get", mock_get)

    food = await get_food_info("unknown-food")
    assert food is None


@pytest.mark.asyncio
async def test_get_food_info_without_calories(monkeypatch):
    async def mock_get(self, url, params):
        class MockResponse:
            status_code = 200

            def json(self):
                return {
                    "products": [
                        {
                            "product_name": "Mystery food",
                            "nutriments": {},
                        }
                    ]
                }

        return MockResponse()

    monkeypatch.setattr(httpx.AsyncClient, "get", mock_get)

    food = await get_food_info("mystery")
    assert food is None
