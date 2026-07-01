import time
import psutil
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database.db import db
from config import Config
from utils.emojis import Emojis as e

START_TIME = time.time()

def start_panel_markup(bot_username):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(f"{e.GROUP} Add to Group {e.GROUP}", url=f"http://t.me/{bot_username}?startgroup=true")],
        [InlineKeyboardButton(f"{e.SHIELD} Help & Commands", callback_data="show_help"), 
         InlineKeyboardButton(f"⚙️ Advanced Features", callback_data="show_features")],
        [InlineKeyboardButton(f"{e.STATS} Stats", callback_data="show_stats"), 
         InlineKeyboardButton(f"{e.LINK} Support", url="https://t.me/TGVoidAPI_Support")]
    ])

@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client: Client, message: Message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    await db.add_user(user_id, first_name)
    
    text = f"""
{e.CROWN} **Welcome to TGVoid Engine, {first_name}!** {e.CROWN}

I am a high-performance bot built for **Telegram Dominance**. 
My ecosystem handles everything from bulk tagging to automated security.

{e.DIAMOND} **Total Users:** `{await db.users.count_documents({})}`
{e.GROUP} **Total Groups:** `{await db.groups.count_documents({})}`
"""
    markup = start_panel_markup(client.me.username)
    if Config.START_PIC:
        await message.reply_photo(photo=Config.START_PIC, caption=text, reply_markup=markup)
    else:
        await message.reply_text(text=text, reply_markup=markup)

# --- CALLBACK HANDLERS ---
@Client.on_callback_query()
async def callbacks(client: Client, query: CallbackQuery):
    data = query.data
    
    if data == "back_to_start":
        text = f"{e.CROWN} **Welcome to TGVoid Engine, {query.from_user.first_name}!** {e.CROWN}\n\n{e.DIAMOND} **Total Users:** `{await db.users.count_documents({})}`\n{e.GROUP} **Total Groups:** `{await db.groups.count_documents({})}`"
        await query.message.edit_text(text, reply_markup=start_panel_markup(client.me.username))

    elif data == "show_features":
        text = f"""
⚙️ **Advanced TGVoid Features** ⚙️

> 🛡️ **Strict FSub (Force Join):**
> Automatically deletes messages of non-subscribed users and alerts them with a 30s auto-delete warning.

> 🔄 **Auto-Repeater:**
> Schedule messages/albums at custom intervals. Never let your shop/service go offline.

> ⚡ **Tagging Engine:**
> Professional batch tagging with custom formatting and FloodWait protection.

> 👑 **Ecosystem Sync:**
> Centralized branding with `@ToxicTGUpdates` and `@TGVoidAPI_Support`.
"""
        markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back_to_start")]])
        await query.message.edit_text(text=text, reply_markup=markup)

    elif data == "show_help":
        text = f"""
{e.FLASH} **Command Center** {e.FLASH}

> **Admin Commands:**
> `/tagall` - Tag everyone
> `/setfsub @channel` - Activate Security
> `/settings` - Group Configuration
> `/repeat[2,5,60]min` - Start Auto-Repost
> `/cancel` - Stop current task
"""
        markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back_to_start")]])
        await query.message.edit_text(text=text, reply_markup=markup)

    elif data == "show_stats":
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        uptime = int(time.time() - START_TIME)
        h, m = divmod(uptime, 3600)
        m, s = divmod(m, 60)
        
        users_count = await db.users.count_documents({})
        groups_count = await db.groups.count_documents({})
        
        text = (
            f"📊 **System Status**\n\n"
            f"👥 `Total Users   :` `{users_count}`\n"
            f"🏢 `Total Groups  :` `{groups_count}`\n\n"
            f"💻 `CPU           :` `{cpu}%`\n"
            f"💾 `RAM           :` `{ram}%`\n"
            f"⏱️ `Uptime        :` `{h}h {m}m {s}s`\n\n"
            f"*Powered by Toxic Ecosystem*"
        )
        await query.message.edit_text(text=text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back_to_start")]]))

@Client.on_message(filters.new_chat_members)
async def auto_group_save(client: Client, message: Message):
    for member in message.new_chat_members:
        if member.id == client.me.id:
            await db.add_group(message.chat.id, message.chat.title)
            await message.reply_text(f"{e.TICK} **Successfully Synced with TGVoid Ecosystem.**")
            
