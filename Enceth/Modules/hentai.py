# meta developer: @Enceth
__version__ = (1, 0, 0)

from .. import loader, utils  
import asyncio  

class Venom(loader.Module):  
    """Ода хентай"""  
    strings = {"name": "EHentai"}  

    async def hentaicmd(self, message):  
        """Рандом"""  
        await self.send_request(message, "Рандом🎲")  

    async def hentaipcmd(self, message):  
        """Картинка"""  
        await self.send_request(message, "Картинки🌄")  

    async def hentaivcmd(self, message):  
        """Видео"""  
        await self.send_request(message, "Видео📺")  

    async def hentaigcmd(self, message):  
        """Гиф"""  
        await self.send_request(message, "Гиф🗂️")  

    async def send_request(self, message, request_text):  
        bot_username = "@Hentairu_bot"  

        async with self._client.conversation(bot_username) as conv:  
            try:  
                await message.edit("<b>🔍 Запрос...</b>")  
                sent_msg = await conv.send_message(request_text)  
                response = await conv.get_response()  

                if response.media:  
                    await message.client.send_message(  
                        message.peer_id, response, reply_to=message.reply_to_msg_id  
                    )  
                    await response.delete()  
                    await sent_msg.delete()  # хуй
                    await message.delete()  
                else:  
                    await message.edit("<b>❌ Ошибка: бот сын хуйни</b>")  

            except Exception as e:  
                await message.edit(f"<b>❌ Ошибка:</b> {e}")