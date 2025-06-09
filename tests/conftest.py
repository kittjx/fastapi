import pytest
import pytest_asyncio # Import pytest_asyncio
from fastapi.testclient import TestClient
from sqlmodel import create_engine, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker
import asyncio

from src.main import app
from src.db.session import get_async_session
from src.user.model import User # Import User model for table creation

# Use an in-memory SQLite database for testing
sqlite_file_name = "test.db"
sqlite_url = f"sqlite+aiosqlite:///{sqlite_file_name}" # Use aiosqlite for async
async_engine: AsyncEngine = create_async_engine(sqlite_url, echo=False)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

@pytest_asyncio.fixture(name="session") # Use pytest_asyncio.fixture
async def session_fixture():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    async with TestingSessionLocal() as session:
        yield session
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

@pytest_asyncio.fixture(name="client") # Use pytest_asyncio.fixture
async def client_fixture(session: AsyncSession):
    app.dependency_overrides[get_async_session] = lambda: session
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
