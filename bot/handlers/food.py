from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.database.session import async_session_maker
from bot.services.food_service import add_food
from bot.integrations.food_api import get_food_calories_per_100g
from bot.states import FoodStates

router = Router()


@router.message(Command("log_food"))
async def log_food(message: Message, state: FSMContext):
    args = message.text.split(maxsplit=1)
    if len(args) != 2:
        await message.answer("Использование: /log_food <продукт>")
        return

    product = args[1].strip()
    calories_100g = await get_food_calories_per_100g(product)

    if calories_100g is None:
        await message.answer("❌ Продукт не найден")
        return

    await state.update_data(product=product, calories_100g=calories_100g)
    await state.set_state(FoodStates.grams)

    await message.answer(f"🍽 {product} — {calories_100g} ккал/100г\nСколько грамм?")


@router.message(FoodStates.grams)
async def food_grams_handler(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Введите число")
        return

    grams = int(message.text)
    data = await state.get_data()
    calories = int(data["calories_100g"] * grams / 100)

    async with async_session_maker() as session:
        total_today = await add_food(
            session, message.from_user.id, data["product"], calories
        )

    await state.clear()
    await message.answer(
        f"✅ Записано {calories} ккал\nСегодня всего: {total_today} ккал"
    )
