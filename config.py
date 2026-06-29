# ==========================================
# UserTagger Pro
# config.py
# ==========================================

import os
from dotenv import load_dotenv

load_dotenv()

# ==========================================
# Telegram
# ==========================================

API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# ==========================================
# Owner
# ==========================================

OWNER_ID = int(os.getenv("OWNER_ID", "0"))

# ==========================================
# MongoDB
# ==========================================

MONGO_URI = os.getenv("MONGO_URI", "")

DATABASE_NAME = os.getenv(
    "DATABASE_NAME",
    "UserTaggerPro"
)

# ==========================================
# Logs
# ==========================================

LOG_CHANNEL = int(
    os.getenv(
        "LOG_CHANNEL",
        "0"
    )
)

# ==========================================
# Force Join
# ==========================================

FORCE_SUB = os.getenv(
    "FORCE_SUB",
    ""
)

# ==========================================
# Bot
# ==========================================

BOT_VERSION = os.getenv(
    "BOT_VERSION",
    "1.0.0"
)

START_PIC = os.getenv(
    "START_PIC",
    ""
)

BOT_NAME = os.getenv(
    "BOT_NAME",
    "UserTagger Pro"
)

# ==========================================
# Default Settings
# ==========================================

DEFAULT_BATCH = int(
    os.getenv(
        "DEFAULT_BATCH",
        "5"
    )
)

DEFAULT_DELAY = int(
    os.getenv(
        "DEFAULT_DELAY",
        "3"
    )
)

DEFAULT_TAG_MESSAGE = os.getenv(
    "DEFAULT_TAG_MESSAGE",
    "📢 Attention Everyone!"
)

# ==========================================
# Broadcast
# ==========================================

BROADCAST_SLEEP = float(
    os.getenv(
        "BROADCAST_SLEEP",
        "0.08"
    )
)

# ==========================================
# FloodWait
# ==========================================

MAX_FLOODWAIT = int(
    os.getenv(
        "MAX_FLOODWAIT",
        "300"
    )
)

# ==========================================
# Developer
# ==========================================

DEVELOPER = os.getenv(
    "DEVELOPER",
    "Toxic"
)

# ==========================================
# Validation
# ==========================================

REQUIRED = {
    "API_ID": API_ID,
    "API_HASH": API_HASH,
    "BOT_TOKEN": BOT_TOKEN,
    "MONGO_URI": MONGO_URI,
    "OWNER_ID": OWNER_ID,
}

missing = []

for key, value in REQUIRED.items():

    if value in ("", 0, None):
        missing.append(key)

if missing:

    raise RuntimeError(
        "Missing environment variables:\n"
        + "\n".join(missing)
    )
