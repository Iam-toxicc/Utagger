from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database.db import db
from utils.emojis import Emojis as e
from config import Config

# Helper function to generate settings keyboard
async def get_settings_markup(chat_id):
    fsub_active, fsub_channel = await db.get_fsub_config(chat_id)
    fsub_btn_text = "✅ ON" if fsub_active else "❌ OFF"
    chan_text = fsub_channel if fsub_channel else "Not Set"

    return InlineKeyboardMarkup([
        [InlineKeyboardButton(f"Force Join: {fsub_btn_text}", callback_data=f"toggle_fsub_{chat_id}")],
        [InlineKeyboardButton(f"FSub Channel: {chan_text}", callback_data="alert_setfsub")],
        [InlineKeyboardButton(f"{e.CANCEL} Close Settings", callback_data="close_panel")]
    ])

@Client.on_message(filters.command("settings") & filters.group)
async def group_settings_cmd(client: Client, message: Message):
    chat_id = message.chat.id
    member = await client.get_chat_member(chat_id, message.from_user.id)
    if member.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER] and message.from_user.id != Config.OWNER_ID:
        return await message.reply_text(f"{e.CANCEL} Only admins can open settings!")

    markup = await get_settings_markup(chat_id)
    await message.reply_text(f"{e.SETTING} **Group Settings Panel**\nManage your tagging engine and Force Join here:", reply_markup=markup)

@Client.on_message(filters.command("setfsub") & filters.group)
async def set_fsub_cmd(client: Client, message: Message):
    chat_id = message.chat.id
    member = await client.get_chat_member(chat_id, message.from_user.id)
    if member.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER] and message.from_user.id != Config.OWNER_ID:
        return await message.reply_text(f"{e.CANCEL} Only admins can configure Force Join!")

    if len(message.command) < 2:
        return await message.reply_text(f"{e.SETTING} **Force Join Setup**\n\nExample: `/setfsub @YourChannel`\n*Make sure I am an admin there!*")

    channel_input = message.command[1]
    
    try:
        bot_member = await client.get_chat_member(channel_input, client.me.id)
        if bot_member.status != enums.ChatMemberStatus.ADMINISTRATOR:
            return await message.reply_text(f"{e.CANCEL} I must be an Admin in `{channel_input}`!")
    except Exception as err:
        return await message.reply_text(f"{e.CANCEL} Failed to verify channel. Error: `{err}`")

    await db.set_fsub_channel(chat_id, channel_input)
    await db.update_fsub_status(chat_id, True)
    await message.reply_text(f"{e.TICK} **Force Join Activated for {channel_input}!**")

@Client.on_callback_query(filters.regex(r"^toggle_fsub_") | filters.regex(r"^alert_setfsub") | filters.regex(r"^close_panel"))
async def admin_callbacks(client: Client, query: CallbackQuery):
    data = query.data
    
    if data.startswith("toggle_fsub_"):
        chat_id = int(data.split("_")[2])
        # Verify admin clicking the button
        member = await client.get_chat_member(chat_id, query.from_user.id)
        if member.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER] and query.from_user.id != Config.OWNER_ID:
            return await query.answer("You are not an admin!", show_alert=True)

        fsub_active, fsub_channel = await db.get_fsub_config(chat_id)
        if not fsub_channel:
            return await query.answer("Please set a channel first using /setfsub!", show_alert=True)
        
        # Toggle DB Status
        await db.update_fsub_status(chat_id, not fsub_active)
        markup = await get_settings_markup(chat_id)
        await query.message.edit_reply_markup(reply_markup=markup)
        await query.answer("Force Join status updated!")

    elif data == "alert_setfsub":
        await query.answer("Use the command /setfsub @channel to change this!", show_alert=True)
        
    elif data == "close_panel":
        await query.message.delete()
        
