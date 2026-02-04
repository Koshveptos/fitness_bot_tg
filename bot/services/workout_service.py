from typing import Optional
from bot.database.crud.workout import create_workout_log, get_workout_calories_today
from bot.database.crud.user import get_user_by_telegram_id


async def add_workout(
    session,
    telegram_id: int,
    workout_type: str,
    duration: int,
    burned_calories: int = 0,
) -> Optional[int]:
    if burned_calories <= 0 or burned_calories >= 15000:
        return None
    user = await get_user_by_telegram_id(session, telegram_id)
    if not user:
        return None
    await create_workout_log(session, user.id, workout_type, duration, burned_calories)
    return await get_workout_calories_today(session, user.id)


async def get_today_burned_calories(session, telegram_id: int) -> Optional[int]:
    user = await get_user_by_telegram_id(session, telegram_id)
    if not user:
        return None
    return await get_workout_calories_today(session, user.id)
