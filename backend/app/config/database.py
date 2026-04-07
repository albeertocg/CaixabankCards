from typing import Any

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.config.settings import settings

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
        print(f"Conectado a MongoDB: {settings.mongo_db_name}")
    except Exception as e:
        print(f"Error conectando a MongoDB: {e}")
        raise


async def close_db() -> None:
    """Close MongoDB connection during application shutdown."""
    client.close()
    print("Conexion a MongoDB cerrada")
