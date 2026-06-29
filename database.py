# ==========================================
# UserTagger Pro
# database.py
# ==========================================

from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING

from config import (
    MONGO_URI,
    DATABASE_NAME,
    DEFAULT_BATCH,
    DEFAULT_DELAY,
    DEFAULT_TAG_MESSAGE
)

# ==========================================
# Mongo Client
# ==========================================

mongo = AsyncIOMotorClient(
    MONGO_URI,
    maxPoolSize=100,
    minPoolSize=5,
)

db = mongo[DATABASE_NAME]

users = db.users
groups = db.groups
settings = db.settings
bans = db.bans
broadcasts = db.broadcasts


# ==========================================
# Startup
# ==========================================

async def init_database():

    await users.create_index(
        [("_id", ASCENDING)],
        unique=True
    )

    await groups.create_index(
        [("_id", ASCENDING)],
        unique=True
    )

    await settings.create_index(
        [("_id", ASCENDING)],
        unique=True
    )

    await bans.create_index(
        [("_id", ASCENDING)],
        unique=True
    )


# ==========================================
# USERS
# ==========================================

async def add_user(user_id: int):

    if await users.find_one({"_id": user_id}):
        return False

    await users.insert_one({
        "_id": user_id,
        "joined": datetime.utcnow()
    })

    return True


async def remove_user(user_id: int):

    await users.delete_one({
        "_id": user_id
    })


async def get_users():

    async for user in users.find({}):
        yield user


async def total_users():

    return await users.count_documents({})


# ==========================================
# GROUPS
# ==========================================

async def add_group(chat_id: int):

    if await groups.find_one({"_id": chat_id}):
        return False

    await groups.insert_one({
        "_id": chat_id,
        "joined": datetime.utcnow()
    })

    return True


async def remove_group(chat_id: int):

    await groups.delete_one({
        "_id": chat_id
    })


async def get_groups():

    async for group in groups.find({}):
        yield group


async def total_groups():

    return await groups.count_documents({})


# ==========================================
# SETTINGS
# ==========================================

DEFAULT_SETTINGS = {
    "batch": DEFAULT_BATCH,
    "delay": DEFAULT_DELAY,
    "tag_message": DEFAULT_TAG_MESSAGE,
    "force_sub": False,
    "force_channel": "",
}


async def get_settings(chat_id: int):

    data = await settings.find_one({
        "_id": chat_id
    })

    if data:
        return data

    data = {
        "_id": chat_id,
        **DEFAULT_SETTINGS
    }

    await settings.insert_one(data)

    return data


async def update_setting(
    chat_id: int,
    key: str,
    value
):

    await settings.update_one(
        {
            "_id": chat_id
        },
        {
            "$set": {
                key: value
            }
        },
        upsert=True
    )


# ==========================================
# BANS
# ==========================================

async def ban_user(user_id: int):

    await bans.update_one(
        {
            "_id": user_id
        },
        {
            "$set": {
                "banned_at": datetime.utcnow()
            }
        },
        upsert=True
    )


async def unban_user(user_id: int):

    await bans.delete_one({
        "_id": user_id
    })


async def is_banned(user_id: int):

    return bool(
        await bans.find_one({
            "_id": user_id
        })
    )


# ==========================================
# BROADCAST
# ==========================================

async def create_broadcast():

    data = {
        "created_at": datetime.utcnow(),
        "success": 0,
        "failed": 0,
        "blocked": 0,
        "status": "running"
    }

    result = await broadcasts.insert_one(data)

    return result.inserted_id


async def finish_broadcast(
    broadcast_id,
    success,
    failed,
    blocked
):

    await broadcasts.update_one(
        {
            "_id": broadcast_id
        },
        {
            "$set": {
                "success": success,
                "failed": failed,
                "blocked": blocked,
                "status": "completed",
                "finished_at": datetime.utcnow()
            }
        }
    )


# ==========================================
# STATS
# ==========================================

async def get_stats():

    return {
        "users": await total_users(),
        "groups": await total_groups(),
        "banned": await bans.count_documents({})
    }
