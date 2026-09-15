import logging

from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.router import api_router
from app.core.config import get_settings
from app.core.logging import setup_logging


setup_logging()

logger = logging.getLogger(__name__)
settings = get_settings()

@asynccontextmanager
async def lifespan(app:FastAPI):
    logger.info(
        "Starting %s version %s",
        settings.app_name,
        settings.app_version,
    )
    
    yield
    
    logger.info(
        "Shutting down %s",
        settings.app_name,
    )

app=FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)

app.include_router(
    api_router,
    prefix="/api/v1")

@app.get("/")
def root() -> dict[str,str]:
    return {
        "message":"Enterprise RAG Agent is running."
    }
    