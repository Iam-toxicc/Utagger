from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

HIDER_SETTINGS = {}

# ==========================================
# 🎛️ HIDER TOGGLE COMMAND (/hider)
# ==========================================
@Client.on_message(filters.command("hider") & filters.group)
async def hider_command(client: Client, message: Message):
    try:
        user = await client.get_chat_member(message.chat.id, message.from_user.id)
        if user.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
            return
    except: return

    chat_id = message.chat.id
    current_state = HIDER_SETTINGS.get(chat_id, True) 
    status_text = "🟢 **ON**" if current_state else "🔴 **OFF**"

    text = (
        "**⚙️ ᴊᴏɪɴ/ʟᴇғᴛ ᴍᴇssᴀɢᴇ ʜɪᴅᴇʀ**\n\n"
        f"**ᴄᴜʀʀᴇɴᴛ sᴛᴀᴛᴜs:** {status_text}\n\n"
        "> *All service messages (join/add/left) will be auto-deleted.*"
    )
    
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ ᴛᴜʀɴ ᴏɴ", callback_data="hider_on"), InlineKeyboardButton("❌ ᴛᴜʀɴ ᴏғғ", callback_data="hider_off")],
        [InlineKeyboardButton("🗑 ᴄʟᴏsᴇ", callback_data="hider_close")]
    ])
    await message.reply_text(text, reply_markup=buttons)

@Client.on_callback_query(filters.regex(r"^hider_"))
async def hider_button_handler(client: Client, callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id
    if callback_query.data == "hider_on":
        HIDER_SETTINGS[chat_id] = True
        await callback_query.message.edit_text("✅ **Hider is now ON.**")
    elif callback_query.data == "hider_off":
        HIDER_SETTINGS[chat_id] = False
        await callback_query.message.edit_text("❌ **Hider is now OFF.**")
    elif callback_query.data == "hider_close":
        await callback_query.message.delete()

# ==========================================
# 🧹 BULLETPROOF AUTO-DELETE (Using Raw Handler)
# ==========================================
# Yeh handler har tarah ke system update ko pakdega
@Client.on_raw_update(group=2)
async def raw_hider_handler(client, update, users, chats):
    # Sirf message updates check karega
    if hasattr(update, 'message') and update.message:
        msg = update.message
        
        # Check if it's a service message (join/left/added)
        # Service messages mein 'action' hota hai
        if hasattr(msg, 'action') and msg.action:
            chat_id = msg.chat.id
            if HIDER_SETTINGS.get(chat_id, True):
                try:
                    await client.delete_messages(chat_id, msg.id)
                except:
                    pass
                    
