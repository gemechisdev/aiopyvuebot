"""
/addnote — save a new note.

Usage:
    /addnote Title | Content
    /addnote Single-line title and content
"""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.utils.database.users import upsert_user
from bot.utils.database.notes import create_note

router = Router()

_USAGE = (
    "📝 <b>Add a Note</b>\n\n"
    "Format:  <code>/addnote Title | Content</code>\n\n"
    "Examples:\n"
    "<code>/addnote Shopping List | Milk, eggs, bread</code>\n"
    "<code>/addnote Remember to call mum tomorrow</code>"
)


@router.message(Command("addnote"))
async def cmd_addnote(message: Message) -> None:
    user = message.from_user
    await upsert_user(user.id, user.first_name, user.last_name, user.username)

    args = message.text[len("/addnote"):].strip()
    if not args:
        await message.reply(_USAGE)
        return

    if "|" in args:
        raw_title, _, raw_content = args.partition("|")
        title = raw_title.strip()
        content = raw_content.strip()
    else:
        # First line = title, rest = content (or same when single line)
        lines = args.split("\n", 1)
        title = lines[0].strip()
        content = lines[1].strip() if len(lines) > 1 else args.strip()

    if not title:
        await message.reply("❌ Please provide a title.\n\n" + _USAGE)
        return
    if not content:
        await message.reply("❌ Please provide content.\n\n" + _USAGE)
        return

    note_id = await create_note(user.id, title, content)
    preview = content[:100] + "…" if len(content) > 100 else content

    await message.reply(
        f"✅ <b>Note saved!</b>\n\n"
        f"📝 <b>{title}</b>\n"
        f"<i>{preview}</i>\n\n"
        f"<code>ID: {note_id}</code>"
    )
