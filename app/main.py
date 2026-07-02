from fastapi import FastAPI

from app.api.v1.router import api_router

from app.core.config import settings
from app.core.exceptions import global_exception_handler

from app.middleware.logging_middleware import LoggingMiddleware

app = FastAPI(
title=settings.APP_NAME,
version=settings.APP_VERSION
)

app.add_middleware(LoggingMiddleware)

app.add_exception_handler(
Exception,
global_exception_handler
)

app.include_router(
api_router,
prefix=settings.API_V1_PREFIX
)

@app.get("/")
async def root():
    return {
    "message": "Backend Running Successfully"
    }
