from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

# Saari commands jo sirf groups ke liye hain unki list (Updated with recent commands)
GROUP_ONLY_COMMANDS = [
    "settings", "reload", "utag", "atag", "cancel", 
    "repeat", "jobs", "stop", 
    "fsub", "setfsub", "check", "biolink", "auth"
]

@Client.on_message(filters.command(GROUP_ONLY_COMMANDS) & filters.private)
async def group_commands_in_dm_warning(client: Client, message: Message):
    # Hint hata kar sirf error message rakha hai
    text = (
        f"> ⚠️ **ᴀᴄᴛɪᴏɴ ᴅᴇɴɪᴇᴅ :**\n>\n"
        f"> ➻ **ᴍsɢ :** ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴄᴀɴ ᴏɴʟʏ ʙᴇ ᴜsᴇᴅ ɪɴ ɢʀᴏᴜᴘs."
    )
    
    # "Add me to your group" ka dynamic button
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎧 ᴧᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ 🎧", url=f"https://t.me/{client.me.username}?startgroup=true")]
    ])
    
    await message.reply_text(text, reply_markup=markup)
    
