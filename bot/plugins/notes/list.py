"""
/notes — list all notes for the current user.
Also handles the `list_notes` inline callback from the start/home screen.
"""

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from bot.utils.database.notes import get_user_notes, count_user_notes
from bot.utils.formatters import format_notes_list

router = Router()


def _notes_keyboard(notes: list) -> InlineKeyboardMarkup | None:
    if not notes:
        return None
    buttons = [
        [
            InlineKeyboardButton(
                text=f"{'📌' if n.get('is_pinned') else '📝'} {n['title'][:30]}",
                callback_data=f"note:view:{str(n['_id'])}",
            )
        ]
        for n in notes[:10]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.message(Command("notes"))
async def cmd_notes(message: Message) -> None:
    user_id = message.from_user.id
    notes = await get_user_notes(user_id, limit=10)
    total = await count_user_notes(user_id)
    await message.answer(
        format_notes_list(notes, total),
        reply_markup=_notes_keyboard(notes),
    )


@router.callback_query(F.data == "list_notes")
async def cb_list_notes(callback: CallbackQuery) -> None:
    user_id = callback.from_user.id
    notes = await get_user_notes(user_id, limit=10)
    total = await count_user_notes(user_id)

    buttons = [
        [
            InlineKeyboardButton(
                text=f"{'📌' if n.get('is_pinned') else '📝'} {n['title'][:30]}",
                callback_data=f"note:view:{str(n['_id'])}",
            )
        ]
        for n in notes[:10]
    ]
    buttons.append([InlineKeyboardButton(text="🏠 Home", callback_data="nav:home")])

    await callback.message.edit_text(
        format_notes_list(notes, total),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
    )
    await callback.answer()
