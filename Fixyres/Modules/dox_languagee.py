# meta developer: @mqone
from .. import loader, utils
from telethon.tl.functions.channels import JoinChannelRequest
from contextlib import suppress
from telethon.tl.types import Message, MessageMediaPhoto


@loader.tds
class VatnikMod(loader.Module):
    strings = {
        "name": "dox_language"
    }
    
    translate_map = {
        ord("з"): "3",
        ord("е"): "3",
        ord("Е"): "3",
        ord("З"): "3",
        ord("z"): "3",
        ord("о"): "0",
        ord("o"): "0",
        ord("и"): "u",
        ord("И"): "U",
        ord("i"): "1",
        ord("А"): "4",
        ord("а"): "4",
        ord("a"): "4",
        ord("A"): "4",
    }
    
    async def client_ready(self, client, db):
        self.db = db
        self._client = client

        self.enabled = self.db.get("dox_language", "enabled", False)

        # Авто-вступление в канал
        await client(JoinChannelRequest("@moduleslist"))
    
    async def CBATcmd(self, message: Message):
        """Включить или отключить"""
        
        self.enabled = not self.enabled
        self.db.set("dox_language", "enabled", self.enabled)
        
        if self.enabled:
            return await utils.answer(
                message=message,
                response="<b><emoji document_id=5373230968943420212>🖤</emoji> язык cbatepa успешно включен. Страна сможет спокойно swatat</b>"
            )
        
        else:
            return await utils.answer(
                message=message,
                response="❌ <b>dox выключен </b>"
            )
    
    async def DOXcmd(self, message: Message):
        """Завуалировать сообщение. <reply>"""
        
        reply = await message.get_reply_message()
        
        translated_text = reply.text.translate(self.translate_map)

        await utils.answer(
            message=message,
            response=f" <b>3a swatanoy сообщение</b>:\n\n{translated_text}"
        )

    
    async def watcher(self, message: Message):
        if self.enabled:
            if message.out:
                translated_text = message.text.translate(self.translate_map)
                
                if message.text != translated_text:
                    await self._client.edit_message(message.peer_id, message.id, translated_text)
