from datetime import date
import pytest
from bot.database.crud.water import (
    create_water_log,
    get_water_today,
    get_water_logs_by_date,
)


@pytest.mark.asyncio
async def test_create_water_log(async_session, test_user):
    await create_water_log(async_session, test_user.id, 600)
    await async_session.commit()
    total = await get_water_today(async_session, test_user.id)
    assert total == 600


@pytest.mark.asyncio
async def test_water_logs_sum_correctly(async_session, test_user):
    await create_water_log(async_session, test_user.id, 400)
    await create_water_log(async_session, test_user.id, 800)
    await async_session.commit()
    total = await get_water_today(async_session, test_user.id)
    assert total == 1200


@pytest.mark.asyncio
async def test_get_water_logs_by_date(async_session, test_user):
    await create_water_log(async_session, test_user.id, 300)
    await async_session.commit()
    logs = await get_water_logs_by_date(async_session, test_user.id, date.today())
    assert len(logs) == 1
    assert logs[0].amount == 300
