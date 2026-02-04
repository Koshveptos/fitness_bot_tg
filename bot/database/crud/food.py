from datetime import date
from typing import List, Optional
from sqlalchemy import func, select
from bot.database.models import FoodLog


async def create_food_log(
    session,
    user_id: int,
    food_name: str,
    calories: int = 0,
    log_date: Optional[date] = None,
) -> FoodLog:
    food_log = FoodLog(
        user_id=user_id,
        log_date=log_date or date.today(),
        food_name=food_name,
        calories=calories,
    )
    session.add(food_log)
    return food_log


async def get_food_calories_today(session, user_id: int) -> int:
    result = await session.execute(
        select(func.sum(FoodLog.calories)).where(
            FoodLog.user_id == user_id, FoodLog.log_date == date.today()
        )
    )
    return result.scalar() or 0


async def get_food_logs_by_user(session, user_id: int) -> List[FoodLog]:
    result = await session.execute(
        select(FoodLog)
        .where(FoodLog.user_id == user_id)
        .order_by(FoodLog.log_date.desc())
    )
    return list(result.scalars().all())


async def get_food_logs_by_date(session, user_id: int, log_date: date) -> List[FoodLog]:
    result = await session.execute(
        select(FoodLog)
        .where(FoodLog.user_id == user_id, FoodLog.log_date == log_date)
        .order_by(FoodLog.id)
    )
    return list(result.scalars().all())


async def get_food_logs_by_date_range(
    session, user_id: int, start_log: date, end_log: date
) -> List[FoodLog]:
    result = await session.execute(
        select(FoodLog)
        .where(
            FoodLog.user_id == user_id,
            FoodLog.log_date >= start_log,
            FoodLog.log_date <= end_log,
        )
        .order_by(FoodLog.log_date, FoodLog.id)
    )
    return list(result.scalars().all())


async def get_total_calories_by_date(session, user_id: int, log_date: date) -> int:
    result = await session.execute(
        select(func.sum(FoodLog.calories)).where(
            FoodLog.user_id == user_id, FoodLog.log_date == log_date
        )
    )
    total = result.scalar()
    return total or 0
