import time
import os
import sys
import psutil
from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from database.db import db

# ----------------- PING COMMAND -----------------
@Client.on_message(filters.command("ping"))
async def ping_cmd(client: Client, message: Message):
    start_time = time.time()
    m = await message.reply_text("⊚ **ᴘɪɴɢɪɴɢ sʏsᴛᴇᴍ...**")
    end_time = time.time()
    
    ping_time = round((end_time - start_time) * 1000, 3)
    uptime = int(time.time() - psutil.boot_time())
    
    text = (
        f"⊚ **sʏsᴛᴇᴍ ᴘᴏɴɢ :**\n\n"
        f"> ➻ **ʟᴀᴛᴇɴᴄʏ :** `{ping_time}ms`\n"
        f"> ➻ **ᴄᴘᴜ :** `{psutil.cpu_percent()}%`\n"
        f"> ➻ **ʀᴀᴍ :** `{psutil.virtual_memory().percent}%`\n"
    )
    await m.edit_text(text)


# ----------------- REBOOT COMMAND (OWNER ONLY) -----------------
@Client.on_message(filters.command("reboot") & filters.user(Config.OWNER_ID))
async def reboot_cmd(client: Client, message: Message):
    await message.reply_text("⊚ **ʀᴇʙᴏᴏᴛɪɴɢ sʏsᴛᴇᴍ... ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ!**\n> ➻ `The bot will be back online in a few seconds.`")
    os.execl(sys.executable, sys.executable, *sys.argv)


# ----------------- RELOAD COMMAND (ADMINS) -----------------
@Client.on_message(filters.command("reload") & filters.group)
async def reload_cmd(client: Client, message: Message):
    # Yeh check karega ki command dene wala admin hai ya nahi
    user = await client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
        return await message.reply_text("❌ **You must be an admin to use this command!**")

    m = await message.reply_text("⊚ **ʀᴇғʀᴇsʜɪɴɢ ᴀᴅᴍɪɴ ᴅᴀᴛᴀ ᴄᴀᴄʜᴇ...**")
    
    admin_count = 0
    async for admin in client.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
        admin_count += 1
        
    await m.edit_text(
        f"⊚ **ᴄᴀᴄʜᴇ ʀᴇғʀᴇsʜᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!**\n\n"
        f"> ➻ **ᴛᴏᴛᴀʟ ᴀᴅᴍɪɴs ʟᴏᴀᴅᴇᴅ :** `{admin_count}`\n"
        f"> ➻ **sᴛᴀᴛᴜs :** `Ready for secure operations.`"
    )


# ----------------- SETTINGS COMMAND (ADMINS) -----------------
@Client.on_message(filters.command("settings") & filters.group)
async def settings_cmd(client: Client, message: Message):
    user = await client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
        return await message.reply_text("❌ **Only admins can access settings!**")

    text = (
        f"⊚ **ɢʀᴏᴜᴘ ᴄᴏɴғɪɢᴜʀᴀᴛɪᴏɴ ᴘᴀɴᴇʟ :**\n\n"
        f"> ➻ **ᴄʜᴀᴛ ɪᴅ :** `{message.chat.id}`\n"
        f"> ➻ **ᴀᴅᴊᴜsᴛ ʏᴏᴜʀ ᴘʀᴇғᴇʀᴇɴᴄᴇs ʙᴇʟᴏᴡ.**"
    )
    
    # Inline buttons for settings (Dummy toggles for now, can be linked to DB later)
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("ғ-sᴜʙ : ᴏғғ ❌", callback_data="toggle_fsub"), 
         InlineKeyboardButton("ᴀɴᴛɪ-sᴘᴀᴍ : ᴏɴ ✅", callback_data="toggle_antispam")],
        [InlineKeyboardButton("ᴄʟᴏsᴇ ᴘᴀɴᴇʟ 🗑️", callback_data="close_panel")]
    ])
    
    await message.reply_text(text, reply_markup=buttons)

# Callback for settings panel closure
@Client.on_callback_query(filters.regex("close_panel"))
async def close_settings(client: Client, query):
    await query.message.delete()
    
# ----------------- SETTINGS TOGGLE & CLOSE LOGIC -----------------
@Client.on_callback_query(filters.regex(r"^(toggle_|close_panel)"))
async def admin_callbacks(client: Client, query):
    
    # 1. Close Panel Logic
    if query.data == "close_panel":
        return await query.message.delete()

    # 2. Admin Verification for Toggles
    user = await client.get_chat_member(query.message.chat.id, query.from_user.id)
    if user.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
        return await query.answer("❌ You must be an admin to change settings!", show_alert=True)

    data = query.data
    markup = query.message.reply_markup
    
    new_keyboard = []
    action_text = "Updated"

    # 3. Smart Keyboard Reconstruction (100% Working)
    for row in markup.inline_keyboard:
        new_row = []
        for btn in row:
            if btn.callback_data == data:
                # Agar OFF hai toh ON karo
                if "❌" in btn.text:
                    new_text = btn.text.replace("ᴏғғ ❌", "ᴏɴ ✅")
                    action_text = "Enabled ✅"
                # Agar ON hai toh OFF karo
                elif "✅" in btn.text:
                    new_text = btn.text.replace("ᴏɴ ✅", "ᴏғғ ❌")
                    action_text = "Disabled ❌"
                else:
                    new_text = btn.text
                
                # Naya button append karo
                new_row.append(InlineKeyboardButton(new_text, callback_data=btn.callback_data))
            else:
                # Baaki buttons ko waisa hi rehne do
                new_row.append(btn)
        new_keyboard.append(new_row)

    # 4. Update Message and Send Pop-up
    await query.message.edit_reply_markup(InlineKeyboardMarkup(new_keyboard))
    await query.answer(f"Setting {action_text}", show_alert=False)
    
