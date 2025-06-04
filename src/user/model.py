from typing import Optional
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(max_length=128)
    email: str = Field(max_length=128)
    phone: str = Field(max_length=32)
