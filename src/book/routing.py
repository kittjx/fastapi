from fastapi import APIRouter
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends

from db.session import get_async_session
from .model import Book

book_router = APIRouter(
    prefix="/book",
    tags=["book"],
    responses={404: {"description": "Not found"}},
)

@book_router.get("/")
async def list_books():
    return {"message": "list books"}

@book_router.get("/{book_id}")
async def get_book(book_id: int):
    return {"message": f"get book {book_id}"}

@book_router.post("/", response_model=Book)
async def create_book(book: Book, session: AsyncSession = Depends(get_async_session)):
    session.add(book)
    await session.commit()
    await session.refresh(book)
    return book

@book_router.put("/{book_id}")
async def create_book(book: Book):
    return {"message": f"update book {book.title}"}
