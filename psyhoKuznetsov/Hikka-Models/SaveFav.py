__version__ = (1, 0, 0)
# meta developer: @psyho_Kuznetsov

from .. import loader, utils
from telethon import types

@loader.tds
class SimpleFavMod(loader.Module):
    """Сохраняет сообщения, видео, файлы и т.д в избранное"""    
    strings = {"name": "SaveFav"}

    @loader.command()
    async def fav(self, message):
        """Сохраняет в избранное. Использование: .fav"""
        if not message.is_reply:
            return await message.edit("<b>❌ Ответьте на сообщение.</b>", parse_mode="html")            
        reply = await message.get_reply_message()

        await self._client.forward_messages("me", reply)
        await message.edit("<b>✅ Успешно отправлено в избранное.</b>", parse_mode="html")
