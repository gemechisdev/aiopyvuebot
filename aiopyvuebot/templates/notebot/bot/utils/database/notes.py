"""Notes collection helpers – full async CRUD."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from bson import ObjectId
from bson.errors import InvalidId

from bot.core.mongo import db


# ── helpers ────────────────────────────────────────────────────────────────────


def _oid(note_id: str) -> ObjectId | None:
    try:
        return ObjectId(note_id)
    except (InvalidId, TypeError):
        return None


# ── write ──────────────────────────────────────────────────────────────────────


async def create_note(
    user_id: int,
    title: str,
    content: str,
    tags: list[str] | None = None,
) -> str:
    """Insert a note and return its string ID."""
    if db is None:
        raise RuntimeError("Database not connected.")
    now = datetime.now(timezone.utc)
    doc = {
        "user_id": user_id,
        "title": title,
        "content": content,
        "tags": tags or [],
        "is_pinned": False,
        "created_at": now,
        "updated_at": now,
    }
    result = await db.notes.insert_one(doc)
    return str(result.inserted_id)


async def update_note(note_id: str, user_id: int, **fields: Any) -> bool:
    """Partial update; returns True if a document was modified."""
    if db is None:
        return False
    oid = _oid(note_id)
    if oid is None:
        return False
    fields["updated_at"] = datetime.now(timezone.utc)
    result = await db.notes.update_one(
        {"_id": oid, "user_id": user_id},
        {"$set": fields},
    )
    return result.modified_count > 0


async def delete_note(note_id: str, user_id: int) -> bool:
    """Delete a note; returns True on success."""
    if db is None:
        return False
    oid = _oid(note_id)
    if oid is None:
        return False
    result = await db.notes.delete_one({"_id": oid, "user_id": user_id})
    return result.deleted_count > 0


async def pin_note(note_id: str, user_id: int) -> bool:
    """Toggle the pin flag; returns True if the note was found."""
    note = await get_note_by_id(note_id, user_id)
    if note is None:
        return False
    return await update_note(note_id, user_id, is_pinned=not note.get("is_pinned", False))


# ── read ───────────────────────────────────────────────────────────────────────


async def get_note_by_id(
    note_id: str, user_id: int
) -> dict[str, Any] | None:
    if db is None:
        return None
    oid = _oid(note_id)
    if oid is None:
        return None
    return await db.notes.find_one({"_id": oid, "user_id": user_id})


async def get_user_notes(
    user_id: int,
    limit: int = 20,
    skip: int = 0,
) -> list[dict[str, Any]]:
    """Return all user notes: pinned first, then newest."""
    if db is None:
        return []
    cursor = (
        db.notes.find({"user_id": user_id})
        .sort([("is_pinned", -1), ("created_at", -1)])
        .skip(skip)
        .limit(limit)
    )
    return await cursor.to_list(length=limit)


async def search_notes(
    user_id: int, query: str, limit: int = 10
) -> list[dict[str, Any]]:
    """Search notes by full-text index OR regex fallback."""
    if db is None:
        return []
    cursor = db.notes.find(
        {
            "user_id": user_id,
            "$or": [
                {"$text": {"$search": query}},
                {"title": {"$regex": query, "$options": "i"}},
                {"content": {"$regex": query, "$options": "i"}},
                {"tags": {"$in": [query.lower()]}},
            ],
        }
    ).sort("created_at", -1).limit(limit)
    return await cursor.to_list(length=limit)


# ── counters ───────────────────────────────────────────────────────────────────


async def count_user_notes(user_id: int) -> int:
    if db is None:
        return 0
    return await db.notes.count_documents({"user_id": user_id})


async def count_total_notes() -> int:
    if db is None:
        return 0
    return await db.notes.count_documents({})
