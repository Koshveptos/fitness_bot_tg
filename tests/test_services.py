import pytest
from bot.services.food_service import add_food
from bot.services.water_service import add_water
from bot.services.workout_service import add_workout


@pytest.mark.asyncio
async def test_add_food_service(async_session, test_user):
    calories = await add_food(async_session, test_user.telegram_id, "авокадо", 160)
    assert calories == 160


@pytest.mark.asyncio
async def test_add_water_service(async_session, test_user):
    water = await add_water(async_session, test_user.telegram_id, 750)
    assert water == 750


@pytest.mark.asyncio
async def test_add_workout_service(async_session, test_user):
    burned = await add_workout(
        async_session, test_user.telegram_id, "велосипед", 60, 550
    )
    assert burned == 550
