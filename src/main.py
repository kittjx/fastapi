from fastapi import FastAPI
from src.book.book import book_router

app = FastAPI()

app.include_router(book_router)
