import logging
import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from __version__ import __version__
from core.routes import router as core_router
from database import close_connection
from folders.routes import router as folder_router
from notes.routes import router as note_router
from settings import settings

logger = logging.getLogger(__name__)

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(module)s] [%(funcName)s] - %(message)s",
)


@asynccontextmanager
async def lifespan(app: "FastAPI"):
    yield
    await close_connection()


DOCS_URL = "/api/docs"
app = FastAPI(
    lifespan=lifespan, title="Notes API", version=__version__, docs_url=DOCS_URL
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
for router in [core_router, note_router, folder_router]:
    app.include_router(router)


@app.get("/", include_in_schema=False)
async def home():
    return RedirectResponse(url=DOCS_URL)


if __name__ == "__main__":
    uvicorn.run(
        app="main:app", host=settings.HOST, reload=settings.RELOAD, port=settings.PORT
    )
