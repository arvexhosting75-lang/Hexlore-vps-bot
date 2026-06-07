"""MongoDB connection management"""

import asyncio
from motor.motor_asyncio import AsyncClient, AsyncDatabase
from typing import Optional
from utils.logger import get_logger

logger = get_logger(__name__)

# Global database connection
_db_connection: Optional[AsyncDatabase] = None
_client: Optional[AsyncClient] = None


async def connect_database(uri: str, db_name: str) -> AsyncDatabase:
    """Connect to MongoDB

    Args:
        uri: MongoDB connection URI
        db_name: Database name

    Returns:
        AsyncDatabase instance
    """
    global _db_connection, _client

    try:
        _client = AsyncClient(uri, serverSelectionTimeoutMS=5000)

        # Verify connection
        await _client.admin.command("ping")
        logger.info("MongoDB connection verified")

        _db_connection = _client[db_name]
        return _db_connection

    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise


async def close_database() -> None:
    """Close MongoDB connection"""
    global _client

    if _client:
        _client.close()
        logger.info("MongoDB connection closed")


def get_database() -> AsyncDatabase:
    """Get current database connection

    Returns:
        AsyncDatabase instance
    """
    if not _db_connection:
        raise RuntimeError("Database not connected")
    return _db_connection
