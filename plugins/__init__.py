# plugins/__init__.py
import asyncio
import logging
from pyrogram import Client

logger = logging.getLogger(__name__)

async def init_plugins():
    """Initialize all plugins"""
    try:
        from .bypass_handler import init_user_client
        await init_user_client()
        logger.info("Plugins initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize plugins: {e}")
