"""
Central configuration loaded from environment variables.
Copy sample.env → .env and fill in your values before running.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ── Bot ──────────────────────────────────────────────────────────────────────
BOT_TOKEN: str = os.environ.get("BOT_TOKEN", "")

# Comma-separated Telegram user IDs with admin access
ADMIN_IDS: list[int] = [
    int(x) for x in os.environ.get("ADMIN_IDS", "").split(",") if x.strip()
]

# ── Web App ───────────────────────────────────────────────────────────────────
WEB_APP_URL: str = os.environ.get("WEB_APP_URL", "")
TELEGRAM_BOT_LINK: str = os.environ.get(
    "TELEGRAM_BOT_LINK",
    os.environ.get("VITE_TELEGRAM_BOT_LINK", ""),
)

# ── MongoDB ───────────────────────────────────────────────────────────────────
MONGO_URI: str = os.environ.get("MONGO_URI", "")
MONGO_DB_NAME: str = os.environ.get("MONGO_DB_NAME", "{{ project_slug }}")

# ── Webhook ───────────────────────────────────────────────────────────────────
WEBHOOK_URL: str = os.environ.get("WEBHOOK_URL", "")
WEBHOOK_PATH: str = "/api/telegram/webhook"

# ── Server ────────────────────────────────────────────────────────────────────
APP_HOST: str = os.environ.get("APP_HOST", "0.0.0.0")
APP_PORT: int = int(os.environ.get("APP_PORT", "8000"))
