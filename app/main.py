from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.config.database import connect_to_mongo, close_mongo_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle."""
    # Startup
    await connect_to_mongo()
    yield
    # Shutdown
    await close_mongo_connection()


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"message": "CaixaBank Cards API"}
