from motor.motor_asyncio import AsyncIOMotorClient
from config import Config
from utils import send_log


class Database:
    def __init__(self, uri, database_name):
        self._client = AsyncIOMotorClient(uri)
        self.jishubotz = self._client[database_name]
        self.col = self.jishubotz["user"]  # Use brackets in case "user" is not a valid dot attribute

    def new_user(self, user_id):
        return {
            "_id": int(user_id),
            "file_id": None,
            "caption": None,
            "prefix": None,
            "suffix": None,
            "metadata": False,
            "metadata_code": "By :- @RDX_PVT_LTD"
        }

    async def add_user(self, bot, message):
        user = message.from_user
        if not await self.is_user_exist(user.id):
            await self.col.insert_one(self.new_user(user.id))
            await send_log(bot, user)

    async def is_user_exist(self, user_id):
        return await self.col.find_one({"_id": int(user_id)}) is not None

    async def total_users_count(self):
        return await self.col.count_documents({})

    async def get_all_users(self):
        return self.col.find({})

    async def delete_user(self, user_id):
        await self.col.delete_many({"_id": int(user_id)})

    # ----------------- Thumbnail -----------------
    async def set_thumbnail(self, user_id, file_id):
        await self.col.update_one({"_id": int(user_id)}, {"$set": {"file_id": file_id}})

    async def get_thumbnail(self, user_id):
        user = await self.col.find_one({"_id": int(user_id)})
        return user.get("file_id") if user else None

    # ----------------- Caption -----------------
    async def set_caption(self, user_id, caption):
        await self.col.update_one({"_id": int(user_id)}, {"$set": {"caption": caption}})

    async def get_caption(self, user_id):
        user = await self.col.find_one({"_id": int(user_id)})
        return user.get("caption") if user else None

    # ----------------- Prefix -----------------
    async def set_prefix(self, user_id, prefix):
        await self.col.update_one({"_id": int(user_id)}, {"$set": {"prefix": prefix}})

    async def get_prefix(self, user_id):
        user = await self.col.find_one({"_id": int(user_id)})
        return user.get("prefix") if user else None

    # ----------------- Suffix -----------------
    async def set_suffix(self, user_id, suffix):
        await self.col.update_one({"_id": int(user_id)}, {"$set": {"suffix": suffix}})

    async def get_suffix(self, user_id):
        user = await self.col.find_one({"_id": int(user_id)})
        return user.get("suffix") if user else None

    # ----------------- Metadata -----------------
    async def set_metadata(self, user_id, value: bool):
        await self.col.update_one({"_id": int(user_id)}, {"$set": {"metadata": value}})

    async def get_metadata(self, user_id):
        user = await self.col.find_one({"_id": int(user_id)})
        return user.get("metadata") if user else False

    # ----------------- Metadata Code -----------------
    async def set_metadata_code(self, user_id, code: str):
        await self.col.update_one({"_id": int(user_id)}, {"$set": {"metadata_code": code}})

    async def get_metadata_code(self, user_id):
        user = await self.col.find_one({"_id": int(user_id)})
        return user.get("metadata_code") if user else "By :- @RDX_PVT_LTD"


# Create global instance
jishubotz = Database(Config.DATABASE_URL, Config.DATABASE_NAME)
