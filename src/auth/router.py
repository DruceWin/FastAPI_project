from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database import database, get_session
from .models import users
from .schemas import UserIn, User, UserPatch

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@auth_router.get("/users/{id}")
async def get_user_by_id(id: int, session: AsyncSession = Depends(get_session)) -> User:
    user = select(users).where(users.c.id == id)
    result = await session.execute(user)
    print(dir(result))
    return result.first()


@auth_router.delete("/users/{id}")
async def delete_user_by_id(id: int, session: AsyncSession = Depends(get_session)):
    user = delete(users).where(users.c.id == id)
    await session.execute(user)
    await session.commit()
    return {'delete'}


@auth_router.patch("/users/{id}")
async def patch_user_by_id(id: int, user: UserPatch, session: AsyncSession = Depends(get_session)):
    user_dict = dict(user)
    for i in user_dict.copy():
        if user_dict[i] is None:
            user_dict.pop(i)
    user = update(users).where(users.c.id == id).values(**user_dict)
    await session.execute(user)
    await session.commit()
    user = select(users).where(users.c.id == id)
    result = await session.execute(user)
    return result.first()


@auth_router.get("/users")
async def get_users():
    query = users.select()
    return await database.fetch_all(query)


@auth_router.get("/users_alch")
async def get_users_by_sql_alch(session: AsyncSession = Depends(get_session)) -> List[User]:
    query = select(users)
    result = await session.execute(query)
    return result.all()


@auth_router.post("/users_alch")
async def post_users_by_sql_alch(user: UserIn, session: AsyncSession = Depends(get_session)) -> List[User]:
    query = insert(users).values(
        email=user.email,
        username=user.username,
        password=user.password,
        first_name=user.first_name,
        second_name=user.second_name,
        role_id=user.role_id,
    )
    await session.execute(query)
    await session.commit()
    return {'result.all()'}


@auth_router.post("/users")
async def create_users(user: UserIn):
    query = users.insert().values(
        email=user.email,
        username=user.username,
        password=user.password,
        first_name=user.first_name,
        second_name=user.second_name,
        role_id=user.role_id,
    )
    last_record_id = await database.execute(query)
    return {**user.dict(), 'id': last_record_id}
