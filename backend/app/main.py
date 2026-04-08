from asyncio import get_running_loop
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.database import connect_db, close_db
from app.config.settings import settings
from app.routes.auth_routes import router as auth_router
from app.routes.card_routes import router as card_router
from app.routes.chat_routes import router as chat_router
from app.agent.rag.indexer import ensure_indexed


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()

    if settings.google_api_key and settings.google_api_key.strip():
        loop = get_running_loop()
        await loop.run_in_executor(None, ensure_indexed)
    yield
    await close_db()


app = FastAPI(title="CaixabankCards API", lifespan=lifespan)

# CORS - permitir peticiones del frontend (Next.js)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas
app.include_router(auth_router)
app.include_router(card_router)
app.include_router(chat_router)
