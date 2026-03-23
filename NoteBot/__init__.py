"""
NoteBot package.

Plugin loader lives here so every entry point (main.py, api/index.py)
uses the same single function to wire all routers into the Dispatcher.
"""

from __future__ import annotations

import logging
from aiogram import Dispatcher

logger = logging.getLogger(__name__)


def load_all_plugins(dp: Dispatcher) -> None:
    """Import every plugin router and include it in the Dispatcher."""

    # ── bot ──────────────────────────────────────────────────────────────────
    from NoteBot.plugins.bot.start import router as start_router
    from NoteBot.plugins.bot.inline import router as inline_router

    # ── notes ─────────────────────────────────────────────────────────────────
    from NoteBot.plugins.notes.add import router as notes_add_router
    from NoteBot.plugins.notes.list import router as notes_list_router
    from NoteBot.plugins.notes.view import router as notes_view_router
    from NoteBot.plugins.notes.delete import router as notes_delete_router
    from NoteBot.plugins.notes.search import router as notes_search_router

    # ── sudo ──────────────────────────────────────────────────────────────────
    from NoteBot.plugins.sudo.stats import router as stats_router

    routers = [
        start_router,
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

    logger.info("Loaded %d plugin router(s)", len(routers))
