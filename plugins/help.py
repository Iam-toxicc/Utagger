from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import Config
from database.db import db

@Client.on_callback_query()
async def help_callbacks(client: Client, query: CallbackQuery):
    if query.data == "help_main":
        text = (
            f"> **DIVE INTO ALL COMMAND CATEGORIES BELOW**\n\n"
            f"• **GET GUIDANCE & SUPPORT ASSISTANCE**\n"
            f"• **USE COMMANDS WITH THIS SYNTAX ➻ /**"
        )
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("𝐀𝐃𝐌𝐈𝐍", "help_admin"), InlineKeyboardButton("𝐀𝐔𝐓𝐇", "help_auth"), InlineKeyboardButton("𝐁-𝐂𝐀𝐒𝐓", "help_bcast")],
            [InlineKeyboardButton("𝐏𝐋𝐀𝐘", "help_play"), InlineKeyboardButton("𝐒𝐔𝐃𝐎", "help_sudo"), InlineKeyboardButton("𝐑𝐄𝐒𝐓𝐑𝐈𝐂𝐓", "help_restrict")],
            [InlineKeyboardButton("𝐓𝐇𝐔𝐌𝐁𝐍𝐀𝐈𝐋", "help_thumb"), InlineKeyboardButton("𝐒𝐓𝐀𝐑𝐓", "help_start"), InlineKeyboardButton("𝐀𝐔𝐓𝐎𝐏𝐋𝐀𝐘", "help_auto")],
            [InlineKeyboardButton("𝐁𝐀𝐂𝐊", "back_to_start")]
        ])
        await query.message.edit_text(text, reply_markup=markup)

    # Example: Basic Commands Page
    elif query.data == "help_start":
        text = (
            f"⊚ **BASIC COMMANDS :**\n\n"
            f"➻ `/start` : INITIALIZE THE SERVICE.\n"
            f"➻ `/help` : ACCESS THE COMMAND GUIDELINES.\n"
            f"➻ `/stats` : VIEW COMPREHENSIVE BOT METRICS."
        )
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("BACK", "help_main")]]))

    elif query.data == "back_to_start":
        # Yahan wahi Start message wala logic call karo ya redirect karo
        await query.answer("Returning...", show_alert=True)
        
