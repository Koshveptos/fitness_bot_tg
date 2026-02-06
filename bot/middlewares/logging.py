import logging
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: TelegramObject, data: dict):
        if isinstance(event, Message):
            user = event.from_user
            text = event.text or event.caption or "[no text]"
            logger.info(f"User {user.id} (@{user.username or 'no_username'}) → {text}")

        elif isinstance(event, CallbackQuery):
            user = event.from_user
            logger.info(f"Callback from {user.id} (@{user.username}) → {event.data}")

        return await handler(event, data)
