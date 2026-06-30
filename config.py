import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

class Config:
    API_ID = int(os.environ.get("API_ID", "0"))
    API_HASH = os.environ.get("API_HASH", "")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    MONGO_URL = os.environ.get("MONGO_URL", "")
    
    OWNER_ID = int(os.environ.get("OWNER_ID", "0"))
    
    # Void ecosystem logging channel
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "0"))
    
    # Premium start image URL
    START_PIC = os.environ.get("START_PIC", "")
  
