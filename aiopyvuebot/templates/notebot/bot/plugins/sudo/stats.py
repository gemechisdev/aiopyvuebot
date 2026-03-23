"""
/stats — admin-only bot statistics.
"""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.utils.database.users import count_total_users
from bot.utils.database.notes import count_total_notes
from bot.utils.decorators.admins import admin_only

router = Router()


@router.message(Command("stats"))
@admin_only
async def cmd_stats(message: Message) -> None:
    users = await count_total_users()
    notes = await count_total_notes()

    await message.answer(
        "📊 <b>NoteBot Statistics</b>\n\n"
        f"👥 <b>Total Users:</b> {users:,}\n"
        f"📝 <b>Total Notes:</b> {notes:,}\n"
        f"🚀 <b>Status:</b> Active\n"
        f"⚡ <b>Stack:</b> aiogram · MongoDB · FastAPI · Vue 3\n"
        f"🛠 <b>Developer:</b> @venopyx\n\n"
        "<b>System:</b> ✅ All systems operational"
    )
