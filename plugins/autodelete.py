import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.types import Message

logger = logging.getLogger(__name__)

# Background task to delete message after a short delay
async def delete_task(message: Message):
    # 5 second ka delay taaki bot araam se apna reply bhej sake.
    # Agar instantly delete kiya, toh bot ko "Message Not Found" error aa sakta hai.
    await asyncio.sleep(5)
    try:
        await message.delete()
    except Exception:
        # Ignore errors if message is already deleted or bot lacks admin rights
        pass

# Regex pattern jo har tarah ke command signs ko pakdega: /, !, ., ?, $ etc.
COMMAND_PATTERN = r"^[/\!\.\?\$]"

# Watcher that catches ALL commands in Groups and DMs (Group -10 means it checks first)
@Client.on_message(filters.text & filters.regex(COMMAND_PATTERN), group=-10)
async def auto_delete_commands_handler(client: Client, message: Message):
    
    # Background mein delete timer start kar dega
    asyncio.create_task(delete_task(message))
    
    # ⚠️ VERY IMPORTANT: Yeh line message ko aage baaki commands (repeater, tagger) 
    # tak jaane degi. Iske bina tumhara koi command kaam nahi karega.
    message.continue_propagation()
  
