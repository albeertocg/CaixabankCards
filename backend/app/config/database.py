from typing import Any

import logging

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.config.settings import settings

logger = logging.getLogger(__name__)

client: AsyncIOMotorClient[dict[str, Any]] = AsyncIOMotorClient(settings.mongo_uri)
db: AsyncIOMotorDatabase[dict[str, Any]] = client[settings.mongo_db_name]


async def connect_db() -> None:
    """Connect to MongoDB and verify connection.

    Pings the database to confirm connectivity during application startup.

    Raises:
        Exception: If MongoDB connection fails.
    """
    try:
        await client.admin.command("ping")
        logger.info("Conectado a MongoDB: %s", settings.mongo_db_name)
    except Exception as e:
        logger.error("Error conectando a MongoDB: %s", e)
        raise


async def close_db() -> None:
    """Close MongoDB connection during application shutdown."""
    client.close()
    logger.info("Conexion a MongoDB cerrada")
