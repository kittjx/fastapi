from typing import Optional
from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    username: str = Field(unique=True, max_length=128)
    email: str = Field(max_length=128)
    phone: str = Field(max_length=32)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    passwd_hash: str = Field(max_length=255, exclude=True)

class UserCreate(UserBase):
    password: str = Field(max_length=255)

class UserUpdate(SQLModel):
    email: Optional[str] = Field(default=None, max_length=128)
    phone: Optional[str] = Field(default=None, max_length=32)
