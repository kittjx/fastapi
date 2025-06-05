
from fastapi import APIRouter, HTTPException
from sqlmodel import select

from db.session import DBSession
from user.model import User, UserUpdate


user_router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)


@user_router.get("/", response_model=list[User])
async def list_users(session: DBSession):
    result = await session.exec(select(User))
    users = result.all()
    return users


@user_router.get("/{user_id}", response_model=User)
async def get_user(user_id: int, session: DBSession):
    # optimized for primary key
    user = await session.get(User, user_id)
    # general query
    # result = await session.exec(select(User).where(User.id == user_id))
    # user = result.one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, user_update: UserUpdate, session: DBSession):
    db_user = await session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    updates = user_update.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(db_user, field, value)

    await session.commit()
    await session.refresh(db_user)
    return db_user


@user_router.delete("/{user_id}", response_model=User)
async def delete_user(user_id: int, session: DBSession):
    db_user = await session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    await session.delete(db_user)
    await session.commit()
    return db_user
