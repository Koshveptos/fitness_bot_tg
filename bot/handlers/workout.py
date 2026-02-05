from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from bot.services.workout_service import add_workout
from bot.services.workout_service import calculate_burned_calories

from bot.database.session import async_session_maker

router = Router()


@router.message(Command("log_workout"))
async def log_workout(message: Message):
    parts = message.text.split()

    if len(parts) != 3 or not parts[2].isdigit():
        await message.answer(
            "Использование: /log_workout <тип> <минуты>\n" "Пример: /log_workout бег 30"
        )
        return

    workout_type = parts[1]
    minutes = int(parts[2])

    burned = calculate_burned_calories(workout_type, minutes)
    extra_water = (minutes // 30) * 200

    async with async_session_maker() as session:
        await add_workout(
            session,
            telegram_id=message.from_user.id,
            workout_type=workout_type,
            duration=minutes,
            burned_calories=burned,
        )

    await message.answer(
        f"🏃 {workout_type.capitalize()} {minutes} мин\n"
        f"🔥 Сожжено: {burned} ккал\n"
        f"💧 Рекомендуется выпить: {extra_water} мл воды"
    )
