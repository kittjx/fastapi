import os
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker

DB_URL = os.environ.get("DB_URL")
if not DB_URL:
    raise ValueError("DB_URL is not set")

async_engine: AsyncEngine = create_async_engine(
    DB_URL, 
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    echo=True
)

async_session = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_async_session():
    async with async_session() as session:
        yield session
