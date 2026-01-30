from datetime import date
from sqlalchemy import func, select, update

from sqlalchemy.orm import selectinload
from typing import Optional, List
from session import connection
from .models import FoodLog, UserBase, GenderEnum, WaterLog, WorkoutLog


"""
для воды, тренировки и еды пока что написаны будут операции создания и получение
обновлять и удалять  записи как то безсмысленно на начальном этапке , но можно дописать потом если будет время, а то выйдет много кода)
пока делаю mvp

"""


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


@connection
async def create_water_log(
    session, user_id: int, amount: int, log_date: Optional[date] = None
) -> WaterLog:
    water_log = WaterLog(
        user_id=user_id, amount=amount, log_date=log_date or date.today()
    )
    session.add(water_log)
    return water_log


@connection
async def get_water_logs_by_user(session, user_id: int) -> List[WaterLog]:
    result = await session.execute(
        select(WaterLog)
        .where(WaterLog.user_id == user_id)
        .order_by(WaterLog.log_date.desc())
    )
    return list(result.scalars().all())


@connection
async def get_water_logs_by_date(
    session, user_id: int, log_date: date
) -> List[WaterLog]:
    result = await session.execute(
        select(WaterLog)
        .where(WaterLog.user_id == user_id, WaterLog.log_date == log_date)
        .order_by(WaterLog.id)
    )
    return list(result.scalars().all)


@connection
async def get_water_log_by_date_range(
    session, user_id: int, start_log: date, end_log: date
) -> List[WaterLog]:
    result = await session.execute(
        select(WaterLog)
        .where(
            WaterLog.user_id == user_id,
            WaterLog.log_date <= end_log,
            WaterLog.log_date >= start_log,
        )
        .order_by(WaterLog.log_date, WaterLog.id)
    )
    return list(result.scalars().all())


###############
####писать много, и по идее апдейт и делит для воды то и не нужен, пользователь будет вносить, а удалять ему зачем (дописать если лень)
#####


###Foods logs


@connection
async def create_food_log(
    session,
    user_id: int,
    food_name: str,
    calories: int = 0,
    log_date: Optional[date] = None,
) -> FoodLog:
    food_log = FoodLog(
        user_id=user_id,
        log_date=log_date or date.today(),
        food_name=food_name,
        calories=calories,
    )
    session.add(food_log)
    return food_log


@connection
async def get_food_logs_by_user(session, user_id: int) -> List[FoodLog]:
    result = await session.execute(
        select(FoodLog)
        .where(FoodLog.user_id == user_id)
        .order_by(FoodLog.log_date.desc())
    )
    return list(result.scalars().all())


@connection
async def get_food_logs_by_date(session, user_id: int, log_date: date) -> List[FoodLog]:
    result = await session.execute(
        select(FoodLog)
        .where(FoodLog.user_id == user_id, FoodLog.log_date == log_date)
        .order_by(FoodLog.id)
    )
    return list(result.scalars().all())


@connection
async def get_food_logs_by_date_range(
    session, user_id: int, start_log: date, end_log: date
) -> List[FoodLog]:
    result = await session.execute(
        select(FoodLog)
        .where(
            FoodLog.user_id == user_id,
            FoodLog.log_date >= start_log,
            FoodLog.log_date <= end_log,
        )
        .order_by(FoodLog.log_date, FoodLog.id)
    )
    return list(result.scalars().all())


@connection
async def get_total_caloraes_by_date(session, user_id: int, log_date: date) -> int:
    result = await session.execute(
        select(func.sum(FoodLog.calories)).where(
            FoodLog.user_id == user_id, FoodLog.log_date == log_date
        )
    )
    total = result.scalar()
    return 0 or total


###workout logs


@connection
async def create_workout_log(
    session,
    user_id: int,
    workout_type: str,
    duration: int,
    burned_calories: int = 0,
    log_date: Optional[date] = None,
) -> WorkoutLog:
    workout_log = WorkoutLog(
        user_id=user_id,
        workout_type=workout_type,
        duration=duration,
        burned_calories=burned_calories,
        log_date=log_date or date.today(),
    )
    session.add(workout_log)
    return workout_log


