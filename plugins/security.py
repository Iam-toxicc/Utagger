import re
import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import Message
from pyrogram.errors import UserNotParticipant

# ----------------- DATABASE (TEMPORARY) -----------------
GROUP_SETTINGS = {}
AUTH_USERS = set()  # Master whitelist for bypassing all security checks

def get_settings(chat_id):
    if chat_id not in GROUP_SETTINGS:
        GROUP_SETTINGS[chat_id] = {"biolink_enabled": False, "fsub": False, "fsub_channel": None}
    return GROUP_SETTINGS[chat_id]

# ----------------- BIOLINK TOGGLE -----------------
@Client.on_message(filters.command("biolink") & filters.group)
async def toggle_biolink(client: Client, message: Message):
    user = await client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
        return await message.reply_text("❌ **ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴄʜᴀɴɢᴇ sᴇᴄᴜʀɪᴛʏ sᴇᴛᴛɪɴɢs!**")

    if len(message.command) < 2 or message.command[1].lower() not in ["on", "off"]:
        return await message.reply_text("⊚ **ᴜsᴀɢᴇ :** `/biolink on` ᴏʀ `/biolink off`")
    
    state = message.command[1].lower()
    settings = get_settings(message.chat.id)
    
    if state == "on":
        settings["biolink_enabled"] = True
        await message.reply_text("✅ **ʙɪᴏʟɪɴᴋ sᴇᴄᴜʀɪᴛʏ ᴇɴᴀʙʟᴇᴅ!**")
    else:
        settings["biolink_enabled"] = False
        await message.reply_text("❌ **ʙɪᴏʟɪɴᴋ sᴇᴄᴜʀɪᴛʏ ᴅɪsᴀʙʟᴇᴅ!**")

# ----------------- FSUB TOGGLE (NEW) -----------------
@Client.on_message(filters.command("fsub") & filters.group)
async def toggle_fsub(client: Client, message: Message):
    user = await client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
        return await message.reply_text("❌ **ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs!**")
        
    if len(message.command) < 2 or message.command[1].lower() not in ["on", "off"]:
        return await message.reply_text("⊚ **ᴜsᴀɢᴇ :** `/fsub on` ᴏʀ `/fsub off`")
        
    state = message.command[1].lower()
    settings = get_settings(message.chat.id)
    
    if state == "on":
        if not settings.get("fsub_channel"):
            return await message.reply_text("❌ **ᴘʟᴇᴀsᴇ sᴇᴛ ᴀ ᴄʜᴀɴɴᴇʟ ғɪʀsᴛ ᴜsɪɴɢ `/setfsub`**")
        settings["fsub"] = True
        await message.reply_text("✅ **ғ-sᴜʙ sᴇᴄᴜʀɪᴛʏ ᴇɴᴀʙʟᴇᴅ!**")
    else:
        settings["fsub"] = False
        await message.reply_text("❌ **ғ-sᴜʙ sᴇᴄᴜʀɪᴛʏ ᴅɪsᴀʙʟᴇᴅ & ʀᴇsᴇᴛ!**")

# ----------------- SET FSUB CHANNEL -----------------
@Client.on_message(filters.command("setfsub") & filters.group)
async def set_fsub(client: Client, message: Message):
    user = await client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
        return await message.reply_text("❌ **ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs!**")
        
    if len(message.command) < 2:
        return await message.reply_text("⊚ **ᴜsᴀɢᴇ :** `/setfsub @YourChannel` ᴏʀ `-100xxxx`")
        
    channel = message.command[1]
    
    if channel.startswith("-100") and channel.lstrip("-").isdigit():
        channel = int(channel)
    elif not channel.startswith("@") and not channel.lstrip("-").isdigit():
        channel = f"@{channel}"
        
    settings = get_settings(message.chat.id)
    settings["fsub_channel"] = channel
    settings["fsub"] = True  
    
    await message.reply_text(
        f"✅ **ғ-sᴜʙ ᴄʜᴀɴɴᴇʟ sᴇᴛ & ᴇɴᴀʙʟᴇᴅ!**\n"
        f"> ➻ **ᴄʜᴀɴɴᴇʟ :** {channel}\n"
        f"> ➻ ⚠️ **ɴᴏᴛᴇ :** ᴍᴀᴋᴇ sᴜʀᴇ ʙᴏᴛ ɪs ᴀᴅᴍɪɴ ɪɴ {channel}!"
    )

# ----------------- AUTH COMMAND -----------------
@Client.on_message(filters.command("auth") & filters.group)
async def auth_user(client: Client, message: Message):
    user = await client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
        return await message.reply_text("❌ **ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴀᴜᴛʜᴏʀɪᴢᴇ ᴜsᴇʀs!**")

    if not message.reply_to_message:
        return await message.reply_text("❌ **ᴘʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ ᴛᴏ ᴀᴜᴛʜ ᴛʜᴇᴍ.**")
    
    target_id = message.reply_to_message.from_user.id
    AUTH_USERS.add(target_id)
    
    await message.reply_text(
        f"✅ **{message.reply_to_message.from_user.mention} ʜᴀs ʙᴇᴇɴ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ!**\n"
        f"> ➻ ᴛʜᴇʏ ᴄᴀɴ ɴᴏᴡ ʙʏᴘᴀss ғsᴜʙ & ʙɪᴏʟɪɴᴋ sᴇᴄᴜʀɪᴛʏ."
    )

