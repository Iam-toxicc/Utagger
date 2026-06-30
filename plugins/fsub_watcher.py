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
    
    is_participant = False
    try:
        check = await client.get_chat_member(target_chat, user_id)
        if check.status not in [ChatMemberStatus.LEFT, ChatMemberStatus.BANNED]:
            is_participant = True
    except Exception:
        pass

    if not is_participant:
        try:
            await message.delete()
            
            # Link Logic
            is_private = str(fsub_channel).startswith("-100")
            invite_link = f"https://t.me/{str(fsub_channel).replace('@', '')}"
            if is_private:
                try:
                    invite_link = await client.export_chat_invite_link(int(fsub_channel))
                except:
                    pass

            # Message Formatting
            name = message.from_user.first_name
            username = f"@{message.from_user.username}" if message.from_user.username else ""
            
            # Logic: Agar public channel hai toh @username dikhao, varna simple msg
            if not is_private:
                warn_text = f"**{name}** {username}, to write in the chat, you need to subscribe to the channel:\n{fsub_channel}"
            else:
                warn_text = f"**{name}** {username}, to write in the chat, you need to subscribe to the channel."

            btn = InlineKeyboardMarkup([[InlineKeyboardButton("📢 Subscribe", url=invite_link)]])
            
            warn_msg = await message.reply_text(warn_text, reply_markup=btn)
            
            await asyncio.sleep(10)
            await warn_msg.delete()
            raise StopPropagation
        except StopPropagation:
            raise
        except Exception:
            pass
            
