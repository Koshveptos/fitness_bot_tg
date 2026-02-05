import pytest
from bot.services.summary_service import get_today_summary
from bot.services.food_service import add_food
from bot.services.water_service import add_water
from bot.services.workout_service import add_workout


@pytest.mark.asyncio
async def test_get_today_summary_empty(async_session):
    summary = await get_today_summary(async_session, telegram_id=111111111)
    assert summary["water_ml"] == 0
    assert summary["food_calories"] == 0


@pytest.mark.asyncio
async def test_get_today_summary_with_data(async_session, test_user):
    await add_water(async_session, test_user.telegram_id, 1200)
    await add_food(async_session, test_user.telegram_id, "рис", 400)
    await add_workout(async_session, test_user.telegram_id, "бег", 40, 450)

    summary = await get_today_summary(async_session, test_user.telegram_id)
    assert summary["water_ml"] == 1200
    assert summary["food_calories"] == 400
    assert summary["burned_calories"] == 450
    assert summary["balance_calories"] == -50
