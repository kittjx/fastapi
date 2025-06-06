from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlmodel import select

from jose import jwt, JWTError

from db.session import DBSession
from auth.model import TokenData
from user.model import User

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
    
    result = await session.exec(select(User).where(User.username == username))
    user = result.one_or_none()
    if user is None:
        raise credential_exception
    return user


async def verify_current_user(current_user: User = Depends(get_current_user)) -> User:
    # if not current_user.is_active:
    #     raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
