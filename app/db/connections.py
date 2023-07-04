import os
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

DATABASE_URL = os.environ.get("DATABASE_URL")
engine: AsyncEngine = create_async_engine(DATABASE_URL)  # type: ignore
async_session = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency used to supply database session."""
    async with async_session() as session:
        yield session
