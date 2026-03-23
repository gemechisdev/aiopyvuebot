"""Structured logging setup for NoteBot."""

import logging
import sys


def setup_logging(level: int = logging.INFO) -> None:
    """Configure root logger with a clean, readable format."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(name)-28s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    # Reduce noise from third-party libraries
    logging.getLogger("aiogram").setLevel(logging.WARNING)
    logging.getLogger("motor").setLevel(logging.WARNING)
    logging.getLogger("pymongo").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
