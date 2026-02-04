# tests/conftest.py
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import delete

from bot.database.models import Base, FoodLog, UserBase, WaterLog, WorkoutLog
from bot.database.crud.user import create_user
from bot.database.models import GenderEnum


@pytest_asyncio.fixture(autouse=True)
async def clear_tables(async_session):
    yield
    await async_session.execute(delete(FoodLog))
    await async_session.execute(delete(WaterLog))
    await async_session.execute(delete(WorkoutLog))
    await async_session.execute(delete(UserBase))
    await async_session.commit()


@pytest_asyncio.fixture(scope="session")
async def test_engine():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def async_session(test_engine):
    async_session_factory = async_sessionmaker(test_engine, expire_on_commit=False)
    async with async_session_factory() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture(scope="function")
async def test_user(async_session: AsyncSession):
    user = await create_user(
        async_session,
        telegram_id=999999999,
        weight=75.0,
        height=175.0,
        age=30,
        city="TestCity",
        gender=GenderEnum.MALE,
        water_goal=2500,
        calorie_goal=2200,
        activity_minutes=60,
    )
    await async_session.commit()
    await async_session.refresh(user)

    yield user

    await async_session.execute(delete(UserBase).where(UserBase.id == user.id))
    await async_session.commit()
