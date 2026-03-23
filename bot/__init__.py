"""
bot – NoteBot StarterKit main package.

`load_all_plugins(dp)` is the single function that wires every plugin
router into the aiogram Dispatcher. Call it once before starting
polling or serving the webhook.
"""

from __future__ import annotations

import logging
from aiogram import Dispatcher

logger = logging.getLogger(__name__)


def load_all_plugins(dp: Dispatcher) -> None:
    """Import every plugin Router and include it in the Dispatcher."""

    # ── bot (entry-point commands & inline) ───────────────────────────────────
    from bot.plugins.bot.start import router as start_router
    from bot.plugins.bot.help import router as help_router
    from bot.plugins.bot.inline import router as inline_router

    # ── notes CRUD ────────────────────────────────────────────────────────────
    from bot.plugins.notes.add import router as notes_add_router
    from bot.plugins.notes.list import router as notes_list_router
    from bot.plugins.notes.view import router as notes_view_router
    from bot.plugins.notes.delete import router as notes_delete_router
    from bot.plugins.notes.search import router as notes_search_router

    # ── sudo / admin ──────────────────────────────────────────────────────────
    from bot.plugins.sudo.stats import router as stats_router

    routers = [
        start_router,
        help_router,
        inline_router,
        notes_add_router,
        notes_list_router,
        notes_view_router,
        notes_delete_router,
        notes_search_router,
        stats_router,
    ]

    for router in routers:
        dp.include_router(router)

    logger.info("✅ Loaded %d plugin router(s)", len(routers))
