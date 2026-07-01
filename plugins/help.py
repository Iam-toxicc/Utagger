from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

@Client.on_callback_query(filters.regex(r"^(help_|back_to_start)"))
async def help_callbacks(client: Client, query: CallbackQuery):
    
    # 1. MAIN MENU
    if query.data == "help_main":
        text = (f"> 💮 **ᴄᴏᴍᴍᴀɴᴅ ᴄᴀᴛᴇɢᴏʀɪᴇs**\n\n"
                f"> ᴇxᴘʟᴏʀᴇ ᴏᴜʀ ғᴇᴀᴛᴜʀᴇs ʙᴇʟᴏᴡ.")
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("ᴛᴧɢɢᴇʀ", "help_tag"), InlineKeyboardButton("ʀᴇᴘᴇᴧᴛᴇʀ", "help_repeat")],
            [InlineKeyboardButton("sᴇᴄᴜʀɪᴛʏ", "help_fsub"), InlineKeyboardButton("ᴧᴅᴍɪɴ", "help_admin")],
            [InlineKeyboardButton("ᴏᴡɴᴇʀ", "help_owner"), InlineKeyboardButton("ʙᴧᴄᴋ", "back_to_start")]
        ])
        await query.message.edit_text(text, reply_markup=markup)

    # 2. TAGGER
    elif query.data == "help_tag":
        text = (f"> ⊚ **ᴛᴧɢɢɪɴɢ ᴄᴏᴍᴍᴧɴᴅs :**\n\n"
                f"> ➻ `/utag` : ᴀʟʟ ᴍᴇᴍʙᴇʀ ᴛᴀɢ.\n"
                f"> ➻ `/atag` : ᴀᴅᴠᴀɴᴄᴇᴅ ᴄᴜsᴛᴏᴍ ᴛᴀɢ.\n"
                f"> ➻ `/cancel` : sᴛᴏᴘ ᴘʀᴏᴄᴇss.\n\n"
                f"**ᴄʜᴀᴛ sᴄᴏᴘᴇ :** ɢʀᴏᴜᴘ ᴏɴʟʏ.")
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ʙᴧᴄᴋ", "help_main")]]))

    # 3. REPEATER
    elif query.data == "help_repeat":
        text = (f"> ⊚ **ʀᴇᴘᴇᴧᴛᴇʀ ᴄᴏᴍᴍᴧɴᴅs :**\n\n"
                f"> ➻ `/repeat2min` : sᴇᴛ 2 ᴍɪɴ ʀᴇᴘᴇᴀᴛ.\n"
                f"> ➻ `/repeat5min` : sᴇᴛ 5 ᴍɪɴ ʀᴇᴘᴇᴀᴛ.\n"
                f"> ➻ `/jobs` : ᴠɪᴇᴡ ᴀᴄᴛɪᴠᴇ ᴛᴀsᴋs.\n"
                f"> ➻ `/stop` : sᴛᴏᴘ ʀᴇᴘᴇᴀᴛᴇʀs.\n\n"
                f"**ᴄʜᴀᴛ sᴄᴏᴘᴇ :** ɢʀᴏᴜᴘ ᴏɴʟʏ.")
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ʙᴧᴄᴋ", "help_main")]]))

    # 4. SECURITY (Fixed Error)
    elif query.data == "help_fsub":
        text = (f"> ⊚ **sᴇᴄᴜʀɪᴛʏ ᴄᴏᴍᴍᴧɴᴅs :**\n\n"
                f"> ➻ `/fsub \{on/off\}` : ᴛᴏɢɢʟᴇ ᴍᴏᴅᴇ.\n"
                f"> ➻ `/setfsub \{username/id\}` : sᴇᴛ ᴄʜᴀɴɴᴇʟ.\n"
                f"> ➻ `/check` : ᴄʜᴇᴄᴋ ᴜsᴇʀ sᴛᴀᴛᴜs.\n\n"
                f"> 💡 **ʜᴏᴡ ᴛᴏ ᴜsᴇ :**\n"
                f"> ᴘʜʟᴇ ᴄʜᴀɴɴᴇʟ sᴇᴛ ᴋᴀʀᴏ ᴜsᴋᴇ ʙᴀᴀᴅ /fsub on ʟɪᴋʜᴏ.\n\n"
                f"**ᴄʜᴀᴛ sᴄᴏᴘᴇ :** ɢʀᴏᴜᴘ ᴏɴʟʏ.")
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ʙᴧᴄᴋ", "help_main")]]))

    # 5. ADMIN
    elif query.data == "help_admin":
        text = (f"> ⊚ **ᴧᴅᴍɪɴ ᴄᴏᴍᴍᴧɴᴅs :**\n\n"
                f"> ➻ `/settings` : ᴏᴘᴇɴ ᴘᴀɴᴇʟ.\n"
                f"> ➻ `/ping` : ᴄʜᴇᴄᴋ sᴘᴇᴇᴅ.\n"
                f"> ➻ `/reload` : ᴀᴅᴍɪɴ ʀᴇғʀᴇsʜ.\n"
                f"> ➻ `/reboot` : ʀᴇsᴛᴀʀᴛ ʙᴏᴛ.\n\n"
                f"**ᴄʜᴀᴛ sᴄᴏᴘᴇ :** ɢʀᴏᴜᴘ ᴏɴʟʏ.")
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ʙᴧᴄᴋ", "help_main")]]))

    # 6. OWNER (Fixed Error)
    elif query.data == "help_owner":
        text = (f"> ⊚ **ᴏᴡɴᴇʀ ᴄᴏᴍᴍᴧɴᴅs :**\n\n"
                f"> ➻ `/broadcast \{message\}` : sᴇɴᴅ ᴀʟʟ.\n"
                f"> ➻ `/stats` : ɢʟᴏʙᴀʟ ᴅᴀᴛᴀ.\n\n"
                f"**ᴄʜᴀᴛ sᴄᴏᴘᴇ :** ᴘʀɪᴠᴀᴛᴇ.")
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ʙᴧᴄᴋ", "help_main")]]))
        
