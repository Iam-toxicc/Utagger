import re
import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import Message

# ----------------- DATABASE (TEMPORARY) -----------------
# (Agar server restart hoga toh ye reset ho jayega, baad me isse MongoDB/SQL me convert kar lena)
GROUP_SETTINGS = {}
APPROVED_USERS = set()

def get_settings(chat_id):
    if chat_id not in GROUP_SETTINGS:
        GROUP_SETTINGS[chat_id] = {"biolink_enabled": False}
    return GROUP_SETTINGS[chat_id]

# ----------------- TOGGLE BIOLINK COMMAND -----------------
@Client.on_message(filters.command("biolink") & filters.group)
async def toggle_biolink(client: Client, message: Message):
    # Check if user is Admin
    user = await client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
        return await message.reply_text("❌ **Only admins can change Biolink settings!**")

    # Command Usage Check
    if len(message.command) < 2 or message.command[1].lower() not in ["on", "off"]:
        return await message.reply_text("⊚ **ᴜsᴀɢᴇ :** `/biolink on` ᴏʀ `/biolink off`")
    
    state = message.command[1].lower()
    settings = get_settings(message.chat.id)
    
    if state == "on":
        settings["biolink_enabled"] = True
        await message.reply_text("✅ **ʙɪᴏʟɪɴᴋ sᴇᴄᴜʀɪᴛʏ ᴇɴᴀʙʟᴇᴅ!**\n> ➻ ᴜsᴇʀs ᴡɪᴛʜ ʟɪɴᴋs ɪɴ ᴛʜᴇɪʀ ʙɪᴏ ᴡɪʟʟ ʙᴇ ʀᴇsᴛʀɪᴄᴛᴇᴅ.")
    else:
        settings["biolink_enabled"] = False
        await message.reply_text("❌ **ʙɪᴏʟɪɴᴋ sᴇᴄᴜʀɪᴛʏ ᴅɪsᴀʙʟᴇᴅ!**")

# ----------------- APPROVE COMMAND -----------------
@Client.on_message(filters.command("approve") & filters.group)
async def approve_user(client: Client, message: Message):
    # Check if user is Admin
    user = await client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
        return await message.reply_text("❌ **Only admins can approve users!**")

    if not message.reply_to_message:
        return await message.reply_text("❌ **ᴘʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ ᴛᴏ ᴀᴘᴘʀᴏᴠᴇ ᴛʜᴇᴍ.**")
    
    target_id = message.reply_to_message.from_user.id
    APPROVED_USERS.add(target_id)
    
    await message.reply_text(f"✅ **{message.reply_to_message.from_user.mention} ʜᴀs ʙᴇᴇɴ ᴀᴘᴘʀᴏᴠᴇᴅ!**\n> ➻ ᴛʜᴇʏ ᴄᴀɴ ɴᴏᴡ ᴍᴇssᴀɢᴇ ʙʏᴘᴀssɪɴɢ ʙɪᴏʟɪɴᴋ sᴇᴄᴜʀɪᴛʏ.")

# ----------------- CORE SECURITY ENGINE (MONITOR) -----------------
# group=2 ensures it runs in the background for every message without blocking commands
@Client.on_message(filters.group & ~filters.bot, group=2)
async def biolink_check(client: Client, message: Message):
    if not message.from_user:
        return
        
    chat_id = message.chat.id
    settings = get_settings(chat_id)
    
    # 1. Agar feature OFF hai, toh kuch mat karo
    if not settings.get("biolink_enabled", False):
        return

    user_id = message.from_user.id
    
    # 2. Skip checks for Admins
    chat_member = await client.get_chat_member(chat_id, user_id)
    if chat_member.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
        return
        
    # 3. Skip checks if user is in APPROVED list
    if user_id in APPROVED_USERS:
        return
        
    # 4. Fetch Live Bio and Check
    try:
        user_info = await client.get_users(user_id)
        bio = user_info.bio or ""
        
        # Detect http/https, t.me, or @username in bio
        if re.search(r"(https?://|t\.me/|@[a-zA-Z0-9_]+)", bio, re.IGNORECASE):
            await message.delete()
            
            # Send Warning
            warning = await message.reply_text(
                f"> ⚠️ **ᴀᴄᴛɪᴏɴ ʀᴇǫᴜɪʀᴇᴅ :**\n>\n"
                f"> ➻ **ᴜsᴇʀ :** {message.from_user.mention}\n"
                f"> ➻ **ɪssᴜᴇ :** ʏᴏᴜʀ ʙɪᴏ ᴄᴏɴᴛᴀɪɴs ᴀ ʟɪɴᴋ ᴏʀ ᴜsᴇʀɴᴀᴍᴇ.\n"
                f"> ➻ **ʀᴇǫᴜᴇsᴛ :** ᴘʟᴇᴀsᴇ ʀᴇᴍᴏᴠᴇ ɪᴛ ᴛᴏ ᴍᴇssᴀɢᴇ ʜᴇʀᴇ.\n\n"
                f"**ɴᴏᴛᴇ :** ᴛʜɪs ᴡᴀʀɴɪɴɢ ᴡɪʟʟ ʙᴇ ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇᴅ ɪɴ 10 sᴇᴄᴏɴᴅs."
            )
            
            # Auto-delete warning after 10 seconds
            await asyncio.sleep(10)
            await warning.delete()
            
    except Exception as e:
        # Ignore minor errors like API timeouts
        pass
        
