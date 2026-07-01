from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import Config

@Client.on_callback_query()
async def help_callbacks(client: Client, query: CallbackQuery):
    
    # 1. MAIN GRID MENU
    if query.data == "help_main":
        text = (
            f"> 💮 **ᴅɪᴠᴇ ɪɴᴛᴏ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅ ᴄᴀᴛᴇɢᴏʀɪᴇs ʙᴇʟᴏᴡ**\n\n"
            f"• **ɢᴇᴛ ɢᴜɪᴅᴀɴᴄᴇ & sᴜᴘᴘᴏʀᴛ ᴀssɪsᴛᴀɴᴄᴇ**\n"
            f"• **ᴜsᴇ ᴄᴏᴍᴍᴀɴᴅs ᴡɪᴛʜ ᴛʜɪs sʏɴᴛᴀx ➜ /**"
        )
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("ᴛᴧɢɢᴇʀ", callback_data="help_tag"), 
             InlineKeyboardButton("ʀᴇᴘᴇᴧᴛᴇʀ", callback_data="help_repeat"), 
             InlineKeyboardButton("sᴇᴄᴜʀɪᴛʏ", callback_data="help_fsub")],
            [InlineKeyboardButton("ᴧᴅᴍɪɴ", callback_data="help_admin"), 
             InlineKeyboardButton("ᴏᴡɴᴇʀ", callback_data="help_owner"), 
             InlineKeyboardButton("ʙᴧᴄᴋ", callback_data="back_to_start")]
        ])
        await query.message.edit_text(text, reply_markup=markup)

    # 2. TAGGER CATEGORY
    elif query.data == "help_tag":
        text = (
            f"⊚ **ᴛᴀɢɢɪɴɢ ᴄᴏᴍᴍᴀɴᴅs :**\n\n"
            f"➻ `/utag` : ᴛᴀɢ ᴀʟʟ ᴍᴇᴍʙᴇʀs ɪɴ ɢʀᴏᴜᴘ.\n"
            f"➻ `/atag` : ᴀᴅᴠᴀɴᴄᴇᴅ ᴄᴜsᴛᴏᴍ ᴛᴀɢɢɪɴɢ.\n"
            f"➻ `/cancel` : sᴛᴏᴘ ᴀɴʏ ᴀᴄᴛɪᴠᴇ ᴘʀᴏᴄᴇss.\n"
            f"➻ `/setformat` : sᴇᴛ ᴛᴀɢ sᴛʏʟᴇ ғᴏʀᴍᴀᴛ."
        )
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ʙᴧᴄᴋ", callback_data="help_main")]]))

    # 3. REPEATER CATEGORY
    elif query.data == "help_repeat":
        text = (
            f"⊚ **ʀᴇᴘᴇᴀᴛᴇʀ ᴄᴏᴍᴍᴀɴᴅs :**\n\n"
            f"➻ `/repeat2min` : sᴇᴛ 2 ᴍɪɴ ʀᴇᴘᴇᴀᴛᴇʀ.\n"
            f"➻ `/repeat5min` : sᴇᴛ 5 ᴍɪɴ ʀᴇᴘᴇᴀᴛᴇʀ.\n"
            f"➻ `/repeat60min` : sᴇᴛ 1 ʜᴏᴜʀ ʀᴇᴘᴇᴀᴛᴇʀ.\n"
            f"➻ `/jobs` : ᴠɪᴇᴡ ᴀʟʟ ᴀᴄᴛɪᴠᴇ ᴛᴀsᴋs.\n"
            f"➻ `/stop` : sᴛᴏᴘ ᴀʟʟ ʀᴇᴘᴇᴀᴛᴇʀs."
        )
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ʙᴧᴄᴋ", callback_data="help_main")]]))

    # 4. SECURITY (FSUB) CATEGORY
    elif query.data == "help_fsub":
        text = (
            f"⊚ **sᴇᴄᴜʀɪᴛʏ ᴄᴏᴍᴍᴀɴᴅs :**\n\n"
            f"➻ `/fsub on/off` : ᴛᴏɢɢʟᴇ ғᴏʀᴄᴇ ᴊᴏɪɴ.\n"
            f"➻ `/setfsub` : sᴇᴛ ғ-sᴜʙ ʟɪɴᴋ ᴡɪᴛʜ ᴄʜᴀɴɴᴇʟ.\n"
            f"➻ `/check` : ᴄʜᴇᴄᴋ ᴜsᴇʀ sᴛᴀᴛᴜs."
        )
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ʙᴧᴄᴋ", callback_data="help_main")]]))

    # 5. ADMIN CATEGORY
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
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ʙᴧᴄᴋ", callback_data="help_main")]]))

    # 6. OWNER CATEGORY
    elif query.data == "help_owner":
        text = (
            f"⊚ **ᴏᴡɴᴇʀ ᴏɴʟʏ :**\n\n"
            f"➻ `/broadcast` : sᴇɴᴅ ᴍsɢ ᴛᴏ ᴀʟʟ ᴜsᴇʀs.\n"
            f"➻ `/stats` : ᴠɪᴇᴡ sʏsᴛᴇᴍ ᴍᴇᴛʀɪᴄs.\n"
            f"➻ `/globalfsub` : ᴀᴘᴘʟʏ ɢʟᴏʙᴀʟ sᴇᴄᴜʀɪᴛʏ."
        )
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ʙᴧᴄᴋ", callback_data="help_main")]]))
        
