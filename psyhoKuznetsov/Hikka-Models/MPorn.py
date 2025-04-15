__version__ = (2, 0, 1)
# meta developer: @psyhomodules

from .. import loader, utils
import random
import asyncio
import logging
from telethon.tl.types import Message, InputMessagesFilterVideo, InputMessagesFilterPhotos

@loader.tds
class Mporn(loader.Module):
    """+18 модуль!!!!!"""
    
    strings = {
        "name": "MPorn",
        "error_category": "<b>Ошибка:</b> Неверная категория!",
        "error_media": "<b>Ошибка:</b> Не удалось найти медиа!",
        "error_channel": "<b>Ошибка:</b> Не удалось получить данные из канала {channel}.\n{error}",
        "loading": "<b>Загрузка медиа...</b>",
        "loading_video": "<b>Загрузка видео... {progress}%</b>",
        "loading_photo": "<b>Загрузка фото... {progress}%</b>",
        "thanks": "<b>Спасибо за использование нашего модуля!</b> ♥️"
    }

    CHANNELS = {  
        "gay": ["@gay_porn18", "@FreeGayPornHD"],  
        "hentai_video": ["@hentai_tgg", "@anime_hentai_xxx"],  
        "hentai": ["@hentaiarts4", "@mirhentaya"],  
        "porn": ["@Pornhub_prr", "@Legal_Teen"],  
        "lesbian": ["@lesbians_4_me", "@lesbinka"],  
    }  

    def __init__(self):  
        self.config = loader.ModuleConfig(  
            "cache_size", 100,
            "timeout", 5,
            "delete_command", True,
            "show_progress", True,
            "max_video_duration", 300, 
        )  
        self.channel_cache = {}
        self.used_media_ids = {}
        self._locks = {}
        self.blacklisted_channels = set()

     async def client_ready(self, client, db):
        self.client = client
        self.db = db
        all_channels = set()
        for channels in self.CHANNELS.values():
            all_channels.update(channels)
        self.CHANNELS["random"] = list(all_channels)
        
        for channel in all_channels:
            self.channel_cache[channel] = []
            self.used_media_ids[channel] = set()
            self._locks[channel] = asyncio.Lock()
        
        asyncio.create_task(self._background_preload())
        logging.info("MPorn модуль загружен")


    async def _background_preload(self):
        while True:
            try:
                for category, channels in self.CHANNELS.items():
                    if category != "random":
                        for channel in channels:
                            if channel not in self.blacklisted_channels:
                                is_photo = category == "hentai"
                                await self._prefetch_media(channel, is_photo)
                await asyncio.sleep(1800)
            except Exception as e:
                logging.error(f"Ошибка предзагрузки: {str(e)}")
                await asyncio.sleep(300)

    async def _prefetch_media(self, channel, is_photo=False):
        if channel in self.blacklisted_channels:
            return
        
        async with self._locks[channel]:
            if len(self.channel_cache[channel]) >= self.config["cache_size"]:
                return
            
            media_filter = InputMessagesFilterPhotos if is_photo else InputMessagesFilterVideo
            try:
                messages = await self._client.get_messages(
                    channel, 
                    limit=self.config["cache_size"] * 2,
                    filter=media_filter
                )
                
                if not messages or not messages.total:
                    self.blacklisted_channels.add(channel)
                    return
                
                new_messages = []
                for msg in messages:
                    if not msg.media or msg.id in self.used_media_ids[channel]:
                        continue
                    if not is_photo and hasattr(msg.media, 'video'):
                        duration = getattr(msg.media.document.attributes[0], 'duration', 0)
                        if duration <= self.config["max_video_duration"]:
                            new_messages.append(msg)
                    else:
                        new_messages.append(msg)
                
                self.channel_cache[channel] = new_messages[:self.config["cache_size"]]
            except Exception as e:
                logging.error(f"Ошибка предзагрузки {channel}: {str(e)}")
                self.blacklisted_channels.add(channel)

    async def _update_progress(self, loading_msg, is_photo=False):
        progress = 0
        template = self.strings["loading_photo"] if is_photo else self.strings["loading_video"]
        try:
            while progress < 99:
                progress += random.uniform(5, 15)
                progress = min(99, progress)
                await loading_msg.edit(template.format(progress=int(progress)))
                await asyncio.sleep(0.3)
        except Exception:
            pass

    async def _get_random_media(self, channel, is_photo=False, loading_msg=None):
        if channel in self.blacklisted_channels:
            return None
            
        async with self._locks[channel]:
            available_media = [
                msg for msg in self.channel_cache[channel]
                if msg.id not in self.used_media_ids[channel]
            ]
            
            if not available_media:
                media_filter = InputMessagesFilterPhotos if is_photo else InputMessagesFilterVideo
                try:
                    messages = await self._client.get_messages(
                        channel,
                        limit=self.config["cache_size"] * 2,
                        filter=media_filter
                    )
                    
                    if not messages or not messages.total:
                        self.blacklisted_channels.add(channel)
                        return None
                    
                    available_media = []
                    for msg in messages:
                        if not msg.media or msg.id in self.used_media_ids[channel]:
                            continue
                        if not is_photo and hasattr(msg.media, 'video'):
                            duration = getattr(msg.media.document.attributes[0], 'duration', 0)
                            if duration <= self.config["max_video_duration"]:
                                available_media.append(msg)
                        else:
                            available_media.append(msg)
                    
                    if not available_media:
                        return None
                        
                    self.channel_cache[channel] = available_media[:self.config["cache_size"]]
                
                except Exception as e:
                    logging.error(f"Ошибка получения медиа из {channel}: {str(e)}")
                    return None
            
            if not available_media:
                return None
                
            selected_msg = random.choice(available_media)
            self.used_media_ids[channel].add(selected_msg.id)
            
            if len(available_media) < self.config["cache_size"] // 2:
                asyncio.create_task(self._prefetch_media(channel, is_photo))
                
            return selected_msg

    async def send_random_media(self, message: Message, category: str, is_photo=False):
        if category not in self.CHANNELS:
            await message.respond(self.strings["error_category"])
            return
        
        if self.config["delete_command"]:
            await message.delete()  # Заменили utils.delete_message на message.delete()
            
        loading_msg = await message.respond(self.strings["loading"])
        progress_task = None
        
        try:
            if self.config["show_progress"]:
                progress_task = asyncio.create_task(self._update_progress(loading_msg, is_photo))
                
            channels = self.CHANNELS[category]
            random.shuffle(channels)
            
            for channel in channels:
                try:
                    media_msg = await asyncio.wait_for(
                        self._get_random_media(channel, is_photo, loading_msg),
                        timeout=self.config["timeout"]
                    )
                    
                    if media_msg:
                        await self._client.send_file(
                            message.peer_id,
                            file=media_msg.media,
                            caption=self.strings["thanks"],
                            reply_to=message.reply_to_msg_id if message.is_reply else None
                        )
                        break
                except asyncio.TimeoutError:
                    continue
            else:
                await loading_msg.edit(self.strings["error_media"])
                
        except Exception as e:
            logging.error(f"Ошибка отправки медиа: {str(e)}")
            await loading_msg.edit(self.strings["error_media"])
            
        finally:
            if progress_task:
                progress_task.cancel()
            await loading_msg.delete()  # Заменили utils.delete_message на loading_msg.delete()

    @loader.unrestricted
    async def gayvideocmd(self, message: Message):
        """Отправляет случайное гей видео"""
        await self.send_random_media(message, "gay")

    @loader.unrestricted
    async def randomvideocmd(self, message: Message):
        """Отправляет случайное 18+ видео"""
        await self.send_random_media(message, "random")

    @loader.unrestricted
    async def hentaivideocmd(self, message: Message):
        """Отправляет случайное хентай видео"""
        await self.send_random_media(message, "hentai_video")

    @loader.unrestricted
    async def hentaiphotocmd(self, message: Message):
        """Отправляет случайное хентай фото"""
        await self.send_random_media(message, "hentai", is_photo=True)

    @loader.unrestricted
    async def pornvideocmd(self, message: Message):
        """Отправляет случайное порно видео"""
        await self.send_random_media(message, "porn")

    @loader.unrestricted
    async def lesbianvideocmd(self, message: Message):
        """Отправляет случайное лесбийское видео"""
        await self.send_random_media(message, "lesbian")

    @loader.unrestricted
    async def randommediacmd(self, message: Message):
        """Отправляет случайное видео или фото из всех категорий"""
        await self.send_random_media(message, "random", is_photo=random.choice([True, False]))
