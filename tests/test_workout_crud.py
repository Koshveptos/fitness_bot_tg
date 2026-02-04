from datetime import date
import pytest
from bot.database.crud.workout import (
    create_workout_log,
    get_workout_calories_today,
    get_total_workout_status_by_date,
)


@pytest.mark.asyncio
async def test_create_workout_log(async_session, test_user):
    await create_workout_log(async_session, test_user.id, "бег", 30, 350)
    await async_session.commit()
    burned = await get_workout_calories_today(async_session, test_user.id)
    assert burned == 350


@pytest.mark.asyncio
async def test_workout_calories_sum(async_session, test_user):
    await create_workout_log(async_session, test_user.id, "бег", 30, 350)
    await create_workout_log(async_session, test_user.id, "отжимания", 20, 150)
    await async_session.commit()
    total = await get_workout_calories_today(async_session, test_user.id)
    assert total == 500


@pytest.mark.asyncio
async def test_get_total_workout_status(async_session, test_user):
    await create_workout_log(async_session, test_user.id, "плавание", 45, 400)
    await async_session.commit()
    status = await get_total_workout_status_by_date(
        async_session, test_user.id, date.today()
    )
    assert status["total_duration"] == 45
    assert status["total_calories"] == 400
