from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from db.session import DBSession
from auth.auth import authenticate_user, create_access_token, get_current_user, get_passwd_hash
from auth.model import Token, UserLogin
from user.model import User, UserCreate

from auth.auth import ACCESS_TOKEN_EXPIRE_MINUTES

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@auth_router.post("/register", response_model=User)
async def create_user(user: UserCreate, session: DBSession):
    result = await session.exec(
        select(User).where(User.username == user.username))
    db_user = result.one_or_none()
    if db_user:
        raise HTTPException(status_code=400, detail=f"User {user.username} already registered")

    new_user = User(
        **user.model_dump(exclude={"password"}),
        passwd_hash=get_passwd_hash(user.password)
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


@auth_router.post("/login", response_model=Token)
async def login(
    session: DBSession,
    user: UserLogin
):
    user = await authenticate_user(session, user.username, user.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@auth_router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
