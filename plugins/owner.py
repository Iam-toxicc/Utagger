import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from database.db import db
from config import Config
from utils.emojis import Emojis as e

# Custom decorator for Owner commands
def is_owner(_, __, message: Message):
    return message.from_user and message.from_user.id == Config.OWNER_ID
owner_filter = filters.create(is_owner)

@Client.on_message(filters.command("stats") & owner_filter)
async def bot_stats(client: Client, message: Message):
    msg = await message.reply_text(f"{e.FLASH} Fetching Database Stats...")
    
    total_users = await db.users.count_documents({})
    total_groups = await db.groups.count_documents({})
    
    stats_text = f"""
{e.STATS} **Utagger Database Stats** {e.STATS}

{e.USER} **Total Users:** `{total_users}`
{e.GROUP} **Total Groups:** `{total_groups}`

{e.DIAMOND} **Status:** System running perfectly.
"""
    await msg.edit_text(stats_text)

@Client.on_message(filters.command("broadcast") & owner_filter)
async def broadcast_cmd(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text(f"{e.CANCEL} Please reply to a message to broadcast it.")

    msg = await message.reply_text(f"{e.FLASH} **Starting Broadcast...**")
    
    users = await db.users.find().to_list(length=None)
    groups = await db.groups.find().to_list(length=None)
    
    all_targets = [u["_id"] for u in users] + [g["_id"] for g in groups]
    
    success = 0
    failed = 0
    
    for target in all_targets:
        try:
            await message.reply_to_message.copy(target)
            success += 1
            await asyncio.sleep(0.1) # Safe broadcasting delay
        except Exception:
            failed += 1
            
    await msg.edit_text(f"""
{e.TICK} **Broadcast Completed!**

{e.USER} **Total Sent:** `{success}`
{e.CANCEL} **Failed:** `{failed}`
""")
  
