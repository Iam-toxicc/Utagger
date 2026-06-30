import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

class Config:
    API_ID = int(os.environ.get("API_ID", "39934421"))
    API_HASH = os.environ.get("API_HASH", "407aaa4db92ab5d0b32027d6482a5fff")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "8750600665:AAEDyDCwIny6q4XGKBqF2Huu_r-kNJ32JrM")
    MONGO_URL = os.environ.get("MONGO_URL", "mongodb+srv://Toxicbots:TOXIC0000@cluster0.u5sllsx.mongodb.net/?appName=Cluster0")
    
    OWNER_ID = int(os.environ.get("OWNER_ID", "8238387029"))
    
    # Void ecosystem logging channel
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1003747918681"))
    
    # Premium start image URL
    START_PIC = os.environ.get("START_PIC", "")
  
