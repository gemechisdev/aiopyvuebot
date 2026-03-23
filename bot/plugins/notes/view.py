"""
/note <id>        — view a single note
note:view:<id>    — same via inline button
note:pin:<id>     — toggle pin
"""

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from bot.utils.database.notes import get_note_by_id, pin_note
from bot.utils.formatters import format_note_full

router = Router()


def _note_keyboard(note_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📌 Pin/Unpin", callback_data=f"note:pin:{note_id}"),
            InlineKeyboardButton(text="🗑 Delete", callback_data=f"note:del_confirm:{note_id}"),
        ],
        [InlineKeyboardButton(text="◀️ All Notes", callback_data="list_notes")],
    ])


@router.message(Command("note"))
async def cmd_note(message: Message) -> None:
    note_id = message.text[len("/note"):].strip()
    if not note_id:
        await message.reply("Usage: <code>/note &lt;id&gt;</code>")
        return

    note = await get_note_by_id(note_id, message.from_user.id)
    if not note:
        await message.reply("❌ Note not found or you don't have access to it.")
        return

    await message.reply(format_note_full(note), reply_markup=_note_keyboard(note_id))


@router.callback_query(F.data.startswith("note:view:"))
async def cb_view_note(callback: CallbackQuery) -> None:
    note_id = callback.data.split(":", 2)[2]
    note = await get_note_by_id(note_id, callback.from_user.id)

    if not note:
        await callback.answer("❌ Note not found.", show_alert=True)
        return

    await callback.message.edit_text(
        format_note_full(note), reply_markup=_note_keyboard(note_id)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("note:pin:"))
async def cb_pin_note(callback: CallbackQuery) -> None:
    note_id = callback.data.split(":", 2)[2]
    success = await pin_note(note_id, callback.from_user.id)

    if not success:
        await callback.answer("❌ Could not update note.", show_alert=True)
        return

    note = await get_note_by_id(note_id, callback.from_user.id)
    status = "pinned 📌" if note and note.get("is_pinned") else "unpinned"
    await callback.answer(f"✅ Note {status}!")

    if note:
        await callback.message.edit_text(
            format_note_full(note), reply_markup=_note_keyboard(note_id)
        )
