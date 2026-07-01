import asyncio
import logging
from pyrogram import Client, filters, enums
from pyrogram.types import Message
from config import Config  # Logger ID ke liye import kiya hai

logger = logging.getLogger(__name__)

ACTIVE_TASKS = {}

# Worker ab message ko Logger channel se uthayega
async def repeat_worker(client, chat_id, message_id, interval, *args, **kwargs):
    is_album = kwargs.get('is_album', False)
    if args and isinstance(args[0], bool):
        is_album = args[0]

    while True:
        await asyncio.sleep(interval)
        try:
            # 1. Naya Logic (Safe Vault): Message ko Logger ID se copy karega
            if is_album:
                await client.copy_media_group(chat_id, Config.LOGGER_ID, message_id)
            else:
                await client.copy_message(chat_id, Config.LOGGER_ID, message_id)
                
        except Exception as e:
            # 2. Purana Logic (Fallback): Agar task DB se resume hua hai (purana task) 
            # toh group se hi copy karne ki koshish karega
            try:
                if is_album:
                    await client.copy_media_group(chat_id, chat_id, message_id)
                else:
                    await client.copy_message(chat_id, chat_id, message_id)
            except Exception as fallback_e:
                error_msg = str(fallback_e).lower()
                logger.error(f"❌ Repeater Error in {chat_id}: {error_msg}")
                
                if "not found" in error_msg or "deleted" in error_msg:
                    logger.warning(f"🛑 Message deleted in {chat_id} and not found in Logger. Repeater stopped.")
                    break
                elif any(x in error_msg for x in ["forbidden", "kicked", "banned", "deactivated"]):
                    break
                continue

# Time parser
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
    except:
        return

    if not message.reply_to_message:
        return await message.reply_text("❌ **Reply to a message to repeat it.**")

    msg_to_repeat = message.reply_to_message
    
    # Anti-Spam check
    if (msg_to_repeat.text and msg_to_repeat.text.startswith("/")) or \
       (msg_to_repeat.text and any(x in msg_to_repeat.text.lower() for x in ["/utag", "/atag", "/cancel", "/stop", "/jobs"])):
        return await message.reply_text("⚠️ **Security Alert:** Cannot repeat commands or taggers.")

    if len(message.command) < 2:
        return await message.reply_text("⊚ **Usage:** `/repeat 1m`")

    interval = parse_time(message.command[1])
    if not interval:
        return await message.reply_text("❌ **Invalid time format! (Use 1m, 1h, etc.)**")

    is_album = bool(msg_to_repeat.media_group_id)

    # 🔒 MESSAGE KO LOGGER CHANNEL MEIN SAFE KARNA
    try:
        if is_album:
            safe_msg = await client.copy_media_group(Config.LOGGER_ID, message.chat.id, msg_to_repeat.id)
            safe_msg_id = safe_msg[0].id
        else:
            safe_msg = await client.copy_message(Config.LOGGER_ID, message.chat.id, msg_to_repeat.id)
            safe_msg_id = safe_msg.id
    except Exception as e:
        return await message.reply_text("❌ **Error:** Bot must be an Admin in the Logger Channel to secure the message!")

    # Start task using the SAFE MESSAGE ID from Logger Channel
    task = asyncio.create_task(repeat_worker(client, message.chat.id, safe_msg_id, interval, is_album))
    
    if message.chat.id not in ACTIVE_TASKS:
        ACTIVE_TASKS[message.chat.id] = []
    
    if not isinstance(ACTIVE_TASKS[message.chat.id], list):
        ACTIVE_TASKS[message.chat.id] = [ACTIVE_TASKS[message.chat.id]]
        
    ACTIVE_TASKS[message.chat.id].append(task)

    await message.reply_text(f"✅ **Repeater activated for every {message.command[1]}.**\n🛡️ *Message secured. You can now delete the original message!*")

# ==========================================
# 🛑 STOP REPEATER COMMAND
# ==========================================
@Client.on_message(filters.command("stop") & filters.group)
async def stop_repeat_cmd(client: Client, message: Message):
    try:
        user = await client.get_chat_member(message.chat.id, message.from_user.id)
        if user.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
            return
    except:
        return

    chat_id = message.chat.id
    if chat_id in ACTIVE_TASKS and ACTIVE_TASKS[chat_id]:
        tasks = ACTIVE_TASKS[chat_id]
        if isinstance(tasks, list):
            for task in tasks:
                task.cancel()
        else:
            tasks.cancel()
            
        ACTIVE_TASKS[chat_id] = []
        await message.reply_text("✅ **All Repeater Jobs Stopped Successfully.**")
    else:
        await message.reply_text("❌ **No active repeaters found to stop.**")

# ==========================================
# 📋 JOBS COMMAND
# ==========================================
@Client.on_message(filters.command("jobs") & filters.group)
async def jobs_cmd(client: Client, message: Message):
    try:
        user = await client.get_chat_member(message.chat.id, message.from_user.id)
        if user.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
            return
    except:
        return

    chat_id = message.chat.id
    if chat_id in ACTIVE_TASKS and ACTIVE_TASKS[chat_id]:
        tasks = ACTIVE_TASKS[chat_id]
        active_count = sum(1 for t in tasks if not t.cancelled()) if isinstance(tasks, list) else (0 if tasks.cancelled() else 1)

        if active_count > 0:
            await message.reply_text(f"✅ **Active Jobs Running:** {active_count}")
        else:
            await message.reply_text("❌ **No active jobs running in this group.**")
    else:
        await message.reply_text("❌ **No active jobs running in this group.**")
            
