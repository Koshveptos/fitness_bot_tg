from datetime import date
from typing import Dict
from bot.database.crud.summary import get_daily_summary
from bot.database.crud.user import get_user_by_telegram_id


async def get_today_summary(session, telegram_id: int) -> Dict:
    user = await get_user_by_telegram_id(session, telegram_id)
    if not user:
        return {
            "water_ml": 0,
            "food_calories": 0,
            "burned_calories": 0,
            "net_calories": 0,
            "workout_duration_min": 0,
        }

    return await get_daily_summary(session, user.id, date.today())
