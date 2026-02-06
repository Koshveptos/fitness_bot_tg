from datetime import date
from typing import List, Optional
from sqlalchemy import func, select
from bot.database.models import WorkoutLog


async def create_workout_log(
    session,
    user_id: int,
    workout_type: str,
    duration: int,
    burned_calories: int = 0,
    log_date: Optional[date] = None,
) -> WorkoutLog:
    workout_log = WorkoutLog(
        user_id=user_id,
        workout_type=workout_type,
        duration=duration,
        burned_calories=burned_calories,
        log_date=log_date or date.today(),
    )
    session.add(workout_log)
    return workout_log


async def get_workout_logs_by_user(session, user_id: int) -> List[WorkoutLog]:
    result = await session.execute(
        select(WorkoutLog)
        .where(WorkoutLog.user_id == user_id)
        .order_by(WorkoutLog.log_date.desc())
    )
    return list(result.scalars().all())


async def get_workout_calories_today(session, user_id: int) -> int:
    result = await session.execute(
        select(func.coalesce(func.sum(WorkoutLog.burned_calories), 0)).where(
            WorkoutLog.user_id == user_id, WorkoutLog.log_date == date.today()
        )
    )
    return result.scalar() or 0


async def get_workout_logs_by_date(
    session, user_id: int, log_date: date
) -> List[WorkoutLog]:
    result = await session.execute(
        select(WorkoutLog)
        .where(WorkoutLog.user_id == user_id, WorkoutLog.log_date == log_date)
        .order_by(WorkoutLog.id)
    )
    return list(result.scalars().all())


async def get_workout_logs_by_date_range(
    session, user_id: int, start_date: date, end_date: date
) -> List[WorkoutLog]:
    result = await session.execute(
        select(WorkoutLog)
        .where(
            WorkoutLog.user_id == user_id,
            WorkoutLog.log_date >= start_date,
            WorkoutLog.log_date <= end_date,
        )
        .order_by(WorkoutLog.log_date, WorkoutLog.id)
    )
    return list(result.scalars().all())


async def get_total_workout_status_by_date(
    session, user_id: int, log_date: date
) -> dict:
    result = await session.execute(
        select(
            func.sum(WorkoutLog.duration),
            func.sum(WorkoutLog.burned_calories),
            func.count(WorkoutLog.id),
        ).where(WorkoutLog.user_id == user_id, WorkoutLog.log_date == log_date)
    )
    duration, calories, count = result.first()
    return {
        "total_duration": duration or 0,
        "total_calories": calories or 0,
        "workout_count": count or 0,
    }
