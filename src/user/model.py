from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class UserRoleLink(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", primary_key=True)
    role_id: Optional[int] = Field(default=None, foreign_key="role.id", primary_key=True)

class Role(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, max_length=64)
    users: List["User"] = Relationship(back_populates="roles", link_model=UserRoleLink)

class UserBase(SQLModel):
    username: str = Field(unique=True, max_length=128)
    email: str = Field(max_length=128)
    phone: str = Field(max_length=32)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    passwd_hash: str = Field(max_length=255, exclude=True)
    roles: List["Role"] = Relationship(back_populates="users", link_model=UserRoleLink)

class UserCreate(UserBase):
    password: str = Field(max_length=255)

class UserUpdate(SQLModel):
    email: Optional[str] = Field(default=None, max_length=128)
    phone: Optional[str] = Field(default=None, max_length=32)
