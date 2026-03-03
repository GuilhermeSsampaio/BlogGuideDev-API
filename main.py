from contextlib import asynccontextmanager
from fastapi import FastAPI
from config.db import create_db_and_tables
from config.settings import API_TITLE, API_VERSION
from config.middlewares import setup_middlewares
from config.routers import setup_routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(title=API_TITLE, version=API_VERSION, lifespan=lifespan)

setup_middlewares(app)
setup_routers(app)


@app.get("/")
async def root():
    return {"Bem vindo": "GuiSamp api"}
