import pytest
from bot.database.crud.user import (
    get_or_create_user,
    get_user_by_telegram_id,
    get_user_by_id,
)
from bot.services.user_service import update_user_profile


@pytest.mark.asyncio
async def test_create_and_get_user(async_session, test_user):
    user = await get_user_by_telegram_id(async_session, 999999999)
    assert user is not None
    assert user.telegram_id == 999999999


@pytest.mark.asyncio
async def test_get_or_create_creates_new(async_session):
    user = await get_or_create_user(
        async_session, telegram_id=777777777, username="newguy"
    )
    assert user.telegram_id == 777777777
    assert user.username == "newguy"


@pytest.mark.asyncio
async def test_update_user_profile(async_session, test_user):
    success = await update_user_profile(
        async_session, test_user.telegram_id, weight=90.0, city="UpdatedCity"
    )
    assert success is True

    updated = await get_user_by_telegram_id(async_session, test_user.telegram_id)
    assert updated.weight == 90.0


@pytest.mark.asyncio
async def test_get_user_by_id(async_session, test_user):
    user = await get_user_by_id(async_session, test_user.id)
    assert user.id == test_user.id
