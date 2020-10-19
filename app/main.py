from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import db
from .routes import common

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=False,
    allow_methods=['*'],
    allow_headers=['*']
)


@app.on_event('startup')
async def startup():
    await db.connect()


@app.on_event('shutdown')
async def shutdown():
    await db.disconnect()


app.include_router(
    common.router,
    tags=['common']
)
