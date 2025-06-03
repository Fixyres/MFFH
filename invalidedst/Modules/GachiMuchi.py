#  _____                          
# |_   _|____  ____ _ _ __   ___  
#   | |/ _ \ \/ / _` | '_ \ / _ \ 
#   | | (_) >  < (_| | | | | (_) |
#   |_|\___/_/\_\__,_|_| |_|\___/ 
#                              
# meta banner: https://envs.sh/oJH.jpg
# meta developer: @Toxano_Modules

from .. import loader, utils
from telethon import types
import random
import logging

@loader.tds
class RandomPhotoMod(loader.Module):
    """GachiMuchoHentay💙"""
    
    strings = {
        "name": "GachiMuchi",
        "_cls_doc": "send gachimuchi 18+",
        "_cmd_doc_randpic": "send gachimuchi 18+"
    }
    
    strings_ru = {
        "name": "GachiMuchi",
        "_cls_doc": "отправить гачимучи 18+",
        "_cmd_doc_randpic": "отправить гачимучи 18+"
    }
    
    async def client_ready(self, client, db):
        self._db = db
        self._client = client
        if not self.get("seen_photos"):
            self.set("seen_photos", [])

    async def get_channel_photos(self, channel):
        """Gets photos from channel without subscription"""
        try:
            messages = await self._client.get_messages(
                channel,
                limit=100,
                filter=types.InputMessagesFilterPhotos
            )
            return [msg for msg in messages if msg.photo]
        except Exception as e:
            logging.error(f"Error getting photos from {channel}: {e}")
            return []

    @loader.command()
    async def randpic(self, message):
        """Send a random anime photo"""
        channels = ["dvach18", "allconH", "hdjrkdjrkdkd", "Animeplaneta", "Gi_Hent"]
        seen_photos = self.get("seen_photos", [])
        
        # Show loading message
        await utils.answer(message, "<b>Loading photo...</b>")
        
        all_photos = []
        for channel in channels:
            photos = await self.get_channel_photos(channel)
            all_photos.extend(photos)

        if not all_photos:
            await message.delete()
            return

        unseen_photos = [p for p in all_photos if p.photo.id not in seen_photos]
        
        if not unseen_photos:
            seen_photos.clear()
            unseen_photos = all_photos

        chosen_photo = random.choice(unseen_photos)
        
        seen_photos.append(chosen_photo.photo.id)
        if len(seen_photos) > 1000:
            seen_photos = seen_photos[-1000:]
            
        self.set("seen_photos", seen_photos)

        # Send as new message instead of editing
        await message.delete()
        await self._client.send_file(
            message.chat_id,
            file=chosen_photo.photo,
            reply_to=message.reply_to_msg_id if message.is_reply else None
        )
