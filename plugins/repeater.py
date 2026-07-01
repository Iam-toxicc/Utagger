import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import Message

# Active jobs ko store karne ke liye dictionary {chat_id: [task1, task2]}
ACTIVE_JOBS = {}

# Time ko samajhne wala Smart Parser
def parse_time(time_str):
    time_str = time_str.lower()
    try:
        if time_str.endswith('m'):
            val = int(time_str[:-1]) * 60
        elif time_str.endswith('h'):
            val = int(time_str[:-1]) * 3600
        else:
            val = int(time_str) * 60 # Default to minutes agar sirf number ho
        
        # Limit: 1 Minute (60s) to 24 Hours (86400s)
        if 60 <= val <= 86400:
            return val
        return None
    except ValueError:
        return None

def format_time(seconds):
    if seconds >= 3600:
        return f"{seconds // 3600} ʜᴏᴜʀ(s)"
    return f"{seconds // 60} ᴍɪɴᴜᴛᴇ(s)"

async def repeat_task(client, chat_id, message_id, interval):
    while True:
        await asyncio.sleep(interval)
        try:
            # Reply kiye gaye message ko copy karke bhejega
            await client.copy_message(chat_id, chat_id, message_id)
        except Exception:
            break # Agar bot ko group se nikal diya gaya ya error aaya toh task stop

# ----------------- REPEAT COMMAND -----------------
@Client.on_message(filters.command("repeat") & filters.group)
async def set_repeat_cmd(client: Client, message: Message):
    # Admin Check
    user = await client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
        return await message.reply_text("❌ **ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ sᴇᴛ ʀᴇᴘᴇᴀᴛᴇʀs!**")

    if not message.reply_to_message:
        return await message.reply_text("❌ **ᴘʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ʀᴇᴘᴇᴀᴛ ɪᴛ.**")

    if len(message.command) < 2:
        return await message.reply_text(
            f"> ⊚ **ᴜsᴀɢᴇ :** `/repeat {time}`\n"
            f"> ➻ **ᴇxᴀᴍᴘʟᴇs :** `/repeat 10m`, `/repeat 2h`, `/repeat 45m`\n"
            f"> ➻ **ʟɪᴍɪᴛs :** 1 ᴍɪɴᴜᴛᴇ ᴛᴏ 24 ʜᴏᴜʀs."
        )

    time_str = message.command[1]
    interval_seconds = parse_time(time_str)

    if not interval_seconds:
        return await message.reply_text("❌ **ɪɴᴠᴀʟɪᴅ ᴛɪᴍᴇ ғᴏʀᴍᴀᴛ!** ᴜsᴇ 'm' ғᴏʀ ᴍɪɴᴜᴛᴇs ᴏʀ 'h' ғᴏʀ ʜᴏᴜʀs (1m - 24h).")

    chat_id = message.chat.id
    msg_id = message.reply_to_message.id

    # Background task start karna
    task = asyncio.create_task(repeat_task(client, chat_id, msg_id, interval_seconds))
    
    if chat_id not in ACTIVE_JOBS:
        ACTIVE_JOBS[chat_id] = []
    ACTIVE_JOBS[chat_id].append(task)

    time_formatted = format_time(interval_seconds)
    await message.reply_text(
        f"> ✅ **ʀᴇᴘᴇᴀᴛᴇʀ ᴀᴄᴛɪᴠᴀᴛᴇᴅ :**\n>\n"
        f"> ➻ **ɪɴᴛᴇʀᴠᴀʟ :** {time_formatted}\n"
        f"> ➻ **sᴛᴀᴛᴜs :** ʀᴜɴɴɪɴɢ ɪɴ ʙᴀᴄᴋɢʀᴏᴜɴᴅ."
    )

# ----------------- STOP COMMAND -----------------
@Client.on_message(filters.command("stop") & filters.group)
async def stop_repeat_cmd(client: Client, message: Message):
    user = await client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
        return await message.reply_text("❌ **ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ sᴛᴏᴘ ʀᴇᴘᴇᴀᴛᴇʀs!**")

    chat_id = message.chat.id
    if chat_id in ACTIVE_JOBS and ACTIVE_JOBS[chat_id]:
        # Saare active tasks ko cancel karna
        for task in ACTIVE_JOBS[chat_id]:
            task.cancel()
        
        ACTIVE_JOBS[chat_id].clear()
        await message.reply_text("> 🛑 **ᴀʟʟ ᴀᴄᴛɪᴠᴇ ʀᴇᴘᴇᴀᴛᴇʀs ʜᴀᴠᴇ ʙᴇᴇɴ sᴛᴏᴘᴘᴇᴅ!**")
    else:
        await message.reply_text("❌ **ɴᴏ ᴀᴄᴛɪᴠᴇ ʀᴇᴘᴇᴀᴛᴇʀs ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ.**")

# ----------------- JOBS COMMAND -----------------
@Client.on_message(filters.command("jobs") & filters.group)
async def show_jobs_cmd(client: Client, message: Message):
    user = await client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
        return
        
    chat_id = message.chat.id
    active_count = len(ACTIVE_JOBS.get(chat_id, []))
    
    if active_count > 0:
        await message.reply_text(
            f"> ⊚ **ᴀᴄᴛɪᴠᴇ ᴛᴀsᴋs :**\n>\n"
            f"> ➻ **ʀᴜɴɴɪɴɢ ᴊᴏʙs :** `{active_count}`\n"
            f"> ➻ ᴜsᴇ `/stop` ᴛᴏ ᴄᴀɴᴄᴇʟ ᴛʜᴇᴍ."
        )
    else:
        await message.reply_text("❌ **ɴᴏ ᴀᴄᴛɪᴠᴇ ʀᴇᴘᴇᴀᴛᴇʀs ʀᴜɴɴɪɴɢ.**")
        
