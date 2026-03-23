"""
Telegram webhook + webhook management endpoints.
"""

from __future__ import annotations

import logging

from fastapi import APIRouter, Request, HTTPException, status
from aiogram.types import Update

from bot.core.bot import bot, dp

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/telegram", tags=["telegram"])


@router.post("/webhook")
async def webhook(request: Request) -> dict:
    """Receive and dispatch incoming Telegram updates."""
    from config import BOT_TOKEN
    if not BOT_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="BOT_TOKEN not configured",
        )
    try:
        data = await request.json()
        logger.debug("Received update_id=%s", data.get("update_id"))
        update = Update.model_validate(data)
        await dp.feed_webhook_update(bot=bot, update=update)
        return {"ok": True}
    except Exception as exc:
        logger.error("Error processing update: %s", exc)
        return {"ok": False, "error": str(exc)}


@router.get("/setup-webhook")
async def setup_webhook(webhook_url: str | None = None) -> dict:
    """Register (or replace) the bot webhook on Telegram's servers."""
    from config import BOT_TOKEN, WEBHOOK_PATH
    if not BOT_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="BOT_TOKEN not configured",
        )
    if not webhook_url:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="webhook_url query parameter is required",
        )
    full_url = webhook_url.rstrip("/") + WEBHOOK_PATH
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await bot.set_webhook(url=full_url)
        info = await bot.get_webhook_info()
        logger.info("Webhook registered: %s", info.url)
        return {
            "ok": True,
            "url": info.url,
            "pending_update_count": info.pending_update_count,
        }
    except Exception as exc:
        logger.error("Error setting webhook: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )


@router.get("/webhook-info")
async def webhook_info() -> dict:
    """Return current webhook information."""
    info = await bot.get_webhook_info()
    return {
        "url": info.url,
        "has_custom_certificate": info.has_custom_certificate,
        "pending_update_count": info.pending_update_count,
        "last_error_message": info.last_error_message,
    }
