"""Decorator that restricts a handler to admin users only."""

from __future__ import annotations

from functools import wraps
from typing import Callable

from aiogram.types import Message

from config import ADMIN_IDS


def admin_only(func: Callable) -> Callable:
    """Wrap a message handler so non-admin users get an error reply."""

    @wraps(func)
    async def wrapper(message: Message, *args, **kwargs):
        if message.from_user.id not in ADMIN_IDS:
            await message.reply("⛔ This command is for administrators only.")
            return
        return await func(message, *args, **kwargs)

    return wrapper
