# app/main.py

from fastapi import FastAPI
from app.core.config import settings
from app.api.endpoints import langchain
from app.utils.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(langchain.router, prefix=settings.API_V1_STR)