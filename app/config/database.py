"""Database configuration and connection management."""

import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB configuration
MONGODB_URL = os.getenv("MONGODB_URL")

# Global variables for database connection
client: AsyncIOMotorClient | None = None
database = None


async def connect_to_mongo():
    """Connect to MongoDB database."""
    global client, database
    
    try:
        client = AsyncIOMotorClient(
            MONGODB_URL,
            server_api=ServerApi('1')
        )
        
        # Test the connection
        await client.admin.command('ping')
        
        # Get database from URL
        database = client.get_default_database()
        
        print("Successfully connected to MongoDB!")
        print(f"Database: {database.name}")
        
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        raise


async def close_mongo_connection():
    """Close MongoDB connection."""
    global client
    
    if client:
        client.close()
        print("🔌 MongoDB connection closed")


def get_database():
    """Get the database instance."""
    return database
