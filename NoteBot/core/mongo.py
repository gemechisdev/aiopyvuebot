"""
Async MongoDB client via Motor.

Exposes `db` after `connect_to_mongo()` has been awaited.
Collections are accessed as `db.notes`, `db.users`, etc.
"""

from __future__ import annotations

import logging
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from config import MONGO_URI, MONGO_DB_NAME

logger = logging.getLogger(__name__)

_client: AsyncIOMotorClient | None = None
db: AsyncIOMotorDatabase | None = None


async def connect_to_mongo() -> None:
    """Open the Motor connection and verify it with a ping."""
    global _client, db

    if not MONGO_URI:
        logger.warning(
            "MONGO_URI is not set – database features will be disabled."
        )
        return

    try:
        _client = AsyncIOMotorClient(MONGO_URI)
        db = _client[MONGO_DB_NAME]
        await _client.admin.command("ping")
        logger.info("Connected to MongoDB (db=%s)", MONGO_DB_NAME)

        # TTL index: automatically delete expired notes
        await db.notes.create_index("expires_at", expireAfterSeconds=0, sparse=True)
        # Compound index for fast per-user note listing
        await db.notes.create_index([("user_id", 1), ("is_pinned", -1), ("created_at", -1)])
        # Full-text search index
        await db.notes.create_index([("title", "text"), ("content", "text")])
    except Exception as exc:
        logger.error("Failed to connect to MongoDB: %s", exc)
        raise


async def close_mongo_connection() -> None:
    """Close the Motor connection."""
    global _client
    if _client is not None:
        _client.close()
        logger.info("Disconnected from MongoDB.")
