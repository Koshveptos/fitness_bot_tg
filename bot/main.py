import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import settings
from bot.middlewares.logging import LoggingMiddleware

from bot.handlers.start import router as start_router
from bot.handlers.profile_fsm import router as profile_fsm_router
from bot.handlers.food import router as food_router
from bot.handlers.water import router as water_router
from bot.handlers.workout import router as workout_router
from bot.handlers.progress import router as progress_router
from bot.handlers.graph import router as graph_router


async def main():
    bot = Bot(
        token=settings.TG_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML"),
    )

    dp = Dispatcher(storage=MemoryStorage())
    dp.update.middleware(LoggingMiddleware())

    dp.include_router(start_router)
    dp.include_router(profile_fsm_router)
    dp.include_router(food_router)
    dp.include_router(water_router)
    dp.include_router(workout_router)
    dp.include_router(progress_router)
    dp.include_router(graph_router)

    print(" Бот запущен")
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
