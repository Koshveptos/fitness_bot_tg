from datetime import date
from sqlalchemy import func, select
from bot.database.models import FoodLog, UserBase, WaterLog, WorkoutLog


async def get_daily_summary(session, user_id: int, log_date: date) -> dict:
    water_result = await session.execute(
        select(func.sum(WaterLog.amount)).where(
            WaterLog.user_id == user_id, WaterLog.log_date == log_date
        )
    )
    water_total = water_result.scalar() or 0
    food_result = await session.execute(
        select(func.sum(FoodLog.calories)).where(
            FoodLog.user_id == user_id, FoodLog.log_date == log_date
        )
    )
    food_calories = food_result.scalar() or 0
    workout_result = await session.execute(
        select(
            func.sum(WorkoutLog.duration), func.sum(WorkoutLog.burned_calories)
        ).where(WorkoutLog.user_id == user_id, WorkoutLog.log_date == log_date)
    )
    workout_duration, workout_calories = workout_result.first()
    return {
        "date": log_date,
        "water_ml": water_total,
        "food_calories": food_calories,
        "burned_calories": workout_calories or 0,
        "workout_duration_min": workout_duration or 0,
        "net_calories": food_calories - (workout_calories or 0),
    }


##получить цели пользователя


async def get_user_goals(session, user_id: int) -> dict:
    result = await session.execute(
        select(UserBase.water_goal, UserBase.calorie_goal).where(UserBase.id == user_id)
    )
    water_goal, calorie_goal = result.first()
    return {"water_goal": water_goal, "calorie_goal": calorie_goal}
