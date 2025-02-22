# meta developer: @codeer_kot
# не меняйте мой код, пожалуйста, указывая что вы создатель модуля.

from .. import loader, utils
import random
import asyncio

@loader.tds
class KotWinterModule(loader.Module):
    """модуль, который отправляет рандом видио с зимой"""
    strings = {
        "name": "KotWinter",
        "no_media": "медиа в канале не найдено.",
        "error": "Произошла ошибка при получении медиа: {}"
    }

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.зима = db.get(self.strings["name"], "KotWinter", 1)
        self.канал = "https://t.me/+31S-RKH5EfBkZjdk"
    
    @loader.command()
    async def wincmd(self, message):
        "- вывести медиа с зимним вайбом."
        try:
            channel = await self.client.get_entity(self.канал)
            messages = await self.client.get_messages(channel, limit=100)
            media_messages = [msg for msg in messages if msg.media]
            if not media_messages:
                await message.reply(self.strings["no_media"])
                return

            chosen_media = random.choice(media_messages)

            await self.client.send_file(
                message.chat_id,
                chosen_media.media,
                caption=f"<blockquote> Хочу зиму {self.зима}. </blockquote>"
            )
            await message.delete()

            self.зима += 1
            self.db.set(self.strings["name"], "KotWinter", self.зима)

        except Exception as e:
            await message.reply(self.strings["error"].format(str(e)))
