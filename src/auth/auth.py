from datetime import datetime, timedelta
from functools import wraps
from typing import List, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlmodel import select

from jose import jwt, JWTError

from db.session import DBSession
from auth.model import TokenData
from user.model import Permission, Role, RolePermissionLink, User, UserRoleLink
from sqlalchemy.orm import selectinload # Import selectinload

import os
SECRET_KEY = os.getenv("SECRET_KEY", "BdvXAT8C7Ij5GixGsvGc_QyFG7n9E5B5KVB25b4eTGk")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_passwd_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_passwd: str, hash_passwd: str) -> bool:
    return pwd_context.verify(plain_passwd, hash_passwd)

async def authenticate_user(session: DBSession, username: str, password: str) -> Optional[User]:
    result = await session.exec(select(User).where(User.username == username))
    user = result.one_or_none()
    if not user or not verify_password(password, user.passwd_hash):
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(session: DBSession, token: str = Depends(oauth2_scheme)) -> User:
    credential_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise credential_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credential_exception
    
    # ensure that the user.roles relationship is loaded asynchronously before it's accessed. 
    # This can be done using selectinload or joinedload with the select statement that fetches the User object.
    # Eagerly load the 'roles' relationship to avoid MissingGreenlet error on lazy load
    statement = select(User).where(User.username == username).options(selectinload(User.roles))
    result = await session.exec(statement)
    user = result.one_or_none()
    if user is None:
        raise credential_exception
    return user


async def verify_current_user(current_user: User = Depends(get_current_user)) -> User:
    # if not current_user.is_active:
    #     raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def get_user_permissions(user: User, session: DBSession) -> List[str]:
    # This is a lazy load of a relationship.
    # Even though get_user_permissions is async and session.exec is awaited, 
    # the problem is that user.roles is being accessed 
    # before an explicit await on a session operation that would load it. 
    # When user.roles is accessed, SQLAlchemy tries to lazy-load the relationship, 
    # and if the session is an AsyncSession, 
    # this lazy load itself becomes an awaitable operation. 
    # Since it's not explicitly awaited, and it's happening implicitly during attribute access, 
    # it causes the MissingGreenlet error.
    if not user.roles:
        return []
    
    role_ids = [role.id for role in user.roles]
    
    # Query to get all permissions for all user's roles
    statement = (
        select(Permission.name)
        .join(RolePermissionLink)
        .where(RolePermissionLink.role_id.in_(role_ids))
        .distinct()  # Remove duplicates if user has overlapping permissions
    )
    permissions = await session.exec(statement)
    return list(permissions.all())


def RequirePermission(permission_name: str):
    async def check_permission(
            session: DBSession, 
            current_user: User = Depends(get_current_user)):
        user_permissions = await get_user_permissions(current_user, session)
        print("checking permission.......................")
        if permission_name not in user_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied. Required: {permission_name}"
            )
        return current_user
    
    return check_permission


# Helper functions for role management
async def assign_role_to_user(user_id: int, role_id: int, session: DBSession):
    """Assign a role to a user"""
    # Check if the relationship already exists
    result = await session.exec(
        select(UserRoleLink).where(
            UserRoleLink.user_id == user_id,
            UserRoleLink.role_id == role_id
        )
    )
    existing = result.one_or_none()
    
    if not existing:
        link = UserRoleLink(user_id=user_id, role_id=role_id)
        session.add(link)
        await session.commit()

async def remove_role_from_user(user_id: int, role_id: int, session: DBSession):
    """Remove a role from a user"""
    result = await session.exec(
        select(UserRoleLink).where(
            UserRoleLink.user_id == user_id,
            UserRoleLink.role_id == role_id
        )
    )
    link = result.one_or_none()
    
    if link:
        await session.delete(link)
        await session.commit()

async def get_user_roles(user_id: int, session: DBSession) -> List[Role]:
    """Get all roles for a user"""
    statement = (
        select(Role)
        .join(UserRoleLink)
        .where(UserRoleLink.user_id == user_id)
    )
    result = await session.exec(statement)
    return list(result.all())
