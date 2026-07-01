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
            [InlineKeyboardButton("sᴇᴄᴜʀɪᴛʏ", "help_fsub"), InlineKeyboardButton("ʙɪᴏʟɪɴᴋ", "help_biolink")],
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
            f"> ➻ `/fsub {{on/off}}` : ᴛᴏɢɢʟᴇ ғᴏʀᴄᴇ ᴊᴏɪɴ.\n"
            f"> ➻ `/setfsub {{id}}` : sᴇᴛ ғ-sᴜʙ ʟɪɴᴋ.\n"
            f"> ➻ `/approve` : ᴡʜɪᴛᴇʟɪsᴛ ᴀ ᴜsᴇʀ.\n"
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
            f"> ➻ `/broadcast {{msg}}` : ʙʀᴏᴀᴅᴄᴧsᴛ ᴍsɢ.\n"
            f"> ➻ `/stats` : ɢʟᴏʙᴧʟ ᴍᴇᴛʀɪᴄs.\n\n"
            f"**ᴄʜᴀᴛ sᴄᴏᴘᴇ :** ᴘʀɪᴠᴧᴛᴇ."
        )
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ʙᴧᴄᴋ", "help_main")]]))

    # 7. BIOLINK (REPLACED THUMBNAIL)
    elif query.data == "help_biolink":
        text = (
            f"> ⊚ **ʙɪᴏʟɪɴᴋ sᴇᴛᴛɪɴɢs :**\n>\n"
            f"> ➻ `/biolink {{on/off}}` : ᴇɴᴀʙʟᴇ/ᴅɪsᴀʙʟᴇ ғᴇᴀᴛᴜʀᴇ.\n>\n"
            f"> ⊚ **ᴡʜᴧᴛ ɪs ʙɪᴏʟɪɴᴋ?**\n>\n"
            f"> 💮 **ᴀᴜᴛᴏᴍᴧᴛɪᴄᴧʟʟʏ ᴅᴇʟᴇᴛᴇs ᴍsɢs ɪғ ᴜsᴇʀ ʜᴀs ʟɪɴᴋ ɪɴ ʙɪᴏ.**\n\n"
            f"**ᴄʜᴀᴛ sᴄᴏᴘᴇ :** ɢʀᴏᴜᴘ ᴏɴʟʏ."
        )
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ʙᴧᴄᴋ", "help_main")]]))

    # 8. BACK TO START LOGIC
    elif query.data == "back_to_start":
        text = "> 💮 **ᴡᴇʟᴄᴏᴍᴇ ʙᴀᴄᴋ!**\n> ʏᴏᴜ ᴀʀᴇ ᴀᴛ ᴛʜᴇ ᴍᴀɪɴ ᴍᴇɴᴜ."
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("🎧 ᴧᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ᴄʜᴧᴛ 🎧", url=f"https://t.me/{client.me.username}?startgroup=true")],
            [InlineKeyboardButton("ʜᴇʟᴘ ᴧɴᴅ ᴄᴏᴍᴍᴧɴᴅs", callback_data="help_main")]
        ])
        await query.message.edit_text(text, reply_markup=markup)
        
