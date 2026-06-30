import logging
from pyrogram import Client
from config import Config

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
            plugins=dict(root="plugins") # Yeh automatically plugins folder read karega
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        logger.info(f"💎 Bot Started as {me.username}!")
        logger.info("👑 Developer: Toxic")

    async def stop(self, *args):
        await super().stop()
        logger.info("❌ Bot Stopped.")

if __name__ == "__main__":
    app = Utagger()
    app.run()
  
