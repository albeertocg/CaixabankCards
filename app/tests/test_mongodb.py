"""Test MongoDB connection."""

import asyncio
from app.config.database import connect_to_mongo, close_mongo_connection, get_database


async def test_connection():
    """Test MongoDB connection and list collections."""
    try:
        # Connect to database
        await connect_to_mongo()
        
        # Get database instance
        db = get_database()
        
        # List collections
        collections = await db.list_collection_names()
        print(f"\nCollections in database: {collections if collections else 'No collections yet'}")
        
        # Get server info
        db_client = db.client
        server_info = await db_client.server_info()
        print(f"\n MongoDB version: {server_info.get('version')}")
        
        # Close connection
        await close_mongo_connection()
        
        print("\nConnection test completed successfully!")
        
    except Exception as e:
        print(f"\nConnection test failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(test_connection())
