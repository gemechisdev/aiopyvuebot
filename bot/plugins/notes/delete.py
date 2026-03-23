"""
/delnote <id>           — confirm then delete a note
note:del_confirm:<id>   — show confirmation dialog (from view callback)
note:del_do:<id>        — execute deletion after confirmation
"""

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from bot.utils.database.notes import delete_note

router = Router()


def _confirm_keyboard(note_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Yes, delete", callback_data=f"note:del_do:{note_id}"),
            InlineKeyboardButton(text="❌ Cancel", callback_data=f"note:view:{note_id}"),
        ],
    ])


@router.message(Command("delnote"))
async def cmd_delnote(message: Message) -> None:
    note_id = message.text[len("/delnote"):].strip()
    if not note_id:
        await message.reply("Usage: <code>/delnote &lt;id&gt;</code>")
        return

    await message.reply(
        f"🗑 Delete note <code>{note_id}</code>? This cannot be undone.",
        reply_markup=_confirm_keyboard(note_id),
    )


@router.callback_query(F.data.startswith("note:del_confirm:"))
async def cb_del_confirm(callback: CallbackQuery) -> None:
    note_id = callback.data.split(":", 2)[2]
    await callback.message.edit_text(
        "🗑 Are you sure you want to delete this note?",
        reply_markup=_confirm_keyboard(note_id),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("note:del_do:"))
async def cb_del_do(callback: CallbackQuery) -> None:
    note_id = callback.data.split(":", 2)[2]
    success = await delete_note(note_id, callback.from_user.id)

    if success:
        await callback.message.edit_text(
            "✅ Note deleted.",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📒 My Notes", callback_data="list_notes")],
            ]),
        )
    else:
        await callback.answer("❌ Could not delete note.", show_alert=True)

    await callback.answer()
