from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.database.session import async_session_maker
from bot.services.food_service import add_food
from bot.states import FoodStates

router = Router()


@router.message(FoodStates.grams)
async def food_grams_handler(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Введите число грамм")
        return

    grams = int(message.text)
    data = await state.get_data()
    calories = int(data["calories_100g"] * grams / 100)

    async with async_session_maker() as session:
        total = await add_food(session, message.from_user.id, data["product"], calories)

    await state.clear()
    await message.answer(f"✅ Записано {calories} ккал\nСегодня всего: {total} ккал")
