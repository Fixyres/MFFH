# meta developer: @shkipermolodec 

from .. import loader, utils

from contextlib import suppress
from telethon.tl.types import Message, MessageMediaPhoto


@loader.tds
class VatnikMod(loader.Module):
    strings = {
        "name": "🇷🇺 Патриот"
    }
    
    translate_map = {
        ord("з"): "Z",
        ord("З"): "Z",
        ord("z"): "Z",
        ord("о"): "O",
        ord("o"): "О",
        ord("в"): "V",
        ord("В"): "V",
        ord("v"): "V"
    }
    
    async def client_ready(self, client, db):
        self.db = db
        self._client = client

        self.enabled = self.db.get("patriot", "enabled", False)
    
    async def patriotcmd(self, message: Message):
        """Включить или отключить патриота"""
        
        self.enabled = not self.enabled
        self.db.set("patriot", "enabled", self.enabled)
        
        if self.enabled:
            return await utils.answer(
                message=message,
                response="<b>🇷🇺 Патриот успешно включен. Страна может спать спокойно</b>"
            )
        
        else:
            return await utils.answer(
                message=message,
                response="❌ <b>Патриот выключен</b>"
            )
    
    async def patcmd(self, message: Message):
        """pat сообщение. <reply>"""
        
        reply = await message.get_reply_message()
        
        translated_text = reply.text.translate(self.translate_map)

        await utils.answer(
            message=message,
            response=f"🇷🇺 <b>Патриот отредактировал сообщение</b>:\n\n{translated_text}"
        )

    
    async def watcher(self, message: Message):
        if self.enabled:
            if message.out:
                translated_text = message.text.translate(self.translate_map)
                
                if message.text != translated_text:
                    await self._client.edit_message(message.peer_id, message.id, translated_text)
