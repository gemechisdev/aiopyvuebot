"""
python -m NoteBot   →   starts the bot in polling mode.
"""

import asyncio
import logging

from NoteBot.utils.logger import setup_logging
from NoteBot.core.mongo import connect_to_mongo, close_mongo_connection
from NoteBot.core.bot import bot, dp
from NoteBot import load_all_plugins

logger = logging.getLogger(__name__)


async def main() -> None:
    setup_logging()
    logger.info("Starting NoteBot…")

    await connect_to_mongo()

    load_all_plugins(dp)

    try:
        logger.info("Bot is running (polling mode). Press Ctrl+C to stop.")
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await close_mongo_connection()
        await bot.session.close()
        logger.info("NoteBot shut down cleanly.")


if __name__ == "__main__":
    asyncio.run(main())
