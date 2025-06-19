# meta developer: @YahooMods
# requires: pillow ffmpeg-python

import io
import os
import tempfile
import ffmpeg
from PIL import Image
from telethon.tl.types import DocumentAttributeSticker, DocumentAttributeAnimated, DocumentAttributeVideo
from .. import loader, utils


@loader.tds
class StickerDownloaderMod(loader.Module):
    """Модуль для скачивания стикеров в различных форматах"""
    
    strings = {
        "name": "StickerDownloader",
        "no_reply": "❌ <b>Ответьте на стикер</b>",
        "not_sticker": "❌ <b>Это не стикер</b>",
        "downloading": "⏳ <b>Скачиваю стикер...</b>",
        "converting": "🔄 <b>Конвертирую в {}...</b>",
        "error": "❌ <b>Ошибка при обработке стикера</b>",
        "choose_format": "📥 <b>Выберите формат для скачивания:</b>",
        "webp_format": "📄 WebP",
        "png_format": "🖼 PNG",
        "jpg_format": "🖼 JPEG", 
        "tgs_format": "🎭 TGS",
        "webm_format": "🎬 WebM",
        "mp4_format": "🎥 MP4"
    }

    async def sdowncmd(self, message):
        """Скачать стикер - используйте в ответ на стикер"""
        reply = await message.get_reply_message()
        
        if not reply:
            await utils.answer(message, self.strings["no_reply"])
            return
            
        if not reply.sticker:
            await utils.answer(message, self.strings["not_sticker"])
            return
            
        # Определяем тип стикера
        is_animated = reply.sticker.mime_type == "application/x-tgs"
        is_video = reply.sticker.mime_type == "video/webm"
        
        # Формируем кнопки
        buttons = [
            [
                {"text": self.strings["webp_format"], "callback": self.download_format, "args": ("webp", reply)},
                {"text": self.strings["png_format"], "callback": self.download_format, "args": ("png", reply)}
            ],
            [
                {"text": self.strings["jpg_format"], "callback": self.download_format, "args": ("jpg", reply)}
            ]
        ]
        
        if is_animated:
            buttons.append([
                {"text": self.strings["tgs_format"], "callback": self.download_format, "args": ("tgs", reply)}
            ])
            
        if is_video or is_animated:
            buttons.append([
                {"text": self.strings["webm_format"], "callback": self.download_format, "args": ("webm", reply)},
                {"text": self.strings["mp4_format"], "callback": self.download_format, "args": ("mp4", reply)}
            ])
        
        await self.inline.form(
            text=self.strings["choose_format"],
            message=message,
            reply_markup=buttons
        )

    async def download_format(self, call, format_type, reply_msg):
        """Универсальный метод для скачивания в разных форматах"""
        await call.edit(self.strings["converting"].format(format_type.upper()))
        
        try:
            # Создаем временный файл для входного стикера
            with tempfile.NamedTemporaryFile(delete=False, suffix=".tmp") as input_file:
                await reply_msg.download_media(input_file.name)
                input_path = input_file.name
            
            try:
                # Конвертируем в нужный формат
                if format_type == "webp":
                    output_path = input_path
                    send_params = {
                        "mime_type": "image/webp",
                        "file_name": "sticker.webp"
                    }
                elif format_type == "png":
                    output_path = await self._convert_to_png(input_path)
                    send_params = {
                        "mime_type": "image/png", 
                        "file_name": "sticker.png"
                    }
                elif format_type == "jpg":
                    output_path = await self._convert_to_jpg(input_path)
                    send_params = {
                        "mime_type": "image/jpeg",
                        "file_name": "sticker.jpg"
                    }
                elif format_type == "tgs":
                    output_path = input_path
                    send_params = {
                        "mime_type": "application/x-tgs",
                        "file_name": "sticker.tgs",
                        "attributes": [DocumentAttributeAnimated()]
                    }
                elif format_type == "webm":
                    output_path = await self._convert_to_webm(input_path)
                    send_params = {
                        "mime_type": "video/webm",
                        "file_name": "sticker.webm",
                        "attributes": [DocumentAttributeVideo(
                            duration=5,
                            w=512,
                            h=512,
                            round_message=False,
                            supports_streaming=True
                        )]
                    }
                elif format_type == "mp4":
                    output_path = await self._convert_to_mp4(input_path)
                    send_params = {
                        "mime_type": "video/mp4",
                        "file_name": "sticker.mp4", 
                        "attributes": [DocumentAttributeVideo(
                            duration=5,
                            w=512,
                            h=512,
                            round_message=False,
                            supports_streaming=True
                        )]
                    }
                else:
                    output_path = input_path
                    send_params = {}
                
                # Отправляем результат
                await self._client.send_file(
                    call.form["chat"], 
                    output_path,
                    reply_to=call.form.get("reply_to"),
                    **send_params
                )
                
                # Удаляем временные файлы
                if output_path != input_path and os.path.exists(output_path):
                    os.remove(output_path)
                    
            finally:
                # Всегда удаляем исходный временный файл
                if os.path.exists(input_path):
                    os.remove(input_path)
                    
            await call.delete()
            
        except Exception as e:
            await call.edit(f"{self.strings['error']}: {str(e)}")

    async def _convert_to_png(self, input_path):
        """Конвертация в PNG"""
        output_path = input_path + ".png"
        
        try:
            image = Image.open(input_path)
            if image.mode in ("RGBA", "LA", "P"):
                image = image.convert("RGBA")
            else:
                image = image.convert("RGB")
            image.save(output_path, format='PNG')
            return output_path
        except Exception:
            try:
                (
                    ffmpeg
                    .input(input_path)
                    .output(output_path, vframes=1, vf="pad=ceil(iw/2)*2:ceil(ih/2)*2")
                    .run(overwrite_output=True, capture_stderr=True, quiet=True)
                )
                return output_path
            except ffmpeg.Error as e:
                raise Exception(f"Ошибка конвертации PNG: {e.stderr.decode()}")

    async def _convert_to_jpg(self, input_path):
        """Конвертация в JPEG"""
        output_path = input_path + ".jpg"
        
        try:
            image = Image.open(input_path)
            if image.mode in ("RGBA", "LA", "P"):
                background = Image.new("RGB", image.size, (255, 255, 255))
                if image.mode == "P":
                    image = image.convert("RGBA")
                if image.mode == "RGBA":
                    background.paste(image, mask=image.split()[-1])
                else:
                    background.paste(image)
                image = background
            else:
                image = image.convert("RGB")
            image.save(output_path, format='JPEG', quality=95)
            return output_path
        except Exception:
            try:
                (
                    ffmpeg
                    .input(input_path)
                    .output(output_path, vframes=1, vf="pad=ceil(iw/2)*2:ceil(ih/2)*2", qscale=2)
                    .run(overwrite_output=True, capture_stderr=True, quiet=True)
                )
                return output_path
            except ffmpeg.Error as e:
                raise Exception(f"Ошибка конвертации JPEG: {e.stderr.decode()}")

    async def _convert_to_webm(self, input_path):
        """Конвертация в WebM"""
        if input_path.endswith('.webm'):
            return input_path
        
        output_path = input_path + ".webm"
        
        try:
            (
                ffmpeg
                .input(input_path)
                .output(
                    output_path,
                    vcodec='libvpx-vp9',
                    vf="pad=ceil(iw/2)*2:ceil(ih/2)*2",
                    f='webm'
                )
                .run(overwrite_output=True, capture_stderr=True, quiet=True)
            )
            return output_path
        except ffmpeg.Error as e:
            error_msg = e.stderr.decode() if e.stderr else "Неизвестная ошибка ffmpeg"
            raise Exception(f"Ошибка конвертации WebM: {error_msg}")

    async def _convert_to_mp4(self, input_path):
        """Конвертация в MP4"""
        output_path = input_path + ".mp4"
        
        try:
            (
                ffmpeg
                .input(input_path)
                .output(
                    output_path,
                    vcodec='libx264',
                    vf="pad=ceil(iw/2)*2:ceil(ih/2)*2",
                    movflags='faststart',
                    pix_fmt='yuv420p',
                    f='mp4'
                )
                .run(overwrite_output=True, capture_stderr=True, quiet=True)
            )
            return output_path
        except ffmpeg.Error as e:
            error_msg = e.stderr.decode() if e.stderr else "Неизвестная ошибка ffmpeg"
            raise Exception(f"Ошибка конвертации MP4: {error_msg}")
