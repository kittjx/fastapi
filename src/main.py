from fastapi import FastAPI
from book.router import book_router

from contextlib import asynccontextmanager

from db.session import async_engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # use alembic to do the migrations
    # await init_db()
    yield
    await async_engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(book_router)
