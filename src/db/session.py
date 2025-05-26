import os
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker

DB_URL = os.environ["DB_URL"]

async_engine: AsyncEngine = create_async_engine(DB_URL, echo=True)

async_session = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_db():
    async with async_engine.begin() as conn:
        print("Initializing database", DB_URL)
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_async_session():
    async with async_session() as session:
        yield session
