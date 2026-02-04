from typing import Optional
from bot.database.crud.water import create_water_log, get_water_today
from bot.database.crud.user import get_user_by_telegram_id


async def add_water(session, telegram_id: int, amount: int) -> Optional[int]:
    if amount <= 0 or amount > 5000:
        return None
    user = await get_user_by_telegram_id(session, telegram_id)
    if not user:
        return None
    await create_water_log(session, user.id, amount)
    return await get_water_today(session, user.id)


async def get_today_water_intake(session, telegram_id: int) -> Optional[int]:
    user = await get_user_by_telegram_id(session, telegram_id)
    if not user:
        return None
    return await get_water_today(session, user.id)
