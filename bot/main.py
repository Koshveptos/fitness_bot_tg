import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import settings

from bot.handlers.start import router as start_router
from bot.handlers.profile import router as profile_router
from bot.handlers.food import router as food_router
from bot.handlers.water import router as water_router
from bot.handlers.workout import router as workout_router
from bot.handlers.progress import router as progress_router


async def main():
    bot = Bot(token=settings.TG_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.include_router(start_router)
    dp.include_router(profile_router)
    dp.include_router(food_router)
    dp.include_router(water_router)
    dp.include_router(workout_router)
    dp.include_router(progress_router)

    print("🤖 Бот запущен")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
