from fastapi import FastAPI
from src.book.router import book_router
from src.user.router import user_router
from src.auth.router import auth_router

from contextlib import asynccontextmanager

from src.db.session import async_engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # use alembic to do the migrations
    # await init_db()
    yield
    await async_engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(book_router)
app.include_router(user_router)
app.include_router(auth_router)
