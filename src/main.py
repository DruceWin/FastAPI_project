from fastapi import FastAPI

from auth.router import auth_router
from database import database

app = FastAPI(title='auth')
app.include_router(auth_router)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
def my_func():
    return {'hi': 'bitch'}
