from datetime import date
import pytest
from bot.database.crud.food import (
    create_food_log,
    get_food_calories_today,
    get_food_logs_by_date,
)


@pytest.mark.asyncio
async def test_create_food_log(async_session, test_user):
    await create_food_log(async_session, test_user.id, "яблоко", 80)
    await async_session.commit()
    calories = await get_food_calories_today(async_session, test_user.id)
    assert calories == 80


@pytest.mark.asyncio
async def test_multiple_food_logs_sum(async_session, test_user):
    await create_food_log(async_session, test_user.id, "банан", 120)
    await create_food_log(async_session, test_user.id, "курица", 300)
    await async_session.commit()
    total = await get_food_calories_today(async_session, test_user.id)
    assert total == 420


@pytest.mark.asyncio
async def test_get_food_logs_by_date(async_session, test_user):
    await create_food_log(async_session, test_user.id, "пицца", 800)
    await async_session.commit()
    logs = await get_food_logs_by_date(async_session, test_user.id, date.today())
    assert len(logs) == 1
    assert logs[0].calories == 800
