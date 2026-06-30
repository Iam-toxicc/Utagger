import asyncio
from pyrogram import Client, filters, StopPropagation
from pyrogram.types import Message, ChatMemberUpdated, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatMemberStatus
from database.db import db
from config import Config

# Global Cache
VERIFIED_CACHE = {}

# 1. CHANNEL LEAVE DETECTOR (Jab banda channel leave kare, cache turant delete)
@Client.on_chat_member_updated(filters.channel)
async def handle_channel_leave(client: Client, event: ChatMemberUpdated):
    if event.new_chat_member and event.new_chat_member.status == ChatMemberStatus.LEFT:
        user_id = event.new_chat_member.user.id
        channel_id = event.chat.id
        cache_key = f"{user_id}_{channel_id}"
        
        # Cache se hatao, taaki agle msg par bot check kare
        if cache_key in VERIFIED_CACHE:
            del VERIFIED_CACHE[cache_key]

# 2. MESSAGE WATCHER (Gatekeeper)
@Client.on_message(filters.group & ~filters.bot, group=-1)
async def enforce_strict_fsub(client: Client, message: Message):
    if not message.from_user:
        return

    chat_id = message.chat.id
    user_id = message.from_user.id

    if user_id == Config.OWNER_ID:
        return

    fsub_active, fsub_channel = await db.get_fsub_config(chat_id)
    if not fsub_active or not fsub_channel:
        return

    target_chat = int(fsub_channel) if str(fsub_channel).startswith("-100") else fsub_channel
    cache_key = f"{user_id}_{target_chat}"

    # Cache check
    if VERIFIED_CACHE.get(cache_key):
        return

    # Check Admin Bypass
    try:
        member = await client.get_chat_member(chat_id, user_id)
        if member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return
    except:
        pass

    # Live Check
    is_participant = False
    try:
        check = await client.get_chat_member(target_chat, user_id)
        if check.status not in [ChatMemberStatus.LEFT, ChatMemberStatus.BANNED]:
            is_participant = True
            VERIFIED_CACHE[cache_key] = True 
    except Exception:
        pass

    # Action
    if not is_participant:
        try:
            await message.delete()
            
            invite_link = f"https://t.me/{str(fsub_channel).replace('@', '')}"
            if str(fsub_channel).startswith("-100"):
                try:
                    invite_link = await client.export_chat_invite_link(int(fsub_channel))
                except:
                    pass

            name = message.from_user.first_name
            warn_text = f"**{name}**, to write in the chat, you need to subscribe to the channel:\n{fsub_channel}"
            btn = InlineKeyboardMarkup([[InlineKeyboardButton("🛡️ Join & Verify", url=invite_link)]])
            
            warn_msg = await message.reply_text(warn_text, reply_markup=btn)
            await asyncio.sleep(10)
            await warn_msg.delete()
            raise StopPropagation
        except StopPropagation:
            raise
        except Exception:
            pass
            
