from typing import Optional
from bot.database.crud.water import create_water_log, get_water_today
from bot.services.user_service import get_user_by_telegram_id
from bot.integrations.weather_api import get_city_temperature


async def add_water(session, telegram_id: int, amount: int) -> Optional[int]:
    if amount <= 0 or amount > 5000:
        return None
    user = await get_user_by_telegram_id(session, telegram_id)
    if not user:
        return None
    await create_water_log(session, user.id, amount)
    await session.commit()
    return await get_water_today(session, user.id)


async def get_today_water_intake(session, telegram_id: int) -> Optional[int]:
    user = await get_user_by_telegram_id(session, telegram_id)
    if not user:
        return None
    return await get_water_today(session, user.id)


async def calculate_water_goal(
    weight: float,
    activity_minutes: int,
    city: str,
) -> int:
    water_ml = weight * 30
    water_ml += (activity_minutes // 30) * 500

    try:
        temp = await get_city_temperature(city)
    except Exception:
        temp = None
    if temp is not None:
        if temp >= 30:
            water_ml += 1000
        elif temp >= 25:
            water_ml += 500

    return int(water_ml)
