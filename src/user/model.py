from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class RolePermissionLink(SQLModel, table=True):
    role_id: Optional[int] = Field(default=None, foreign_key="role.id", primary_key=True)
    permission_id: Optional[int] = Field(default=None, foreign_key="permission.id", primary_key=True)


class Permission(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, max_length=64)  # e.g., "users.read", "books.write"
    description: Optional[str] = Field(default=None, max_length=255)
    
    roles: List["Role"] = Relationship(back_populates="permissions", link_model=RolePermissionLink)


class UserRoleLink(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", primary_key=True)
    role_id: Optional[int] = Field(default=None, foreign_key="role.id", primary_key=True)


class Role(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, max_length=64)
    description: Optional[str] = Field(default=None, max_length=255)
    
    users: List["User"] = Relationship(back_populates="roles", link_model=UserRoleLink)
    permissions: List["Permission"] = Relationship(back_populates="roles", link_model=RolePermissionLink)


class UserBase(SQLModel):
    username: str = Field(unique=True, max_length=128)
    email: str = Field(max_length=128)
    phone: str = Field(max_length=32)


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    passwd_hash: str = Field(max_length=255, exclude=True)
    roles: List["Role"] = Relationship(back_populates="users", link_model=UserRoleLink)



# schemas

class UserCreate(UserBase):
    password: str = Field(max_length=255)


class UserUpdate(SQLModel):
    email: Optional[str] = Field(default=None, max_length=128)
    phone: Optional[str] = Field(default=None, max_length=32)

