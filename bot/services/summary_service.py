from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from sqlalchemy import select, func
from bot.database.models import GenderEnum

from bot.database.models import WaterLog, FoodLog, WorkoutLog


async def get_today_summary(session: AsyncSession, telegram_id: int) -> dict:
    today = date.today()

    water = (
        await session.scalar(
            select(func.sum(WaterLog.amount))
            .join(WaterLog.user)
            .where(
                WaterLog.log_date == today, WaterLog.user.has(telegram_id=telegram_id)
            )
        )
        or 0
    )

    food = (
        await session.scalar(
            select(func.sum(FoodLog.calories))
            .join(FoodLog.user)
            .where(FoodLog.log_date == today, FoodLog.user.has(telegram_id=telegram_id))
        )
        or 0
    )

    burned = (
        await session.scalar(
            select(func.sum(WorkoutLog.burned_calories))
            .join(WorkoutLog.user)
            .where(
                WorkoutLog.log_date == today,
                WorkoutLog.user.has(telegram_id=telegram_id),
            )
        )
        or 0
    )

    return {
        "water_ml": water,
        "food_calories": food,
        "burned_calories": burned,
        "balance_calories": food - burned,
    }


def calculate_calorie_goal(
    weight: float,
    height: float,
    age: int,
    activity_minutes: int,
    gender: GenderEnum,
) -> int:
    if gender == GenderEnum.MALE:
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    activity_bonus = min(activity_minutes * 5, 400)

    return int(bmr + activity_bonus)
