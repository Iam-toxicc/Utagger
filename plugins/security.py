import re
from pyrogram import Client, filters, enums
from pyrogram.types import Message
from pyrogram.errors import UserNotParticipant

# In-memory temporary database (Jisse turant kaam kare)
GROUP_SETTINGS = {}

def get_settings(chat_id):
    if chat_id not in GROUP_SETTINGS:
        # Default settings: Anti-spam ON, F-Sub OFF
        GROUP_SETTINGS[chat_id] = {"fsub": False, "antispam": True, "fsub_channel": None}
    return GROUP_SETTINGS[chat_id]

# ----------------- SET FSUB CHANNEL COMMAND -----------------
@Client.on_message(filters.command("setfsub") & filters.group)
async def set_fsub(client: Client, message: Message):
    user = await client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
        return await message.reply_text("❌ **ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs!**")
        
    if len(message.command) < 2:
        return await message.reply_text("⊚ **ᴜsᴀɢᴇ :** `/setfsub @YourChannel`\n> ➻ Example: `/setfsub @ToxicTGUpdates`")
        
    channel = message.command[1]
    settings = get_settings(message.chat.id)
    settings["fsub_channel"] = channel
    
    await message.reply_text(f"⊚ **ғ-sᴜʙ ᴄʜᴀɴɴᴇʟ sᴇᴛ!**\n> ➻ **ᴄʜᴀɴɴᴇʟ :** {channel}\n> ➻ ɴᴏᴡ ᴛᴜʀɴ ᴏɴ ғ-sᴜʙ ғʀᴏᴍ `/settings`.")

# ----------------- MAIN SECURITY ENFORCER -----------------
# group=1 makes it run alongside your other commands without blocking them
@Client.on_message(filters.group & ~filters.bot, group=1) 
async def security_check(client: Client, message: Message):
    chat_id = message.chat.id
    settings = get_settings(chat_id)
    
    # 1. Skip admins from security checks (Admins can do anything)
    user = await client.get_chat_member(chat_id, message.from_user.id)
    if user.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
        return

    # 2. F-SUB CHECK (Agar on hai aur user ne join nahi kiya)
    if settings["fsub"] and settings["fsub_channel"]:
        try:
            await client.get_chat_member(settings["fsub_channel"], message.from_user.id)
        except UserNotParticipant:
            await message.delete()
            return await message.reply_text(
                f"❌ **{message.from_user.mention}, ʏᴏᴜ ᴍᴜsᴛ ᴊᴏɪɴ {settings['fsub_channel']} ᴛᴏ ᴍᴇssᴀɢᴇ ʜᴇʀᴇ!**", 
                quote=True
            )
        except Exception:
            pass # Agar channel invalid hai ya bot admin nahi hai wahan

    # 3. ANTI-SPAM CHECK (Agar on hai toh Links/Forwards delete karega)
    if settings["antispam"]:
        has_link = message.text and re.search(r"(https?://|t\.me/|telegram\.me/)", message.text, re.IGNORECASE)
        has_forward = message.forward_date is not None
        
        if has_link or has_forward:
            await message.delete()
            await message.reply_text(f"🚫 **{message.from_user.mention}, ʟɪɴᴋs ᴀɴᴅ ғᴏʀᴡᴀʀᴅs ᴀʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ!**", quote=True)
          
