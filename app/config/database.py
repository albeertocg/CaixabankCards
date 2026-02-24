from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "caixabank_cards")

client = AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB_NAME]


async def connect_db():
    """Verificar conexión a MongoDB al iniciar."""
    try:
        await client.admin.command("ping")
        print(f"✅ Conectado a MongoDB: {MONGO_DB_NAME}")
    except Exception as e:
        print(f"❌ Error conectando a MongoDB: {e}")
        raise e


async def close_db():
    """Cerrar conexión a MongoDB."""
    client.close()
    print("🔌 Conexión a MongoDB cerrada")
