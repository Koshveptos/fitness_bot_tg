from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from bot.database.session import async_session_maker
from bot.services.workout_service import add_workout, calculate_burned_calories

router = Router()


@router.message(Command("log_workout"))
async def log_workout(message: Message):
    parts = message.text.split()
    if len(parts) != 3 or not parts[2].isdigit():
        await message.answer("Использование: /log_workout тип минуты")
        return

    workout_type = parts[1]
    minutes = int(parts[2])
    burned = calculate_burned_calories(workout_type, minutes)

    async with async_session_maker() as session:
        await add_workout(session, message.from_user.id, workout_type, minutes, burned)

    await message.answer(f"🏃 {workout_type} {minutes} мин — {burned} ккал сожжено")
