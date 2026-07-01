import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# Temporary storage for group settings
HIDER_SETTINGS = {}

# ==========================================
# 🎛️ HIDER TOGGLE COMMAND (/hider)
# ==========================================
@Client.on_message(filters.command("hider") & filters.group)
async def hider_command(client: Client, message: Message):
    # Admin Check
    try:
        user = await client.get_chat_member(message.chat.id, message.from_user.id)
        if user.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
            return
    except:
        return

    chat_id = message.chat.id
    
    # 🟢 NAYA UPDATE: Default state is now True (ON) for all groups!
    current_state = HIDER_SETTINGS.get(chat_id, True) 
    status_text = "🟢 **ON**" if current_state else "🔴 **OFF**"

    text = (
        "**⚙️ ᴊᴏɪɴ/ʟᴇғᴛ ᴍᴇssᴀɢᴇ ʜɪᴅᴇʀ**\n\n"
        f"**ᴄᴜʀʀᴇɴᴛ sᴛᴀᴛᴜs:** {status_text}\n\n"
        "> *Turn ON to automatically delete 'User joined' and 'User left' service messages.*"
    )
    
    # Inline Buttons
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ ᴛᴜʀɴ ᴏɴ", callback_data="hider_on"),
            InlineKeyboardButton("❌ ᴛᴜʀɴ ᴏғғ", callback_data="hider_off")
        ],
        [InlineKeyboardButton("🗑 ᴄʟᴏsᴇ", callback_data="hider_close")]
    ])
    
    await message.reply_text(text, reply_markup=buttons)


# ==========================================
# 🔘 BUTTON CALLBACKS HANDLER
# ==========================================
@Client.on_callback_query(filters.regex(r"^hider_"))
async def hider_button_handler(client: Client, callback_query: CallbackQuery):
    # Security Check
    try:
        user = await client.get_chat_member(callback_query.message.chat.id, callback_query.from_user.id)
        if user.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
            return await callback_query.answer("⚠️ Only Admins can use this!", show_alert=True)
    except:
        return

    chat_id = callback_query.message.chat.id
    data = callback_query.data

    if data == "hider_on":
        HIDER_SETTINGS[chat_id] = True
        await callback_query.message.edit_text("✅ **ᴊᴏɪɴ/ʟᴇғᴛ ʜɪᴅᴇʀ ɪs ɴᴏᴡ ᴏɴ.**\n> *Service messages will be auto-deleted.*")
    
    elif data == "hider_off":
        HIDER_SETTINGS[chat_id] = False
        await callback_query.message.edit_text("❌ **ᴊᴏɪɴ/ʟᴇғᴛ ʜɪᴅᴇʀ ɪs ɴᴏᴡ ᴏғғ.**\n> *Service messages will be visible.*")
    
    elif data == "hider_close":
        await callback_query.message.delete()


# ==========================================
# 🧹 ACTUAL AUTO-DELETE LOGIC (Group 2)
# ==========================================
@Client.on_message(filters.new_chat_members | filters.left_chat_member, group=2)
async def delete_service_messages(client: Client, message: Message):
    chat_id = message.chat.id
    
    # Check karega, agar OFF nahi kiya gaya hai toh by default saaf karega
    if HIDER_SETTINGS.get(chat_id, True):
        try:
            # 0.5 sec ka chota sa delay taaki bot ko admin powers lene ka time mil jaye
            await asyncio.sleep(0.5)
            await message.delete()
        except Exception:
            # Agar group me normal member jaisa add kiya (bina admin rights ke), 
            # toh error chup chap ignore kar dega
            pass
  
