from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

# List of commands that are strictly for groups
GROUP_ONLY_COMMANDS = [
    "settings", 
    "reload", 
    "utag", 
    "atag", 
    "cancel", 
    "repeat", 
    "jobs", 
    "stop", 
    "fsub", 
    "setfsub", 
    "check", 
    "biolink", 
    "auth", 
    "unauth"
]

@Client.on_message(filters.command(GROUP_ONLY_COMMANDS) & filters.private)
async def group_commands_in_dm_warning(client: Client, message: Message):
    # Premium warning message structure
    text = (
        f"> ⚠️ **ᴀᴄᴛɪᴏɴ ᴅᴇɴɪᴇᴅ :**\n>\n"
        f"> ➻ **ᴍsɢ :** ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴄᴀɴ ᴏɴʟʏ ʙᴇ ᴜsᴇᴅ ɪɴ ɢʀᴏᴜᴘs."
    )
    
    # Inline button to add the bot to a group
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎧 ᴧᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ 🎧", url=f"https://t.me/{client.me.username}?startgroup=true")]
    ])
    
    # Sending the response
    await message.reply_text(text, reply_markup=markup)
    
