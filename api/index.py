"""
NoteBot StarterKit – FastAPI application.

This single file is the Vercel serverless entry point.
It:
  1. Bootstraps MongoDB + plugin routers (once per process via a flag)
  2. Exposes Telegram webhook at  POST /api/telegram/webhook
  3. Exposes REST endpoints for the Mini App at   /api/notes/*
  4. Provides auto-register webhook on startup when WEBHOOK_URL is set
  5. Serves Swagger docs at /api/docs

Vercel rewrite rule in vercel.json routes:
  /api/*  →  api/index.py  (Python serverless function)
  /*      →  dist/         (Vite-built Mini App)
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from bot.utils.logger import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

# ── lazy-init guard (Vercel can reuse the same process across requests) ────────
_initialized = False


async def _ensure_initialized() -> None:
    global _initialized
    if _initialized:
        return

    from bot.core.mongo import connect_to_mongo
    from bot.core.bot import dp
    from bot import load_all_plugins

    await connect_to_mongo()
    load_all_plugins(dp)

    # Auto-register webhook when running in production
    from config import WEBHOOK_URL, WEBHOOK_PATH, BOT_TOKEN
    if WEBHOOK_URL and BOT_TOKEN:
        try:
            from bot.core.bot import bot
            full_url = WEBHOOK_URL.rstrip("/") + WEBHOOK_PATH
            await bot.set_webhook(url=full_url)
            logger.info("Webhook registered: %s", full_url)
        except Exception as exc:
            logger.warning("Could not auto-register webhook: %s", exc)

    _initialized = True


# ── FastAPI app ────────────────────────────────────────────────────────────────


@asynccontextmanager
async def lifespan(app: FastAPI):
    await _ensure_initialized()
    yield


def _custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    schema = get_openapi(
        title="NoteBot StarterKit API",
        version="2.0.0",
        description=(
            "REST API for the NoteBot Telegram Mini App.\n\n"
            "**Authentication**: All `/api/notes` endpoints require\n"
            "`Authorization: Telegram <url-encoded initData>` header."
        ),
        routes=app.routes,
    )
    app.openapi_schema = schema
    return schema


app = FastAPI(
    lifespan=lifespan,
    openapi_url="/api/openapi.json",
    docs_url=None,
    redoc_url=None,
)

app.openapi = _custom_openapi  # type: ignore[method-assign]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── routers ────────────────────────────────────────────────────────────────────

from api.routes import telegram as tg_routes  # noqa: E402
from api.routes import notes as notes_routes  # noqa: E402

app.include_router(tg_routes.router)
app.include_router(notes_routes.router)


# ── utility endpoints ──────────────────────────────────────────────────────────


@app.get("/api/docs", include_in_schema=False)
async def swagger_ui():
    return get_swagger_ui_html(
        openapi_url="/api/openapi.json",
        title="NoteBot API Docs",
    )


@app.get("/api/health", tags=["health"])
async def health_check() -> dict:
    from config import BOT_TOKEN, MONGO_URI
    return {
        "status": "ok",
        "bot_configured": bool(BOT_TOKEN),
        "db_configured": bool(MONGO_URI),
        "message": "NoteBot StarterKit is running 🚀",
    }
