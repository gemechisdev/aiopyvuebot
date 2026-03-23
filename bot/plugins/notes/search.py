"""
/search <query> — full-text note search.
"""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from bot.utils.database.notes import search_notes
from bot.utils.formatters import _escape

router = Router()


@router.message(Command("search"))
async def cmd_search(message: Message) -> None:
    query = message.text[len("/search"):].strip()
    if not query:
        await message.reply(
            "🔍 <b>Search Notes</b>\n\n"
            "Usage: <code>/search &lt;query&gt;</code>\n"
            "Example: <code>/search shopping</code>"
        )
        return

    notes = await search_notes(message.from_user.id, query)

    if not notes:
        await message.reply(f"🔍 No notes found for <b>{_escape(query)}</b>.")
        return

    lines = [f"🔍 <b>Results for \"{_escape(query)}\":</b>\n"]
    buttons = []

    for note in notes:
        preview = note["content"][:80] + "…" if len(note["content"]) > 80 else note["content"]
        lines.append(
            f"{'📌' if note.get('is_pinned') else '📝'} <b>{_escape(note['title'])}</b>\n"
            f"<i>{_escape(preview)}</i>"
        )
        buttons.append([
            InlineKeyboardButton(
                text=f"📝 {note['title'][:35]}",
                callback_data=f"note:view:{str(note['_id'])}",
            )
        ])

    await message.reply(
        "\n\n".join(lines),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
    )
