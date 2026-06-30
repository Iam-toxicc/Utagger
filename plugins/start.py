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
        [InlineKeyboardButton(f"{e.SHIELD} Help & Commands {e.SHIELD}", callback_data="show_help")],
        [InlineKeyboardButton(f"{e.STATS} Stats", callback_data="show_stats"), InlineKeyboardButton(f"{e.SETTING} Settings", callback_data="show_settings")],
        [InlineKeyboardButton(f"{e.LINK} Support", url="https://t.me/TGVoidAPI_Support")]
    ])

@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client: Client, message: Message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    
    is_new = await db.add_user(user_id, first_name)
    
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

    # --- START MENU ---
    if data == "back_to_start":
        text = f"{e.CROWN} **Welcome to Utagger Premium, {query.from_user.first_name}!** {e.CROWN}\n\n{e.DIAMOND} **I am the most advanced and fastest tagging bot.**\n{e.FLASH} **Features:** Fast batching, Auto FloodWait handling, & Custom delays.\n\n{e.SHIELD} Add me to your group and give admin rights to start tagging!"
        await query.message.edit_text(text=text, reply_markup=start_panel_markup(client.me.username))

    # --- HELP CENTER MENU ---
    elif data == "show_help":
        text = f"""
{e.SHIELD} **Utagger Help Center** {e.SHIELD}

> Welcome to the control center. Utagger is the ultimate tagging and marketing engine designed for dominance.
> 
> Choose a category below to explore my capabilities:
"""
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{e.DIAMOND} Bot Features", callback_data="help_features")],
            [InlineKeyboardButton(f"{e.FLASH} All Commands", callback_data="help_commands")],
            [InlineKeyboardButton(f"🔙 Back to Main Menu", callback_data="back_to_start")]
        ])
        await query.message.edit_text(text=text, reply_markup=markup)

    # --- HELP: FEATURES ---
    elif data == "help_features":
        text = f"""
{e.DIAMOND} **Utagger Premium Features** {e.DIAMOND}

> ⚡ **Ultra-Fast Tagging:** Bypass limits with smart batching and FloodWait handling.
> 🔄 **Auto-Repeater:** Schedule messages & albums (2m, 5m, 1h, 24h, etc.).
> 🛡️ **Force Join (FSub):** Force users to join your channel before using the bot.
> 💾 **Auto-Save Database:** MongoDB powered user & group tracking.
> 🎨 **Custom Formatting:** Set your own tag styles with premium emojis.
> 👑 **Owner Control:** Advanced broadcast, stats, and active job tracking.
"""
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"🔙 Back to Help", callback_data="show_help")],
            [InlineKeyboardButton(f"🔙 Back to Main Menu", callback_data="back_to_start")]
        ])
        await query.message.edit_text(text=text, reply_markup=markup)

    # --- HELP: COMMANDS ---
    elif data == "help_commands":
        text = f"""
{e.FLASH} **Utagger Commands List** {e.FLASH}

> **Admin Commands:**
> `/tagall` or `/all` - Tag everyone in the group
> `/cancel` - Stop an active tagging process
> `/setformat` - Customize your tag style
> `/settings` - Open the group settings panel
> `/fsub on/off` - Toggle Force Join
> `/setfsub @channel` - Set FSub channel
> 
> **Repeater Commands (Admins):**
> Reply to a message with:
> `/repeat2min`, `/repeat5min`, `/repeat60min`, etc.
> `/jobs` - Check active repeating tasks
> `/stop` - Stop all repeaters
"""
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"🔙 Back to Help", callback_data="show_help")],
            [InlineKeyboardButton(f"🔙 Back to Main Menu", callback_data="back_to_start")]
        ])
        await query.message.edit_text(text=text, reply_markup=markup)

    # --- STATS PANEL ---
    elif data == "show_stats":
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        uptime = int(time.time() - START_TIME)
        m, s = divmod(uptime, 60)
        h, m = divmod(m, 60)
        
        text = f"📊 **System Statistics**\n\n`CPU      :` `{cpu}%`\n`RAM      :` `{ram}%`\n`Uptime   :` `{h}h {m}m {s}s`\n`DB Ping  :` `Connected {e.TICK}`\n\n━━━━━━━━━━━━━━━━━━━━\n*Developed by Toxic* {e.CROWN}"
        markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Main Menu", callback_data="back_to_start")]])
        await query.message.edit_text(text=text, reply_markup=markup)

    # --- SETTINGS ALERT ---
    elif data == "show_settings":
        await query.answer("Please use the /settings command inside a group to configure your group options!", show_alert=True)
    
