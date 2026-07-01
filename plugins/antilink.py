import re
import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import Message

# Regex pattern to catch all http/https links, t.me links, and @usernames
LINK_PATTERN = r"(?i)(https?://|t\.me/|telegram\.me/|telegram\.dog/|@[a-zA-Z0-9_]+)"

# group=1 ensure karta hai ki ye normal commands se pehle check ho
@Client.on_message(filters.group & filters.text & filters.regex(LINK_PATTERN), group=1)
async def anti_link_system(client: Client, message: Message):
    if not message.from_user:
        return
        
    # 1. Bypass Admins & Owners (Wo links bhej sakte hain)
    try:
        user = await client.get_chat_member(message.chat.id, message.from_user.id)
        if user.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
            return
    except:
        pass
        
    # 2. Instant Delete & Warn Logic
    try:
        # Message ko turant uda do
        await message.delete()
        
        # Ek premium warning bhejo
        warn = await message.reply_text(
            f"⚠️ **{message.from_user.mention}, ʟɪɴᴋs ᴀɴᴅ ᴜsᴇʀɴᴀᴍᴇs ᴀʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ ʜᴇʀᴇ!**\n"
            f"> ➻ *ᴍᴇssᴀɢᴇ ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇᴅ ᴛᴏ ᴘʀᴇᴠᴇɴᴛ sᴘᴀᴍ.*"
        )
        
        # Chat clean rakhne ke liye warning ko 5 sec baad hata do
        await asyncio.sleep(5)
        await warn.delete()
        
    except Exception:
        # Agar bot ke paas delete power nahi hai, toh error ignore karega
        pass
      
