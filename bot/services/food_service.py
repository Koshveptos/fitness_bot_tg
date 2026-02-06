from typing import Optional
from bot.database.crud.food import create_food_log, get_food_calories_today
from bot.services.user_service import get_user_by_telegram_id


async def add_food(
    session, telegram_id: int, food_name: str, calories: int
) -> Optional[int]:
    user = await get_user_by_telegram_id(session, telegram_id)
    if not user:
        return None

    await create_food_log(session, user.id, food_name, calories)
    await session.commit()
    return await get_food_calories_today(session, user.id)


async def get_today_food_calories_intake(session, telegram_id: int) -> Optional[int]:
    user = await get_user_by_telegram_id(session, telegram_id)
    if not user:
        return None
    return await get_food_calories_today(session, user.id)
