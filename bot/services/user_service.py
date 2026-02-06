# bot/services/user_service.py
from typing import Optional
from bot.database.crud.user import (
    get_or_create_user,
    update_user_by_id,
    get_user_by_telegram_id_crud,
)
from bot.database.models import UserBase


async def register_or_get_user(
    session,
    telegram_id: int,
    username: Optional[str] = None,
    first_name: Optional[str] = None,
) -> UserBase:
    user = await get_or_create_user(session, telegram_id, username, first_name)
    await session.commit()
    return user


async def update_user_profile(session, telegram_id: int, **kwargs) -> bool:
    if not kwargs:
        return False

    user = await get_user_by_telegram_id(session, telegram_id)
    if not user:
        return False

    success = await update_user_by_id(session, user.id, **kwargs)
    await session.commit()
    return success


async def get_user_by_telegram_id(
    session, telegram_id: int, **kwargs
) -> Optional[UserBase]:
    return await get_user_by_telegram_id_crud(session, telegram_id)
