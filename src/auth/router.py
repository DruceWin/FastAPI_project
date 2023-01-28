from fastapi import APIRouter

from .database import database
from .models import users

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@auth_router.get("/users")
async def get_users():
    query = users.select()
    return await database.fetch_all(query)
