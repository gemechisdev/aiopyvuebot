"""User collection helpers."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from bot.core import mongo as _mongo


async def upsert_user(
    user_id: int,
    first_name: str,
    last_name: str | None = None,
    username: str | None = None,
) -> None:
    """Insert a new user or refresh their profile fields."""
    if _mongo.db is None:
        return
    await _mongo.db.users.update_one(
        {"_id": user_id},
        {
            "$set": {
                "first_name": first_name,
                "last_name": last_name,
                "username": username,
                "updated_at": datetime.now(timezone.utc),
            },
            "$setOnInsert": {"created_at": datetime.now(timezone.utc)},
        },
        upsert=True,
    )


async def get_user(user_id: int) -> dict[str, Any] | None:
    if _mongo.db is None:
        return None
    return await _mongo.db.users.find_one({"_id": user_id})


async def count_total_users() -> int:
    if _mongo.db is None:
        return 0
    return await _mongo.db.users.count_documents({})
