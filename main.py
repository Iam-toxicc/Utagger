import logging
import asyncio
from pyrogram import Client
from config import Config
from database.db import db

# Logging setup terminal ko clean rakhne ke liye
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class Utagger(Client):
    def __init__(self):
        super().__init__(
            name="utagger_session",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            plugins=dict(root="plugins")
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        logger.info(f"💎 Bot Started as {me.username}!")
        
        # --- STARTUP LOG TO LOGGER CHANNEL ---
        try:
            # Pura startup message jo tumhare logger group me jayega
            startup_msg = (
                f"💎 **{me.first_name} is now Online!**\n\n"
                f"👑 **Developer:** Toxic\n"
                f"⚙️ **Status:** All Systems (Tagger, Security, Repeater) Running smoothly."
            )
            # Config se LOGGER_ID utha raha hai
            await self.send_message(Config.LOGGER_ID, startup_msg)
            logger.info("✅ Startup log sent to Logger Channel.")
        except Exception as e:
            logger.error(f"⚠️ Could not send startup log! Check if LOGGER_ID is in config & Bot is Admin. Error: {e}")

        # --- AUTO RESUME REPEAT TASKS ---
        try:
            from plugins.repeater import repeat_worker, ACTIVE_TASKS
            jobs = await db.get_all_repeat_jobs()
            resumed = 0
            
            for job in jobs:
                chat_id = job["_id"]
                msg_id = job["message_id"]
                interval = job["interval"]
                is_album = job.get("is_album", False)
                
                # Background me task run karna
                task = asyncio.create_task(repeat_worker(self, chat_id, msg_id, interval, is_album))
                ACTIVE_TASKS[chat_id] = task
                resumed += 1
                
            if resumed > 0:
                logger.info(f"⚡ Successfully resumed {resumed} repeat jobs from Database!")
        except Exception as e:
            logger.error(f"❌ Failed to resume repeat tasks: {e}")
            
        # --- BRANDING CLEANUP ---
        # TGVoid hata diya, sirf Toxic
        logger.info("👑 Developer: Toxic")

    async def stop(self, *args):
        await super().stop()
        logger.info("❌ Bot Stopped.")

if __name__ == "__main__":
    app = Utagger()
    app.run()
    
