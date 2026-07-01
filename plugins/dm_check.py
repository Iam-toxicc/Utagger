from pyrogram import Client, filters
from pyrogram.types import Message

# Saari commands jo sirf groups ke liye hain unki list
GROUP_ONLY_COMMANDS = [
    "settings", "reload", "utag", "atag", "cancel", 
    "repeat2min", "repeat5min", "jobs", "stop", 
    "fsub", "setfsub", "check", "biolink", "approve"
]

@Client.on_message(filters.command(GROUP_ONLY_COMMANDS) & filters.private)
async def group_commands_in_dm_warning(client: Client, message: Message):
    text = (
        f"> ⚠️ **ᴀᴄᴛɪᴏɴ ᴅᴇɴɪᴇᴅ :**\n>\n"
        f"> ➻ **ᴍsɢ :** ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴄᴀɴ ᴏɴʟʏ ʙᴇ ᴜsᴇᴅ ɪɴ ɢʀᴏᴜᴘs.\n"
        f"> ➻ **ʜɪɴᴛ :** ᴧᴅᴅ ᴍᴇ ᴛᴏ ᴧ ɢʀᴏᴜᴘ ᴛᴏ ᴜsᴇ ᴛʜɪs ғᴇᴀᴛᴜʀᴇ."
    )
    await message.reply_text(text)
  
