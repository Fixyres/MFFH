__version__ = (2, 1, 0)
# meta developer: @psyho_Kuznetsov

from .. import loader, utils
import random
import asyncio
import logging
import time
from telethon.tl.types import Message, InputMessagesFilterVideo, InputMessagesFilterPhotos
from telethon.errors import ChannelPrivateError

@loader.tds
class Mporn(loader.Module):
    """+18 модуль!!!!!!!"""
    strings = {  
        "name": "MPorn",  
        "error_category": "<b>Ошибка:</b> Неверная категория!",  
        "error_media": "<b>Ошибка:</b> Не удалось найти медиа!",  
        "error_channel": "<b>Ошибка:</b> Не удалось получить данные из канала {channel}.\n{error}",  
        "loading": "<b>Загрузка медиа...</b>",
        "loading_video": "<b>Загрузка видео... {progress}%</b>",
        "loading_photo": "<b>Загрузка изображения... {progress}%</b>",
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
            "размер_кэша", 300,
            "таймаут", 5,
            "удалять_команду", True,
            "авто_обновление", True,
            "показывать_прогресс", True,
            "интервал_обновления_прогресса", 0.5,
        )  
        self.channel_cache = {}
        self.used_media = {}
        self._locks = {}
        self._preload_tasks = {}

    async def client_ready(self, client, db):  
        self._client = client  
        self._db = db  
        
        all_channels = []  
        for channels in self.CHANNELS.values():  
            all_channels.extend(channels)  
        # Fixed: Create a list of unique channels instead of trying to append to a set
        self.CHANNELS["рандом"] = list(set(all_channels)) 
        
        for category in self.CHANNELS:
            for channel in self.CHANNELS[category]:
                if channel not in self.channel_cache:
                    self.channel_cache[channel] = []
                if channel not in self.used_media:
                    self.used_media[channel] = set()
                if channel not in self._locks:
                    self._locks[channel] = asyncio.Lock()
        
        if self.config["авто_обновление"]:
            asyncio.create_task(self._background_preload())
        
        logging.info("Ай шалунишка зачем скачал модуль?")

    async def _background_preload(self):
        while True:
            try:
                channels_to_preload = []
                for category, channels in self.CHANNELS.items():
                    if category != "рандом":  
                        for channel in channels:
                            cache_size = len(self.channel_cache.get(channel, []))
                            priority = max(0, self.config["размер_кэша"] - cache_size)
                            if priority > 0:
                                is_photo = category == "хентай"
                                channels_to_preload.append((channel, is_photo, priority))
                
                channels_to_preload.sort(key=lambda x: x[2], reverse=True)
                
                max_concurrent = 3
                active_tasks = []
                
                for channel, is_photo, _ in channels_to_preload[:10]: 
                    if len(active_tasks) >= max_concurrent:
                       
                        done, active_tasks = await asyncio.wait(
                            active_tasks, 
                            return_when=asyncio.FIRST_COMPLETED
                        )
                        for task in done:
                            try:
                                await task
                            except Exception as e:
                                logging.error(f"Ошибка при предзагрузке: {str(e)}")
                    
                    task = asyncio.create_task(self._prefetch_media(channel, is_photo))
                    active_tasks.append(task)
                
                if active_tasks:
                    await asyncio.gather(*active_tasks, return_exceptions=True)
                
                await asyncio.sleep(1800) 
            except Exception as e:
                logging.error(f"Ошибка при фоновой предзагрузке: {str(e)}")
                await asyncio.sleep(5) 

    async def _prefetch_media(self, channel, is_photo=False):
        try:
            async with self._locks[channel]:
                if len(self.channel_cache[channel]) >= self.config["размер_кэша"]:
                    return 
                
                media_filter = InputMessagesFilterPhotos if is_photo else InputMessagesFilterVideo
                
                try:
                    messages = []
                    total_messages = await self._client.get_messages(channel, limit=1)
                    
                    if not total_messages:
                        logging.warning(f"Канал {channel} пуст или недоступен.")
                        return
                    
                    total_count = total_messages.total
                    if total_count == 0:
                        logging.warning(f"В канале {channel} нет сообщений.")
                        return
                    
                    batch_size = min(self.config["размер_кэша"] - len(self.channel_cache[channel]), 50)
                    if batch_size <= 0:
                        return
                        
                    random_offset = random.randint(0, max(0, total_count - batch_size))
                    
                    async for msg in self._client.iter_messages(
                        channel,
                        offset_id=random_offset,
                        reverse=True,
                        limit=batch_size,
                        filter=media_filter
                    ):
                        if msg.media and msg.id not in self.used_media[channel]:
                            messages.append(msg)
                    
                    if messages:
                        self.channel_cache[channel].extend(messages)
                       
                        
                        seen_ids = set()
                        unique_messages = []
                        for msg in self.channel_cache[channel]:
                            if msg.id not in seen_ids:
                                seen_ids.add(msg.id)
                                unique_messages.append(msg)
                        
                    
                        unique_messages.sort(key=lambda msg: msg.id, reverse=True)
                        self.channel_cache[channel] = unique_messages[:self.config["размер_кэша"]]
                        
                except Exception as e:
                    logging.error(f"Ошибка при предзагрузке медиа из {channel}: {str(e)}")
        except Exception as e:
            logging.error(f"Ошибка при получении блокировки для {channel}: {str(e)}")

    async def _get_random_media_from_channel(self, channel, is_photo=False, loading_msg=None):
        try:
            progress_task = None
            if loading_msg and self.config["показывать_прогресс"]:
                progress_task = asyncio.create_task(
                    self._update_progress(
                        loading_msg, 
                        is_photo
                    )
                )
            
            try:
                async with self._locks[channel]:
                    available_media = [msg for msg in self.channel_cache[channel] if msg.id not in self.used_media[channel]]
                    
                    if available_media:
                        selected_msg = random.choice(available_media)
                        self.used_media[channel].add(selected_msg.id)
                        
                        if len(self.used_media[channel]) > self.config["размер_кэша"] * 2:
                            self.used_media[channel] = set(list(self.used_media[channel])[-self.config["размер_кэша"]:])
                            
                        return selected_msg
                    
                    media_filter = InputMessagesFilterPhotos if is_photo else InputMessagesFilterVideo
                    
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
                            limit=50, 
                            filter=media_filter
                        ):
                            if msg.media and msg.id not in self.used_media[channel]:
                                messages.append(msg)
                                if len(messages) >= 20: 
                                    break
                        
                        if not messages:
                            old_used = self.used_media[channel]
                            self.used_media[channel] = set()
                            

                            async for msg in self._client.iter_messages(
                                channel,
                                limit=30,
                                filter=media_filter
                            ):
                                if msg.media:
                                    messages.append(msg)
                                    if len(messages) >= 15:
                                        break
                            
                            if not messages:
                                self.used_media[channel] = old_used
                        
                        if not messages:
                            logging.warning(f"Не найдено медиа в канале {channel}.")
                            return None
                        
                    
                        self.channel_cache[channel] = messages
                        
                    
                        selected_msg = random.choice(messages)
                        self.used_media[channel].add(selected_msg.id)
                        return selected_msg
                        
                    except ChannelPrivateError:
                        logging.error(f"Канал {channel} недоступен (приватный).")
                        return None
                    except Exception as e:
                        logging.error(f"Ошибка при получении медиа из {channel}: {str(e)}")
                        return None
                    
            except Exception as e:
                logging.error(f"Ошибка при получении блокировки для {channel}: {str(e)}")
                return None
            finally:
                if progress_task:
                    progress_task.cancel()
                    try:
                        await progress_task
                    except asyncio.CancelledError:
                        pass
        except Exception as e:
            logging.error(f"Общая ошибка при получении медиа: {str(e)}")
            return None

    async def _update_progress(self, loading_msg, is_photo=False):
        progress = 0
        increment = random.randint(5, 15)
        try:
            template = self.strings["loading_photo"] if is_photo else self.strings["loading_video"]
            
            while progress < 99:
                progress = min(99, progress + increment)
                increment = random.randint(5, 20)
                
                try:
                    await loading_msg.edit(template.format(progress=progress))
                except Exception:
                    break
                
                await asyncio.sleep(self.config["интервал_обновления_прогресса"])
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logging.error(f"Ошибка при обновлении прогресса: {str(e)}")

    async def send_random_media(self, message: Message, category: str):
        if self.config["удалять_команду"]:
            await message.delete()
        
        if category not in self.CHANNELS:
            return await message.respond(self.strings["error_category"])
        
        loading_msg = await message.respond(self.strings["loading"])
        
        channels = self.CHANNELS[category]
        channels_sorted = sorted(
            channels,
            key=lambda ch: len([m for m in self.channel_cache.get(ch, []) if m.id not in self.used_media.get(ch, set())]),
            reverse=True
        )
        
        is_photo = category == "хентай"
        media_found = False
        
        for channel in channels_sorted:
            try:
                task = self._get_random_media_from_channel(channel, is_photo, loading_msg)
                media_msg = await asyncio.wait_for(task, timeout=self.config["таймаут"])
                
                if media_msg:
                    try:
                        await message.respond(file=media_msg.media)
                        media_found = True
                        break
                    except Exception as e:
                        logging.error(f"Ошибка при отправке медиа из {channel}: {str(e)}")
            except asyncio.TimeoutError:
                logging.warning(f"Таймаут при получении данных из канала {channel}.")
            except Exception as e:
                logging.error(f"Ошибка при получении медиа из канала {channel}: {str(e)}")
        
        try:
            await loading_msg.delete()
        except Exception:
            if media_found:
                await loading_msg.edit(f"<b>Медиа загружено успешно!</b>")
            else:
                await loading_msg.edit(self.strings["error_media"])
        
        if media_found and random.random() < 0.3:
            for ch in random.sample(channels, min(2, len(channels))):
                asyncio.create_task(self._prefetch_media(ch, is_photo))

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
