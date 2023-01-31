from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from database import database, get_session
from .models import users
from .schemas import UserIn, User

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@auth_router.get("/users")
async def get_users():
    query = users.select()
    return await database.fetch_all(query)


@auth_router.get("/users_alch")
async def get_users_by_sql_alch(session: AsyncSession = Depends(get_session)) -> List[User]:
    query = select(users)
    print(query)
    result = await session.execute(query)
    return result.all()


@auth_router.post("/users_alch")
async def get_users_by_sql_alch(user: UserIn, session: AsyncSession = Depends(get_session)) -> List[User]:
    query = insert(users).values(
        email=user.email,
        username=user.username,
        password=user.password,
        first_name=user.name,
        second_name=user.surname,
        role_id=user.role_id,
    )
    print(query)
    await session.execute(query)
    await session.commit()
    return {'result.all()'}


@auth_router.post("/users")
async def create_users(user: UserIn):
    query = users.insert().values(
        email=user.email,
        username=user.username,
        password=user.password,
        first_name=user.name,
        second_name=user.surname,
        role_id=user.role_id,
    )
    last_record_id = await database.execute(query)
    return {**user.dict(), 'id': last_record_id}
