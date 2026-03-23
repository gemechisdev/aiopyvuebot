"""
Telegram WebApp initData authentication middleware.

Every request from the Mini App must include:
    Authorization: Telegram <url-encoded initData>

The middleware validates the HMAC-SHA256 signature and injects
`request.state.user` (dict with id, first_name, username, …).

Reference: https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app
"""

from __future__ import annotations

import hashlib
import hmac
import json
import logging
from urllib.parse import unquote, parse_qsl

from fastapi import Request, HTTPException, status

from config import BOT_TOKEN

logger = logging.getLogger(__name__)


def _compute_hash(data_check_string: str) -> str:
    secret = hmac.new(b"WebAppData", BOT_TOKEN.encode(), hashlib.sha256).digest()
    return hmac.new(secret, data_check_string.encode(), hashlib.sha256).hexdigest()


def parse_and_validate_init_data(raw: str) -> dict:
    """
    Validate Telegram initData and return the parsed payload.
    Raises HTTPException 401 on invalid / missing data.
    """
    if not raw:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Telegram initData",
        )

    try:
        params = dict(parse_qsl(unquote(raw), keep_blank_values=True))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Malformed initData",
        )

    received_hash = params.pop("hash", None)
    if not received_hash:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="initData has no hash",
        )

    data_check_string = "\n".join(
        f"{k}={v}" for k, v in sorted(params.items())
    )

    expected = _compute_hash(data_check_string)
    if not hmac.compare_digest(expected, received_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid initData signature",
        )

    # Parse the user JSON embedded in the payload
    user_raw = params.get("user", "{}")
    try:
        user = json.loads(user_raw)
    except json.JSONDecodeError:
        user = {}

    return {"raw": params, "user": user}


async def get_current_user(request: Request) -> dict:
    """
    FastAPI dependency — validates initData from the Authorization header
    and returns the user dict.

    Use as:
        @router.get("/notes")
        async def my_endpoint(user: dict = Depends(get_current_user)):
            ...
    """
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Telegram "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header must start with 'Telegram '",
        )
    init_data = auth_header[len("Telegram "):]
    parsed = parse_and_validate_init_data(init_data)
    return parsed["user"]
