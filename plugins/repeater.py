import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import Message

# Global variable for your main.py to resume tasks
ACTIVE_TASKS = {}

# *args and **kwargs added to safely accept the 5th argument from main.py without crashing
async def repeat_worker(client, chat_id, message_id, interval, *args, **kwargs):
    while True:
        await asyncio.sleep(interval)
        try:
            await client.copy_message(chat_id, chat_id, message_id)
        except Exception:
            break

# Time parser for minutes and hours
def parse_time(time_str):
    time_str = time_str.lower()
    try:
        if time_str.endswith('m'): val = int(time_str[:-1]) * 60
        elif time_str.endswith('h'): val = int(time_str[:-1]) * 3600
        else: val = int(time_str) * 60
        return val if 60 <= val <= 86400 else None
    except: return None

# The Repeat Command
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
       (msg_to_repeat.text and any(x in msg_to_repeat.text.lower() for x in ["/utag", "/atag", "/cancel"])):
        return await message.reply_text("⚠️ **Security Alert:** Cannot repeat commands or taggers.")

    if len(message.command) < 2:
        return await message.reply_text("⊚ **Usage:** `/repeat 10m`")

    interval = parse_time(message.command[1])
    if not interval:
        return await message.reply_text("❌ **Invalid time format! (Use 1m, 1h, etc.)**")

    # Start task
    task = asyncio.create_task(repeat_worker(client, message.chat.id, msg_to_repeat.id, interval))
    
    if message.chat.id not in ACTIVE_TASKS:
        ACTIVE_TASKS[message.chat.id] = []
    ACTIVE_TASKS[message.chat.id].append(task)

    await message.reply_text(f"✅ **Repeater activated for every {message.command[1]}.**")
    
