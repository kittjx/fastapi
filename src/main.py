from fastapi import FastAPI

from contextlib import asynccontextmanager

from core.db import init_db, close_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db(app)
    yield
    await close_db()


app = FastAPI(lifespan=lifespan)

from app.api import student_router
app.include_router(student_router)
