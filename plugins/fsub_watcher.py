import asyncio
import time
from pyrogram import Client, filters, enums
from pyrogram.handlers.message_handler import StopPropagation
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database.db import db
from config import Config

# Format: {"user_id_channel": expiry_timestamp}
VERIFIED_CACHE = {}

@Client.on_message(filters.group & ~filters.bot, group=-1)
async def enforce_strict_fsub(client: Client, message: Message):
    if not message.from_user:
        return

    chat_id = message.chat.id
    user_id = message.from_user.id

    # Owner Bypass
    if user_id == Config.OWNER_ID:
        return

    # Check Database for FSUB Configuration
    fsub_active, fsub_channel = await db.get_fsub_config(chat_id)
    if not fsub_active or not fsub_channel:
        return

    target_chat = int(fsub_channel) if str(fsub_channel).startswith("-100") else fsub_channel
    cache_key = f"{user_id}_{target_chat}"
    current_time = time.time()

    # 1. Check Smart Cache (Valid for 60 seconds only)
    if cache_key in VERIFIED_CACHE:
        if current_time < VERIFIED_CACHE[cache_key]:
            return # User is temporarily cached as verified, skip heavy API call
        else:
            del VERIFIED_CACHE[cache_key] # Cache expired, check again!

    # 2. Check if user is Admin in the Group (Admins bypass FSub)
    try:
        member = await client.get_chat_member(chat_id, user_id)
        if member.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
            return
    except:
        pass

    # 3. Live Check from Telegram API
    is_participant = False
    try:
        check = await client.get_chat_member(target_chat, user_id)
        if check.status not in [enums.ChatMemberStatus.LEFT, enums.ChatMemberStatus.BANNED]:
            is_participant = True
            # Cache the user's status for 60 seconds
            VERIFIED_CACHE[cache_key] = current_time + 60 
    except Exception:
        pass # Not a member or error checking

    # 4. Action if Not Joined
    if not is_participant:
        try:
            # Message delete karo
            await message.delete()
            
            # Link Generate karo
            invite_link = f"https://t.me/{str(fsub_channel).replace('@', '')}"
            if str(fsub_channel).startswith("-100"):
                try:
                    invite_link = await client.export_chat_invite_link(int(fsub_channel))
                except:
                    pass

            # Warning bhejo
            name = message.from_user.first_name
            warn_text = f"**{name}**, to write in the chat, you need to subscribe to the channel:\n{fsub_channel}"
            btn = InlineKeyboardMarkup([[InlineKeyboardButton("🛡️ Join & Verify", url=invite_link)]])
            
            warn_msg = await message.reply_text(warn_text, reply_markup=btn)

            # Auto-delete warning
            await asyncio.sleep(10)
            await warn_msg.delete()
            
            # Stop command execution
            raise StopPropagation
            
        except StopPropagation:
            raise
        except Exception:
            pass
            
