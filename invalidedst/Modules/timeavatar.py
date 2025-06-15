#  _____                          
# |_   _|____  ____ _ _ __   ___  
#   | |/ _ \ \/ / _` | '_ \ / _ \ 
#   | | (_) >  < (_| | | | | (_) |
#   |_|\___/_/\_\__,_|_| |_|\___/ 
#                              
# meta banner: https://i.ibb.co/BV2s93rS/image-10098.jpg
# meta developer: @mqvon
# scope: @mqvon

import asyncio
import logging
import io
import aiohttp
import base64
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest
from telethon import utils
from .. import loader, utils as hikka_utils

logger = logging.getLogger(__name__)


@loader.tds
class TimeAvatarMod(loader.Module):
    """Модуль для автоматического обновления времени в аватарке"""
    
    strings = {
        "name": "TimeAvatar",
        "avatar_enabled": "🖼 <b>Время в аватарке включено!</b>\n"
                         "Ваша аватарка будет обновляться каждую минуту с московским временем",
        "avatar_disabled": "⏹ <b>Время в аватарке отключено</b>",
        "photo_set": "🖼 <b>Фото установлено!</b>\n"
                    "Теперь время будет отображаться поверх этого изображения",
        "photo_error": "❌ <b>Ошибка при установке фото</b>\n"
                      "Проверьте ссылку на изображение",
        "download_error": "❌ <b>Не удалось скачать изображение</b>",
        "already_running": "⚠️ <b>Время в аватарке уже включено</b>",
        "not_running": "⚠️ <b>Время в аватарке не запущено</b>",
        "no_photo": "❌ <b>Сначала установите фото командой .setavatarphoto</b>",
        "help_timeavatar": "Включить автоматическое обновление времени в аватарке",
        "help_setavatarphoto": "Установить фото, на которое будет накладываться время",
        "help_stopavatar": "Отключить время в аватарке"
    }
    
    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "timezone_offset",
                3,
                "Смещение часового пояса от UTC (для Москвы: 3)",
                validator=loader.validators.Integer(minimum=-12, maximum=14)
            ),
            loader.ConfigValue(
                "update_interval",
                60,
                "Интервал обновления в секундах",
                validator=loader.validators.Integer(minimum=30, maximum=3600)
            )
        )
        self._task = None
        self._background_photo = None
        
    async def client_ready(self, client, db):
        self._client = client
        self._db = db

        photo_b64 = self._db.get("TimeAvatar", "background_photo", None)
        if photo_b64:
            try:
                self._background_photo = base64.b64decode(photo_b64)
            except Exception as e:
                logger.error(f"Ошибка загрузки фото из базы: {e}")
                self._background_photo = None

    @loader.command()
    async def timeavatar(self, message):
        """Включить время в аватарке"""
        if self._task and not self._task.done():
            await hikka_utils.answer(message, self.strings["already_running"])
            return
            
        if not self._background_photo:
            await hikka_utils.answer(message, self.strings["no_photo"])
            return
        
        self._task = asyncio.create_task(self._update_time_loop())
        
        await hikka_utils.answer(message, self.strings["avatar_enabled"])
    
    @loader.command()
    async def setavatarphoto(self, message):
        """Установить фото для времени в аватарке"""
        args = hikka_utils.get_args_raw(message)
        
        if not args:

            if message.reply_to_msg_id:
                reply = await message.get_reply_message()
                if reply and reply.photo:
                    photo_data = await reply.download_media(bytes)
                    await self._process_background_photo(message, photo_data)
                    return
            
            await hikka_utils.answer(message, "❌ <b>Укажите ссылку на изображение или ответьте на сообщение с фото</b>")
            return
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(args) as response:
                    if response.status == 200:
                        photo_data = await response.read()
                        await self._process_background_photo(message, photo_data)
                    else:
                        await hikka_utils.answer(message, self.strings["download_error"])
        except Exception as e:
            logger.error(f"Ошибка скачивания изображения: {e}")
            await hikka_utils.answer(message, self.strings["download_error"])
    
    async def _process_background_photo(self, message, photo_data):
        """Обработка фонового изображения"""
        try:
            with Image.open(io.BytesIO(photo_data)) as img:
 
                self._background_photo = photo_data

                photo_b64 = base64.b64encode(photo_data).decode('utf-8')
                self._db.set("TimeAvatar", "background_photo", photo_b64)
                
                await hikka_utils.answer(message, self.strings["photo_set"])
        except Exception as e:
            logger.error(f"Ошибка обработки фото: {e}")
            await hikka_utils.answer(message, self.strings["photo_error"])
    
    @loader.command()
    async def stopavatar(self, message):
        """Отключить время в аватарке"""
        if not self._task or self._task.done():
            await hikka_utils.answer(message, self.strings["not_running"])
            return
        

        self._task.cancel()
        
        try:
            photos = await self._client.get_profile_photos("me", limit=1)
            if photos and self._background_photo:
                await self._client(DeletePhotosRequest(photos))
        except Exception as e:
            logger.error(f"Ошибка удаления фото: {e}")
        
        await hikka_utils.answer(message, self.strings["avatar_disabled"])
    
    async def _update_time_loop(self):
        """Основной цикл обновления времени"""
        while True:
            try:
                await self._update_nick_with_time()
                await asyncio.sleep(self.config["update_interval"])
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Ошибка обновления времени в нике: {e}")
                await asyncio.sleep(60)  
    
    async def _update_nick_with_time(self):
        """Обновление аватарки с текущим временем"""
        try:

            now = datetime.utcnow() + timedelta(hours=self.config["timezone_offset"])
            time_str = now.strftime("%H:%M")
            

            if self._background_photo:
                await self._update_profile_photo_with_time(time_str)
                
        except Exception as e:
            logger.error(f"Ошибка обновления аватарки: {e}")
    
    async def _update_profile_photo_with_time(self, time_str):
        """Обновление фото профиля с временем"""
        try:

            try:
                photos = await self._client.get_profile_photos("me", limit=1)
                if photos:
                    await self._client(DeletePhotosRequest(photos))
            except Exception as e:
                logger.debug(f"Предупреждение при удалении старого фото: {e}")
            

            with Image.open(io.BytesIO(self._background_photo)) as img:
               
                img = img.resize((640, 640), Image.Resampling.LANCZOS)
                
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                overlay = Image.new('RGBA', (640, 640), (0, 0, 0, 120))  
                img_rgba = img.convert('RGBA')
                img = Image.alpha_composite(img_rgba, overlay).convert('RGB')
                
                draw = ImageDraw.Draw(img)
                
                now = datetime.utcnow() + timedelta(hours=self.config["timezone_offset"])
                date_str = now.strftime('%d.%m.%Y')
                weekday_str = now.strftime('%A')
                
                weekdays = {
                    'Monday': 'Понедельник', 'Tuesday': 'Вторник', 'Wednesday': 'Среда',
                    'Thursday': 'Четверг', 'Friday': 'Пятница', 'Saturday': 'Суббота', 'Sunday': 'Воскресенье'
                }
                weekday_ru = weekdays.get(weekday_str, weekday_str)
                
                try:
                    time_font = ImageFont.truetype("/system/fonts/Arial.ttf", 90)
                    date_font = ImageFont.truetype("/system/fonts/Arial.ttf", 45)
                    day_font = ImageFont.truetype("/system/fonts/Arial.ttf", 38)
                except:
                    try:
                        time_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 90)
                        date_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 45)
                        day_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 38)
                    except:
                        time_font = ImageFont.load_default()
                        date_font = ImageFont.load_default()
                        day_font = ImageFont.load_default()
                
                time_bbox = draw.textbbox((0, 0), time_str, font=time_font)
                time_width = time_bbox[2] - time_bbox[0]
                time_height = time_bbox[3] - time_bbox[1]
                
                date_bbox = draw.textbbox((0, 0), date_str, font=date_font)
                date_width = date_bbox[2] - date_bbox[0]
                date_height = date_bbox[3] - date_bbox[1]
                
                day_bbox = draw.textbbox((0, 0), weekday_ru, font=day_font)
                day_width = day_bbox[2] - day_bbox[0]
                day_height = day_bbox[3] - day_bbox[1]
                
                center_x = 320
                
                time_x = center_x - time_width // 2
                time_y = 280
                
                date_x = center_x - date_width // 2
                date_y = time_y + time_height + 20
                
                day_x = center_x - day_width // 2
                day_y = date_y + date_height + 15
                
                def draw_text_with_shadow(x, y, text, font, shadow_offset=2):
                    for dx in range(-shadow_offset, shadow_offset + 1):
                        for dy in range(-shadow_offset, shadow_offset + 1):
                            if dx != 0 or dy != 0:
                                draw.text((x + dx, y + dy), text, font=font, fill='black')

                    draw.text((x, y), text, font=font, fill='white')
                

                draw_text_with_shadow(time_x, time_y, time_str, time_font, 3)
                
                draw_text_with_shadow(date_x, date_y, date_str, date_font, 2)
                
                draw_text_with_shadow(day_x, day_y, weekday_ru, day_font, 2)
                
                output = io.BytesIO()
                img.save(output, format='JPEG', quality=95)
                photo_bytes = output.getvalue()
                
                await self._client(UploadProfilePhotoRequest(
                    file=await self._client.upload_file(photo_bytes, file_name="time_photo.jpg")
                ))
                
        except Exception as e:
            logger.error(f"Ошибка обновления фото профиля: {e}")
    
    async def on_unload(self):
        """Очистка при выгрузке модуля"""
        if self._task and not self._task.done():
            self._task.cancel()
            
            try:
                photos = await self._client.get_profile_photos("me", limit=1)
                if photos and self._background_photo:
                    await self._client(DeletePhotosRequest(photos))
            except:
                pass