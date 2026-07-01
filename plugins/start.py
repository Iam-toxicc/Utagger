from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database.db import db
from config import Config
from utils.emojis import Emojis as e

@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client: Client, message: Message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    await db.add_user(user_id, name)
    
    text = (
        f"**❭ GREETINGS**\n"
        f"❭ … 🌹\n\n"
        f"> **YOU ARE USING 𝐓𝚶𝚾𝚰𝐂 𝐕𝚶𝚰𝐃 :**\n"
        f"THE ULTIMATE DESTINATION FOR TELEGRAM DOMINANCE.\n\n"
        f"● **BUILD** : v2.0 STABLE.\n"
        f"● **OUTPUT** : HI-RES CONTROL.\n"
        f"● **LATENCY** : ZERO DELAY.\n\n"
        f"🥀 **CLICK HELP TO SEE ALL AVAILABLE COMMANDS.**"
    )
    
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎧 ADD ME TO YOUR CHAT 🎧", url=f"https://t.me/{client.me.username}?startgroup=true")],
        [InlineKeyboardButton("H𝐄𝐋𝐏 𝐀𝐍𝐃 𝐂𝐎𝐌𝐌𝐀𝐍𝐃", callback_data="help_main")],
        [InlineKeyboardButton("UPDATES ↗", url="https://t.me/ToxicTGUpdates"), 
         InlineKeyboardButton("SUPPORT ↗", url="https://t.me/TGVoidAPI_Support")]
    ])
    
    await message.reply_photo(photo=Config.START_PIC, caption=text, reply_markup=buttons)
    
