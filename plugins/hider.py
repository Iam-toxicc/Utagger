from pyrogram import Client, filters, enums
from pyrogram.types import Message
from pyrogram.raw.types import MessageActionChatJoinedByLink, MessageActionChatAddUser, MessageActionChatJoinedByRequest

# Settings global storage
HIDER_SETTINGS = {}

@Client.on_raw_update(group=2)
async def raw_hider_handler(client, update, users, chats):
    if hasattr(update, 'message') and update.message:
        msg = update.message
        
        # Check if it's a service message
        if hasattr(msg, 'action') and msg.action:
            chat_id = msg.chat.id
            
            # --- FILTER LOGIC ---
            # Hum sirf inko delete karenge: Join, Add, Request
            # VC Invites ko yahan include nahi kiya hai, isliye wo delete nahi honge
            from pyrogram.raw.types import (
                MessageActionChatJoinedByLink, 
                MessageActionChatAddUser, 
                MessageActionChatJoinedByRequest,
                MessageActionChatDeleteUser
            )
            
            # Yahan define karo kaunse actions delete karne hain
            actions_to_delete = (
                MessageActionChatJoinedByLink,
                MessageActionChatAddUser,
                MessageActionChatJoinedByRequest,
                MessageActionChatDeleteUser
            )
            
            if isinstance(msg.action, actions_to_delete):
                if HIDER_SETTINGS.get(chat_id, True):
                    try:
                        await client.delete_messages(chat_id, msg.id)
                    except:
                        pass
                        
