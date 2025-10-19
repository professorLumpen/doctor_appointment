from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import settings


class Base(DeclarativeBase):
    pass


engine = create_async_engine(settings.db_url)
session_maker = async_sessionmaker(engine)


async def get_session():
    async with session_maker() as session:
        yield session
