"""YAML-based string loader for bot messages."""

from __future__ import annotations

import os
from typing import Any

import yaml

_strings: dict[str, Any] = {}


def load_strings(lang: str = "en") -> None:
    """Load strings from strings/langs/<lang>.yml into memory."""
    global _strings
    path = os.path.join(os.path.dirname(__file__), "langs", f"{lang}.yml")
    with open(path, encoding="utf-8") as fh:
        _strings = yaml.safe_load(fh) or {}


def get_string(key: str, **kwargs: Any) -> str:
    """Return the string for *key*, optionally formatting it with kwargs."""
    text: str = _strings.get(key, f"[Missing string: {key}]")
    if kwargs:
        text = text.format(**kwargs)
    return text.strip()
