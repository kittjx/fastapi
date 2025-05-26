from fastapi import FastAPI
from book.routing import book_router

from contextlib import asynccontextmanager

from db.session import init_db, async_engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await async_engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(book_router)
