"""Webhook management helpers (thin wrapper around Telegram Bot API)."""

from __future__ import annotations

import requests


class WebhookManager:
    """Manage Telegram bot webhooks without requiring aiogram at CLI time."""

    BASE = "https://api.telegram.org"

    def __init__(self, token: str) -> None:
        self.token = token
        self._base = f"{self.BASE}/bot{token}"

    # ── public API ────────────────────────────────────────────────────────────

    def set(self, url: str, path: str = "/api/telegram/webhook") -> dict:
        full_url = url.rstrip("/") + path
        return self._post("setWebhook", {"url": full_url, "drop_pending_updates": True})

    def info(self) -> dict:
        return self._get("getWebhookInfo")

    def delete(self, drop_pending: bool = False) -> dict:
        return self._post("deleteWebhook", {"drop_pending_updates": drop_pending})

    # ── private ───────────────────────────────────────────────────────────────

    def _get(self, method: str) -> dict:
        r = requests.get(f"{self._base}/{method}", timeout=10)
        r.raise_for_status()
        return r.json()

    def _post(self, method: str, payload: dict) -> dict:
        r = requests.post(f"{self._base}/{method}", json=payload, timeout=10)
        r.raise_for_status()
        return r.json()
