from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import Config

@Client.on_callback_query(filters.regex(r"^(help_|back_to_start)"))
async def help_callbacks(client: Client, query: CallbackQuery):
    
    # 1. MAIN MENU
    if query.data == "help_main":
        text = (
            f"> 💮 **ᴅɪᴠᴇ ɪɴᴛᴏ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅ ᴄᴀᴛᴇɢᴏʀɪᴇs ʙᴇʟᴏᴡ**\n>\n"
            f"> • **ɢᴇᴛ ɢᴜɪᴅᴀɴᴄᴇ & sᴜᴘᴘᴏʀᴛ ᴀssɪsᴛᴀɴᴄᴇ**\n"
            f"> • **ᴜsᴇ ᴄᴏᴍᴍᴀɴᴅs ᴡɪᴛʜ ᴛʜɪs sʏɴᴛᴀx ➜ /**"
        )
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("ᴛᴧɢɢᴇʀ", "help_tag"), InlineKeyboardButton("ʀᴇᴘᴇᴧᴛᴇʀ", "help_repeat")],
            [InlineKeyboardButton("sᴇᴄᴜʀɪᴛʏ", "help_fsub"), InlineKeyboardButton("ᴛʜᴜᴍʙɴᴧɪʟ", "help_thumb")],
            [InlineKeyboardButton("ᴧᴅᴍɪɴ", "help_admin"), InlineKeyboardButton("ᴏᴡɴᴇʀ", "help_owner")],
            [InlineKeyboardButton("ʙᴧᴄᴋ", "back_to_start")]
        ])
        await query.message.edit_text(text, reply_markup=markup)

    # 2. TAGGER
    elif query.data == "help_tag":
        text = (
            f"> ⊚ **ᴛᴧɢɢɪɴɢ ᴄᴏᴍᴍᴧɴᴅs :**\n>\n"
            f"> ➻ `/utag` : ᴛᴀɢ ᴀʟʟ ᴍᴇᴍʙᴇʀs ɪɴ ɢʀᴏᴜᴘ.\n"
            f"> ➻ `/atag` : ᴀᴅᴠᴀɴᴄᴇᴅ ᴄᴜsᴛᴏᴍ ᴛᴀɢɢɪɴɢ.\n"
            f"> ➻ `/cancel` : sᴛᴏᴘ ᴀɴʏ ᴀᴄᴛɪᴠᴇ ᴘʀᴏᴄᴇss.\n\n"
            f"**ᴄʜᴀᴛ sᴄᴏᴘᴇ :** ɢʀᴏᴜᴘ ᴏɴʟʏ."
        )
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ʙᴧᴄᴋ", "help_main")]]))

    # 3. REPEATER
    elif query.data == "help_repeat":
        text = (
            f"> ⊚ **ʀᴇᴘᴇᴧᴛᴇʀ ᴄᴏᴍᴍᴧɴᴅs :**\n>\n"
            f"> ➻ `/repeat2min` : sᴇᴛ 2 ᴍɪɴ ʀᴇᴘᴇᴀᴛᴇʀ.\n"
            f"> ➻ `/repeat5min` : sᴇᴛ 5 ᴍɪɴ ʀᴇᴘᴇᴀᴛᴇʀ.\n"
            f"> ➻ `/jobs` : ᴠɪᴇᴡ ᴀʟʟ ᴀᴄᴛɪᴠᴇ ᴛᴀsᴋs.\n"
            f"> ➻ `/stop` : sᴛᴏᴘ ᴀʟʟ ʀᴇᴘᴇᴀᴛᴇʀs.\n\n"
            f"**ᴄʜᴀᴛ sᴄᴏᴘᴇ :** ɢʀᴏᴜᴘ ᴏɴʟʏ."
        )
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ʙᴧᴄᴋ", "help_main")]]))

    # 4. SECURITY
    elif query.data == "help_fsub":
        text = (
            f"> ⊚ **sᴇᴄᴜʀɪᴛʏ ᴄᴏᴍᴍᴧɴᴅs :**\n>\n"
            f"> ➻ `/fsub` : ᴛᴏɢɢʟᴇ ғᴏʀᴄᴇ ᴊᴏɪɴ.\n"
            f"> ➻ `/setfsub` : sᴇᴛ ғ-sᴜʙ ʟɪɴᴋ.\n"
            f"> ➻ `/check` : ᴄʜᴇᴄᴋ ᴜsᴇʀ sᴛᴀᴛᴜs.\n\n"
            f"**ᴄʜᴀᴛ sᴄᴏᴘᴇ :** ɢʀᴏᴜᴘ ᴏɴʟʏ."
        )
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ʙᴧᴄᴋ", "help_main")]]))

    # 5. ADMIN
    elif query.data == "help_admin":
        text = (
            f"> ⊚ **ᴧᴅᴍɪɴ ᴄᴏᴍᴍᴧɴᴅs :**\n>\n"
            f"> ➻ `/settings` : ɢʀᴏᴜᴘ ᴄᴏɴғɪɢᴜʀᴀᴛɪᴏɴ.\n"
            f"> ➻ `/ping` : sʏsᴛᴇᴍ ʟᴀᴛᴇɴᴄʏ.\n"
            f"> ➻ `/reload` : ʀᴇғʀᴇsʜ ᴅᴀᴛᴀ ᴄᴀᴄʜᴇ.\n"
            f"> ➻ `/reboot` : ʀᴇsᴛᴀʀᴛ sᴇʀᴠɪᴄᴇ.\n"
            f"> ➻ `/stats` : ʙᴏᴛ ᴍᴇᴛʀɪᴄs.\n\n"
            f"**ᴄʜᴀᴛ sᴄᴏᴘᴇ :** ɢʀᴏᴜᴘ ᴏɴʟʏ."
        )
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ʙᴧᴄᴋ", "help_main")]]))

    # 6. OWNER
    elif query.data == "help_owner":
        text = (
            f"> ⊚ **ᴏᴡɴᴇʀ ᴏɴʟʏ :**\n>\n"
            f"> ➻ `/broadcast` : ʙʀᴏᴀᴅᴄᴧsᴛ ᴍsɢ.\n"
            f"> ➻ `/stats` : ɢʟᴏʙᴧʟ ᴍᴇᴛʀɪᴄs.\n\n"
            f"**ᴄʜᴀᴛ sᴄᴏᴘᴇ :** ᴘʀɪᴠᴧᴛᴇ."
        )
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ʙᴧᴄᴋ", "help_main")]]))

    # 7. THUMBNAIL (As requested)
    elif query.data == "help_thumb":
        text = (
            f"> ⊚ **ᴛʜᴜᴍʙɴᴧɪʟ sᴇᴛᴛɪɴɢs :**\n>\n"
            f"> ➻ `/thumb` : ᴍᴀɴᴀɢᴇ ᴠɪsᴜᴀʟ sᴇᴛᴛɪɴɢs.\n>\n"
            f"> ⊚ **ᴡʜᴧᴛ ɪs ᴛʜᴜᴍʙɴᴧɪʟ?**\n>\n"
            f"> 💮 **ᴛᴏɢɢʟᴇ ᴀʀᴛ ᴅɪsᴘʟᴀʏ ᴛᴏ ʀᴇᴅᴜᴄᴇ ᴅᴀᴛᴀ ʟᴏᴀᴅ.**\n\n"
            f"**ᴄʜᴀᴛ sᴄᴏᴘᴇ :** ɢʀᴏᴜᴘ ᴏɴʟʏ."
        )
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ʙᴧᴄᴋ", "help_main")]]))
        
