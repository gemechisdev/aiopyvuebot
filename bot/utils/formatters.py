"""HTML formatters for note messages sent through the bot."""

from __future__ import annotations

from typing import Any


def _escape(text: str) -> str:
    """Minimal HTML escaping for user-supplied content."""
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def format_note_preview(note: dict[str, Any]) -> str:
    """One-liner preview used in list views."""
    pin = "📌 " if note.get("is_pinned") else "📝 "
    title = _escape(note["title"])
    content = _escape(note["content"])
    preview = content[:60] + "…" if len(content) > 60 else content
    nid = str(note["_id"])
    return f"{pin}<b>{title}</b>\n<i>{preview}</i>\n<code>{nid}</code>"


def format_note_full(note: dict[str, Any]) -> str:
    """Full note view with title, content, tags and metadata."""
    pin = "📌 " if note.get("is_pinned") else "📝 "
    title = _escape(note["title"])
    content = _escape(note["content"])
    tags = "  ".join(f"#{_escape(t)}" for t in note.get("tags", []))
    created = (
        note["created_at"].strftime("%Y-%m-%d %H:%M")
        if note.get("created_at")
        else "—"
    )
    nid = str(note["_id"])

    parts = [f"{pin}<b>{title}</b>\n\n{content}"]
    if tags:
        parts.append(f"\n{tags}")
    parts.append(f"\n\n<i>Saved: {created}</i>")
    parts.append(f"\n<code>ID: {nid}</code>")
    return "".join(parts)


def format_notes_list(notes: list[dict[str, Any]], total: int) -> str:
    """Header + compact list used by /notes command."""
    if not notes:
        return (
            "📭 <b>No notes yet!</b>\n\n"
            "Use /addnote to save your first note.\n\n"
            "<i>Example:</i>\n"
            "<code>/addnote Shopping List | Milk, eggs, bread</code>"
        )

    header = f"📒 <b>Your Notes</b>  <i>({total} total)</i>\n\n"
    items = "\n\n".join(
        f"{'📌' if n.get('is_pinned') else '📝'} <b>{_escape(n['title'])}</b>\n"
        f"<code>{str(n['_id'])}</code>"
        for n in notes
    )
    footer = "\n\n<i>Tap a note ID or use /note &lt;id&gt; to view.</i>"
    return header + items + footer
