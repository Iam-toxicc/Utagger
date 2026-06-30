from pyrogram import Client, filters, enums
from pyrogram.types import Message
from database.db import db
from utils.emojis import Emojis as e
from config import Config

@Client.on_message(filters.command("setfsub") & filters.group)
async def set_fsub_cmd(client: Client, message: Message):
    chat_id = message.chat.id
    
    # Admin Check
    member = await client.get_chat_member(chat_id, message.from_user.id)
    if member.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER] and message.from_user.id != Config.OWNER_ID:
        return await message.reply_text(f"{e.CANCEL} Only admins can configure Force Join!")

    if len(message.command) < 2:
        return await message.reply_text(f"{e.SETTING} **Force Join Setup**\n\nPlease provide your channel's username or ID.\n**Example:** `/setfsub @TGVoidAPI_Updates`\n\n*Note: The bot MUST be an admin in that channel!*")

    channel_input = message.command[1]
    
    # Verify if bot is admin in the provided channel
    try:
        bot_member = await client.get_chat_member(channel_input, client.me.id)
        if bot_member.status != enums.ChatMemberStatus.ADMINISTRATOR:
            return await message.reply_text(f"{e.CANCEL} I must be an Admin in `{channel_input}` to check if users have joined!")
    except Exception as err:
        return await message.reply_text(f"{e.CANCEL} Failed to verify channel. Make sure the username is correct and I am an admin there.\nError: `{err}`")

    # Save to Database
    await db.set_fsub_channel(chat_id, channel_input)
    await db.update_fsub_status(chat_id, True) # Auto-turn ON after setting
    
    await message.reply_text(f"{e.TICK} **Force Join Activated!**\n\nUsers must now join {channel_input} to use tagging commands.\nUse `/fsub off` to disable it.")


@Client.on_message(filters.command(["fsub", "forcejoin"]) & filters.group)
async def toggle_fsub_cmd(client: Client, message: Message):
    chat_id = message.chat.id
    
    member = await client.get_chat_member(chat_id, message.from_user.id)
    if member.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER] and message.from_user.id != Config.OWNER_ID:
        return await message.reply_text(f"{e.CANCEL} Only admins can toggle Force Join!")

    if len(message.command) < 2 or message.command[1].lower() not in ["on", "off"]:
        status, channel = await db.get_fsub_config(chat_id)
        state_text = f"✅ ON" if status else f"❌ OFF"
        chan_text = channel if channel else "Not Set"
        return await message.reply_text(f"{e.SETTING} **Force Join Status:** {state_text}\n**Channel:** {chan_text}\n\nTo change, use `/fsub on` or `/fsub off`")

    action = message.command[1].lower()
    
    if action == "on":
        _, channel = await db.get_fsub_config(chat_id)
        if not channel:
            return await message.reply_text(f"{e.CANCEL} No channel set! Use `/setfsub @username` first.")
        await db.update_fsub_status(chat_id, True)
        await message.reply_text(f"{e.TICK} **Force Join turned ON!**")
        
    elif action == "off":
        await db.update_fsub_status(chat_id, False)
        await message.reply_text(f"{e.CANCEL} **Force Join turned OFF!**")
      
