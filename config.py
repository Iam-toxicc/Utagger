import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

class Config:
    API_ID = int(os.environ.get("API_ID", "39934421"))
    API_HASH = os.environ.get("API_HASH", "407aaa4db92ab5d0b32027d6482a5fff")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "8835661225:AAHH-BJyBGFGVLU549EwvEZglyKxw7jQLIM")
    MONGO_URL = os.environ.get("MONGO_URL", "mongodb+srv://Toxicbots:TOXIC0000@cluster0.u5sllsx.mongodb.net/?appName=Cluster0")
    
    OWNER_ID = int(os.environ.get("OWNER_ID", "8238387029"))
    
    # Toxic ecosystem logging channel (Renamed to LOGGER_ID to match main.py)
    LOGGER_ID = int(os.environ.get("LOGGER_ID", "-1003748226916"))
    
    # Updates Channel and Support Group Redirects
    UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL", "https://t.me/ToxicTGUpdates") # Yahan channel username daalo (bina @ ke)
    SUPPORT_GROUP = os.environ.get("SUPPORT_GROUP", "https://t.me/ToxicStoreSupport")       # Yahan group username daalo (bina @ ke)
    
    # Premium start image URL
    START_PIC = os.environ.get("START_PIC", "")
    
