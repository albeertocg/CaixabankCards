from motor.motor_asyncio import AsyncIOMotorClient

from app.config.settings import settings

client = AsyncIOMotorClient(settings.mongo_uri)
db = client[settings.mongo_db_name]


async def connect_db() -> None:
    try:
        await client.admin.command("ping")
        print(f"Conectado a MongoDB: {settings.mongo_db_name}")
    except Exception as e:
        print(f"Error conectando a MongoDB: {e}")
        raise


async def close_db() -> None:
    client.close()
    print("Conexion a MongoDB cerrada")
