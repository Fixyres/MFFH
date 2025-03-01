__version__ = (2, 0, 1)
# meta developer: @psyho_Kuznetsov

from .. import loader, utils
import random
import asyncio
import logging
from telethon.tl.types import Message, InputMessagesFilterVideo, InputMessagesFilterPhotos
from telethon.errors import ChannelPrivateError, MessageDeleteForbiddenError

@loader.tds
class Mporn(loader.Module):
    """+18 module!!!!!"""
    
    strings = {
        "name": "MPorn",
        "error_category": "<b>Error:</b> Invalid category!",
        "error_media": "<b>Error:</b> Failed to find media!",
        "error_channel": "<b>Error:</b> Failed to fetch data from channel {channel}.\n{error}",
        "loading": "<b>Loading media...</b>",
        "loading_video": "<b>Loading video... {progress}%</b>",
        "loading_photo": "<b>Loading photo... {progress}%</b>",
        "thanks": "<b>Thank you for using our module!</b> ♥️",
        "language": "en_doc"
    }

    strings_ru = {
        "name": "MPorn",
        "error_category": "<b>Ошибка:</b> Неверная категория!",
        "error_media": "<b>Ошибка:</b> Не удалось найти медиа!",
        "error_channel": "<b>Ошибка:</b> Не удалось получить данные из канала {channel}.\n{error}",
        "loading": "<b>Загрузка медиа...</b>",
        "loading_video": "<b>Загрузка видео... {progress}%</b>",
        "loading_photo": "<b>Загрузка фото... {progress}%</b>",
        "thanks": "<b>Спасибо за использование нашего модуля!</b> ♥️",
        "language": "ru_doc"
    }

    strings_ua = {
        "name": "MPorn",
        "error_category": "<b>Помилка:</b> Невірна категорія!",
        "error_media": "<b>Помилка:</b> Не вдалося знайти медіа!",
        "error_channel": "<b>Помилка:</b> Не вдалося отримати дані з каналу {channel}.\n{error}",
        "loading": "<b>Завантаження медіа...</b>",
        "loading_video": "<b>Завантаження відео... {progress}%</b>",
        "loading_photo": "<b>Завантаження фото... {progress}%</b>",
        "thanks": "<b>Дякуємо за використання нашого модуля!</b> ♥️",
        "language": "ua_doc"
    }

    strings_de = {
        "name": "MPorn",
        "error_category": "<b>Fehler:</b> Ungültige Kategorie!",
        "error_media": "<b>Fehler:</b> Medien konnten nicht gefunden werden!",
        "error_channel": "<b>Fehler:</b> Daten vom Kanal {channel} konnten nicht abgerufen werden.\n{error}",
        "loading": "<b>Medien werden geladen...</b>",
        "loading_video": "<b>Video wird geladen... {progress}%</b>",
        "loading_photo": "<b>Foto wird geladen... {progress}%</b>",
        "thanks": "<b>Vielen Dank, dass Sie unser Modul verwenden!</b> ♥️",
        "language": "de_doc"
    }

    strings_tr = {
        "name": "MPorn",
        "error_category": "<b>Hata:</b> Geçersiz kategori!",
        "error_media": "<b>Hata:</b> Medya bulunamadı!",
        "error_channel": "<b>Hata:</b> {channel} kanalından veri alınamadı.\n{error}",
        "loading": "<b>Medya yükleniyor...</b>",
        "loading_video": "<b>Video yükleniyor... {progress}%</b>",
        "loading_photo": "<b>Fotoğraf yükleniyor... {progress}%</b>",
        "thanks": "<b>Modülümüzü kullandığınız için teşekkür ederiz!</b> ♥️",
        "language": "tr_doc"
    }

    strings_tt = {
        "name": "MPorn",
        "error_category": "<b>Хата:</b> Яраксыз категория!",
        "error_media": "<b>Хата:</b> Медиа табылмады!",
        "error_channel": "<b>Хата:</b> {channel} каналыннан мәгълүмат алып булмады.\n{error}",
        "loading": "<b>Медиа йөкләнә...</b>",
        "loading_video": "<b>Видео йөкләнә... {progress}%</b>",
        "loading_photo": "<b>Фото йөкләнә... {progress}%</b>",
        "thanks": "<b>Безнең модульны кулланган өчен рәхмәт!</b> ♥️",
        "language": "tt_doc"
    }

    strings_es = {
        "name": "MPorn",
        "error_category": "<b>Error:</b> ¡Categoría inválida!",
        "error_media": "<b>Error:</b> ¡No se encontraron medios!",
        "error_channel": "<b>Error:</b> No se pudieron obtener datos del canal {channel}.\n{error}",
        "loading": "<b>Cargando medios...</b>",
        "loading_video": "<b>Cargando video... {progress}%</b>",
        "loading_photo": "<b>Cargando foto... {progress}%</b>",
        "thanks": "<b>¡Gracias por usar nuestro módulo!</b> ♥️",
        "language": "es_doc"
    }

    strings_kk = {
        "name": "MPorn",
        "error_category": "<b>Қате:</b> Жарамсыз категория!",
        "error_media": "<b>Қате:</b> Медиа табылмады!",
        "error_channel": "<b>Қате:</b> {channel} арнасынан деректер алу мүмкін болмады.\n{error}",
        "loading": "<b>Медиа жүктелуде...</b>",
        "loading_video": "<b>Видео жүктелуде... {progress}%</b>",
        "loading_photo": "<b>Фото жүктелуде... {progress}%</b>",
        "thanks": "<b>Біздің модулімізді пайдаланғаныңызға рахмет!</b> ♥️",
        "language": "kk_doc"
    }

    strings_yz = {
        "name": "MPorn",
        "error_category": "<b>Хато:</b> Яроқсиз категория!",
        "error_media": "<b>Хато:</b> Медиа топилмади!",
        "error_channel": "<b>Хато:</b> {channel} каналидан маълумот олиб булмади.\n{error}",
        "loading": "<b>Медиа юкланмоқда...</b>",
        "loading_video": "<b>Видео юкланмоқда... {progress}%</b>",
        "loading_photo": "<b>Фото юкланмоқда... {progress}%</b>",
        "thanks": "<b>Модулимизни ишлатганингиз учун раҳмат!</b> ♥️",
        "language": "yz_doc"
    } 

    CHANNELS = {  
        "gay": ["@gay_porn18", "@FreeGayPornHD", "@GayBunker", "@gaypornworld"],  
        "hentai_video": ["@hentai_tgg", "@anime_hentai_xxx"],  
        "hentai": ["@hentaiarts4", "@mirhentaya", "@HoQgAVNOBAsxMTJi"],  
        "porn": ["@Pornhub_prr", "@Legal_Teen"],  
        "lesbian": ["@lesbians_4_me", "@lesbinka"],  
    }  

    def __init__(self):  
        self.config = loader.ModuleConfig(  
            "cache_size", 500, 
            "timeout", 5,
            "delete_command", True,
            "auto_preload", True, 
            "show_progress", True,
            "progress_update_interval", 0.5,
            "blacklisted_channels", [],
        )  
        self.channel_cache = {}
        self.used_media = {}
        self._locks = {}
        self.blacklisted_channels = set(self.config["blacklisted_channels"] if self.config["blacklisted_channels"] is not None else [])
        self._last_error = None 

    async def client_ready(self, client, db):  
        self._client = client  
        self._db = db  
        
        all_channels = set() 
        for channels in self.CHANNELS.values():  
            all_channels.update(channels) 
        self.CHANNELS["random"] = list(all_channels) 
        
        for category in self.CHANNELS:
            for channel in self.CHANNELS[category]:
                if channel not in self.channel_cache:
                    self.channel_cache[channel] = []
                if channel not in self.used_media:
                    self.used_media[channel] = set()
                if channel not in self._locks:
                    self._locks[channel] = asyncio.Lock()
        
        if self.config["auto_preload"]:
            asyncio.create_task(self._background_preload())
        
        logging.info("Ай шалунишка зачем скачал модуль?")

    async def _background_preload(self):
        retry_count = 0
        max_retries = 5
        while True:
            try:
                channels_to_preload = []
                for category, channels in self.CHANNELS.items():
                    if category != "random":  
                        for channel in channels:
                            if channel not in self.blacklisted_channels:
                                cache_size = len(self.channel_cache.get(channel, []))
                                priority = max(0, self.config["cache_size"] - cache_size)
                                if priority > 0:
                                    is_photo = category == "hentai"
                                    channels_to_preload.append((channel, is_photo, priority))
                
                if not channels_to_preload:
                    await asyncio.sleep(1800) 
                    continue
                
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
                                logging.error(f"Preload error for {channel}: {str(e)}")
                    
                    task = asyncio.create_task(self._prefetch_media(channel, is_photo))
                    active_tasks.append(task)
                
                if active_tasks:
                    await asyncio.gather(*active_tasks, return_exceptions=True)
                
                retry_count = 0
                await asyncio.sleep(1800) 
            except Exception as e:
                error_msg = f"Background preload error: {str(e)}"
                if error_msg != self._last_error:
                    logging.error(error_msg)
                    self._last_error = error_msg
                retry_count += 1
                if retry_count >= max_retries:
                    logging.error("Max retries reached. Pausing for 1 hour.")
                    await asyncio.sleep(3600)
                    retry_count = 0
                else:
                    await asyncio.sleep(5 * retry_count)

    async def _prefetch_media(self, channel, is_photo=False):
        if channel in self.blacklisted_channels:
            return
        try:
            async with self._locks[channel]:
                if len(self.channel_cache[channel]) >= self.config["cache_size"]:
                    return
                
                media_filter = InputMessagesFilterPhotos if is_photo else InputMessagesFilterVideo
                
                try:
                    messages = await self._client.get_messages(channel, limit=self.config["cache_size"], filter=media_filter)
                    if not messages or not messages.total:
                        logging.warning(f"Channel {channel} is empty or unavailable.")
                        self.blacklisted_channels.add(channel)
                        return
                    
                    unique_messages = []
                    seen_ids = set()
                    for msg in messages:
                        if msg.media and msg.id not in self.used_media[channel] and msg.id not in seen_ids:
                            unique_messages.append(msg)
                            seen_ids.add(msg.id)
                    
                    self.channel_cache[channel] = unique_messages[:self.config["cache_size"]]
                except ChannelPrivateError:
                    self.blacklisted_channels.add(channel)
                    logging.info(f"Channel {channel} added to blacklist (private or unavailable).")
                except Exception as e:
                    logging.error(f"Error preloading media from {channel}: {str(e)}")
        except Exception as e:
            logging.error(f"Lock error for {channel}: {str(e)}")

    async def _get_random_media_from_channel(self, channel, is_photo=False, loading_msg=None):
        if channel in self.blacklisted_channels:
            return None
        try:
            progress_task = None
            if loading_msg and self.config["show_progress"]:
                progress_task = asyncio.create_task(self._update_progress(loading_msg, is_photo))
            
            async with self._locks[channel]:
                available_media = [msg for msg in self.channel_cache.get(channel, []) if msg.id not in self.used_media[channel]]
                
                if available_media:
                    selected_msg = random.choice(available_media)
                    self.used_media[channel].add(selected_msg.id)
                    if len(self.used_media[channel]) > self.config["cache_size"] * 2:
                        self.used_media[channel] = set(list(self.used_media[channel])[-self.config["cache_size"]:])
                    return selected_msg
                
                media_filter = InputMessagesFilterPhotos if is_photo else InputMessagesFilterVideo
                messages = await self._client.get_messages(channel, limit=50, filter=media_filter)
                
                if not messages or not messages.total:
                    logging.warning(f"Channel {channel} is empty or unavailable.")
                    self.blacklisted_channels.add(channel)
                    return None
                
                available_messages = [msg for msg in messages if msg.media and msg.id not in self.used_media[channel]]
                if not available_messages:
                    self.used_media[channel].clear()  # Reset used media if none available
                    messages = await self._client.get_messages(channel, limit=30, filter=media_filter)
                    available_messages = [msg for msg in messages if msg.media]
                
                if not available_messages:
                    logging.warning(f"No media available in {channel}.")
                    self.blacklisted_channels.add(channel)
                    return None
                
                selected_msg = random.choice(available_messages)
                self.used_media[channel].add(selected_msg.id)
                self.channel_cache[channel] = available_messages[:self.config["cache_size"]]
                return selected_msg
        except Exception as e:
            logging.error(f"Error fetching media from {channel}: {str(e)}")
            return None
        finally:
            if progress_task:
                progress_task.cancel()
                try:
                    await progress_task
                except asyncio.CancelledError:
                    pass

    async def _update_progress(self, loading_msg, is_photo=False):
        progress = 0
        try:
            template = self.strings["loading_photo"] if is_photo else self.strings["loading_video"]
            while progress < 99:
                progress += random.uniform(5, 10)
                progress = min(99, progress)
                await loading_msg.edit(template.format(progress=int(progress)))
                await asyncio.sleep(self.config["progress_update_interval"])
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logging.error(f"Progress update error: {str(e)}")

    async def send_random_media(self, message: Message, category: str, is_photo=False):
        if self.config["delete_command"]:
            try:
                logging.debug(f"Attempting to delete command message {message.id} in chat {message.chat_id}")
                await self._client.delete_messages(message.chat_id, [message.id])
                logging.debug(f"Command message {message.id} deleted successfully")
            except MessageDeleteForbiddenError:
                logging.warning(f"Cannot delete message {message.id}: No permission in chat {message.chat_id}")
            except Exception as e:
                logging.error(f"Failed to delete command message {message.id}: {str(e)}")
        
        if category not in self.CHANNELS:
            await message.respond(self.strings["error_category"])
            return
        
        loading_msg = await message.respond(self.strings["loading"])
        
        channels = self.CHANNELS[category]
        media_found = False
        
        for channel in sorted(channels, key=lambda ch: len(self.channel_cache.get(ch, [])), reverse=True):
            try:
                task = self._get_random_media_from_channel(channel, is_photo, loading_msg)
                media_msg = await asyncio.wait_for(task, timeout=self.config["timeout"])
                
                if media_msg:
                    await self._client.send_file(
                        message.peer_id,
                        file=media_msg.media,
                        caption=self.strings["thanks"],
                        reply_to=message.reply_to_msg_id if message.is_reply else None
                    )
                    media_found = True
                    break
            except asyncio.TimeoutError:
                logging.warning(f"Timeout fetching from {channel}")
            except Exception as e:
                logging.error(f"Error fetching media from {channel}: {str(e)}")
        
        try:
            await loading_msg.delete()
        except Exception:
            if not media_found:
                await loading_msg.edit(self.strings["error_media"])

    @loader.unrestricted
    async def gayvideocmd(self, message: Message):
        """Sends a random gay video"""
        await self.send_random_media(message, "gay")

    @loader.unrestricted
    async def randomvideocmd(self, message: Message):
        """Sends a random 18+ video"""
        await self.send_random_media(message, "random")

    @loader.unrestricted
    async def hentaivideocmd(self, message: Message):
        """Sends a random hentai video"""
        await self.send_random_media(message, "hentai_video")

    @loader.unrestricted
    async def hentaiphotocmd(self, message: Message):
        """Sends a random hentai photo"""
        await self.send_random_media(message, "hentai", is_photo=True)

    @loader.unrestricted
    async def pornvideocmd(self, message: Message):
        """Sends a random porn video"""
        await self.send_random_media(message, "porn")

    @loader.unrestricted
    async def lesbianvideocmd(self, message: Message):
        """Sends a random lesbian video"""
        await self.send_random_media(message, "lesbian")

    @loader.unrestricted
    async def randommediacmd(self, message: Message):
        """Sends a random video or photo from all categories"""
        await self.send_random_media(message, "random", is_photo=random.choice([True, False]))
