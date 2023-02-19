import datetime
from typing import List

from fastapi import APIRouter, Depends, Form, HTTPException
from jose import jwt, ExpiredSignatureError
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database import database, get_session
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response

from .models import users
from .schemas import UserIn, User, UserPatch, UserLogin

from .service import Auth

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

auth = Auth()


@auth_router.post('/login')
async def user_login(data: UserLogin, session: AsyncSession = Depends(get_session)):
    try:
        user = select(users).where(users.c.email == data.email)
        get_user = await session.execute(user)
        if data.password == get_user.fetchone()[3]:
            access_token = auth.encode_access_token(data.email)
            refresh_token = auth.encode_refresh_token(data.email)
            return {'access_token': access_token, 'refresh_token': refresh_token}
        else:
            raise HTTPException(status_code=401, detail='Email or password not valid')
    except Exception:
        raise HTTPException(status_code=401, detail='Email or password not valid')


@auth_router.get('/refresh')
async def refresh_token(request: Request):
    refresh_token = request.cookies.get('refresh')
    return auth.get_new_refresh_or_401(refresh_token)


@auth_router.get('/authorization')
async def authorization(request: Request):
    print(request.cookies)
    # access_token = request.cookies.get('access_token')
    # print(access_token)
    # return auth.decode_access_token(access_token)
    return {'ok': 1}




# starii code
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

secret = 'my_secret'


@auth_router.post('/old_login')
async def user_login(
        form_data: UserLogin,
        # email: str = Form(),
        # password: str = Form(),
        session: AsyncSession = Depends(get_session)):
    try:
        user = select(users).where(users.c.email == form_data.email)
        # user = select(users).where(users.c.email == email)
        get_user = await session.execute(user)
        if form_data.password == get_user.fetchone()[3]:
        # if password == get_user.fetchone()[3]:
            access = jwt.encode({'email': form_data.email,
                                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1)},
                                secret, algorithm='HS256')
            refresh = jwt.encode({'email': form_data.email,
                                 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5)},
                                 secret, algorithm='HS256')
            # return RedirectResponse('/user_page', status_code=301)
            return {
                'access': access,
                'refresh': refresh
                    }
        else:
            return {'message': 'email or password not valid'}
    except Exception:
        return {'message': 'email or password not valid'}


@auth_router.get('/auth_token')
async def toke_auth(request: Request, session: AsyncSession = Depends((get_session))):
    try:
        access_token = request.cookies.get('access')
        jwt.decode(access_token, secret, algorithms=['HS256'])
        return {'ok'}
    except ExpiredSignatureError:
        return {'time expired'}


@auth_router.get('/refresh_token')
async def toke_auth(request: Request, session: AsyncSession = Depends((get_session))):
    try:
        refresh_token = request.cookies.get('refresh')
        payload = jwt.decode(refresh_token, secret, algorithms=['HS256'])
        access = jwt.encode(payload | {'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1)},
                            secret, algorithm='HS256')
        refresh = jwt.encode(payload | {'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5)},
                             secret, algorithm='HS256')
        return {
                'access': access,
                'refresh': refresh
                    }
    except ExpiredSignatureError:
        return {'time expired'}
