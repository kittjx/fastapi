from fastapi import APIRouter
from pydantic import BaseModel, Field

book_router = APIRouter(
    prefix="/book",
    tags=["book"],
    responses={404: {"description": "Not found"}},
)

class Book(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    author: str = Field(..., min_length=3, max_length=255)
    year: int = Field(..., ge=1000, le=2025)

@book_router.get("/")
async def list_books():
    return {"message": "list books"}

@book_router.get("/{book_id}")
async def get_book(book_id: int):
    return {"message": f"get book {book_id}"}

@book_router.post("/")
async def create_book(book: Book):
    return {"message": f"create book {book.title}"}

@book_router.put("/{book_id}")
async def create_book(book: Book):
    return {"message": f"update book {book.title}"}
