from datetime import datetime
from typing import Optional

from sqlmodel import Column, DateTime, SQLModel, Field, func


class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(min_length=3, max_length=255)
    author: str = Field(min_length=3, max_length=255)
    year: int = Field(ge=1000, le=2025)

    create_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    )
    update_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    )


class BookUpdate(Book):
    title: Optional[str] = None
    author: Optional[str] = None
