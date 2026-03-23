"""
Singleton aiogram Bot and Dispatcher instances.

Import these anywhere — they are created exactly once per process.
"""

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN

# All messages default to HTML parse mode so plugins don't need
# to pass parse_mode="HTML" on every call.
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)

dp = Dispatcher(storage=MemoryStorage())
