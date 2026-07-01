from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import Config
from database.db import db
from utils.emojis import Emojis as e

@Client.on_message(filters.command("help") & filters.private)
async def help_panel(client: Client, message: Message):
    text = f"{e.SHIELD} **TGVoid Command Center**\n\n> Choose an option to manage your ecosystem."
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("⚡ Commands", callback_data="help_cmds"), 
         InlineKeyboardButton("📖 Help Guide", callback_data="help_guide")],
        [InlineKeyboardButton("📊 System Stats (Owner Only)", callback_data="owner_stats")]
    ])
    await message.reply_text(text, reply_markup=markup)

@Client.on_callback_query()
async def help_callbacks(client: Client, query: CallbackQuery):
    # 1. COMMANDS MENU
    if query.data == "help_cmds":
        text = f"""
{e.FLASH} **All Available Commands** {e.FLASH}

**📢 Tagging Commands:**
`/utag` - Ultimate tag (Everyone)
`/atag` - Advanced tagging (Custom)
`/cancel` - Stop current process

**🛡️ Security:**
`/setfsub @channel` - Force Join
`/fsub on/off` - Toggle security

**🔄 Repeater:**
`/repeat2min` / `/repeat60min` - Set intervals
`/jobs` - Active tasks
`/stop` - Stop all
"""
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back_help")]]))

    # 2. HELP GUIDE
    elif query.data == "help_guide":
        text = f"""
{e.SHIELD} **How to Use?** {e.SHIELD}

1. **/utag:** Simple and fastest way to tag all members.
2. **/atag:** Use this for custom messages like: `/atag Hello guys!`.
3. **/cancel:** Use this if bot gets stuck or tagging isn't needed.
4. **/fsub:** Ensures group quality by forcing users to join your channel first.
"""
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back_help")]]))

    # 3. OWNER STATS (Restricted)
    elif query.data == "owner_stats":
        if query.from_user.id not in [Config.OWNER_ID]: # Yahan tumhare Sudo IDs bhi add kar sakte ho
            await query.answer("❌ Access Denied! Only Owner can view this.", show_alert=True)
            return
        
        u = await db.users.count_documents({})
        g = await db.groups.count_documents({})
        await query.message.edit_text(f"📊 **System Report**\n\nTotal Users: `{u}`\nTotal Groups: `{g}`", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back_help")]]))

    # 4. BACK NAVIGATION
    elif query.data == "back_help":
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("⚡ Commands", callback_data="help_cmds"), 
             InlineKeyboardButton("📖 Help Guide", callback_data="help_guide")],
            [InlineKeyboardButton("📊 System Stats (Owner Only)", callback_data="owner_stats")]
        ])
        await query.message.edit_text("Manage your ecosystem:", reply_markup=markup)
      
