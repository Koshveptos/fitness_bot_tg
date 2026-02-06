from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from bot.database.session import async_session_maker
from bot.services.water_service import add_water
from bot.services.user_service import get_user_by_telegram_id

router = Router()


@router.message(Command("log_water"))
async def log_water(message: Message):
    parts = message.text.split()
    if len(parts) != 2 or not parts[1].isdigit():
        await message.answer("Использование: /log_water <мл>")
        return

    amount = int(parts[1])

    async with async_session_maker() as session:
        user = await get_user_by_telegram_id(session, message.from_user.id)
        if not user:
            await message.answer("Сначала /set_profile")
            return

        total = await add_water(session, message.from_user.id, amount)

    remaining = max(user.water_goal - total, 0)
    await message.answer(
        f"💧 +{amount} мл\n"
        f"Сегодня: {total} / {user.water_goal} мл\n"
        f"Осталось: {remaining} мл"
    )
