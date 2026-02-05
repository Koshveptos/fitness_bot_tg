from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "👋 Привет!\n\n"
        "Я фитнес-бот 💪\n"
        "Команды:\n"
        "/set_profile — настроить профиль\n"
        "/log_food — добавить еду\n"
        "/log_water — добавить воду\n"
        "/log_workout — добавить тренировку\n"
        "/check_progress — прогресс за сегодня"
    )
