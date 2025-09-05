# main.py
import os
import asyncio
import logging
import sys
from aiohttp import web
from datetime import datetime
import pyromod.listen
from pyrogram import Client
from pyrogram.enums import ParseMode
from pyrogram.types import BotCommand
from config import *
from database.database import full_userbase

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def keep_alive(request):
    return web.Response(text="Bot is alive!")

name ="""
 BYPASS BOT BY ATHITHAN
"""

class BypassBot(Client):
    def __init__(self):
        super().__init__(
            name="bypass_bot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="plugins"),
            workers=4,
            in_memory=True
        )
        self.logger = logger
        self.ping_task = None

    async def broadcast_to_users(self, message):
        """Send a message to all users in the database."""
        try:
            users = await full_userbase()
            success_count = 0
            for user_id in users:
                try:
                    await self.send_message(chat_id=user_id, text=message)
                    success_count += 1
                    await asyncio.sleep(0.1)
                except Exception as e:
                    logger.warning(f"Failed to send message to user {user_id}: {e}")
            return success_count
        except Exception as e:
            logger.error(f"Broadcast failed: {e}")
            return 0

    async def start(self):
        try:
            await super().start()
            me = await self.get_me()
            self.username = me.username
            self.uptime = datetime.now()

            # Set bot commands for menu
            commands = [
                BotCommand("start", "Start the bot 🚀"),
                BotCommand("help", "Get help about using the bot ℹ️"),
                BotCommand("by", "Bypass a shortened URL 🔄"),
                BotCommand("stats", "Check your usage statistics 📊"),
                BotCommand("ping", "Check if bot is alive 🏓"),
                BotCommand("about", "About the bot ℹ️"),
                BotCommand("broadcast", "Send message to all users (admin only) 📢"),
                BotCommand("users", "Get user statistics (admin only) 👥"),
                BotCommand("addpre", "for add pro users"),
                BotCommand("removepre", "for remove pro users")
            ]
            await self.set_bot_commands(commands)
            logger.info("Bot commands set in menu")

            # Start web server
            app = web.Application()
            app.router.add_get("/keep-alive", keep_alive)
            runner = web.AppRunner(app)
            await runner.setup()
            await web.TCPSite(runner, "0.0.0.0", PORT).start()

            # Send startup message to admin
            try:
                await self.send_message(
                    chat_id=OWNER_ID,
                    text="<b>✅ Bypass Bot Started Successfully!</b>\n\nDeveloped by @Malli4U_Admin_Bot"
                )
            except Exception as e:
                logger.error(f"Failed to send startup message: {e}")

        except Exception as e:
            if "AUTH_KEY_DUPLICATED" in str(e):
                logger.error(
                    "Session conflict detected! Make sure the bot is not running elsewhere."
                )
                sys.exit(1)
            raise e

    async def stop(self, *args):
        """Stop the bot and cleanup tasks."""
        if self.ping_task:
            self.ping_task.cancel()
            try:
                await self.ping_task
            except asyncio.CancelledError:
                pass
        await super().stop()
        logger.info("Bot stopped.")

    def run(self):
        """Run the bot."""
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.start())
        logger.info("Bot is now running. Developed by @athithan_220")
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            logger.info("Shutting down...")
        finally:
            loop.run_until_complete(self.stop())

if __name__ == "__main__":
    try:
        BypassBot().run()
    except Exception as e:
        LOGGER.error(f"Critical error: {e}")
        sys.exit(1)

    async def start(self):
        try:
            await super().start()
            me = await self.get_me()
            logger.info(f"🚀 Advanced Bypass Bot started successfully as @{me.username}")
            
            # Initialize plugins
            try:
                from plugins.bypass_handler import start_tasks, set_bot_instance
                set_bot_instance(self)
                await start_tasks()
                logger.info("✅ All plugins initialized successfully")
            except Exception as e:
                logger.error(f"⚠️ Plugin initialization failed: {e}")
            
            # Send startup notification to admin
            if ADMIN_ID:
                try:
                    startup_message = (
                        f"🚀 **Advanced Bypass Bot Started!**\n\n"
                        f"**Bot Username:** @{me.username}\n"
                        f"**Bot ID:** `{me.id}`\n"
                        f"**Status:** Online ✅\n\n"
                        f"💎 **Premium Settings:**\n"
                        f"┣ **Price:** ₹25 per month\n"
                        f"┣ **Free Limit:** 3 links/day\n"
                        f"┣ **Premium:** Unlimited\n"
                        f"┗ **Auto Reactions:** Active\n\n"
                        f"👨‍💻 **Developer:** @athithan_220\n"
                        f"📞 **Support:** @ragnarlothbrockV\n\n"
                        f"🎉 **All systems operational!**"
                    )
                    await self.send_message(
                        chat_id=ADMIN_ID,
                        text=startup_message,
                        parse_mode=ParseMode.MARKDOWN
                    )
                    logger.info("✅ Startup notification sent to admin")
                except Exception as e:
                    logger.error(f"Failed to send startup message: {e}")
                    
        except Exception as e:
            logger.error(f"❌ Failed to start bot: {e}")
            raise

    async def stop(self):
        try:
            if ADMIN_ID:
                try:
                    await self.send_message(
                        chat_id=ADMIN_ID,
                        text="🔴 **Bot Shutting Down**\n\nThe bot has been stopped successfully.",
                        parse_mode=ParseMode.MARKDOWN
                    )
                except:
                    pass
            
            await super().stop()
            logger.info("🛑 Bot stopped successfully")
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")

def main():
    print("=" * 60)
    print("🚀 Starting Advanced Bypass Bot")
    print("=" * 60)
    print(f"💎 Premium: ₹25 for unlimited access")
    print(f"🆓 Free: 3 links per day")
    print(f"👨‍💻 Developer: @athithan_220")
    print(f"📞 Support: @ragnarlothbrockV")
    print("=" * 60)
    
    try:
        # Validate configuration
        if not BOT_TOKEN:
            print("❌ BOT_TOKEN is required!")
            return
        
        if not API_ID or not API_HASH:
            print("❌ API_ID and API_HASH are required!")
            return
        
        print("✅ Configuration validation passed")
        print("🤖 Initializing bot...")
        
        # Create and run bot
        app = BypassBot()
        print("🎯 Starting bot...")
        app.run()
        
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user (Ctrl+C)")
    except Exception as e:
        print(f"❌ Critical Error: {e}")
        logger.error(f"Critical error in main: {e}")
    finally:
        print("👋 Goodbye!")

if __name__ == "__main__":
    main()
