from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from bot.services.water_service import add_water, get_today_water_intake
from bot.services.user_service import get_user_by_telegram_id
from bot.database.session import async_session_maker

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
        if not user or user.water_goal is None:
            await message.answer("Сначала настрой профиль: /set_profile")
            return

        await add_water(session, message.from_user.id, amount)
        total = await get_today_water_intake(session, message.from_user.id) or 0

    remaining = max(user.water_goal - total, 0)

    await message.answer(
        f"💧 Записано: {amount} мл\n"
        f"Всего сегодня: {total} / {user.water_goal} мл\n"
        f"Осталось: {remaining} мл"
    )
