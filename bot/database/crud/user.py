from sqlalchemy import select, update

from sqlalchemy.orm import selectinload
from typing import Optional, List
from bot.database.models import UserBase, GenderEnum


###USER CRUD

###создаем дефолтного (если захочет потом сменим пол и остальное))


async def create_user(
    session,
    telegram_id: int,
    weight: float = 70,
    height: float = 170,
    age: int = 30,
    city: str = "Moscow",
    gender: GenderEnum = GenderEnum.MALE,
    water_goal: Optional[int] = 0,
    calorie_goal: Optional[int] = 0,
    activity_minutes: int = 30,
    username: Optional[str] = None,
    first_name: Optional[str] = None,
) -> UserBase:
    # основаня функция после старта бота (дополнение )
    user = UserBase(
        telegram_id=telegram_id,
        weight=weight,
        height=height,
        age=age,
        city=city,
        gender=gender,
        water_goal=water_goal,
        calorie_goal=calorie_goal,
        activity_minutes=activity_minutes,
        username=username,
        first_name=first_name,
    )
    session.add(user)
    return user


async def get_user_by_telegram_id(
    session,
    telegram_id: int,
    load_logs: bool = False,
) -> Optional[UserBase]:
    result = select(UserBase).where(UserBase.telegram_id == telegram_id)
    if load_logs:
        result = result.options(
            selectinload(UserBase.water_logs),
            selectinload(UserBase.food_logs),
            selectinload(UserBase.workout_logs),
        )
    result = await session.execute(result)
    return result.scalar_one_or_none()


async def get_or_create_user(
    session,
    telegram_id: int,
    username: Optional[str] = None,
    first_name: Optional[str] = None,
) -> UserBase:
    user = await get_user_by_telegram_id(session, telegram_id)
    if user:
        return user
    return await create_user(
        session=session,
        telegram_id=telegram_id,
        username=username,
        first_name=first_name,
    )


async def update_user_by_id(session, user_id: int, **kwargs) -> bool:
    if not kwargs:
        return False
    tmp = update(UserBase).where(UserBase.id == user_id).values(**kwargs)
    result = await session.execute(tmp)
    return result.rowcount > 0


async def get_user_by_city(session, city: str) -> List[UserBase]:
    result = await session.execute(select(UserBase).where(UserBase.city == city))
    return list(result.scalars().all())


async def get_user_by_id(
    session, user_id: int, load_logs: bool = False
) -> Optional[UserBase]:
    query = select(UserBase).where(UserBase.id == user_id)
    if load_logs:
        query = query.options(
            selectinload(UserBase.water_logs),
            selectinload(UserBase.food_logs),
            selectinload(UserBase.workout_logs),
        )
    result = await session.execute(query)
    return result.scalar_one_or_none()
