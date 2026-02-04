# bot/services/user_service.py
from typing import Optional
from bot.database.crud.user import (
    get_or_create_user,
    update_user_by_id,
    get_user_by_telegram_id,
)
from bot.database.models import UserBase


async def register_or_get_user(
    session,
    telegram_id: int,
    username: Optional[str] = None,
    first_name: Optional[str] = None,
) -> UserBase:
    return await get_or_create_user(session, telegram_id, username, first_name)


async def update_user_profile(session, telegram_id: int, **kwargs) -> bool:
    user = await get_user_by_telegram_id(session, telegram_id)
    if not user:
        return False
    return await update_user_by_id(session, user.id, **kwargs)
