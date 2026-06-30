import asyncio
from pyrogram import Client, filters, enums, StopPropagation
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
from database.db import db
from config import Config

# RAM Cache taaki bot ko API limit (FloodWait) ka error na aaye
VERIFIED_CACHE = {}

# group=-1 ensures yeh filter sabse pehle run hoga (Commands se bhi pehle)
@Client.on_message(filters.group & ~filters.bot, group=-1)
async def enforce_strict_fsub(client: Client, message: Message):
    if not message.from_user:
        return

    chat_id = message.chat.id
    user_id = message.from_user.id

    # Owner ko hamesha bypass karna hai
    if user_id == Config.OWNER_ID:
        return

    # Check if FSub is active in this group
    fsub_active, fsub_channel = await db.get_fsub_config(chat_id)
    if not fsub_active or not fsub_channel:
        return

    # Cache check (Agar user pehle se verified hai RAM me, toh skip karo)
    cache_key = f"{user_id}_{fsub_channel}"
    if VERIFIED_CACHE.get(cache_key):
        return

    # Check if user is an Admin of the group (Admins bypass FSub)
    try:
        member = await client.get_chat_member(chat_id, user_id)
        if member.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
            return
    except Exception:
        pass

    # Check Channel Membership
    target_chat = int(fsub_channel) if fsub_channel.startswith("-100") else fsub_channel
    is_participant = False

    try:
        check = await client.get_chat_member(target_chat, user_id)
        if check.status not in [enums.ChatMemberStatus.LEFT, enums.ChatMemberStatus.BANNED]:
            is_participant = True
            VERIFIED_CACHE[cache_key] = True # User verified, RAM me save kar lo
    except Exception:
        pass # Not a participant

    # Agar user ne join nahi kiya hai
    if not is_participant:
        try:
            # 1. Message turant delete karo
            await message.delete()
            
            # 2. Invite link nikalo (Public ya Private dono ke liye)
            if str(fsub_channel).startswith("-100"):
                try:
                    invite_link = await client.export_chat_invite_link(int(fsub_channel))
                except Exception:
                    invite_link = "https://t.me/"
            else:
                invite_link = f"https://t.me/{fsub_channel.replace('@', '')}"

            # 3. Exact screenshot jaisa message banao
            name = message.from_user.first_name
            warn_text = f"**{name}**, to write in the chat, you need to subscribe to the channel:\n{fsub_channel}"
            btn = InlineKeyboardMarkup([[InlineKeyboardButton("🛡️ Join & Verify", url=invite_link)]])

            # 4. Warning bhejo
            warn_msg = await message.reply_text(warn_text, reply_markup=btn)

            # 5. Chat clean rakhne ke liye warning ko 10 seconds me auto-delete karo
            await asyncio.sleep(10)
            await warn_msg.delete()

            # StopPropagation ensures ki agar user ne join nahi kiya, toh aage koi command run na ho
            raise StopPropagation
            
        except StopPropagation:
            # Isko explicitly raise karna padta hai varna niche wala Exception isko kha jayega
            raise 
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except Exception as err:
            pass # Ignore deletion errors if bot lacks rights
