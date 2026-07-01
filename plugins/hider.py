from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

HIDER_SETTINGS = {}

# Regex filter use kar rahe hain kyunki ye kabhi fail nahi hota
@Client.on_message(filters.regex(r"^/hider$") & filters.group)
async def hider_command(client, message):
    chat_id = message.chat.id
    current_state = HIDER_SETTINGS.get(chat_id, True)
    status = "🟢 ON" if current_state else "🔴 OFF"
    
    text = f"⚙️ **Join/Left Hider System**\n\nStatus: {status}"
    
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ ON", callback_data="hider_on"),
            InlineKeyboardButton("❌ OFF", callback_data="hider_off")
        ]
    ])
    await message.reply_text(text, reply_markup=buttons)

# Callback handle karne ke liye
@Client.on_callback_query(filters.regex(r"^hider_"))
async def callback_handler(client, query):
    chat_id = query.message.chat.id
    if query.data == "hider_on":
        HIDER_SETTINGS[chat_id] = True
        await query.answer("Hider Enabled!")
    elif query.data == "hider_off":
        HIDER_SETTINGS[chat_id] = False
        await query.answer("Hider Disabled!")
        
