"""
Inline mode — lets users search and share their notes in any Telegram chat.

Usage: @YourBot <search term>
"""

from aiogram import Router
from aiogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
)

from bot.utils.database.users import upsert_user
from bot.utils.database.notes import search_notes, get_user_notes

router = Router()

_NO_NOTES_RESULT = InlineQueryResultArticle(
    id="no_notes",
    title="No notes found",
    description="Use /addnote in the bot chat to create notes",
    input_message_content=InputTextMessageContent(
        message_text=(
            "📭 No notes found.\n"
            "Open the bot and use /addnote to create your first note!"
        )
    ),
)


@router.inline_query()
async def inline_search(inline_query: InlineQuery) -> None:
    user = inline_query.from_user
    await upsert_user(user.id, user.first_name, user.last_name, user.username)

    query = inline_query.query.strip()
    notes = (
        await search_notes(user.id, query) if query
        else await get_user_notes(user.id, limit=20)
    )

    if not notes:
        await inline_query.answer(results=[_NO_NOTES_RESULT], cache_time=5)
        return

    results = [
        InlineQueryResultArticle(
            id=str(note["_id"]),
            title=f"{'📌' if note.get('is_pinned') else '📝'} {note['title']}",
            description=(
                note["content"][:120] + "…"
                if len(note["content"]) > 120
                else note["content"]
            ),
            input_message_content=InputTextMessageContent(
                message_text=(
                    f"📝 <b>{note['title']}</b>\n\n{note['content']}"
                ),
                parse_mode="HTML",
            ),
        )
        for note in notes[:20]
    ]

    await inline_query.answer(results=results, cache_time=10)
