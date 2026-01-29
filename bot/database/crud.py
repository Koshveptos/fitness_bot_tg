from sqlalchemy import select, update

from sqlalchemy.orm import selectinload
from typing import Optional, List
from session import connection
from .models import UserBase, GenderEnum


###USER CRUD


@connection
async def create_user(
    session,
    weight: float,
    height: float,
    age: int,
    city: str,
    gender: GenderEnum,
    water_goal: Optional[int] = None,
    calorie_goal: Optional[int] = None,
    activity_minutes: int = 0,
) -> UserBase:
    user = UserBase(
        weight=weight,
        height=height,
        age=age,
        city=city,
        gender=gender,
        water_goal=water_goal,
        calorie_goal=calorie_goal,
        activity_minutes=activity_minutes,
    )
    session.add(user)
    return user


@connection
async def get_users(session) -> List[UserBase]:
    result = await session.execute(select(UserBase))
    return list(result.scalars().all())


@connection
async def get_user_by_id(session, user_id: int) -> Optional[UserBase]:
    result = await session.execute(
        select(UserBase)
        .where(UserBase.id == user_id)
        .options(
            selectinload(UserBase.water_logs),
            selectinload(UserBase.food_logs),
            selectinload(UserBase.workout_logs),
        )
    )
    return result.scalar_one_or_none()

    """
    TODO
    переделать в фабрику update  или через проход через словарь потом

    Returns:
        _type_: _description_
    """


@connection
async def update_user(
    session,
    user_id: int,
    weight: Optional[float] = None,
    height: Optional[float] = None,
    age: Optional[int] = None,
    city: Optional[str] = None,
    gender: Optional[GenderEnum] = None,
    water_goal: Optional[int] = None,
    calorie_goal: Optional[int] = None,
    activity_minutes: Optional[int] = None,
) -> bool:
    ##ПОТОМ ИСПРАВТЬ ТИПИЗАЦИЮ
    update_data = {}  # type: ignore
    if weight is not None:
        update_data["weight"] = weight
    if height is not None:
        update_data["height"] = height
    if age is not None:
        update_data["age"] = age
    if city is not None:
        update_data["city"] = city  # type: ignore
    if gender is not None:
        update_data["gender"] = gender  # type: ignore
    if water_goal is not None:
        update_data["water_goal"] = water_goal
    if calorie_goal is not None:
        update_data["calorie_goal"] = calorie_goal
    if activity_minutes is not None:
        update_data["activity_minutes"] = activity_minutes
    if not update_data:
        return False

    tmp = update(UserBase).where(UserBase.id == user_id).values(**update_data)
    result = await session.execute(tmp)
    return result.rowcount > 0

    """
    увидел новую форму записи для алхимии, есть  такое, потом поменять
    stmt = select(UserBase).where(UserBase.city == city)
    return list(await session.scalars(stmt))

    """


@connection
async def get_user_by_city(session, city: str) -> List[UserBase]:
    result = await session.execute(select(UserBase).where(UserBase.city == city))
    return list(result.scalars().all())


#####
# WATER LOOOGS
#####
