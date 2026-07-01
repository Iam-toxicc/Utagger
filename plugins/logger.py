import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

# APNA LOGGER CHANNEL ID YAHAN DALO
LOGGER_ID = -1003748226916 

# BOT START LOG
@Client.on_message(filters.command("start") & filters.private) # Example start, but usually handled in main.py
async def bot_start_log(client, message):
    await client.send_message(LOGGER_ID, "💎 **Bot Started Successfully!**")

# GROUP ADDED EVENT
@Client.on_message(filters.new_chat_members)
async def group_added(client: Client, message: Message):
    if not any(member.is_self for member in message.new_chat_members):
        return
    
    chat = message.chat
    me = await client.get_me()
    
    # Get Admin who added
    added_by = message.from_user.mention if message.from_user else "Unknown"
    
    # Try to get invite link
    try:
        chat_link = await client.export_chat_invite_link(chat.id)
    except:
        chat_link = "No Link"

    member_count = await client.get_chat_members_count(chat.id)
    
    msg = f"""
#𝗕𝗢𝗧_𝗔𝗗𝗗𝗘𝗗_𝗡𝗘𝗪_𝗚𝗥𝗢𝗨𝗣

⦿───────────────────⦿

◎ ᴄʜᴀᴛ ɴᴀᴍᴇ ▸ {chat.title}
◎ ᴄʜᴀᴛ ɪᴅ ▸ {chat.id}
◎ ᴄʜᴀᴛ ᴜsᴇʀɴᴀᴍᴇ ▸ @{chat.username if chat.username else "Private"}
◎ ᴄʜᴀᴛ ʟɪɴᴋ ▸ {chat_link}
◎ ɢʀᴏᴜᴘ ᴍᴇᴍʙᴇʀs ▸ {member_count}
◎ ᴀᴅᴅᴇᴅ ʙʏ ▸ {added_by}

⦿───────────────────⦿
"""
    buttons = InlineKeyboardMarkup([[InlineKeyboardButton("ɢʀᴏᴜᴘ ʟɪɴᴋ", url=chat_link)]])
    await client.send_message(LOGGER_ID, msg, reply_markup=buttons)

# GROUP LEFT EVENT
@Client.on_message(filters.left_chat_member)
async def group_left(client: Client, message: Message):
    if not message.left_chat_member.is_self:
        return
    
    chat = message.chat
    removed_by = message.from_user.mention if message.from_user else "Unknown"
    me = await client.get_me()
    
    msg = f"""
.✫ #𝗟𝗘𝗙𝗧_𝗚𝗥𝗢𝗨𝗣 ✫

ᴄʜᴀᴛ ᴛɪᴛʟᴇ : {chat.title}

ᴄʜᴀᴛ ɪᴅ : {chat.id}

ʀᴇᴍᴏᴠᴇᴅ ʙʏ : {removed_by}

ʙᴏᴛ : @{me.username}
"""
    await client.send_message(LOGGER_ID, msg)
  