# ----------------- UNAUTH COMMAND (NEW) -----------------
@Client.on_message(filters.command("unauth") & filters.group)
async def unauth_user(client: Client, message: Message):
    user = await client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
        return await message.reply_text("❌ **ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ!**")

    if not message.reply_to_message:
        return await message.reply_text("❌ **ᴘʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ ᴛᴏ ʀᴇᴍᴏᴠᴇ ᴛʜᴇɪʀ ᴀᴜᴛʜ.**")
    
    target_id = message.reply_to_message.from_user.id
    if target_id in AUTH_USERS:
        AUTH_USERS.remove(target_id)
        await message.reply_text(f"❌ **{message.reply_to_message.from_user.mention}'s ᴀᴜᴛʜ ʜᴀs ʙᴇᴇɴ ʀᴇᴍᴏᴠᴇᴅ!**\n> ➻ ᴛʜᴇʏ ᴡɪʟʟ ɴᴏᴡ ғᴀᴄᴇ ɴᴏʀᴍᴀʟ sᴇᴄᴜʀɪᴛʏ ᴄʜᴇᴄᴋs.")
    else:
        await message.reply_text("⚠️ **ᴛʜɪs ᴜsᴇʀ ɪs ɴᴏᴛ ɪɴ ᴛʜᴇ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ʟɪsᴛ.**")

# ----------------- CORE SECURITY ENGINE (MONITOR) -----------------
@Client.on_message(filters.group & ~filters.bot, group=2)
async def security_check(client: Client, message: Message):
    if not message.from_user:
        return
        
    chat_id = message.chat.id
    settings = get_settings(chat_id)
    user_id = message.from_user.id
    
    try:
        chat_member = await client.get_chat_member(chat_id, user_id)
        if chat_member.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
            return
    except Exception:
        pass
        
    if user_id in AUTH_USERS:
        return

    # ================= FSUB CHECK =================
    fsub_channel = settings.get("fsub_channel")
    if settings.get("fsub", False) and fsub_channel:
        is_participant = False
        try:
            member = await client.get_chat_member(fsub_channel, user_id)
            if member.status not in [enums.ChatMemberStatus.LEFT, enums.ChatMemberStatus.BANNED]:
                is_participant = True
        except UserNotParticipant:
            is_participant = False
        except Exception:
            is_participant = True 
            
        if not is_participant:
            await message.delete()
            fsub_warn = await message.reply_text(
                f"❌ **{message.from_user.mention}, ʏᴏᴜ ᴍᴜsᴛ ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴍᴇssᴀɢᴇ!**\n"
                f"> ➻ **ᴄʜᴀɴɴᴇʟ :** {fsub_channel}\n"
                f"> ➻ **ᴀᴅᴍɪɴs :** ᴜsᴇ `/auth` ᴛᴏ ʙʏᴘᴀss.\n\n"
                f"**ɴᴏᴛᴇ :** ᴛʜɪs ᴡᴀʀɴɪɴɢ ᴡɪʟʟ ʙᴇ ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇᴅ ɪɴ 10 sᴇᴄᴏɴᴅs."
            )
            await asyncio.sleep(10)
            await fsub_warn.delete()
            return  

    # ================= BIOLINK CHECK =================
    if settings.get("biolink_enabled", False):
        try:
            user_chat = await client.get_chat(user_id)
            bio = user_chat.bio or ""
            
            if re.search(r"(https?://|t\.me/|@[a-zA-Z0-9_]+)", bio, re.IGNORECASE):
                await message.delete()
                bio_warn = await message.reply_text(
                    f"> ⚠️ **ᴀᴄᴛɪᴏɴ ʀᴇǫᴜɪʀᴇᴅ :**\n>\n"
                    f"> ➻ **ᴜsᴇʀ :** {message.from_user.mention}\n"
                    f"> ➻ **ɪssᴜᴇ :** ʏᴏᴜʀ ʙɪᴏ ᴄᴏɴᴛᴀɪɴs ᴀ ʟɪɴᴋ ᴏʀ ᴜsᴇʀɴᴀᴍᴇ.\n"
                    f"> ➻ **ʀᴇǫᴜᴇsᴛ :** ᴘʟᴇᴀsᴇ ʀᴇᴍᴏᴠᴇ ɪᴛ ᴏʀ ᴀsᴋ ᴀᴅᴍɪɴs ᴛᴏ `/auth` ʏᴏᴜ.\n\n"
                    f"**ɴᴏᴛᴇ :** ᴛʜɪs ᴡᴀʀɴɪɴɢ ᴡɪʟʟ ʙᴇ ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇᴅ ɪɴ 10 sᴇᴄᴏɴᴅs."
                )
                await asyncio.sleep(10)
                await bio_warn.delete()
        except Exception:
            pass
            
