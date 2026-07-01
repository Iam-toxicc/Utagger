import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import Message

# Global variable for your main.py to resume tasks and for /jobs, /stop commands
ACTIVE_TASKS = {}

# *args and **kwargs added to safely accept extra arguments like 'is_album' from DB
async def repeat_worker(client, chat_id, message_id, interval, *args, **kwargs):
    while True:
        await asyncio.sleep(interval)
        try:
            await client.copy_message(chat_id, chat_id, message_id)
        except Exception:
            # Agar group delete ho jaye ya bot remove ho jaye, toh loop break ho jayega
            break

# Time parser for minutes and hours
def parse_time(time_str):
    time_str = time_str.lower()
    try:
        if time_str.endswith('m'): val = int(time_str[:-1]) * 60
        elif time_str.endswith('h'): val = int(time_str[:-1]) * 3600
        else: val = int(time_str) * 60
        # Min limit 60 sec (1m), Max limit 86400 sec (24h)
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

    # Anti-Spam check: Cannot repeat bot commands
    msg_to_repeat = message.reply_to_message
    if (msg_to_repeat.text and msg_to_repeat.text.startswith("/")) or \
       (msg_to_repeat.text and any(x in msg_to_repeat.text.lower() for x in ["/utag", "/atag", "/cancel", "/stop", "/jobs"])):
        return await message.reply_text("⚠️ **Security Alert:** Cannot repeat commands or taggers.")

    if len(message.command) < 2:
        return await message.reply_text("⊚ **Usage:** `/repeat 10m`")

    interval = parse_time(message.command[1])
    if not interval:
        return await message.reply_text("❌ **Invalid time format! (Use 1m, 1h, etc.)**")

    # Start task in background
    task = asyncio.create_task(repeat_worker(client, message.chat.id, msg_to_repeat.id, interval))
    
    if message.chat.id not in ACTIVE_TASKS:
        ACTIVE_TASKS[message.chat.id] = []
    
    # Store task list if it's not already a list (fallback for DB logic)
    if not isinstance(ACTIVE_TASKS[message.chat.id], list):
        ACTIVE_TASKS[message.chat.id] = [ACTIVE_TASKS[message.chat.id]]
        
    ACTIVE_TASKS[message.chat.id].append(task)

    await message.reply_text(f"✅ **Repeater activated for every {message.command[1]}.**")

# ==========================================
# 🛑 STOP REPEATER COMMAND
# ==========================================
@Client.on_message(filters.command("stop") & filters.group)
async def stop_repeat_cmd(client: Client, message: Message):
    # Admin Check
    try:
        user = await client.get_chat_member(message.chat.id, message.from_user.id)
        if user.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
            return
    except:
        return

    chat_id = message.chat.id
    if chat_id in ACTIVE_TASKS and ACTIVE_TASKS[chat_id]:
        tasks = ACTIVE_TASKS[chat_id]
        
        # Stop all tasks for this group
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
    # Admin Check
    try:
        user = await client.get_chat_member(message.chat.id, message.from_user.id)
        if user.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
            return
    except:
        return

    chat_id = message.chat.id
    if chat_id in ACTIVE_TASKS and ACTIVE_TASKS[chat_id]:
        tasks = ACTIVE_TASKS[chat_id]
        count = len(tasks) if isinstance(tasks, list) else 1
        
        # Clean up any cancelled tasks from the count
        active_count = 0
        if isinstance(tasks, list):
            active_count = sum(1 for t in tasks if not t.cancelled())
        else:
            active_count = 0 if tasks.cancelled() else 1

        if active_count > 0:
            await message.reply_text(f"✅ **Active Jobs Running:** {active_count}")
        else:
            await message.reply_text("❌ **No active jobs running in this group.**")
    else:
        await message.reply_text("❌ **No active jobs running in this group.**")
    
