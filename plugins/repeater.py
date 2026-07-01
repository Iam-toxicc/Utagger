import asyncio
import logging
from pyrogram import Client, filters, enums
from pyrogram.types import Message
from config import Config
from database.db import db # Database import zaroori hai

logger = logging.getLogger(__name__)
ACTIVE_TASKS = {}

# Worker: Logger channel se uthayega, agar nahi mila toh skip karke database clean karega
async def repeat_worker(client, chat_id, message_id, interval, is_album):
    while True:
        await asyncio.sleep(interval)
        try:
            # Copy from Logger Channel (Persistent Storage)
            if is_album:
                await client.copy_media_group(chat_id, Config.LOGGER_ID, message_id)
            else:
                await client.copy_message(chat_id, Config.LOGGER_ID, message_id)
                
        except Exception as e:
            error_msg = str(e).lower()
            
            # Agar message missing hai (Empty)
            if "empty" in error_msg or "not found" in error_msg:
                logger.warning(f"🛑 Message {message_id} in {chat_id} is missing. Removing job.")
                await db.remove_repeat_job(chat_id) # DB clean
                if chat_id in ACTIVE_TASKS: del ACTIVE_TASKS[chat_id]
                break
            
            # Agar bot ban/kick ho gaya
            elif any(x in error_msg for x in ["forbidden", "kicked", "banned"]):
                break
            continue

def parse_time(time_str):
    time_str = time_str.lower()
    try:
        if time_str.endswith('m'): val = int(time_str[:-1]) * 60
        elif time_str.endswith('h'): val = int(time_str[:-1]) * 3600
        else: val = int(time_str) * 60
        return val if 60 <= val <= 86400 else None
    except: return None

# ==========================================
# 🔁 REPEAT COMMAND
# ==========================================
@Client.on_message(filters.command("repeat") & filters.group)
async def set_repeat_cmd(client: Client, message: Message):
    # Admin check
    try:
        user = await client.get_chat_member(message.chat.id, message.from_user.id)
        if user.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
            return
    except: return

    if not message.reply_to_message:
        return await message.reply_text("❌ **Reply to a message.**")

    msg = message.reply_to_message
    interval = parse_time(message.command[1])
    if not interval: return await message.reply_text("❌ **Invalid time! (e.g., 1m)**")

    is_album = bool(msg.media_group_id)

    # 1. Message ko Logger mein copy karo (Safe Vault)
    try:
        if is_album:
            safe = await client.copy_media_group(Config.LOGGER_ID, message.chat.id, msg.id)
            safe_id = safe[0].id
        else:
            safe = await client.copy_message(Config.LOGGER_ID, message.chat.id, msg.id)
            safe_id = safe.id
    except:
        return await message.reply_text("❌ **Admin error in Logger Channel!**")

    # 2. Database mein Save
    await db.save_repeat_job(message.chat.id, safe_id, interval, is_album)

    # 3. Task Cancel & New Task Start
    if message.chat.id in ACTIVE_TASKS:
        ACTIVE_TASKS[message.chat.id].cancel()

    task = asyncio.create_task(repeat_worker(client, message.chat.id, safe_id, interval, is_album))
    ACTIVE_TASKS[message.chat.id] = task

    await message.reply_text(f"✅ **Repeater Started!**")

# ==========================================
# 🛑 STOP COMMAND
# ==========================================
@Client.on_message(filters.command("stop") & filters.group)
async def stop_repeat_cmd(client: Client, message: Message):
    await db.remove_repeat_job(message.chat.id)
    if message.chat.id in ACTIVE_TASKS:
        ACTIVE_TASKS[message.chat.id].cancel()
        del ACTIVE_TASKS[message.chat.id]
        await message.reply_text("✅ **Repeater Stopped.**")
    else:
        await message.reply_text("❌ **No active repeater.**")
        
