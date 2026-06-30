from motor.motor_asyncio import AsyncIOMotorClient
from config import Config

class Database:
    def __init__(self, uri, database_name):
        self._client = AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.users = self.db.users
        self.groups = self.db.groups
        self.repeat_jobs = self.db.repeat_jobs

    # === USERS & GROUPS LOGIC ===
    async def add_user(self, user_id, name):
        user = await self.users.find_one({"_id": user_id})
        if not user:
            await self.users.insert_one({"_id": user_id, "name": name})
            return True
        return False

    async def add_group(self, group_id, group_name):
        group = await self.groups.find_one({"_id": group_id})
        if not group:
            await self.groups.insert_one({"_id": group_id, "name": group_name})
            return True
        return False

    # === TAGGING FORMAT LOGIC ===
    async def set_tag_format(self, group_id, format_string):
        await self.groups.update_one(
            {"_id": group_id}, 
            {"$set": {"tag_format": format_string}}, 
            upsert=True
        )

    async def get_tag_format(self, group_id):
        group = await self.groups.find_one({"_id": group_id})
        if group and "tag_format" in group:
            return group["tag_format"]
        return "{emoji} [{name}](tg://user?id={id})"

    # === REPEAT MESSAGES LOGIC ===
    async def add_repeat_job(self, chat_id, message_id, interval, is_album):
        await self.repeat_jobs.update_one(
            {"_id": chat_id},
            {"$set": {
                "message_id": message_id, 
                "interval": interval, 
                "is_album": is_album
            }},
            upsert=True
        )

    async def remove_repeat_job(self, chat_id):
        await self.repeat_jobs.delete_one({"_id": chat_id})

    async def get_all_repeat_jobs(self):
        return await self.repeat_jobs.find().to_list(length=None)

# Initialize DB connection
try:
    db = Database(Config.MONGO_URL, "UTaggerBot")
except Exception as e:
    print(f"Failed to connect to Database: {e}")

    # === FORCE JOIN (FSUB) LOGIC ===
    async def update_fsub_status(self, group_id, status: bool):
        await self.groups.update_one(
            {"_id": group_id}, 
            {"$set": {"fsub_active": status}}, 
            upsert=True
        )

    async def set_fsub_channel(self, group_id, channel_id):
        await self.groups.update_one(
            {"_id": group_id}, 
            {"$set": {"fsub_channel": channel_id}}, 
            upsert=True
        )

    async def get_fsub_config(self, group_id):
        group = await self.groups.find_one({"_id": group_id})
        if group:
            return group.get("fsub_active", False), group.get("fsub_channel", None)
        return False, None
        
