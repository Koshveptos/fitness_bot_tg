from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from bot.services.summary_service import get_today_summary
from bot.database.crud.user import get_user_by_telegram_id
from bot.database.session import async_session_maker

router = Router()


@router.message(Command("check_progress"))
async def check_progress(message: Message):
    async with async_session_maker() as session:
        user = await get_user_by_telegram_id(session, message.from_user.id)
        if not user:
            await message.answer("Сначала настройте профиль: /set_profile")
            return
        summary = await get_today_summary(session, message.from_user.id)

    water_left = max(user.water_goal - summary["water_ml"], 0)
    calories_left = max(user.calorie_goal - summary["balance_calories"], 0)

    await message.answer(
        "📊 *Прогресс за сегодня*\n\n"
        f"💧 Вода:\n"
        f"- Выпито: {summary['water_ml']} / {user.water_goal} мл\n"
        f"- Осталось: {water_left} мл\n\n"
        f"🍽 Калории:\n"
        f"- Потреблено: {summary['food_calories']} ккал\n"
        f"- Сожжено: {summary['burned_calories']} ккал\n"
        f"- Баланс: {summary['balance_calories']} ккал\n"
        f"- Осталось: {calories_left} ккал",
        parse_mode="Markdown",
    )
