# meta developer: @mqone

from .. import loader, utils

from contextlib import suppress
from telethon.tl.types import Message, MessageMediaPhoto

@loader.tds
class DemonMod(loader.Module):
    strings = {
        "name": "Demon_lang"
    }
    
    translate_map = {
        ord("А"): "𝐀",
        ord("а"): "𝐚",
        ord("Б"): "𝐛",
        ord("б"): "𝐛",
        ord("В"): "𝐁",
        ord("в"): "𝐁",
        ord("г"): "𝐠",
        ord("Г"): "𝐆",
        ord("д"): "𝐝",
        ord("Д"): "𝐃",
        ord("Е"): "𝐄",
        ord("е"): "𝐞",
        ord("з"): "𝐳",
        ord("З"): "𝐙",
        ord("к"): "𝐤",
        ord("К"): "𝐊",
        ord("м"): "𝐦",
        ord("М"): "𝐌",
        ord("о"): "𝐨",
        ord("О"): "𝐎",
        ord("р"): "𝐩",
        ord("Р"): "𝐏",
        ord("С"): "𝐂",
        ord("с"): "𝐜",
        ord("т"): "𝐭",
        ord("Т"): "𝐓",
        ord("У"): "𝐘",
        ord("у"): "𝐲",
        ord("х"): "𝐱",
        ord("Х"): "𝐗",
        ord("ч"): "4",
        ord("Ч"): "4",
        ord("ь"): "𝐛",
        ord("Ь"): "𝐛",
    }
    
    async def client_ready(self, client, db):
        self.db = db
        self._client = client

        self.enabled = self.db.get("Demon_lang", "enabled", False)
    
    async def шрифтcmd(self, message: Message):
        """- активировать форматирование (ещё раз чтобы выключить)"""
        
        self.enabled = not self.enabled
        self.db.set("Demon", "enabled", self.enabled)
        
        if self.enabled:
            return await utils.answer(
                message=message,
                response="<b><emoji document_id=5373230968943420212>🖤</emoji> 𝐀ʙᴛᴏғᴏᴘᴍᴀᴛɪᴘᴏʙᴀʜɪᴇ ᴀᴋᴛɪʙɪᴘᴏʙᴀʜᴏ</b>"
            )
        
        else:
            return await utils.answer(
                message=message,
                response="❌ <b>ᴀʙᴛᴏғᴏᴘᴍᴀᴛɪᴘᴏʙᴀʜɪᴇ ʙыᴋлючᴇʜᴏ</b>"
            )
    
    async def демонcmd(self, message: Message):
        """<reply> - преобразить сообщение в шрифт"""
        
        reply = await message.get_reply_message()
        
        translated_text = reply.text.translate(self.translate_map)

        await utils.answer(
            message=message,
            response=f"<code>{translated_text}</code>"
        )

    
    async def watcher(self, message: Message):
        if self.enabled:
            if message.out:
                translated_text = message.text.translate(self.translate_map)
                
                if message.text != translated_text:
                    await self._client.edit_message(message.peer_id, message.id, translated_text)