# ©️ qq_shark, 2025
# 🌐 https://github.com/qqshark/Modules/blob/main/media2gif.py
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

import os
import subprocess
from .. import loader, utils
from PIL import Image

@loader.tds
class media2gifMod(loader.Module):
    """Конвертор фото/видео в гиф (by @qq_shark)."""

    strings = {
        "name": "media2gif",
        "conversion_error": "❌ Ошибка при преобразовании в GIF.",
        "not_media": "⚠️ Ответьте на фото или видео!",
        "stage_downloading": "⏬ Загружаю файл...",
        "stage_converting": "🔄 Конвертирую...",
        "stage_sending": "📤 Отправляю...",
        "stage_cleanup": "🧹 Завершаю...",
    }

    strings_ru = {
        "conversion_error": "❌ Ошибка при преобразовании в GIF.",
        "not_media": "⚠️ Ответьте на фото или видео!",
        "stage_downloading": "⏬ Загружаю файл...",
        "stage_converting": "🔄 Конвертирую...",
        "stage_sending": "📤 Отправляю...",
        "stage_cleanup": "🧹 Завершаю...",
    }

    @loader.command(
        ru_doc="[ответ на фото или видео] — превращает фото или видео в GIF.",
        en_doc="[reply to photo or video] — converts photo or video to GIF.",
    )
    async def media2gif(self, message):
        reply = await message.get_reply_message()
        if not reply or not (reply.photo or reply.video):
            await utils.answer(message, self.strings("not_media", message))
            return

        status_msg = await utils.answer(message, "⏳ Начинаю...")

        # Фото в гиф
        if reply.photo:
            status_msg = await status_msg.edit(self.strings("stage_downloading", message))
            photo_path = await reply.download_media("pic2gif_in.jpg")
            gif_path = "pic2gif_out.gif"
            try:
                status_msg = await status_msg.edit(self.strings("stage_converting", message))
                img = Image.open(photo_path).convert("RGB")
                img.save(
                    gif_path,
                    save_all=True,
                    append_images=[],
                    duration=100,  # 0.1 сек
                    loop=0,
                    format="GIF"
                )
                status_msg = await status_msg.edit(self.strings("stage_sending", message))
                await message.client.send_file(
                    message.chat_id,
                    gif_path,
                    reply_to=reply.id,
                )
            except Exception as e:
                await status_msg.edit(self.strings("conversion_error", message))
                print(f"Error during photo2gif: {e}")
            finally:
                status_msg = await status_msg.edit(self.strings("stage_cleanup", message))
                self.cleanup_temp_files(photo_path, gif_path)
                await status_msg.delete()
                await message.delete()
            return

        # Видео в гиф
        if reply.video:
            status_msg = await status_msg.edit(self.strings("stage_downloading", message))
            video_path = await reply.download_media("pic2gif_in.mp4")
            gif_path = "pic2gif_out.gif"
            try:
                status_msg = await status_msg.edit(self.strings("stage_converting", message))
                self.convert_video_to_gif(video_path, gif_path)
                status_msg = await status_msg.edit(self.strings("stage_sending", message))
                await message.client.send_file(
                    message.chat_id,
                    gif_path,
                    reply_to=reply.id,
                )
            except Exception as e:
                await status_msg.edit(self.strings("conversion_error", message))
                print(f"Error during video2gif: {e}")
            finally:
                status_msg = await status_msg.edit(self.strings("stage_cleanup", message))
                self.cleanup_temp_files(video_path, gif_path)
                await status_msg.delete()
                await message.delete()
            return

    def convert_video_to_gif(self, video_path: str, gif_path: str) -> None:
        """Конвертирует видео в GIF с оптимальными параметрами."""
        command = [
            "ffmpeg",
            "-y",
            "-i",
            video_path,
            "-vf",
            "fps=30,scale=640:-1:flags=lanczos",
            "-c:v",
            "gif",
            gif_path,
        ]
        subprocess.run(command, check=True)

    def cleanup_temp_files(self, *files):
        """Удаляет временные файлы."""
        for f in files:
            if f and os.path.exists(f):
                try:
                    os.remove(f)
                except Exception:
                    pass
