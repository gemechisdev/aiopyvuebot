"""
bot.core package exports.
bot and dp are imported lazily to avoid errors when BOT_TOKEN is absent.
"""

from bot.core.mongo import connect_to_mongo, close_mongo_connection, db

__all__ = ["db", "connect_to_mongo", "close_mongo_connection"]
