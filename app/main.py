from fastapi import FastAPI

from app.core.config import settings
from app.core.database import Base
from app.core.database import engine

from app.models import User

Base.metadata.create_all(bind=engine)

app = FastAPI(
title=settings.APP_NAME,
version=settings.APP_VERSION
)

@app.get("/")
async def root():
    return {
    "message": "Backend Running Successfully"
    }
