from datetime import date
from typing import List, Optional
from sqlalchemy import func, select
from bot.database.models import WaterLog


async def create_water_log(
    session, user_id: int, amount: int, log_date: Optional[date] = None
) -> WaterLog:
    water_log = WaterLog(
        user_id=user_id, amount=amount, log_date=log_date or date.today()
    )
    session.add(water_log)
    return water_log


async def get_water_today(session, user_id: int) -> int:
    result = await session.execute(
        select(func.sum(WaterLog.amount)).where(
            WaterLog.user_id == user_id, WaterLog.log_date == date.today()
        )
    )
    return result.scalar() or 0


async def get_water_logs_by_user(session, user_id: int) -> List[WaterLog]:
    result = await session.execute(
        select(WaterLog)
        .where(WaterLog.user_id == user_id)
        .order_by(WaterLog.log_date.desc())
    )
    return list(result.scalars().all())


async def get_water_logs_by_date(
    session, user_id: int, log_date: date
) -> List[WaterLog]:
    result = await session.execute(
        select(WaterLog)
        .where(WaterLog.user_id == user_id, WaterLog.log_date == log_date)
        .order_by(WaterLog.id)
    )
    return list(result.scalars().all())


async def get_water_log_by_date_range(
    session, user_id: int, start_log: date, end_log: date
) -> List[WaterLog]:
    result = await session.execute(
        select(WaterLog)
        .where(
            WaterLog.user_id == user_id,
            WaterLog.log_date <= end_log,
            WaterLog.log_date >= start_log,
        )
        .order_by(WaterLog.log_date, WaterLog.id)
    )
    return list(result.scalars().all())
