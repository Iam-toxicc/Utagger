from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import Config

@Client.on_callback_query()
async def help_callbacks(client: Client, query: CallbackQuery):
    
    if query.data == "help_main":
        text = (
            f"> 💮 **ᴅɪᴠᴇ ɪɴᴛᴏ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅ ᴄᴀᴛᴇɢᴏʀɪᴇs ʙᴇʟᴏᴡ**\n\n"
            f"• **ɢᴇᴛ ɢᴜɪᴅᴀɴᴄᴇ & sᴜᴘᴘᴏʀᴛ ᴀssɪsᴛᴀɴᴄᴇ**\n"
            f"• **ᴜsᴇ ᴄᴏᴍᴍᴀɴᴅs ᴡɪᴛʜ ᴛʜɪs sʏɴᴛᴀx ➜ /**"
        )
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("𝐓𝐀𝐆𝐆𝐄𝐑", "help_tag"), InlineKeyboardButton("𝐑𝐄𝐏𝐄𝐀𝐓𝐄𝐑", "help_repeat"), InlineKeyboardButton("𝐒𝐄𝐂𝐔𝐑𝐈𝐓𝐘", "help_fsub")],
            [InlineKeyboardButton("𝐀𝐃𝐌𝐈𝐍", "help_admin"), InlineKeyboardButton("𝐎𝐖𝐍𝐄𝐑", "help_owner"), InlineKeyboardButton("𝐁𝐀𝐂𝐊", "back_to_start")]
        ])
        await query.message.edit_text(text, reply_markup=markup)

    # ADMIN CATEGORY (Updated with your design)
    elif query.data == "help_admin":
        text = (
            f"⊚ **ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅs :**\n\n"
            f"➻ `/settings` : ᴀᴅᴊᴜsᴛ ᴄᴏɴғɪɢᴜʀᴀᴛɪᴏɴ ᴏᴘᴛɪᴏɴs.\n"
            f"➻ `/ping` : ᴍᴇᴀsᴜʀᴇ sʏsᴛᴇᴍ ʟᴀᴛᴇɴᴄʏ ᴀɴᴅ ᴘɪɴɢ.\n"
            f"➻ `/reload` : ʀᴇғʀᴇsʜ ᴀᴅᴍɪɴ ᴅᴀᴛᴀ ᴄᴀᴄʜᴇ.\n"
            f"➻ `/reboot` : ʀᴇsᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ sᴇʀᴠɪᴄᴇ.\n"
            f"➻ `/stats` : ᴠɪᴇᴡ ᴄᴏᴍᴘʀᴇʜᴇɴsɪᴠᴇ ʙᴏᴛ ᴍᴇᴛʀɪᴄs.\n"
            f"➻ `/help` : ᴀᴄᴄᴇss ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ ɢᴜɪᴅᴇʟɪɴᴇs."
        )
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("BACK", "help_main")]]))

    # TAGGER CATEGORY
    elif query.data == "help_tag":
        text = (
            f"⊚ **ᴛᴀɢɢɪɴɢ ᴄᴏᴍᴍᴀɴᴅs :**\n\n"
            f"➻ `/utag` : ᴛᴀɢ ᴀʟʟ ᴍᴇᴍʙᴇʀs ɪɴ ɢʀᴏᴜᴘ.\n"
            f"➻ `/atag` : ᴀᴅᴠᴀɴᴄᴇᴅ ᴄᴜsᴛᴏᴍ ᴛᴀɢɢɪɴɢ.\n"
            f"➻ `/cancel` : sᴛᴏᴘ ᴀɴʏ ᴀᴄᴛɪᴠᴇ ᴘʀᴏᴄᴇss.\n"
            f"➻ `/setformat` : sᴇᴛ ᴛᴀɢ sᴛʏʟᴇ ғᴏʀᴍᴀᴛ."
        )
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("BACK", "help_main")]]))

    # Baki categories waisi hi rahengi...
    elif query.data == "help_owner":
        text = (
            f"⊚ **ᴏᴡɴᴇʀ ᴏɴʟʏ :**\n\n"
            f"➻ `/broadcast` : sᴇɴᴅ ᴍsɢ ᴛᴏ ᴀʟʟ ᴜsᴇʀs.\n"
            f"➻ `/stats` : ᴠɪᴇᴡ sʏsᴛᴇᴍ ᴍᴇᴛʀɪᴄs.\n"
            f"➻ `/globalfsub` : ᴀᴘᴘʟʏ ɢʟᴏʙᴀʟ sᴇᴄᴜʀɪᴛʏ."
        )
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("BACK", "help_main")]]))
        
