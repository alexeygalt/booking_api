from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

if settings.MODE == "TEST":
    DATABASE_URL = settings.get_test_database_url
    DATABASE_PARAMS = {"poolclass": NullPool}

else:
    DATABASE_URL = settings.get_database_url
    DATABASE_PARAMS = {}

engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)

# async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


# Base = declarative_base()

class Base(DeclarativeBase):
    pass


async def get_session() -> async_session_maker:
    async with async_session_maker() as session:
        yield session
