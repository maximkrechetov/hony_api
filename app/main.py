from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from os import environ
# from starlette.middleware.sessions import SessionMiddleware
from .database import engine, SessionLocal
from .routes import common, auth, user
from .models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=False,
    allow_methods=['*'],
    allow_headers=['*']
)
# app.add_middleware(SessionMiddleware, secret_key=environ.get('SECRET_KEY'))


app.include_router(common.router, tags=['common'])
app.include_router(auth.router, tags=['auth'])
app.include_router(user.router, tags=['user'])
