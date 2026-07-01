from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database.db import db
from config import Config

@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client: Client, message: Message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    await db.add_user(user_id, name)
    
    text = (
        f"**❭ ɢʀᴇᴇᴛɪɴɢs {name}**\n"
        f"❭ … 🌹\n\n"
        f"> **ʏᴏᴜ ᴀʀᴇ ᴜsɪɴɢ ᴀʟʟ-ɪɴ-1 ᴍᴀsᴛᴇʀ ʙᴏᴛ :**\n"
        f"ᴛʜᴇ ᴜʟᴛɪᴍᴀᴛᴇ ᴅᴇsᴛɪɴᴀᴛɪᴏɴ ғᴏʀ ᴛᴇʟᴇɢʀᴀᴍ ᴅᴏᴍɪɴᴀɴᴄᴇ.\n\n"
        f"💮 **ᴅɪᴠᴇ ɪɴᴛᴏ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅ ᴄᴀᴛᴇɢᴏʀɪᴇs ʙᴇʟᴏᴡ**\n\n"
        f"• **ɢᴇᴛ ɢᴜɪᴅᴀɴᴄᴇ & sᴜᴘᴘᴏʀᴛ ᴀssɪsᴛᴀɴᴄᴇ**\n"
        f"• **ᴜsᴇ ᴄᴏᴍᴍᴀɴᴅs ᴡɪᴛʜ ᴛʜɪs sʏɴᴛᴀx ➜ /**"
    )
    
    # Custom 'ᴧ' Font applied to buttons
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎧 ᴧᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ᴄʜᴧᴛ 🎧", url=f"https://t.me/{client.me.username}?startgroup=true")],
        [InlineKeyboardButton("ʜᴇʟᴘ ᴧɴᴅ ᴄᴏᴍᴍᴧɴᴅs", callback_data="help_main")],
        [InlineKeyboardButton("ᴜᴘᴅᴧᴛᴇs ↗", url="https://t.me/ToxicTGUpdates"), 
         InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ ↗", url="https://t.me/ToxicStoreSupport")]
    ])
    
    # Safe Photo Sending Logic to prevent crashes
    if Config.START_PIC and Config.START_PIC.strip() != "":
        try:
            await message.reply_photo(photo=Config.START_PIC, caption=text, reply_markup=buttons)
        except Exception:
            await message.reply_text(text=text, reply_markup=buttons)
    else:
        await message.reply_text(text=text, reply_markup=buttons)
        