@connection
async def get_workout_logs_by_user(session, user_id: int) -> List[WorkoutLog]:
    result = await session.execute(
        select(WorkoutLog)
        .where(WaterLog.user_id == user_id)
        .order_by(WaterLog.log_date.desc())
    )
    return list(result.scalars().all())


###потом можно переделать или удалить, ибо ниже есть отдельно полная статистика за день
### или оставить. тут просто сами записи. а ниже статистика
###
@connection
async def get_workout_logs_by_date(
    session, user_id: int, log_date: date
) -> List[WorkoutLog]:
    result = await session.execute(
        select(WorkoutLog)
        .where(WorkoutLog.user_id == user_id, WorkoutLog.log_date == log_date)
        .order_by(WorkoutLog.id)
    )
    return list(result.scalars().all())


@connection
async def get_workout_logs_by_date_range(
    session, user_id: int, start_date: date, end_date: date
) -> List[WorkoutLog]:
    result = await session.execute(
        select(WorkoutLog)
        .where(
            WorkoutLog.user_id == user_id,
            WorkoutLog.log_date >= start_date,
            WorkoutLog.log_date <= end_date,
        )
        .order_by(WorkoutLog.log_date, WorkoutLog.id)
    )
    return list(result.scalars().all())


@connection
async def get_total_workout_status_by_date(
    session, user_id: int, log_date: date
) -> dict:
    result = await session.execute(
        select(
            func.sum(WorkoutLog.duration),
            func.sum(WorkoutLog.burned_calories),
            func.count(WorkoutLog.id),
        ).where(WorkoutLog.user_id == user_id, WorkoutLog.log_date == log_date)
    )
    duration, calories, count = result.first()
    return {
        "total_duration": duration or 0,
        "total_calories": calories or 0,
        "workout_count": count or 0,
    }


####чем дальеш пишу, тем больеш понимаю, что лучше потом или сразу переделать на Enam,
@connection
async def get_workout_by_type(
    session, user_id: int, workout_type: str
) -> List[WorkoutLog]:
    result = await session.execute(
        select(WorkoutLog)
        .where(WorkoutLog.user_id == user_id, WorkoutLog.workout_type == workout_type)
        .order_by(WorkoutLog.log_date.desc())
    )
    return list(result.scalars().all())


####потом если будет кайф можно дописать удаление и обновленеи


"""
тут общие полезные круды, по типу общей статы за день или промежуток
можно тоже потом дописать додумать

"""


###получение  полной статистики за дату
@connection
async def get_daily_summary(session, user_id: int, log_date: date) -> dict:
    water_result = await session.execute(
        select(func.sum(WaterLog.amount)).where(
            WaterLog.user_id == user_id, WaterLog.log_date == log_date
        )
    )
    water_total = water_result.scalar() or 0
    food_result = await session.execute(
        select(func.sum(FoodLog.calories)).where(
            FoodLog.user_id == user_id, FoodLog.log_date == log_date
        )
    )
    food_calories = food_result.scalar() or 0
    workout_result = await session.execute(
        select(
            func.sum(WorkoutLog.duration), func.sum(WorkoutLog.burned_calories)
        ).where(WorkoutLog.user_id == user_id, WorkoutLog.log_date == log_date)
    )
    workout_duration, workout_calories = workout_result.first()
    return {
        "date": log_date,
        "water_ml": water_total,
        "food_calories": food_calories,
        "workout_duration_min": workout_duration or 0,
        "workout_calories_burned": workout_calories or 0,
        "net_calories": food_calories - (workout_calories or 0),
    }


##получить цели пользователя


@connection
async def get_user_goals(session, user_id: int) -> dict:
    result = await session.execute(
        select(UserBase.water_goal, UserBase.calorie_goal).where(UserBase.id == user_id)
    )
    water_goal, calorie_goal = result.first()
    return {"water_goal": water_goal, "calorie_goal": calorie_goal}
