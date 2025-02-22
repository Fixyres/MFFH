# ------------------------------------------------------------
# Module: RandomMemes
# Description: RandomMemes module with a 2 mode. 
# Author: @kmodules
# ------------------------------------------------------------
# Licensed under the GNU AGPLv3
# https:/www.gnu.org/licenses/agpl-3.0.html
# ------------------------------------------------------------
# Author: @MeKsenon
# Commands: .rmeme .rnmeme
# scope: hikka_only
# meta banner: https://i.ibb.co/hK4zxP7/6f8d18ef-53d2-42a5-94e5-c0abef97b1bb.jpg
# meta developer: @kmodules
# ------------------------------------------------------------

from .. import loader, utils
import random

__version__ = (1, 0, 1)

@loader.tds
class RandomMemesModule(loader.Module):
    """2 mode random memes."""
    
    strings = {
        "name": "RandomMemes",
        "process": "<emoji document_id=5307675706283533118>🫥</emoji> <b>Forwarding random meme...</b>",
        "result": "<emoji document_id=5317003825494629922>😁</emoji> <b>Your random meme!</b>",
        "error": "<emoji document_id=5240241223632954241>🚫</emoji> <b>Error occured while getting random meme. How?</b>"
    }
    
    strings_ru = {
        "name": "RandomMemes",
        "process": "<emoji document_id=5307675706283533118>🫥</emoji> <b>Пересылаю случайный мем...</b>",
        "result": "<emoji document_id=5317003825494629922>😁</emoji> <b>Ваш случайный мем!</b>",
        "error": "<emoji document_id=5240241223632954241>🚫</emoji> <b>Произошла ошибка при получении случайного мема. Как?</b>"
    }

    async def client_ready(self, client, db):
        self.client = client

    async def _get_random_meme(self, channel):
        chat = await self.client.get_entity(channel)
        messages = await self.client.get_messages(chat, limit=300)
        media_messages = [msg for msg in messages if msg.media]
        
        if not media_messages:
            return None
            
        return random.choice(media_messages)

    @loader.command(ru_doc="NSFW мемы", en_doc="NSFW memes")
    async def rnmeme(self, message):
        await utils.answer(message, self.strings["process"])
        
        random_msg = await self._get_random_meme("po_memes")
        
        if not random_msg:
            return await utils.answer(message, self.strings["error"])
        
        await message.respond(file=random_msg.media, message=self.strings["result"])
        await message.delete()

    @loader.command(ru_doc="Безопасные мемы", en_doc="Safe memes") 
    async def rmeme(self, message):
        await utils.answer(message, self.strings["process"])
        
        random_msg = await self._get_random_meme("prikoly_i_memy")
        
        if not random_msg:
            return await utils.answer(message, self.strings["error"])
        
        await message.respond(file=random_msg.media, message=self.strings["result"])
        await message.delete()
