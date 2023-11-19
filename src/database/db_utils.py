# Created by https://t.me/vlasovdev db_utils file | Создано https://t.me/vlasovdev db_utils file


from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from database.models import Base
from settings import settings


async def create_tables(engine: AsyncEngine):
    """
    Create database tables
    """

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def create_engine() -> AsyncEngine:
    return create_async_engine(
        url=settings.postgres_dsn,
        future=True,
        pool_size=30,
    )


def create_session(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine, expire_on_commit=False, autoflush=False)
