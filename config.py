import os
from dotenv import load_dotenv

load_dotenv()

# ── Bot ──────────────────────────────────────────────────────────────────────
BOT_TOKEN: str = os.environ.get("BOT_TOKEN", "")

# Comma-separated list of Telegram user IDs that have admin access
# e.g. ADMIN_IDS=123456789,987654321
ADMIN_IDS: list[int] = [
    int(x) for x in os.environ.get("ADMIN_IDS", "").split(",") if x.strip()
]

# ── MongoDB ───────────────────────────────────────────────────────────────────
MONGO_URI: str = os.environ.get("MONGO_URI", "")
MONGO_DB_NAME: str = os.environ.get("MONGO_DB_NAME", "notebot")

# ── Webhook (production) ──────────────────────────────────────────────────────
WEBHOOK_URL: str = os.environ.get("WEBHOOK_URL", "")
WEBHOOK_PATH: str = "/api/telegram/webhook"

# ── Server ────────────────────────────────────────────────────────────────────
APP_HOST: str = os.environ.get("APP_HOST", "0.0.0.0")
APP_PORT: int = int(os.environ.get("APP_PORT", "8000"))
