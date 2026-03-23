"""
REST API routes for the Telegram Mini App.

All endpoints require a valid Telegram initData signature
(see api/middleware/auth.py for details).

Endpoints:
  GET    /api/notes              list user notes
  POST   /api/notes              create note
  GET    /api/notes/{id}         get single note
  PUT    /api/notes/{id}         update note
  DELETE /api/notes/{id}         delete note
  POST   /api/notes/{id}/pin     toggle pin
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from api.middleware.auth import get_current_user
from bot.utils.database.notes import (
    create_note,
    get_user_notes,
    get_note_by_id,
    update_note,
    delete_note,
    pin_note,
    count_user_notes,
    search_notes,
)

router = APIRouter(prefix="/api/notes", tags=["notes"])


# ── Pydantic schemas ───────────────────────────────────────────────────────────


class NoteCreate(BaseModel):
    title: str
    content: str
    tags: list[str] = []


class NoteUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    tags: list[str] | None = None


def _serialize(note: dict[str, Any]) -> dict[str, Any]:
    """Convert MongoDB document to JSON-serialisable dict."""
    return {
        "id": str(note["_id"]),
        "user_id": note["user_id"],
        "title": note["title"],
        "content": note["content"],
        "tags": note.get("tags", []),
        "is_pinned": note.get("is_pinned", False),
        "created_at": note["created_at"].isoformat() if note.get("created_at") else None,
        "updated_at": note["updated_at"].isoformat() if note.get("updated_at") else None,
    }


# ── endpoints ─────────────────────────────────────────────────────────────────


@router.get("/")
async def list_notes(
    limit: int = 20,
    skip: int = 0,
    q: str | None = None,
    user: dict = Depends(get_current_user),
) -> dict:
    uid = user["id"]
    if q:
        notes = await search_notes(uid, q)
    else:
        notes = await get_user_notes(uid, limit=limit, skip=skip)
    total = await count_user_notes(uid)
    return {"notes": [_serialize(n) for n in notes], "total": total}


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(
    body: NoteCreate,
    user: dict = Depends(get_current_user),
) -> dict:
    note_id = await create_note(user["id"], body.title, body.content, body.tags)
    note = await get_note_by_id(note_id, user["id"])
    return _serialize(note)


@router.get("/{note_id}")
async def get_note(
    note_id: str,
    user: dict = Depends(get_current_user),
) -> dict:
    note = await get_note_by_id(note_id, user["id"])
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return _serialize(note)


@router.put("/{note_id}")
async def update(
    note_id: str,
    body: NoteUpdate,
    user: dict = Depends(get_current_user),
) -> dict:
    fields = body.model_dump(exclude_none=True)
    if not fields:
        raise HTTPException(status_code=400, detail="No fields to update")
    ok = await update_note(note_id, user["id"], **fields)
    if not ok:
        raise HTTPException(status_code=404, detail="Note not found")
    note = await get_note_by_id(note_id, user["id"])
    return _serialize(note)


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    note_id: str,
    user: dict = Depends(get_current_user),
) -> None:
    ok = await delete_note(note_id, user["id"])
    if not ok:
        raise HTTPException(status_code=404, detail="Note not found")


@router.post("/{note_id}/pin")
async def toggle_pin(
    note_id: str,
    user: dict = Depends(get_current_user),
) -> dict:
    ok = await pin_note(note_id, user["id"])
    if not ok:
        raise HTTPException(status_code=404, detail="Note not found")
    note = await get_note_by_id(note_id, user["id"])
    return _serialize(note)
