from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from bot.database.session import async_session_maker
from bot.services.user_service import register_or_get_user, update_user_profile
from bot.services.water_service import calculate_water_goal
from bot.services.summary_service import calculate_calorie_goal
from bot.database.models import GenderEnum

router = Router()


@router.message(Command("set_profile"))
async def set_profile(message: Message):
    args = message.text.split()

    if len(args) != 7:
        await message.answer(
            "Использование:\n"
            "/set_profile <вес> <рост> <возраст> <активность_мин> <город> <пол>\n"
            "Пример:\n"
            "/set_profile 80 180 25 45 Moscow male"
        )
        return

    _, weight, height, age, activity, city, gender_raw = args

    try:
        weight = float(weight)
        height = float(height)
        age = int(age)
        activity = int(activity)
        gender = GenderEnum.MALE if gender_raw.lower() == "male" else GenderEnum.FEMALE
    except ValueError:
        await message.answer("❌ Неверный формат данных")
        return

    async with async_session_maker() as session:
        await register_or_get_user(session, message.from_user.id)

        water_goal = await calculate_water_goal(
            weight=weight,
            activity_minutes=activity,
            city=city,
        )

        calorie_goal = calculate_calorie_goal(
            weight=weight,
            height=height,
            age=age,
            activity_minutes=activity,
            gender=gender,
        )

        await update_user_profile(
            session,
            message.from_user.id,
            weight=weight,
            height=height,
            age=age,
            activity_minutes=activity,
            city=city,
            gender=gender,
            water_goal=water_goal,
            calorie_goal=calorie_goal,
        )

    await message.answer(
        f"✅ Профиль сохранён\n\n"
        f"💧 Норма воды: {water_goal} мл\n"
        f"🔥 Норма калорий: {calorie_goal} ккал"
    )
