from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.core.config import settings

async_engine = create_async_engine(settings.DATABASE_URL)
AsyncSessionLocal = async_sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

async def get_db() -> AsyncSession:
    """Получить сессию БД"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def get_db_background() -> AsyncSession:
    """Сессия для фоновых задач (без автоматического закрытия через генератор)"""
    async with AsyncSessionLocal() as session:
        yield session
