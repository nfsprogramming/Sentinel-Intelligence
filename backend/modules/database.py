from pymongo import MongoClient
import os
import logging

logger = logging.getLogger("sentinel.db")

class DatabaseManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance.client = None
            cls._instance.db = None
            cls._instance._connect()
        return cls._instance

    def _connect(self):
        # Default to local, or use env var for Atlas
        mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
        try:
            self.client = MongoClient(mongo_uri, serverSelectionTimeoutMS=2000)
            # Trigger connection check
            self.client.server_info()
            self.db = self.client["sentinel_intelligence"]
            logger.info(f"✅ Connected to MongoDB at {mongo_uri}")
        except Exception as e:
            logger.warning(f"⚠️ MongoDB Connection Failed: {e}. Falling back to file storage.")
            self.client = None
            self.db = None

    def is_connected(self):
        return self.db is not None

    def get_collection(self, name):
        if self.db is not None:
            return self.db[name]
        return None

# Global instance
db_manager = DatabaseManager()
