# ©️ qq_shark, 2025
# 🌐 https://github.com/qqshark/Modules/blob/main/AudioConvertor.py
# Licensed under GNU AGPL v3.0
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

# meta developer: @qq_shark && @SharkHostBot

__version__ = (1, 0, 0)

from pydub import AudioSegment 
from .. import loader, utils 
from telethon import types 
import io 
import aiohttp
import os
import uuid
import asyncio
from PIL import Image

def register(cb): 
    cb(AudioConverterMod()) 

class AudioConverterMod(loader.Module): 
    """Конвертор аудио и голосовых (by @qq_shark).
    
    Поддерживаемые форматы аудио: mp3, m4a, ogg, mpeg, wav, oga, 3gp.""" 
    strings = {'name': 'AudioConverter'} 
    
    def __init__(self): 
        self.name = self.strings['name'] 
        self._me = None 
        self._ratelimit = [] 
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "default_format",
                "mp3",
                "Формат по умолчанию для конвертации",
                validator=loader.validators.Choice(["mp3", "m4a", "ogg", "mpeg", "wav", "oga", "3gp"])
            ),
            loader.ConfigValue(
                "default_title",
                "Converted to {format}",
                "Название по умолчанию (используйте {format} для подстановки формата)"
            ),
            loader.ConfigValue(
                "default_performer",
                "t.me/qq_shark",
                "Исполнитель по умолчанию"
            ),
            loader.ConfigValue(
                "default_cover",
                "https://pomf2.lain.la/f/1m07e3re.jpg",
                "URL обложки по умолчанию (или 'none' для отключения обложек)"
            ),
            loader.ConfigValue(
                "max_memory_size",
                11,
                "Максимальный размер файла в МБ для загрузки в память (больше будет загружаться на диск)"
            ),
            loader.ConfigValue(
                "max_file_size",
                700,
                "Максимальный размер файла в МБ для обработки"
            )
        )
    
    async def client_ready(self, client, db): 
        self._db = db 
        self._client = client 
        self.me = await client.get_me() 
    
    def create_temp_filename(self, suffix=""):
        unique_id = str(uuid.uuid4())[:8]
        return f"temp_audio_{unique_id}{suffix}"
    
    def cleanup_file(self, filepath):
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                return True
        except Exception:
            pass
        return False
    
    def get_file_size_mb(self, reply):
        try:
            return reply.media.document.size / (1024 * 1024)
        except:
            return 0
    
    def get_file_size_bytes(self, reply):
        try:
            return reply.media.document.size
        except:
            return 0
    
    def create_progress_bar(self, current, total, length=10):
        if total == 0:
            return "[" + "□" * length + "]"
        
        progress = current / total
        filled = int(progress * length)
        empty = length - filled
        
        bar = "■" * filled + "□" * empty
        percentage = int(progress * 100)
        
        return f"[{bar}] {percentage}%"
    
    async def download_with_progress(self, message, media, destination, file_size_bytes):
        downloaded = 0
        last_update = 0
        
        async def progress_callback(current, total):
            nonlocal downloaded, last_update
            downloaded = current
            
            if asyncio.get_event_loop().time() - last_update > 1:
                progress_bar = self.create_progress_bar(current, total)
                await message.edit(f"[AudioConverter] Скачиваем... {progress_bar}")
                last_update = asyncio.get_event_loop().time()
        
        if isinstance(destination, str):
            await message.client.download_media(
                media, 
                destination, 
                progress_callback=progress_callback
            )
        else:
            await message.client.download_media(
                media, 
                destination, 
                progress_callback=progress_callback
            )
    
    def get_media_duration(self, reply):
        try:
            for attr in reply.media.document.attributes:
                if hasattr(attr, 'duration') and attr.duration:
                    return int(attr.duration)
            return 0
        except:
            return 0
    
    def is_media_file(self, reply):
        if not reply or not reply.media or not hasattr(reply.media, 'document'):
            return False
        
        mime_type = reply.media.document.mime_type
        return (mime_type.startswith('audio/') or 
                mime_type.startswith('video/') or
                any(hasattr(attr, 'voice') for attr in reply.media.document.attributes))
    
    def is_voice_note(self, reply):
        try:
            for attr in reply.media.document.attributes:
                if hasattr(attr, 'voice') and attr.voice:
                    return True
            return False
        except:
            return False
    
    async def download_cover(self, cover_url):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(cover_url) as response:
                    if response.status == 200:
                        content = await response.read()
                        if len(content) > 5 * 1024 * 1024:
                            return None
                        
                        img_io = io.BytesIO(content)
                        try:
                            img = Image.open(img_io)
                            if img.format.lower() in ['jpeg', 'jpg', 'png']:
                                img_io.seek(0)
                                return img_io
                        except:
                            pass
            return None
        except:
            return None
    
    def parse_toformat_args(self, message):
        text = utils.get_args_raw(message)
        frmts = ['ogg', 'mpeg', 'mp3', 'wav', 'oga', 'm4a', '3gp']
        
        if not text:
            return self.config["default_format"], None, None, None, None
        
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        if not lines:
            return self.config["default_format"], None, None, None, None
        
        first_line_parts = lines[0].split(' ', 1)
        
        formatik = None
        cover_url = None
        
        if first_line_parts[0].lower() in frmts:
            formatik = first_line_parts[0].lower()
            if len(first_line_parts) > 1:
                cover_part = first_line_parts[1].strip()
                if cover_part.lower() == 'none':
                    cover_url = 'none'
                elif cover_part.startswith('http'):
                    cover_url = cover_part
        else:
            formatik = self.config["default_format"]
            cover_part = lines[0].strip()
            if cover_part.lower() == 'none':
                cover_url = 'none'
            elif cover_part.startswith('http'):
                cover_url = cover_part
        
        custom_title = None
        custom_performer = None
        
        remaining_lines = lines[1:] if formatik == first_line_parts[0].lower() else lines[1:] if cover_url else lines
        
        if len(remaining_lines) >= 1:
            custom_title = remaining_lines[0]
        if len(remaining_lines) >= 2:
            custom_performer = remaining_lines[1]
        
        return formatik, cover_url, custom_title, custom_performer, None
    
    async def tovoicecmd(self, message): 
        """- <reply to media> 
        Конвертировать аудио/видео в голосовое.
        """ 
        reply = await message.get_reply_message() 
        if not reply: 
            await message.edit("А где реплай?") 
            return 
        
        if not self.is_media_file(reply):
            await message.edit("Это не медиафайл!") 
            return 
        
        file_size_mb = self.get_file_size_mb(reply)
        file_size_bytes = self.get_file_size_bytes(reply)
        max_file_size_mb = self.config["max_file_size"]
        max_memory_mb = self.config["max_memory_size"]
        
        if file_size_mb > max_file_size_mb:
            await message.edit(f"❌ Файл слишком большой ({file_size_mb:.1f}МБ). Максимальный размер: {max_file_size_mb}МБ")
            return
        
        use_disk = file_size_mb > max_memory_mb
        
        temp_input_file = None
        temp_output_file = None
        
        try:
            await message.edit("[AudioConverter] Скачиваем... [□□□□□□□□□□] 0%")
            
            if use_disk:
                temp_input_file = self.create_temp_filename(".tmp")
                await self.download_with_progress(message, reply.media.document, temp_input_file, file_size_bytes)
                
                await message.edit("[AudioConverter] Делаем войс...")
                audio = AudioSegment.from_file(temp_input_file)
            else:
                au = io.BytesIO()
                await self.download_with_progress(message, reply.media.document, au, file_size_bytes)
                au.seek(0)
                
                await message.edit("[AudioConverter] Делаем войс...")
                audio = AudioSegment.from_file(au)
            
            audio = audio.split_to_mono()[0] if len(audio.split_to_mono()) > 1 else audio
            dur = int(len(audio) / 1000)
            
            await message.edit("[AudioConverter] Экспортируем...")
            
            if use_disk:
                temp_output_file = self.create_temp_filename(".ogg")
                audio.export(temp_output_file, format="ogg", bitrate="64k", codec="libopus")
                
                await message.edit("[AudioConverter] Отправляем...")
                await message.client.send_file(
                    message.to_id,
                    temp_output_file,
                    reply_to=reply.id,
                    voice_note=True,
                    duration=dur
                )
            else:
                m = io.BytesIO()
                m.name = "voice.ogg"
                audio.export(m, format="ogg", bitrate="64k", codec="libopus")
                
                await message.edit("[AudioConverter] Отправляем...")
                m.seek(0)
                await message.client.send_file(
                    message.to_id,
                    m,
                    reply_to=reply.id,
                    voice_note=True,
                    duration=dur
                )
            
            await message.delete()
            
        except Exception as e:
            await message.edit(f"❌ Ошибка при конвертации: {str(e)}")
        finally:
            if temp_input_file:
                self.cleanup_file(temp_input_file)
            if temp_output_file:
                self.cleanup_file(temp_output_file)
    
    async def toformatcmd(self, message): 
        """- <replay to media> [format] [url_cover/none]
        [name]
        [author]
        """ 
        frmts = ['ogg', 'mpeg', 'mp3', 'wav', 'oga', 'm4a', '3gp'] 
        reply = await message.get_reply_message() 
        
        if not reply: 
            await message.edit("А где реплай?") 
            return 
        
        if not self.is_media_file(reply):
            await message.edit("Это не медиафайл!") 
            return 
        
        formatik, cover_url, custom_title, custom_performer, _ = self.parse_toformat_args(message)
        
        if formatik not in frmts: 
            await message.edit(f"Формат {formatik} для конвертирования не поддерживается!") 
            return 
        
        if not custom_title:
            custom_title = self.config["default_title"].format(format=formatik)
        if not custom_performer:
            custom_performer = self.config["default_performer"]
        if cover_url is None:
            cover_url = self.config["default_cover"]
        
        file_size_mb = self.get_file_size_mb(reply)
        file_size_bytes = self.get_file_size_bytes(reply)
        max_file_size_mb = self.config["max_file_size"]
        max_memory_mb = self.config["max_memory_size"]
        
        if file_size_mb > max_file_size_mb:
            await message.edit(f"❌ Файл слишком большой ({file_size_mb:.1f}МБ). Максимальный размер: {max_file_size_mb}МБ")
            return
        
        use_disk = file_size_mb > max_memory_mb
        
        temp_input_file = None
        temp_output_file = None
        
        try:
            await message.edit("[AudioConverter] Скачиваем... [□□□□□□□□□□] 0%")
            
            if use_disk:
                temp_input_file = self.create_temp_filename(".tmp")
                await self.download_with_progress(message, reply.media.document, temp_input_file, file_size_bytes)
                
                cover_data = None
                if cover_url and cover_url.lower() != 'none':
                    cover_data = await self.download_cover(cover_url)
                    if not cover_data:
                        await message.edit("⚠️ Не удалось скачать обложку, продолжаем без неё...")
                
                await message.edit(f"[AudioConverter] Конвертируем в {formatik}...")
                audio = AudioSegment.from_file(temp_input_file)
                audio = audio.split_to_mono()[0] if len(audio.split_to_mono()) > 1 else audio
                
                temp_output_file = self.create_temp_filename(f".{formatik}")
                await message.edit("[AudioConverter] Экспортируем...")
                audio.export(temp_output_file, format=formatik)
                
                duration = self.get_media_duration(reply)
                if duration == 0:
                    duration = int(len(audio) / 1000)
                
                attributes = [
                    types.DocumentAttributeAudio(
                        duration=duration,
                        title=custom_title,
                        performer=custom_performer
                    )
                ]
                
                await message.edit("[AudioConverter] Отправляем...")
                await message.client.send_file(
                    message.to_id,
                    temp_output_file,
                    reply_to=reply.id,
                    attributes=attributes,
                    thumb=cover_data
                )
            else:
                au = io.BytesIO()
                await self.download_with_progress(message, reply.media.document, au, file_size_bytes)
                au.seek(0)
                
                cover_data = None
                if cover_url and cover_url.lower() != 'none':
                    cover_data = await self.download_cover(cover_url)
                    if not cover_data:
                        await message.edit("⚠️ Не удалось скачать обложку, продолжаем без неё...")
                
                await message.edit(f"[AudioConverter] Конвертируем в {formatik}...")
                audio = AudioSegment.from_file(au)
                m = io.BytesIO()
                m.name = f"Converted_to.{formatik}"
                audio = audio.split_to_mono()[0] if len(audio.split_to_mono()) > 1 else audio
                
                await message.edit("[AudioConverter] Экспортируем...")
                audio.export(m, format=formatik)
                
                duration = self.get_media_duration(reply)
                if duration == 0:
                    duration = int(len(audio) / 1000)
                
                attributes = [
                    types.DocumentAttributeAudio(
                        duration=duration,
                        title=custom_title,
                        performer=custom_performer
                    )
                ]
                
                await message.edit("[AudioConverter] Отправляем...")
                m.seek(0)
                await message.client.send_file(
                    message.to_id,
                    m,
                    reply_to=reply.id,
                    attributes=attributes,
                    thumb=cover_data
                )
            
            await message.delete()
            
        except Exception as e:
            await message.edit(f"❌ Ошибка при конвертации: {str(e)}")
        finally:
            if temp_input_file:
                self.cleanup_file(temp_input_file)
            if temp_output_file:
                self.cleanup_file(temp_output_file)
