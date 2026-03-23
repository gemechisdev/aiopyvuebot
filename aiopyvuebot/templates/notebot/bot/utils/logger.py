"""Structured logging configuration for NoteBot StarterKit."""

import logging
import sys


def setup_logging(level: int = logging.INFO) -> None:
    """Configure root logger with a clean, readable format."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(name)-30s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    # Suppress noisy third-party loggers
    for noisy in ("aiogram", "motor", "pymongo", "uvicorn.access"):
        logging.getLogger(noisy).setLevel(logging.WARNING)
