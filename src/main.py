from fastapi import FastAPI

from auth.router import auth_router

app = FastAPI(title='auth')
app.include_router(auth_router)


@app.get("/")
def my_func():
    return {'hi': 'bitch'}
