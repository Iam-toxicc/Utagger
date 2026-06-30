from motor.motor_asyncio import AsyncIOMotorClient
from config import Config

class Database:
    def __init__(self, uri, database_name):
        self._client = AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.users = self.db.users
        self.groups = self.db.groups

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

# Initialize DB connection
try:
    db = Database(Config.MONGO_URL, "UTaggerBot")
except Exception as e:
    print(f"Failed to connect to Database: {e}")
  
