from typing import Optional
from bot.database.crud.workout import create_workout_log, get_workout_calories_today
from bot.services.user_service import get_user_by_telegram_id


async def add_workout(
    session,
    telegram_id: int,
    workout_type: str,
    duration: int,
    burned_calories: Optional[int] = None,
) -> Optional[int]:
    user = await get_user_by_telegram_id(session, telegram_id)
    if not user:
        return None

    if burned_calories is None:
        burned_calories = calculate_burned_calories(workout_type, duration)

    if burned_calories <= 0 or burned_calories >= 15000:
        return None

    await create_workout_log(session, user.id, workout_type, duration, burned_calories)
    await session.commit()
    return await get_workout_calories_today(session, user.id)


async def get_today_burned_calories(session, telegram_id: int) -> Optional[int]:
    user = await get_user_by_telegram_id(session, telegram_id)
    if not user:
        return None
    return await get_workout_calories_today(session, user.id)


def calculate_burned_calories(workout_type: str, minutes: int) -> int:
    rates = {
        "бег": 10,
        "ходьба": 4,
        "велосипед": 8,
        "плавание": 9,
    }

    rate = rates.get(workout_type.lower(), 6)
    return rate * minutes
