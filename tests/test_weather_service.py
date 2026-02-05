import pytest
import httpx

from bot.services.weather_service import (
    get_current_temperature,
    CityNotFoundError,
    WeatherServiceError,
)


@pytest.mark.asyncio
async def test_get_current_temperature_success(monkeypatch):
    monkeypatch.setenv("OPENWEATHER_API_KEY", "fake-key")

    async def mock_get(self, url, params):
        class MockResponse:
            status_code = 200

            def json(self):
                return {"main": {"temp": 21.5}}

        return MockResponse()

    monkeypatch.setattr(httpx.AsyncClient, "get", mock_get)

    temp = await get_current_temperature("Moscow")
    assert temp == 21.5


@pytest.mark.asyncio
async def test_get_current_temperature_city_not_found(monkeypatch):
    monkeypatch.setenv("OPENWEATHER_API_KEY", "fake-key")

    async def mock_get(self, url, params):
        class MockResponse:
            status_code = 404

            def json(self):
                return {}

        return MockResponse()

    monkeypatch.setattr(httpx.AsyncClient, "get", mock_get)

    with pytest.raises(CityNotFoundError):
        await get_current_temperature("NoCity")


@pytest.mark.asyncio
async def test_weather_api_key_missing(monkeypatch):
    monkeypatch.delenv("OPENWEATHER_API_KEY", raising=False)

    with pytest.raises(WeatherServiceError):
        await get_current_temperature("Moscow")
