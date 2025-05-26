from sqlmodel import SQLModel, Field

class Book(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(min_length=3, max_length=255)
    author: str = Field(min_length=3, max_length=255)
    year: int = Field(ge=1000, le=2025)
