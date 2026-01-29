from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from bot.config import settings


engine = create_async_engine(settings.DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


def connection(method):
    async def wrapper(*args, **kwargs):
        async with async_session_maker() as session:
            try:
                result = await method(*args, session=session, **kwargs)
                await session.commit()
                return result
            except Exception:
                await session.rollback()
                raise
            # finally:
            #     await session.close()

    return wrapper
