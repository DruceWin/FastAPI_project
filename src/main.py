from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware

from auth.router import auth_router
from database import database
from app_admin.router import admin_router

app = FastAPI(title='auth')
app.include_router(auth_router)
app.include_router(admin_router)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount('/static', StaticFiles(directory='static'))

templates = Jinja2Templates('templates')


@app.get('/login_form', response_class=HTMLResponse)
async def get_login_form(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})


@app.get('/user_page', response_class=HTMLResponse)
async def get_user_page(request: Request):
    return templates.TemplateResponse('user_page.html', {'request': request})


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
def my_func():
    return {'hi': 'bitch'}
