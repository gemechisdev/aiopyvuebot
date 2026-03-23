"""
/help command and nav:help callback.
"""

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from strings import get_string

router = Router()


def _help_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔍 Try Inline Search", switch_inline_query="")],
        [InlineKeyboardButton(text="🏠 Home", callback_data="nav:home")],
    ])


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(get_string("help"), reply_markup=_help_keyboard())


@router.callback_query(F.data == "nav:help")
async def nav_help(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        get_string("help"), reply_markup=_help_keyboard()
    )
    await callback.answer()
