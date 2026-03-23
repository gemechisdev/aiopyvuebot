"""
Singleton aiogram Bot and Dispatcher.

Import `bot` and `dp` anywhere — they are created exactly once per
process.  All outgoing messages default to HTML parse mode so plugins
never need to pass parse_mode="HTML" explicitly.
"""

from __future__ import annotations

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN

if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN is not set. "
        "Copy sample.env → .env and fill in your Telegram bot token."
    )

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)

dp = Dispatcher(storage=MemoryStorage())
