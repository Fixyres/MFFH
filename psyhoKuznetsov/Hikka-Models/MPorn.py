__version__ = (1, 0, 0)
# meta developer: @psyho_Kuznetsov

from .. import loader, utils
import random
import asyncio
import logging
from telethon.tl.types import Message, InputMessagesFilterVideo, InputMessagesFilterPhotos

@loader.tds
class Mporn(loader.Module):
    """+18 модуль!!!!!!!"""
    strings = {  
        "name": "MPorn",  
        "error_category": "<b>Ошибка:</b> Неверная категория!",  
        "error_media": "<b>Ошибка:</b> Не удалось найти медиа!",  
        "error_channel": "<b>Ошибка:</b> Не удалось получить данные из канала {channel}.\n{error}",  
        "loading": "<b>Загрузка медиа...</b>",  
    }  

    CHANNELS = {  
        "гей": ["@gay_porn18", "@FreeGayPornHD", "@GayBunker", "@gaypornworld"],  
        "хентай_видео": ["@hentai_tgg", "@anime_hentai_xxx"],  
        "хентай": ["@hentaiarts4", "@mirhentaya", "@HoQgAVNOBAsxMTJi"],  
        "порно": ["@Pornhub_prr", "@Legal_Teen", "@hot_videosxx"],  
        "лесби": ["@lesbians_4_me", "@lesbinka"],  
    }  

    def __init__(self):  
        self.config = loader.ModuleConfig(  
            "размер_кэша", 100,  
            "таймаут", 5,  
            "удалять_команду", True,
        )  
        self.channel_cache = {} 
        self.used_media = {} 

    async def client_ready(self, client, db):  
        self._client = client  
        self._db = db  
        all_channels = []  
        for channels in self.CHANNELS.values():  
            all_channels.extend(channels)  
        self.CHANNELS["рандом"] = all_channels  
        logging.info("Ай шалунишка зачем скачал модуль?")  

    async def _get_random_media_from_channel(self, channel, is_photo=False):
        if channel not in self.channel_cache:
            self.channel_cache[channel] = []
        if channel not in self.used_media:
            self.used_media[channel] = set()

        media_filter = InputMessagesFilterPhotos if is_photo else InputMessagesFilterVideo

        available_media = [msg for msg in self.channel_cache[channel] if msg.id not in self.used_media[channel]]
        if available_media:
            selected_msg = random.choice(available_media)
            self.used_media[channel].add(selected_msg.id)
            return selected_msg

        try:
            total_messages = await self._client.get_messages(channel, limit=1)
            if not total_messages:
                logging.warning(f"Канал {channel} пуст или недоступен.")
                return None

            total_count = total_messages.total 
            if total_count == 0:
                logging.warning(f"В канале {channel} нет сообщений.")
                return None

            random_offset = random.randint(0, max(0, total_count - 1))
            messages = []
            async for msg in self._client.iter_messages(
                channel,
                offset_id=random_offset,
                reverse=True,
                limit=self.config["размер_кэша"],  
                filter=media_filter
            ):
                if msg.media and msg.id not in self.used_media[channel]:
                    messages.append(msg)

            if not messages:
                logging.warning(f"Не найдено новое медиа в канале {channel}.")
                return None

            self.channel_cache[channel] = messages
            selected_msg = random.choice(messages)
            self.used_media[channel].add(selected_msg.id)
            return selected_msg

        except Exception as e:
            logging.error(f"Ошибка при получении медиа из {channel}: {str(e)}")
            return None

    async def send_random_media(self, message: Message, category: str):  
        if self.config["удалять_команду"]:  
            await message.delete()  

        if category not in self.CHANNELS:  
            return await message.respond(self.strings["error_category"])  

        loading_msg = await message.respond(self.strings["loading"])  
        channel = random.choice(self.CHANNELS[category])  
        is_photo = category == "хентай"  

        try:  
            task = self._get_random_media_from_channel(channel, is_photo)  
            media_msg = await asyncio.wait_for(task, timeout=self.config["таймаут"])  

            if media_msg:  
                await message.respond(file=media_msg.media)  
                await loading_msg.delete()  
            else:  
                await loading_msg.edit(self.strings["error_media"])  
        except asyncio.TimeoutError:  
            await loading_msg.edit(f"<b>Ошибка:</b> Таймаут при получении данных из канала {channel}.")  
        except Exception as e:  
            await loading_msg.edit(self.strings["error_channel"].format(  
                channel=channel, error=str(e)  
            ))  

    @loader.unrestricted  
    async def гейcmd(self, message: Message):  
        """Отправляет случайное гей видео"""  
        await self.send_random_media(message, "гей")  

    @loader.unrestricted  
    async def рандомcmd(self, message: Message):  
        """Отправляет случайный контент 18+"""  
        await self.send_random_media(message, "рандом")  

    @loader.unrestricted  
    async def хентайвcmd(self, message: Message):  
        """Отправляет случайное хентай видео"""  
        await self.send_random_media(message, "хентай_видео")  

    @loader.unrestricted  
    async def хентайcmd(self, message: Message):  
        """Отправляет случайное хентай фото"""  
        await self.send_random_media(message, "хентай")  

    @loader.unrestricted  
    async def порноcmd(self, message: Message):  
        """Отправляет случайное порно видео"""  
        await self.send_random_media(message, "порно")  

    @loader.unrestricted  
    async def лесбиcmd(self, message: Message):  
        """Отправляет случайное лесбийское видео"""  
        await self.send_random_media(message, "лесби")  