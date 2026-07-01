from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import Config

@Client.on_callback_query()
async def help_callbacks(client: Client, query: CallbackQuery):
    
    # 1. MAIN GRID MENU
    if query.data == "help_main":
        text = (
            f"> **DIVE INTO ALL COMMAND CATEGORIES BELOW**\n\n"
            f"• **GET GUIDANCE & SUPPORT ASSISTANCE**\n"
            f"• **USE COMMANDS WITH THIS SYNTAX ➻ /**"
        )
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("𝐓𝐀𝐆𝐆𝐄𝐑", "help_tag"), InlineKeyboardButton("𝐑𝐄𝐏𝐄𝐀𝐓𝐄𝐑", "help_repeat"), InlineKeyboardButton("𝐒𝐄𝐂𝐔𝐑𝐈𝐓𝐘", "help_fsub")],
            [InlineKeyboardButton("𝐀𝐃𝐌𝐈𝐍", "help_admin"), InlineKeyboardButton("𝐎𝐖𝐍𝐄𝐑", "help_owner"), InlineKeyboardButton("𝐁𝐀𝐂𝐊", "back_to_start")]
        ])
        await query.message.edit_text(text, reply_markup=markup)

    # 2. TAGGER CATEGORY
    elif query.data == "help_tag":
        text = (
            f"⊚ **TAGGING COMMANDS :**\n\n"
            f"➻ `/utag` : TAG ALL MEMBERS IN GROUP.\n"
            f"➻ `/atag` : ADVANCED CUSTOM TAGGING.\n"
            f"➻ `/cancel` : STOP ANY ACTIVE PROCESS.\n"
            f"➻ `/setformat` : SET TAG STYLE FORMAT."
        )
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("BACK", "help_main")]]))

    # 3. REPEATER CATEGORY
    elif query.data == "help_repeat":
        text = (
            f"⊚ **REPEATER COMMANDS :**\n\n"
            f"➻ `/repeat2min` : SET 2 MIN REPEATER.\n"
            f"➻ `/repeat5min` : SET 5 MIN REPEATER.\n"
            f"➻ `/repeat60min` : SET 1 HOUR REPEATER.\n"
            f"➻ `/jobs` : VIEW ALL ACTIVE TASKS.\n"
            f"➻ `/stop` : STOP ALL REPEATERS."
        )
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("BACK", "help_main")]]))

    # 4. SECURITY (FSUB) CATEGORY
    elif query.data == "help_fsub":
        text = (
            f"⊚ **SECURITY COMMANDS :**\n\n"
            f"➻ `/fsub on/off` : TOGGLE FORCE JOIN.\n"
            f"➻ `/setfsub @channel` : SET F-SUB LINK.\n"
            f"➻ `/check` : CHECK USER STATUS."
        )
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("BACK", "help_main")]]))

    # 5. ADMIN/OWNER CATEGORY
    elif query.data == "help_admin":
        text = (
            f"⊚ **ADMIN COMMANDS :**\n\n"
            f"➻ `/settings` : GROUP CONFIGURATION.\n"
            f"➻ `/ping` : CHECK BOT LATENCY."
        )
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("BACK", "help_main")]]))
        
    elif query.data == "help_owner":
        text = (
            f"⊚ **OWNER ONLY :**\n\n"
            f"➻ `/broadcast` : SEND MSG TO ALL.\n"
            f"➻ `/stats` : VIEW SYSTEM METRICS.\n"
            f"➻ `/globalfsub` : APPLY GLOBAL SECURITY."
        )
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("BACK", "help_main")]]))
        
