from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.database.session import async_session_maker
from bot.services.user_service import register_or_get_user, update_user_profile
from bot.services.water_service import calculate_water_goal
from bot.services.summary_service import calculate_calorie_goal
from bot.database.models import GenderEnum
from bot.states import ProfileStates

router = Router()


@router.message(Command("set_profile"))
async def cmd_set_profile(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(ProfileStates.weight)
    await message.answer("Введите ваш вес в кг (например: 75)")


@router.message(ProfileStates.weight)
async def process_weight(message: Message, state: FSMContext):
    try:
        weight = float(message.text.replace(",", "."))
        if not 30 <= weight <= 200:
            raise ValueError
        await state.update_data(weight=weight)
        await state.set_state(ProfileStates.height)
        await message.answer("Введите ваш рост в см:")
    except ValueError:
        await message.answer("Пожалуйста, введите число (например: 75)")


@router.message(ProfileStates.height)
async def process_height(message: Message, state: FSMContext):
    try:
        height = float(message.text.replace(",", "."))
        await state.update_data(height=height)
        await state.set_state(ProfileStates.age)
        await message.answer("Введите ваш возраст:")
    except ValueError:
        await message.answer("Введите число")


@router.message(ProfileStates.age)
async def process_age(message: Message, state: FSMContext):
    try:
        age = int(message.text)
        await state.update_data(age=age)
        await state.set_state(ProfileStates.activity)
        await message.answer(
            "Сколько минут физической активности в день (тренировки, ходьба)?"
        )
    except ValueError:
        await message.answer("Введите число")


@router.message(ProfileStates.activity)
async def process_activity(message: Message, state: FSMContext):
    try:
        activity = int(message.text)
        await state.update_data(activity=activity)
        await state.set_state(ProfileStates.city)
        await message.answer("В каком городе вы живёте? (для погоды)")
    except ValueError:
        await message.answer("Введите число")


@router.message(ProfileStates.city)
async def process_city(message: Message, state: FSMContext):
    city = message.text.strip()
    await state.update_data(city=city)
    await state.set_state(ProfileStates.gender)
    await message.answer("Ваш пол? Напишите male или female")


@router.message(ProfileStates.gender)
async def process_gender(message: Message, state: FSMContext):
    gender_text = message.text.strip().lower()
    gender = (
        GenderEnum.MALE if gender_text in ["male", "муж", "м"] else GenderEnum.FEMALE
    )

    data = await state.get_data()

    async with async_session_maker() as session:
        await register_or_get_user(
            session,
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
        )

        water_goal = await calculate_water_goal(
            data["weight"], data["activity"], data["city"]
        )
        calorie_goal = calculate_calorie_goal(
            data["weight"], data["height"], data["age"], data["activity"], gender
        )

        await update_user_profile(
            session,
            telegram_id=message.from_user.id,
            weight=data["weight"],
            height=data["height"],
            age=data["age"],
            activity_minutes=data["activity"],
            city=data["city"],
            gender=gender,
            water_goal=water_goal,
            calorie_goal=calorie_goal,
        )

    await state.clear()
    await message.answer(
        f"✅ Профиль успешно сохранён!\n\n"
        f"💧 Норма воды: <b>{water_goal}</b> мл\n"
        f"🔥 Норма калорий: <b>{calorie_goal}</b> ккал",
        parse_mode="HTML",
    )
