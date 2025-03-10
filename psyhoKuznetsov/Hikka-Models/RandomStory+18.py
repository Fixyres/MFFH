__version__ = (1, 0, 0)
# meta developer: @psyho_Kuznetsov

import random
from telethon.tl.types import Message
from telethon.errors import ChannelInvalidError, ChannelPrivateError
from .. import loader, utils

@loader.tds
class RandomStory(loader.Module):
    """истории 18+ 🔞"""
    strings = {"name": "RandomStory"}

    def __init__(self):
        self.channels = ["papkastoris", "sexpornotales", "poshlie_skazki", "palata_nom69"]

    @loader.command()
    async def история(self, message: Message):
        """Получить рандом историю 🔞"""
        status_msg = await utils.answer(message, "<b>Ищу историю...</b>")
        

        channel = random.choice(self.channels)
        
        try:
            total_messages = (await self.client.get_messages(channel, limit=1)).total
            
            if total_messages == 0:
                await utils.answer(status_msg, "<b>В канале нет сообщений</b>")
                return
            
            offset_id = random.randint(0, total_messages - 1)
            
            msg = await self.client.get_messages(channel, limit=1, offset_id=offset_id)
            
            if not msg or not msg[0].message or msg[0].media:
                await utils.answer(status_msg, "<b>Не удалось найти подходящую историю</b>")
                return
            
            text = self._clean_text(msg[0].message)
            
            parts = self._split_text(text, 4000)
            
            await utils.answer(status_msg, f"<pre>{parts[0]}</pre>")
            
            for part in parts[1:]:
                await message.respond(f"<pre>{part}</pre>")
        
        except (ChannelInvalidError, ChannelPrivateError):
            await utils.answer(status_msg, "<b>Канал недоступен</b>")

    def _clean_text(self, text):
        phrases = ["SexPornoTales🔸Webcam's 18+", "🔞", "👇", "подписывайтесь"]
        for phrase in phrases:
            text = text.replace(phrase, "")
        return text.strip()
    
    def _split_text(self, text, max_length):
        if len(text) <= max_length:
            return [text]
            
        parts = []
        current = ""
        
        paragraphs = text.split("\n\n")
        for p in paragraphs:
            if len(current) + len(p) + 2 <= max_length:
                current += ("\n\n" + p if current else p)
            else:
                if current:
                    parts.append(current)
                    current = p
                else:
                    sentences = p.replace(". ", ".\n").replace("! ", "!\n").replace("? ", "?\n").split("\n")
                    for s in sentences:
                        if len(current) + len(s) + 1 <= max_length:
                            current += (" " + s if current else s)
                        else:
                            if current:
                                parts.append(current)
                                current = s
                            else:
                                words = s.split()
                                for word in words:
                                    if len(current) + len(word) + 1 <= max_length:
                                        current += (" " + word if current else word)
                                    else:
                                        parts.append(current)
                                        current = word
        
        if current:
            parts.append(current)
            
        return parts
