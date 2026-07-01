import time
import psutil
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database.db import db
from config import Config
from utils.emojis import Emojis as e

START_TIME = time.time()

def start_panel_markup(bot_username, is_owner):
    buttons = [
        [InlineKeyboardButton(f"{e.GROUP} Add to Group", url=f"http://t.me/{bot_username}?startgroup=true")],
        [InlineKeyboardButton(f"{e.SHIELD} Help & Commands", callback_data="show_help"), 
         InlineKeyboardButton(f"⚙️ Features", callback_data="show_features")],
        [InlineKeyboardButton(f"{e.STATS} System Stats", callback_data="show_stats"), 
         InlineKeyboardButton(f"{e.LINK} Support", url="https://t.me/TGVoidAPI_Support")]
    ]
    
    # Sirf Owner ko "Owner Panel" button dikhega
    if is_owner:
        buttons.insert(3, [InlineKeyboardButton("👑 Owner Panel", callback_data="owner_panel")])
        
    return InlineKeyboardMarkup(buttons)

@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client: Client, message: Message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    await db.add_user(user_id, first_name)
    
    is_owner = (user_id == Config.OWNER_ID)
    
    text = f"""
{e.CROWN} **Welcome to TGVoid Engine, {first_name}!** {e.CROWN}

I am a high-performance bot built for **Telegram Dominance**. 
My ecosystem handles everything from bulk tagging to automated security.
"""
    markup = start_panel_markup(client.me.username, is_owner)
    
    if Config.START_PIC:
        await message.reply_photo(photo=Config.START_PIC, caption=text, reply_markup=markup)
    else:
        await message.reply_text(text=text, reply_markup=markup)

@Client.on_callback_query()
async def callbacks(client: Client, query: CallbackQuery):
    data = query.data
    is_owner = (query.from_user.id == Config.OWNER_ID)
    
    if data == "back_to_start":
        text = f"{e.CROWN} **Welcome to TGVoid Engine, {query.from_user.first_name}!** {e.CROWN}\n\nI am a high-performance bot built for **Telegram Dominance**."
        await query.message.edit_text(text, reply_markup=start_panel_markup(client.me.username, is_owner))

    elif data == "owner_panel":
        if not is_owner:
            return await query.answer("❌ Access Denied!", show_alert=True)
        text = f"👑 **Owner Control Center**\n\n> Manage your broadcasts and global settings here."
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 Broadcast", callback_data="broadcast_cmd"), InlineKeyboardButton("📊 Global Stats", callback_data="show_stats")],
            [InlineKeyboardButton("🔙 Back", callback_data="back_to_start")]
        ])
        await query.message.edit_text(text, reply_markup=markup)

    elif data == "show_stats":
        cpu, ram = psutil.cpu_percent(), psutil.virtual_memory().percent
        u = await db.users.count_documents({})
        g = await db.groups.count_documents({})
        
        text = f"📊 **System Status**\n\n👥 Users: `{u}` | 🏢 Groups: `{g}`\n💻 CPU: `{cpu}%` | 💾 RAM: `{ram}%`"
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back_to_start")]]))

    # Baki 'show_features' aur 'show_help' waisa hi rahega...
    elif data == "show_features":
        text = "⚙️ **Advanced TGVoid Features**\n\n> 🛡️ Strict FSub\n> 🔄 Auto-Repeater\n> ⚡ Tagging Engine"
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back_to_start")]]))
        
