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
            "Использование: /set_profile <вес> <рост> <возраст> <активность> <город> <пол>"
        )
        return

    _, weight, height, age, activity, city, gender_raw = args

    try:
        weight = float(weight)
        height = float(height)
        age = int(age)
        activity = int(activity)
        gender = (
            GenderEnum.MALE
            if gender_raw.lower() in ["male", "муж"]
            else GenderEnum.FEMALE
        )
    except ValueError:
        await message.answer("❌ Неверный формат")
        return

    async with async_session_maker() as session:
        await register_or_get_user(
            session,
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
        )

        water_goal = await calculate_water_goal(weight, activity, city)
        calorie_goal = calculate_calorie_goal(weight, height, age, activity, gender)

        await update_user_profile(
            session,
            telegram_id=message.from_user.id,
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
        f"✅ Профиль сохранён!\n\n"
        f"💧 Вода: {water_goal} мл\n"
        f"🔥 Калории: {calorie_goal} ккал"
    )
