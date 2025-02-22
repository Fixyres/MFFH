"""
888    d8P   .d8888b.  888    888     888b     d888  .d88888b.  8888888b.   .d8888b.  
888   d8P   d88P  Y88b 888    888     8888b   d8888 d88P" "Y88b 888  "Y88b d88P  Y88b 
888  d8P    Y88b.      888    888     88888b.d88888 888     888 888    888 Y88b.      
888d88K      "Y888b.   8888888888 d8b 888Y88888P888 888     888 888    888  "Y888b.   
8888888b        "Y88b. 888    888 Y8P 888 Y888P 888 888     888 888    888     "Y88b. 
888  Y88b         "888 888    888     888  Y8P  888 888     888 888    888       "888 
888   Y88b  Y88b  d88P 888    888 d8b 888   "   888 Y88b. .d88P 888  .d88P Y88b  d88P 
888    Y88b  "Y8888P"  888    888 Y8P 888       888  "Y88888P"  8888888P"   "Y8888P"
                                                                     
(C) 2025 t.me/kshmods
Licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
"""

# meta developer: @kshmods

from telethon.tl.types import Message
from PIL import Image
import os
import subprocess
from .. import loader, utils

@loader.tds
class P2G(loader.Module):
    """Модуль для преобразования изображения в GIF"""
    strings = {
        "name": "ImageToGif",
        "processing": "📤 Image Processing...",
        "no_image": "❌ No image found!",
        "gif_ready": "✅ GIF is ready!"
    }

    strings_ru = { 
        "name": "ImageToGif",
        "processing": "📤 Обработка изображения...",
        "no_image": "❌ Изображение не найдено!",
        "gif_ready": "✅ GIF готов!"
    }

    @loader.command(
        doc_ru = "Создает GIF из изображения. Использование: .gif (ответ на изображение)"
    )
    async def p2g(self, message: Message):
        """Creates a GIF from an image. Usage: .gif (response to the image)"""
        reply = await message.get_reply_message()
        if not reply or not reply.media:
            await utils.answer(message, self.strings("no_image", message))
            return

        await utils.answer(message, self.strings["processing"])

        file = await reply.download_media()
        if not file or not file.endswith((".jpg", ".jpeg", ".png")):
            await utils.answer(message, self.strings("no_image", message))
            return
        
        try:
            img = Image.open(file)
            if img.format.lower() == "webp":
                file = file.rsplit(".", 1)[0] + ".png"
                img.save(file, format="PNG")
        except Exception:
            await utils.answer(message, self.strings["no_image"])
            return

        mp4_path = file.rsplit(".", 1)[0] + ".mp4"
        try:
            img = Image.open(file)
            frames = [img.copy() for _ in range(10)]
            temp_dir = "temp_frames"
            os.makedirs(temp_dir, exist_ok=True)
            frame_files = []

            for i, frame in enumerate(frames):
                frame_file = os.path.join(temp_dir, f"frame_{i:03d}.png")
                frame.save(frame_file)
                frame_files.append(frame_file)

            ffmpeg_command = [
                "ffmpeg",
                "-y",
                "-framerate", "10",
                "-i", os.path.join(temp_dir, "frame_%03d.png"),
                "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                mp4_path
            ]

            subprocess.run(ffmpeg_command, check=True)

            async with message.client.action(message.chat_id, "document"):
                await message.client.send_file(
                    message.chat_id, mp4_path, reply_to=reply.id
                )

            await message.delete()
        finally:
            if os.path.exists(file):
                os.remove(file)
            if mp4_path and os.path.exists(mp4_path):
                os.remove(mp4_path)
            for frame_file in frame_files:
                if os.path.exists(frame_file):
                    os.remove(frame_file)
