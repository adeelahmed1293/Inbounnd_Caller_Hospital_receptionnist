"""MongoDB connection and utilities."""

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ServerSelectionTimeoutError
import os
from typing import Optional

class MongoDB:
    _client: Optional[AsyncIOMotorClient] = None
    _db = None
    
    @classmethod
    async def connect(cls):
        """Connect to MongoDB."""
        if cls._client is None:
            mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
            db_name = os.getenv("MONGODB_DB_NAME", "hospital_db")
            
            try:
                cls._client = AsyncIOMotorClient(mongodb_url, serverSelectionTimeoutMS=5000)
                # Test connection
                await cls._client.admin.command('ping')
                cls._db = cls._client[db_name]
                print(f"✅ Connected to MongoDB: {db_name}")
            except ServerSelectionTimeoutError:
                print("❌ Failed to connect to MongoDB")
                raise
    
    @classmethod
    def get_db(cls):
        """Get database instance."""
        if cls._db is None:
            raise RuntimeError("Database not connected. Call MongoDB.connect() first.")
        return cls._db
    
    @classmethod
    async def close(cls):
        """Close MongoDB connection."""
        if cls._client:
            cls._client.close()
            print("✅ MongoDB connection closed")

# Collections
def get_doctors_collection():
    return MongoDB.get_db()["doctors"]

def get_appointments_collection():
    return MongoDB.get_db()["appointments"]

def get_departments_collection():
    return MongoDB.get_db()["departments"]

def get_patients_collection():
    return MongoDB.get_db()["patients"]