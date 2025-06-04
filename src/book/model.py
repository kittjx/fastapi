from datetime import datetime
from typing import Optional

from sqlmodel import Column, DateTime, SQLModel, Field, func

class BookBase(SQLModel):
    title: str = Field(max_length=255)
    author: str = Field(max_length=255)
    year: int = Field(ge=1000, le=2025)

class IdBase(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)

class TimestampBase(SQLModel):
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    )

class Book(TimestampBase, BookBase, IdBase, table=True):
    pass

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    title: Optional[str] = Field(default=None, max_length=255)
    author: Optional[str] = Field(default=None, max_length=255)
    year: Optional[int] = Field(default=None, ge=1000, le=2025)
