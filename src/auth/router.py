from fastapi import APIRouter

from .database import database
from .models import users
from .schemas import UserIn

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@auth_router.get("/users")
async def get_users():
    query = users.select()
    return await database.fetch_all(query)


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
