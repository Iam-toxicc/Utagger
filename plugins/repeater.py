import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import Message
from database.db import db
from utils.emojis import Emojis as e
from config import Config

# RAM me chalne wale background tasks ko track karne ke liye
ACTIVE_TASKS = {}

# Background Worker Jo Har Baar Message Bhejega
async def repeat_worker(client: Client, chat_id: int, message_id: int, interval: int, is_album: bool):
    while True:
        await asyncio.sleep(interval)
        try:
            if is_album:
                await client.copy_media_group(chat_id, chat_id, message_id)
            else:
                await client.copy_message(chat_id, chat_id, message_id)
        except Exception as err:
            print(f"Repeat Error in {chat_id}: {err}")
            # Agar bot ko group se nikal diya ya message delete ho gaya, toh loop break kar do
            break

# Command se Time (Seconds) map karna
TIME_MAP = {
    "repeat2min": 120,
    "repeat5min": 300,
    "repeat20min": 1200,
    "repeat60min": 3600,
    "repeat120min": 7200,
    "repeat24hour": 86400
}

@Client.on_message(filters.command(list(TIME_MAP.keys())) & filters.group)
async def set_repeat_cmd(client: Client, message: Message):
    chat_id = message.chat.id
    
    # Admin & Owner Check
    member = await client.get_chat_member(chat_id, message.from_user.id)
    if member.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER] and message.from_user.id != Config.OWNER_ID:
        return await message.reply_text(f"{e.CANCEL} Only admins can set repeating messages!")

    if not message.reply_to_message:
        return await message.reply_text(f"{e.CANCEL} Please reply to a message or album to repeat it.")

    target_msg = message.reply_to_message
    message_id = target_msg.id
    is_album = bool(target_msg.media_group_id)
    
    # Command string nikalo (jaise 'repeat5min') aur interval seconds me convert karo
    cmd_used = message.command[0].lower()
    interval = TIME_MAP.get(cmd_used, 120)

    # Database mein persistent save karo
    await db.add_repeat_job(chat_id, message_id, interval, is_album)

    # Agar koi purana task chal raha hai is group me, toh usko RAM se cancel karo
    if chat_id in ACTIVE_TASKS:
        ACTIVE_TASKS[chat_id].cancel()

    # Naya background task start karo aur dictionary mein save karo
    task = asyncio.create_task(repeat_worker(client, chat_id, message_id, interval, is_album))
    ACTIVE_TASKS[chat_id] = task

    mins = interval // 60
    await message.reply_text(f"{e.TICK} **Repeat Task Activated!**\n\n{e.FLASH} The replied message/album will now repeat every **{mins} minutes**.\n{e.SETTING} Use `/stop` to cancel.")


@Client.on_message(filters.command("stop") & filters.group)
async def stop_repeat_cmd(client: Client, message: Message):
    chat_id = message.chat.id
    
    member = await client.get_chat_member(chat_id, message.from_user.id)
    if member.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER] and message.from_user.id != Config.OWNER_ID:
        return await message.reply_text(f"{e.CANCEL} Only admins can stop repeating messages!")

    # DB se delete karo
    await db.remove_repeat_job(chat_id)

    # RAM se active task ko roko
    if chat_id in ACTIVE_TASKS:
        ACTIVE_TASKS[chat_id].cancel()
        del ACTIVE_TASKS[chat_id]
        await message.reply_text(f"{e.CANCEL} **All repeating messages have been stopped.**")
    else:
        await message.reply_text("No active repeat tasks found in this group.")
      
