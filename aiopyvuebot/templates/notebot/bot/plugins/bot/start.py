"""
/start command — sends welcome message with a Telegram WebApp button
so users can open the Mini App directly, plus inline-mode and help buttons.
"""

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo,
)

from bot.utils.database.users import upsert_user
from strings import get_string
from config import WEB_APP_URL

router = Router()


def _start_keyboard() -> InlineKeyboardMarkup:
    buttons: list[list[InlineKeyboardButton]] = []

    # Open Mini App button (only shown when WEB_APP_URL is configured)
    if WEB_APP_URL:
        buttons.append([
            InlineKeyboardButton(
                text="📝 Open Note Manager",
                web_app=WebAppInfo(url=WEB_APP_URL),
            )
        ])

    buttons += [
        [InlineKeyboardButton(text="🔍 Search Notes Inline", switch_inline_query="")],
        [
            InlineKeyboardButton(text="❓ Help", callback_data="nav:help"),
            InlineKeyboardButton(text="ℹ️ About", callback_data="nav:about"),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    user = message.from_user
    await upsert_user(user.id, user.first_name, user.last_name, user.username)
    text = get_string("start").format(name=user.first_name)
    await message.answer(text, reply_markup=_start_keyboard())


# ── navigation callbacks from Help / About ────────────────────────────────────


@router.callback_query(F.data == "nav:home")
async def nav_home(callback: CallbackQuery) -> None:
    text = get_string("start").format(name=callback.from_user.first_name)
    await callback.message.edit_text(text, reply_markup=_start_keyboard())
    await callback.answer()


@router.callback_query(F.data == "nav:about")
async def nav_about(callback: CallbackQuery) -> None:
    text = get_string("about")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 Home", callback_data="nav:home")],
    ])
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()
