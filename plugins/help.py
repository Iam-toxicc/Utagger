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
            f"> ➻ `/cancel` : sᴛᴏᴘ ᴀɴʏ ᴀᴄᴛɪᴠᴇ ᴘʀᴏᴄᴇss.\n>\n"
            f"> ⊚ **ᴡʜᴧᴛ ɪs ᴛᴧɢɢᴇʀ?**\n>\n"
            f"> 💮 **ᴛᴏ ᴍᴇɴᴛɪᴏɴ ᴏʀ ᴛᴀɢ ɢʀᴏᴜᴘ ᴍᴇᴍʙᴇʀs ғᴏʀ ɪɴsᴛᴀɴᴛ ᴀʟᴇʀᴛs.**\n\n"
            f"**ᴄʜᴀᴛ sᴄᴏᴘᴇ :** ɢʀᴏᴜᴘ ᴏɴʟʏ."
        )
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ʙᴧᴄᴋ", "help_main")]]))

    # 3. REPEATER
    elif query.data == "help_repeat":
        text = (
            f"> ⊚ **ʀᴇᴘᴇᴧᴛᴇʀ ᴄᴏᴍᴍᴧɴᴅs :**\n>\n"
            f"> ➻ `/repeat {{time}}` : ᴄᴜsᴛᴏᴍ ʀᴇᴘᴇᴀᴛ (1m ᴛᴏ 24h).\n"
            f"> ➻ `/jobs` : ᴠɪᴇᴡ ᴀʟʟ ᴀᴄᴛɪᴠᴇ ᴛᴀsᴋs.\n"
            f"> ➻ `/stop` : sᴛᴏᴘ ᴀʟʟ ʀᴇᴘᴇᴀᴛᴇʀs.\n>\n"
            f"> ⊚ **ᴡʜᴧᴛ ɪs ʀᴇᴘᴇᴧᴛᴇʀ?**\n>\n"
            f"> 💮 **ᴛᴏ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ʀᴇᴘᴇᴀᴛ ɪᴍᴘᴏʀᴛᴀɴᴛ ᴍᴇssᴀɢᴇs ɪɴ ᴀ ᴛɪᴍᴇ ʟᴏᴏᴘ.**\n\n"
            f"**ᴄʜᴀᴛ sᴄᴏᴘᴇ :** ɢʀᴏᴜᴘ ᴏɴʟʏ."
        )
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ʙᴧᴄᴋ", "help_main")]]))

    # 4. SECURITY (Updated /auth)
    elif query.data == "help_fsub":
        text = (
            f"> ⊚ **sᴇᴄᴜʀɪᴛʏ ᴄᴏᴍᴍᴧɴᴅs :**\n>\n"
            f"> ➻ `/fsub {{on/off}}` : ᴛᴏɢɢʟᴇ ғᴏʀᴄᴇ ᴊᴏɪɴ.\n"
            f"> ➻ `/setfsub {{id}}` : sᴇᴛ ғ-sᴜʙ ʟɪɴᴋ.\n"
            f"> ➻ `/auth` : ᴍᴀsᴛᴇʀ ʙʏᴘᴀss ғᴏʀ ᴜsᴇʀs.\n"
            f"> ➻ `/check` : ᴄʜᴇᴄᴋ ᴜsᴇʀ sᴛᴀᴛᴜs.\n>\n"
            f"> ⊚ **ᴡʜᴧᴛ ɪs sᴇᴄᴜʀɪᴛʏ / ғsᴜʙ?**\n>\n"
            f"> 💮 **ᴛᴏ ғᴏʀᴄᴇ ᴜsᴇʀs ᴛᴏ ᴊᴏɪɴ ᴀ sᴘᴇᴄɪғɪᴄ ᴄʜᴀɴɴᴇʟ ʙᴇғᴏʀᴇ sᴇɴᴅɪɴɢ ᴍᴇssᴀɢᴇs.**\n\n"
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
            f"> ➻ `/stats` : ʙᴏᴛ ᴍᴇᴛʀɪᴄs.\n>\n"
            f"> ⊚ **ᴡʜᴧᴛ ɪs ᴧᴅᴍɪɴ ᴘᴧɴᴇʟ?**\n>\n"
            f"> 💮 **ᴛᴏ ᴄᴏɴᴛʀᴏʟ ɢʀᴏᴜᴘ ɪɴᴛᴇʀɴᴀʟ sᴇᴛᴛɪɴɢs, ᴄᴀᴄʜᴇ, ᴀɴᴅ ʙᴏᴛ ᴘᴇʀғᴏʀᴍᴀɴᴄᴇ.**\n\n"
            f"**ᴄʜᴀᴛ sᴄᴏᴘᴇ :** ɢʀᴏᴜᴘ ᴏɴʟʏ."
        )
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ʙᴧᴄᴋ", "help_main")]]))

    # 6. OWNER
    elif query.data == "help_owner":
        text = (
            f"> ⊚ **ᴏᴡɴᴇʀ ᴏɴʟʏ :**\n>\n"
            f"> ➻ `/broadcast {{msg}}` : ʙʀᴏᴀᴅᴄᴧsᴛ ᴍsɢ.\n"
            f"> ➻ `/stats` : ɢʟᴏʙᴧʟ ᴍᴇᴛʀɪᴄs.\n>\n"
            f"> ⊚ **ᴡʜᴧᴛ ɪs ᴏᴡɴᴇʀ ᴘᴧɴᴇʟ?**\n>\n"
            f"> 💮 **ғᴏʀ ᴛʜᴇ ʙᴏᴛ ᴄʀᴇᴀᴛᴏʀ ᴛᴏ ᴠɪᴇᴡ ɢʟᴏʙᴀʟ ᴅᴀᴛᴀ ᴀɴᴅ ʙʀᴏᴀᴅᴄᴀsᴛ ᴍᴇssᴀɢᴇs ᴛᴏ ᴀʟʟ ɢʀᴏᴜᴘs.**\n\n"
            f"**ᴄʜᴀᴛ sᴄᴏᴘᴇ :** ᴘʀɪᴠᴧᴛᴇ."
        )
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ʙᴧᴄᴋ", "help_main")]]))

    # 7. BIOLINK & AUTH (Updated with explanation)
    elif query.data == "help_biolink":
        text = (
            f"> ⊚ **ʙɪᴏʟɪɴᴋ & ᴀᴜᴛʜ sᴇᴛᴛɪɴɢs :**\n>\n"
            f"> ➻ `/biolink {{on/off}}` : ᴇɴᴀʙʟᴇ/ᴅɪsᴀʙʟᴇ ғᴇᴀᴛᴜʀᴇ.\n"
            f"> ➻ `/auth` : ʀᴇᴘʟʏ ᴛᴏ ᴜsᴇʀ ᴛᴏ ᴡʜɪᴛᴇʟɪsᴛ ᴛʜᴇᴍ.\n>\n"
            f"> ⊚ **ᴡʜᴧᴛ ɪs ʙɪᴏʟɪɴᴋ & ᴀᴜᴛʜ?**\n>\n"
            f"> 💮 **ʙɪᴏʟɪɴᴋ ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇs ᴍsɢs ɪғ ᴀ ᴜsᴇʀ ʜᴀs ᴀ ʟɪɴᴋ ɪɴ ᴛʜᴇɪʀ ʙɪᴏ.**\n"
            f"> 💮 **ᴀᴜᴛʜ ɪs ᴀ ᴍᴀsᴛᴇʀ ᴘᴀss: ɪᴛ ɪɢɴᴏʀᴇs ʙᴏᴛʜ ғ-sᴜʙ & ʙɪᴏʟɪɴᴋ ғᴏʀ ᴛʜᴀᴛ ᴜsᴇʀ.**\n\n"
            f"**ᴄʜᴀᴛ sᴄᴏᴘᴇ :** ɢʀᴏᴜᴘ ᴏɴʟʏ."
        )
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ʙᴧᴄᴋ", "help_main")]]))

    # 8. BACK TO START LOGIC
    elif query.data == "back_to_start":
        text = "> 💮 **ᴡᴇʟᴄᴏᴍᴇ ʙᴀᴄᴋ!**\n> ʏᴏᴜ ᴀʀᴇ ᴀᴛ ᴛʜᴇ ᴍᴀɪɴ ᴍᴇɴᴜ."
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("⚡ ᴧᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ᴄʜᴧᴛ ⚡", url=f"https://t.me/{client.me.username}?startgroup=true")],
            [InlineKeyboardButton("ʜᴇʟᴘ ᴧɴᴅ ᴄᴏᴍᴍᴧɴᴅs ☎️", callback_data="help_main")]
        ])
        await query.message.edit_text(text, reply_markup=markup)
        
