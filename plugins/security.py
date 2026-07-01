import re
import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import Message
from pyrogram.errors import UserNotParticipant

# Database
GROUP_SETTINGS = {}
AUTH_USERS = set()

def get_settings(chat_id):
    if chat_id not in GROUP_SETTINGS:
        GROUP_SETTINGS[chat_id] = {
            "biolink_enabled": False, 
            "fsub": False, 
            "fsub_channel": None, 
            "anti_spam": False
        }
    return GROUP_SETTINGS[chat_id]

# --- COMMANDS ---

@Client.on_message(filters.command("biolink") & filters.group)
async def toggle_biolink(client: Client, message: Message):
    user = await client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
        return await message.reply_text("❌ **Only admins can change security settings!**")
    state = message.command[1].lower() if len(message.command) > 1 else None
    if state not in ["on", "off"]: return await message.reply_text("⊚ **Usage:** `/biolink on` or `/biolink off`")
    get_settings(message.chat.id)["biolink_enabled"] = (state == "on")
    await message.reply_text(f"✅ **Biolink security {state.upper()}!**")

@Client.on_message(filters.command("fsub") & filters.group)
async def toggle_fsub(client: Client, message: Message):
    user = await client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
        return
    state = message.command[1].lower() if len(message.command) > 1 else None
    settings = get_settings(message.chat.id)
    if state == "on":
        if not settings.get("fsub_channel"): return await message.reply_text("❌ Set channel first using /setfsub")
        settings["fsub"] = True
    else: settings["fsub"] = False
    await message.reply_text(f"✅ **F-Sub security {state.upper()}!**")

@Client.on_message(filters.command("setfsub") & filters.group)
async def set_fsub(client: Client, message: Message):
    if len(message.command) < 2: return
    channel = message.command[1]
    settings = get_settings(message.chat.id)
    settings["fsub_channel"] = channel if channel.startswith("@") or channel.isdigit() else f"@{channel}"
    settings["fsub"] = True
    await message.reply_text(f"✅ **F-Sub channel set to {settings['fsub_channel']}**")

@Client.on_message(filters.command("anti") & filters.group)
async def toggle_antispam(client: Client, message: Message):
    settings = get_settings(message.chat.id)
    settings["anti_spam"] = not settings.get("anti_spam", False)
    await message.reply_text(f"✅ **Anti-Forward (Anti-Spam) is now {'ON' if settings['anti_spam'] else 'OFF'}**")

@Client.on_message(filters.command("auth") & filters.group)
async def auth_user(client: Client, message: Message):
    if not message.reply_to_message: return await message.reply_text("❌ Reply to a user.")
    AUTH_USERS.add(message.reply_to_message.from_user.id)
    await message.reply_text("✅ **User Authorized!** They now bypass all security.")

@Client.on_message(filters.command("unauth") & filters.group)
async def unauth_user(client: Client, message: Message):
    if not message.reply_to_message: return
    target_id = message.reply_to_message.from_user.id
    if target_id in AUTH_USERS:
        AUTH_USERS.remove(target_id)
        await message.reply_text("❌ **User Unauthorized.**")

# --- CORE SECURITY ENGINE ---
@Client.on_message(filters.group & ~filters.bot, group=2)
async def security_check(client: Client, message: Message):
    if not message.from_user: return
    chat_id = message.chat.id
    settings = get_settings(chat_id)
    user_id = message.from_user.id

    # 1. Admin/Auth Bypass
    try:
        member = await client.get_chat_member(chat_id, user_id)
        if member.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER] or user_id in AUTH_USERS:
            return
    except: pass

    # 2. Anti-Forward Check
    if settings.get("anti_spam") and (message.forward_from or message.forward_from_chat or message.forward_sender_name):
        await message.delete()
        return

    # 3. FSUB Check
    if settings.get("fsub") and settings.get("fsub_channel"):
        try:
            await client.get_chat_member(settings["fsub_channel"], user_id)
        except UserNotParticipant:
            await message.delete()
            warn = await message.reply_text(f"❌ Join {settings['fsub_channel']} to message!")
            await asyncio.sleep(10); await warn.delete()
            return

    # 4. Biolink Check
    if settings.get("biolink_enabled"):
        try:
            user_chat = await client.get_chat(user_id)
            if re.search(r"(https?://|t\.me/|@[a-zA-Z0-9_]+)", user_chat.bio or "", re.IGNORECASE):
                await message.delete()
                warn = await message.reply_text("⚠️ **Action Required:** Remove link from bio to message.")
                await asyncio.sleep(10); await warn.delete()
        except: pass
            
