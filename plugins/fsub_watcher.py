import asyncio
from pyrogram import Client, filters, StopPropagation
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatMemberStatus
from database.db import db
from config import Config

@Client.on_message(filters.group & ~filters.bot, group=-1)
async def enforce_strict_fsub(client: Client, message: Message):
    if not message.from_user:
        return

    chat_id = message.chat.id
    user_id = message.from_user.id

    # Owner & Admin Bypass
    if user_id == Config.OWNER_ID:
        return
    try:
        member = await client.get_chat_member(chat_id, user_id)
        if member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return
    except:
        pass

    fsub_active, fsub_channel = await db.get_fsub_config(chat_id)
    if not fsub_active or not fsub_channel:
        return

    target_chat = int(fsub_channel) if str(fsub_channel).startswith("-100") else fsub_channel
    
    # REAL-TIME CHECK: Har message par live API call
    is_participant = False
    try:
        check = await client.get_chat_member(target_chat, user_id)
        if check.status not in [ChatMemberStatus.LEFT, ChatMemberStatus.BANNED]:
            is_participant = True
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
            warn_text = f"**{name}**, you must subscribe to the channel to chat here."
            
            # Button Updated to "Subscribe"
            btn = InlineKeyboardMarkup([[InlineKeyboardButton("📢 Subscribe", url=invite_link)]])
            
            warn_msg = await message.reply_text(warn_text, reply_markup=btn)
            
            # Auto-delete warning
            await asyncio.sleep(10)
            await warn_msg.delete()
            raise StopPropagation
        except StopPropagation:
            raise
        except Exception:
            pass
            
