import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
from database.db import db
from config import Config

ACTIVE_TAGS = {}

@Client.on_message(filters.command("reload") & filters.group)
async def reload_cmd(client: Client, message: Message):
    member = await client.get_chat_member(message.chat.id, message.from_user.id)
    if member.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER] and message.from_user.id != Config.OWNER_ID:
        return
    await message.reply_text("✅ Admin cache and user list updated successfully!")

@Client.on_message(filters.command(["utag", "tagall"]) & filters.group)
async def utag_cmd(client: Client, message: Message):
    chat_id = message.chat.id
    
    if chat_id in ACTIVE_TAGS:
        ongoing_user = ACTIVE_TAGS[chat_id]
        return await message.reply_text(f"⚠️ **Tagging process is already ongoing by {ongoing_user}.**\nPlease wait for it to complete or use /cancel first.")
    
    member = await client.get_chat_member(chat_id, message.from_user.id)
    if member.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER] and message.from_user.id != Config.OWNER_ID:
        return await message.reply_text("Only admins can use this command!")

    # === FORCE JOIN CHECK BLOCK ===
    try:
        fsub_active, fsub_channel = await db.get_fsub_config(chat_id)
        if fsub_active and fsub_channel:
            # Convert back to integer if it's a private chat ID
            target_chat = int(fsub_channel) if fsub_channel.startswith("-100") else fsub_channel
            
            check = await client.get_chat_member(target_chat, message.from_user.id)
            if check.status in [enums.ChatMemberStatus.LEFT, enums.ChatMemberStatus.BANNED]:
                raise Exception("Not Joined")
    except Exception:
        # Generate Invite Link dynamically if it's a private ID
        if fsub_channel.startswith("-100"):
            try:
                invite_link = await client.export_chat_invite_link(int(fsub_channel))
            except Exception:
                invite_link = "https://t.me/" # Fallback
        else:
            invite_link = f"https://t.me/{fsub_channel.replace('@', '')}"

        btn = InlineKeyboardMarkup([[InlineKeyboardButton("🛡️ Join Channel To Use Bot", url=invite_link)]])
        return await message.reply_text("❌ **Access Denied!**\n\nYou must join our channel to use this bot.", reply_markup=btn)
    # ==============================

    reply_target = message.reply_to_message.id if message.reply_to_message else None
    custom_msg = message.text.split(None, 1)[1] if len(message.command) > 1 else ""
    
    starter_name = message.from_user.first_name
    ACTIVE_TAGS[chat_id] = starter_name
    
    bot_username = client.me.username
    start_text = (
        f"Tag Operation is started by\n**{starter_name}** .\n"
        f"You can use /cancel@{bot_username} Command to **Cancel** the process. Have a nice chat"
    )
    await message.reply_text(start_text)

    users = []
    try:
        async for m in client.get_chat_members(chat_id):
            if m.user.is_bot or m.user.is_deleted:
                continue
            fname = m.user.first_name if m.user.first_name else "User"
            fname = fname.replace("[", "").replace("]", "").replace("*", "").replace("_", "").replace("`", "")
            users.append(f"[{fname}](tg://user?id={m.user.id})")
    except Exception as err:
        ACTIVE_TAGS.pop(chat_id, None)
        return await message.reply_text(f"⚠️ Error fetching members: {err}")

    batch_size = 7
    delay = 2.5

    for i in range(0, len(users), batch_size):
        if chat_id not in ACTIVE_TAGS:
            break
            
        batch = users[i:i + batch_size]
        tags_text = " , ".join(batch)
        
        if custom_msg:
            text = f"**{starter_name}**\n> {custom_msg}\n\n{tags_text}"
        else:
            text = tags_text
        
        try:
            await client.send_message(chat_id, text, reply_to_message_id=reply_target)
            await asyncio.sleep(delay)
        except FloodWait as e_fw:
            await asyncio.sleep(e_fw.value) 
        except Exception:
            continue

    ACTIVE_TAGS.pop(chat_id, None)


@Client.on_message(filters.command(["atag", "tagadmins"]) & filters.group)
async def atag_cmd(client: Client, message: Message):
    chat_id = message.chat.id
    
    if chat_id in ACTIVE_TAGS:
        ongoing_user = ACTIVE_TAGS[chat_id]
        return await message.reply_text(f"⚠️ **Tagging process is already ongoing by {ongoing_user}.**\nPlease wait for it to complete or use /cancel first.")
    
    member = await client.get_chat_member(chat_id, message.from_user.id)
    if member.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER] and message.from_user.id != Config.OWNER_ID:
        return await message.reply_text("Only admins can use this command!")

    reply_target = message.reply_to_message.id if message.reply_to_message else None
    custom_msg = message.text.split(None, 1)[1] if len(message.command) > 1 else ""
    
    starter_name = message.from_user.first_name
    ACTIVE_TAGS[chat_id] = starter_name
    
    bot_username = client.me.username
    await message.reply_text(
        f"Admin Tag Operation is started by\n**{starter_name}** .\n"
        f"You can use /cancel@{bot_username} Command to **Cancel** the process."
    )

    admins = []
    try:
        async for m in client.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            if m.user.is_bot or m.user.is_deleted:
                continue
            fname = m.user.first_name if m.user.first_name else "Admin"
            fname = fname.replace("[", "").replace("]", "").replace("*", "").replace("_", "").replace("`", "")
            admins.append(f"[{fname}](tg://user?id={m.user.id})")
    except Exception as err:
        ACTIVE_TAGS.pop(chat_id, None)
        return await message.reply_text(f"⚠️ Error fetching admins: {err}")

    batch_size = 7
    delay = 2.5

    for i in range(0, len(admins), batch_size):
        if chat_id not in ACTIVE_TAGS:
            break
            
        batch = admins[i:i + batch_size]
        tags_text = " , ".join(batch)
        
        if custom_msg:
            text = f"**{starter_name}**\n> {custom_msg}\n\n{tags_text}"
        else:
            text = tags_text
        
        try:
            await client.send_message(chat_id, text, reply_to_message_id=reply_target)
            await asyncio.sleep(delay)
        except FloodWait as e_fw:
            await asyncio.sleep(e_fw.value) 
        except Exception:
            continue

    ACTIVE_TAGS.pop(chat_id, None)


@Client.on_message(filters.command("cancel") & filters.group)
async def cancel_tag_cmd(client: Client, message: Message):
    chat_id = message.chat.id
    member = await client.get_chat_member(chat_id, message.from_user.id)
    if member.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER] and message.from_user.id != Config.OWNER_ID:
        return
        
    if chat_id in ACTIVE_TAGS:
        ACTIVE_TAGS.pop(chat_id, None)
        await message.reply_text("❌ **Tagging Process Cancelled!**")
    else:
        await message.reply_text("No active tagging process found.")
        
