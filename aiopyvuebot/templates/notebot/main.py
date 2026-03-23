"""
{{ project_name }} – entry point for local development (polling mode).

Run with:
    python main.py
or
    python -m bot
"""

import asyncio
import logging

from bot.__main__ import main

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("{{ project_name }} stopped.")
