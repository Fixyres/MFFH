#------------------------------------------------------------------
#      ___           ___       ___                       ___     
#     /\  \         /\__\     /\  \          ___        /\__\    
#    /::\  \       /:/  /    /::\  \        /\  \      /:/  /    
#   /:/\ \  \     /:/  /    /:/\:\  \       \:\  \    /:/__/     
#  _\:\~\ \  \   /:/  /    /::\~\:\  \      /::\__\  /::\__\____ 
# /\ \:\ \ \__\ /:/__/    /:/\:\ \:\__\  __/:/\/__/ /:/\:::::\__\
# \:\ \:\ \/__/ \:\  \    \/__\:\/:/  / /\/:/  /    \/_|:|~~|~   
#  \:\ \:\__\    \:\  \        \::/  /  \::/__/        |:|  |    
#   \:\/:/  /     \:\  \       /:/  /    \:\__\        |:|  |    
#    \::/  /       \:\__\     /:/  /      \/__/        |:|  |    
#     \/__/         \/__/     \/__/                     \|__|   
#------------------------------------------------------------------ 
# meta developer: @Hicota
# requires: pet-pet-gif

import os
from .. import loader, utils
from io import BytesIO
from petpetgif import petpet

@loader.tds
class PetPetMod(loader.Module):
    """Сделай фото в гифку, которое гладит изображение"""
    
    strings = {"name": "PetPet"}

    @loader.command()
    async def pet(self, message):
        """- Реплай на фото | Отправить команду с фото"""
        if message.is_reply:
            response = await message.get_reply_message()
            await message.delete()
            if response.from_id == self.tg_id:
                await response.delete()
        else:
            if hasattr(message, 'media') and hasattr(message.media, 'photo'):
                response = message.media
                await message.delete()
        try:
            media = await self._client.download_media(response.photo, "pet")
            petgif = BytesIO()
            petpet.make(media, petgif)
            petgif.name = "pet.gif"
            petgif.seek(0)
        except AttributeError :
            await utils.answer(message, '<emoji document_id=5465665476971471368>❌</emoji><b>Вы ответили не на фото</b><emoji document_id=5465665476971471368>❌</emoji>\nОтветьте на фото чтобы команда .pet заработала')
            return
        await self._client.send_file(message.to_id, file=petgif, force_document=False, reply_to=((await message.get_reply_message()).id if message.chat.forum else None) if not message.is_private else None)
        os.remove(media)