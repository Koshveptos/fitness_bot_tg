from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from bot.database.session import async_session_maker
from bot.services.user_service import get_user_by_telegram_id
from bot.utils.helpers import generate_progress_graph

router = Router()


@router.message(Command("graph"))
async def send_graph(message: Message):
    async with async_session_maker() as session:
        user = await get_user_by_telegram_id(session, message.from_user.id)
        if not user:
            await message.answer("Сначала настрой профиль: /set_profile")
            return

    photo = await generate_progress_graph(message.from_user.id)
    await message.answer_photo(photo, caption="📈 Ваш прогресс за последние 7 дней")
