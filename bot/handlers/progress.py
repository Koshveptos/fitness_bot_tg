from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from bot.database.session import async_session_maker
from bot.services.summary_service import get_today_summary

router = Router()


@router.message(Command("check_progress"))
async def check_progress(message: Message):
    async with async_session_maker() as session:
        summary = await get_today_summary(session, message.from_user.id)

    await message.answer(
        f"📊 Прогресс сегодня:\n"
        f"💧 Вода: {summary['water_ml']} мл\n"
        f"🍽 Калории: {summary['food_calories']} (сожжено {summary['burned_calories']})"
    )
