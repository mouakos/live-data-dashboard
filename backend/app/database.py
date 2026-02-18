"""Database connection manager."""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.config import settings

engine = create_async_engine(settings.database_url, echo=settings.database_echo)
session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession]:
    """Provide an async database session for dependency injection.

    This function is designed to be used as a FastAPI dependency to inject
    database sessions into route handlers. The session is automatically
    closed after the request is processed.

    Yields:
        AsyncGenerator[AsyncSession, None, None]: An async generator that yields an asynchronous database session.
    """
    db: AsyncSession = session_maker()
    try:
        yield db
    finally:
        await db.close()


async def init_db() -> None:
    """Initialize the database by creating all tables."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
