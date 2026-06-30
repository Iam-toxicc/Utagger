import time
import psutil
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database.db import db
from config import Config
from utils.emojis import Emojis as e

START_TIME = time.time()

# Function to generate start buttons
def start_panel_markup(bot_username):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(f"{e.GROUP} Add me to your Group {e.GROUP}", url=f"http://t.me/{bot_username}?startgroup=true")],
        [InlineKeyboardButton(f"{e.STATS} Stats", callback_data="show_stats"), InlineKeyboardButton(f"{e.SETTING} Settings", callback_data="show_settings")],
        [InlineKeyboardButton(f"{e.SHIELD} Support", url="https://t.me/TGVoidAPI_Support")]
    ])

@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client: Client, message: Message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    
    # Auto-save user logic
    is_new = await db.add_user(user_id, first_name)
    
    # Optional: Naya user aaye toh Void logs channel me update
    if is_new and Config.LOG_CHANNEL and Config.LOG_CHANNEL != 0:
        try:
            await client.send_message(Config.LOG_CHANNEL, f"{e.USER} **New User Alert**\n\n**Name:** {first_name}\n**ID:** `{user_id}`")
        except:
            pass

    text = f"""
{e.CROWN} **Welcome to Utagger Premium, {first_name}!** {e.CROWN}

{e.DIAMOND} **I am the most advanced and fastest tagging bot.**
{e.FLASH} **Features:** Fast batching, Auto FloodWait handling, & Custom delays.

{e.SHIELD} Add me to your group and give admin rights to start tagging!
"""
    markup = start_panel_markup(client.me.username)
    
    if Config.START_PIC:
        await message.reply_photo(photo=Config.START_PIC, caption=text, reply_markup=markup)
    else:
        await message.reply_text(text=text, reply_markup=markup)

@Client.on_message(filters.new_chat_members)
async def auto_group_save(client: Client, message: Message):
    for member in message.new_chat_members:
        if member.id == client.me.id:
            await db.add_group(message.chat.id, message.chat.title)
            
            # Optional: Naya group join ho toh logs me bhejna
            if Config.LOG_CHANNEL and Config.LOG_CHANNEL != 0:
                try:
                    await client.send_message(Config.LOG_CHANNEL, f"{e.GROUP} **New Group Added**\n\n**Name:** {message.chat.title}\n**ID:** `{message.chat.id}`")
                except:
                    pass
                    
            await message.reply_text(f"{e.TICK} **Successfully activated in {message.chat.title}!**\nUse /help to see my commands.")
            break

@Client.on_callback_query()
async def callbacks(client: Client, query: CallbackQuery):
    data = query.data

    if data == "back_to_start":
        text = f"{e.CROWN} **Welcome to Utagger Premium, {query.from_user.first_name}!** {e.CROWN}\n\n{e.DIAMOND} **I am the most advanced and fastest tagging bot.**\n{e.FLASH} **Features:** Fast batching, Auto FloodWait handling, & Custom delays.\n\n{e.SHIELD} Add me to your group and give admin rights to start tagging!"
        await query.message.edit_text(text=text, reply_markup=start_panel_markup(client.me.username))

    elif data == "show_stats":
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        uptime = int(time.time() - START_TIME)
        m, s = divmod(uptime, 60)
        h, m = divmod(m, 60)
        
        text = f"📊 **System Statistics**\n\n`CPU      :` `{cpu}%`\n`RAM      :` `{ram}%`\n`Uptime   :` `{h}h {m}m {s}s`\n`DB Ping  :` `Connected {e.TICK}`\n\n━━━━━━━━━━━━━━━━━━━━\n*Developed by Toxic* {e.CROWN}"
        markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Main Menu", callback_data="back_to_start")]])
        await query.message.edit_text(text=text, reply_markup=markup)

    elif data == "show_settings":
        text = f"{e.SETTING} **Advanced Group Settings**\nCustomize your tagging engine here.\n\n{e.FLASH} **Force Join:** Users must join your channel to use the bot.\n{e.TICK} **Batch Size:** Number of tags per message.\n{e.STATS} **Tag Delay:** Time gap between tag messages."
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"Force Join: ❌ OFF", callback_data="dummy_alert")],
            [InlineKeyboardButton("Set FSub Channel", callback_data="dummy_alert")],
            [InlineKeyboardButton("➖", callback_data="dummy_alert"), InlineKeyboardButton("Batch: 5", callback_data="dummy_alert"), InlineKeyboardButton("➕", callback_data="dummy_alert")],
            [InlineKeyboardButton("➖", callback_data="dummy_alert"), InlineKeyboardButton("Delay: 2s", callback_data="dummy_alert"), InlineKeyboardButton("➕", callback_data="dummy_alert")],
            [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="back_to_start")]
        ])
        await query.message.edit_text(text=text, reply_markup=markup)
        
    elif data == "dummy_alert":
        await query.answer("This admin setting will be linked to database soon!", show_alert=True)
                    
