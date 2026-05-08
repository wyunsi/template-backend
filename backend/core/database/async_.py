from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from core.config import settings

engine = create_async_engine(
    settings.db.url,
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow,
    pool_pre_ping=settings.db.pool_pre_ping,
    pool_recycle=settings.db.pool_recycle,
    pool_timeout=settings.db.pool_timeout,
    echo=settings.db.echo,
)

async_session_factory = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession]:
    async with async_session_factory() as session:
        try:
            yield session
            if session.in_transaction():
                await session.commit()
        except Exception:
            await session.rollback()
            raise
