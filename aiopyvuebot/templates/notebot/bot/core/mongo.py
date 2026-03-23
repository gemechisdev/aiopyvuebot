"""
Async MongoDB client via Motor.

After `connect_to_mongo()` is awaited, import `db` to access any
collection:  `db.notes`, `db.users`, etc.
"""

from __future__ import annotations

import logging
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from config import MONGO_URI, MONGO_DB_NAME

logger = logging.getLogger(__name__)

_client: AsyncIOMotorClient | None = None
db: AsyncIOMotorDatabase | None = None


async def connect_to_mongo() -> None:
    """Open the Motor connection, verify with ping, and create indexes."""
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
        logger.info("Connected to MongoDB  db=%s", MONGO_DB_NAME)
        await _create_indexes()
    except Exception as exc:
        logger.error("Failed to connect to MongoDB: %s", exc)
        raise


async def _create_indexes() -> None:
    """Idempotent index creation – safe to run on every startup."""
    # TTL: auto-expire notes that have an expires_at field set
    await db.notes.create_index("expires_at", expireAfterSeconds=0, sparse=True)
    # Fast per-user listing, pinned first, then newest
    await db.notes.create_index(
        [("user_id", 1), ("is_pinned", -1), ("created_at", -1)]
    )
    # Full-text search on title + content
    await db.notes.create_index([("title", "text"), ("content", "text")])
    logger.info("MongoDB indexes verified.")


async def close_mongo_connection() -> None:
    """Close the Motor connection gracefully."""
    global _client
    if _client is not None:
        _client.close()
        logger.info("Disconnected from MongoDB.")
