from fastapi import APIRouter

from app.agent.data.card_catalog import CARD_CATALOG

router = APIRouter(prefix="/api/cards", tags=["Cards"])


@router.get("/catalog")
async def get_catalog() -> list:
    return CARD_CATALOG
