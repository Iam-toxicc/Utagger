import asyncio
import random
from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
from database.db import db
from utils.emojis import Emojis as e, PREMIUM_EMOJIS
from config import Config

ACTIVE_TAGS = []

@Client.on_message(filters.command("setformat") & filters.group)
async def set_format_cmd(client: Client, message: Message):
    member = await client.get_chat_member(message.chat.id, message.from_user.id)
    if member.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER] and message.from_user.id != Config.OWNER_ID:
        return await message.reply_text(f"{e.CANCEL} Only admins can change the tag format!")

    if len(message.command) < 2:
        text = f"{e.SETTING} **Custom Tag Format Setup**\n\nUse placeholders:\n`{{name}}` - User's first name\n`{{username}}` - User's username\n`{{id}}` - User's Telegram ID\n`{{emoji}}` - Random premium emoji\n\n**Example:** `/setformat {{emoji}} [{{name}}](tg://user?id={{id}})`"
        return await message.reply_text(text)

    new_format = message.text.split(None, 1)[1]
    await db.set_tag_format(message.chat.id, new_format)
    await message.reply_text(f"{e.TICK} **Tag format updated to:**\n`{new_format}`")


@Client.on_message(filters.command(["tagall", "all"]) & filters.group)
async def tag_all_cmd(client: Client, message: Message):
    chat_id = message.chat.id
    
    if chat_id in ACTIVE_TAGS:
        return await message.reply_text(f"{e.CANCEL} A tagging process is already running! Use /cancel first.")
    
    member = await client.get_chat_member(chat_id, message.from_user.id)
    if member.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER] and message.from_user.id != Config.OWNER_ID:
        return await message.reply_text(f"{e.CANCEL} Only admins can use tagall!")

    # === FORCE JOIN CHECK BLOCK ===
    fsub_active, fsub_channel = await db.get_fsub_config(chat_id)
    if fsub_active and fsub_channel:
        try:
            # Check user status in the required channel
            check = await client.get_chat_member(fsub_channel, message.from_user.id)
            if check.status in [enums.ChatMemberStatus.LEFT, enums.ChatMemberStatus.BANNED]:
                raise Exception("Not a member")
        except Exception:
            # Join button generate karna
            btn = InlineKeyboardMarkup([[InlineKeyboardButton(f"{e.SHIELD} Join Channel To Use Bot", url=f"https://t.me/{fsub_channel.replace('@', '')}")]])
            return await message.reply_text(f"{e.CANCEL} **Access Denied!**\n\nYou must join our channel to use this bot.", reply_markup=btn)
    # ==============================

    custom_msg = message.text.split(None, 1)[1] if len(message.command) > 1 else "Wake up everyone!"
    ACTIVE_TAGS.append(chat_id)
    
    status_msg = await message.reply_text(f"{e.FLASH} **Gathering members...**")
    tag_format = await db.get_tag_format(chat_id)
    users = []
    
    try:
        async for m in client.get_chat_members(chat_id):
            if m.user.is_bot or m.user.is_deleted:
                continue
            
            f_name = m.user.first_name
            f_username = m.user.username if m.user.username else f_name
            f_id = m.user.id
            f_emoji = random.choice(PREMIUM_EMOJIS)
            
            tag_string = tag_format.format(name=f_name, username=f_username, id=f_id, emoji=f_emoji)
            users.append(tag_string)
            
    except Exception as err:
        if chat_id in ACTIVE_TAGS: ACTIVE_TAGS.remove(chat_id)
        return await status_msg.edit_text(f"{e.CANCEL} Error fetching members: {err}")

    await status_msg.edit_text(f"{e.FLASH} **Tagging Started!**\n{e.SHIELD} Target: {len(users)} users\n{e.SETTING} Message: {custom_msg}")

    # TODO: Inko database settings se link karna baaki hai
    batch_size = 5 
    delay = 2

    for i in range(0, len(users), batch_size):
        if chat_id not in ACTIVE_TAGS:
            break
            
        batch = users[i:i + batch_size]
        text = f"**{custom_msg}**\n\n" + "\n".join(batch)
        
        try:
            await client.send_message(chat_id, text)
            await asyncio.sleep(delay)
        except FloodWait as e_fw:
            await asyncio.sleep(e_fw.value) 
        except Exception:
            continue

    if chat_id in ACTIVE_TAGS:
        ACTIVE_TAGS.remove(chat_id)
        await message.reply_text(f"{e.TICK} **Tagging Completed Successfully!**")


@Client.on_message(filters.command("cancel") & filters.group)
async def cancel_tag_cmd(client: Client, message: Message):
    chat_id = message.chat.id
    member = await client.get_chat_member(chat_id, message.from_user.id)
    if member.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER] and message.from_user.id != Config.OWNER_ID:
        return
        
    if chat_id in ACTIVE_TAGS:
        ACTIVE_TAGS.remove(chat_id)
        await message.reply_text(f"{e.CANCEL} **Tagging Process Stopped by Admin!**")
    else:
        await message.reply_text("No active tagging process found.")
        
