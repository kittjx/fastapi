from typing import Any, Dict
from fastapi import APIRouter, HTTPException
from sqlmodel import select

from db.session import DBSession

from .model import Book, BookUpdate

book_router = APIRouter(
    prefix="/book",
    tags=["book"],
    responses={404: {"description": "Not found"}},
)

@book_router.get("/", response_model=list[Book])
async def list_books(session: DBSession):
    result = await session.exec(select(Book))
    books = result.all()
    return books

@book_router.get("/{book_id}", response_model=Book)
async def get_book(book_id: int, session: DBSession):
    # optimized for primary key
    book = await session.get(Book, book_id)
    # general query
    # result = await session.exec(select(Book).where(Book.id == book_id))
    # book = result.one_or_none()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@book_router.post("/", response_model=Book)
async def create_book(book: Book, session: DBSession):
    session.add(book)
    await session.commit()
    await session.refresh(book)
    return book

@book_router.put("/{book_id}", response_model=Book)
async def update_book(book_id: int, book_update: BookUpdate, session: DBSession):
    db_book = await session.get(Book, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    updates = book_update.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(db_book, field, value)

    await session.commit()
    await session.refresh(db_book)
    return db_book

@book_router.delete("/{book_id}", response_model=Book)
async def delete_book(book_id: int, session: DBSession):
    db_book = await session.get(Book, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    await session.delete(db_book)
    await session.commit()
    return db_book

