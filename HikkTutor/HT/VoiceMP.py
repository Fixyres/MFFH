__version__ = (1, 0, 5)

#            © Copyright 2024
#           https://t.me/HikkTutor 
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
#┏┓━┏┓━━┏┓━━┏┓━━┏━━━━┓━━━━━┏┓━━━━━━━━━━━━
#┃┃━┃┃━━┃┃━━┃┃━━┃┏┓┏┓┃━━━━┏┛┗┓━━━━━━━━━━━
#┃┗━┛┃┏┓┃┃┏┓┃┃┏┓┗┛┃┃┗┛┏┓┏┓┗┓┏┛┏━━┓┏━┓━━━━
#┃┏━┓┃┣┫┃┗┛┛┃┗┛┛━━┃┃━━┃┃┃┃━┃┃━┃┏┓┃┃┏┛━━━━
#┃┃━┃┃┃┃┃┏┓┓┃┏┓┓━┏┛┗┓━┃┗┛┃━┃┗┓┃┗┛┃┃┃━━━━━
#┗┛━┗┛┗┛┗┛┗┛┗┛┗┛━┗━━┛━┗━━┛━┗━┛┗━━┛┗┛━━━━━
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# load from: t.me:HikkTutor 
# meta developer:@HikkTutor 
# author: vsakoe
# name: VoiceMP

import os
import json
from pydub import AudioSegment
from telethon.tl.types import Message, DocumentAttributeVideo, DocumentAttributeSticker
from .. import loader, utils
from ..inline.types import InlineCall

class VoiceMP(loader.Module):
    """Конвертер Медиафайлов"""

    strings = {"name": "VoiceMP"}

    def __init__(self):
        self.records_dir = os.path.join(os.path.expanduser("~"), "voice_records")
        self.records_file = os.path.join(self.records_dir, "records.json")
        self.saved_records = self.load_saved_records()

        if not os.path.exists(self.records_dir):
            os.makedirs(self.records_dir)

    def load_saved_records(self):
        """Загружает сохраненные записи из файла"""
        if os.path.exists(self.records_file):
            with open(self.records_file, "r") as f:
                return json.load(f)
        return {}

    def save_records(self):
        """Сохраняет записи в файл"""
        with open(self.records_file, "w") as f:
            json.dump(self.saved_records, f)

    def get_audio_duration(self, file_path):
        """Возвращает длительность аудио в секундах"""
        audio = AudioSegment.from_file(file_path)
        return int(audio.duration_seconds)

    def is_unsupported(self, message):
        """Проверяет, является ли файл неподдерживаемым (не голосовое, не MP3 и не обычное видео)"""
        if message.gif or message.sticker:
            return True
        if message.video:
            for attr in message.video.attributes:
                if isinstance(attr, DocumentAttributeVideo) and attr.round_message:
                    return True
        if not (message.voice or 
                (message.file and message.file.name and message.file.name.endswith('.mp3')) or 
                message.video):
            return True
        return False

    async def convert_to_mp3(self, message: Message):
        """Конвертирует голосовое сообщение в MP3"""
        status_msg = await message.respond("Конвертирую в MP3...")
        file_path = await self.client.download_media(message.media)
        audio = AudioSegment.from_file(file_path)

        if self.get_audio_duration(file_path) > 180:
            await status_msg.edit("⚠️ Длительность превышает 3 минуты.")
            os.remove(file_path)
            return

        mp3_path = file_path.replace('.ogg', '.mp3')
        audio.export(mp3_path, format="mp3")
        os.remove(file_path)

        await status_msg.edit("Отправляю MP3 файл...")
        await message.respond(file=mp3_path)
        os.remove(mp3_path)

    async def convert_to_voice(self, message: Message):
        """Конвертирует MP3 в голосовое сообщение"""
        status_msg = await message.respond("Конвертирую в голосовое...")
        file_path = await self.client.download_media(message.media)
        audio = AudioSegment.from_file(file_path)

        if self.get_audio_duration(file_path) > 180:
            await status_msg.edit("⚠️ Длительность превышает 3 минуты.")
            os.remove(file_path)
            return

        voice_path = file_path.replace('.mp3', '.ogg')
        audio.export(voice_path, format="ogg", codec="libopus")
        os.remove(file_path)

        await status_msg.edit("Отправляю голосовое сообщение...")
        await message.respond(file=voice_path)
        os.remove(voice_path)

    async def convert_video(self, call: InlineCall, message: Message, to_format: str):
        """Конвертирует видео в выбранный формат"""
        if not message or not message.video:
            await call.edit("⚠️ Ошибка: не удалось найти видео для конвертации.")
            return

        try:
            await call.edit(f"Конвертирую в {to_format}...")
            file_path = await self.client.download_media(message.media)

            if self.get_audio_duration(file_path) > 180:
                await call.edit("⚠️ Длительность видео превышает 3 минуты.")
                os.remove(file_path)
                return

            audio = AudioSegment.from_file(file_path)
            output_path = (file_path.replace('.mp4', '.mp3') if to_format == "музыку" 
                           else file_path.replace('.mp4', '.ogg'))
            audio.export(output_path, format="mp3" if to_format == "музыку" else "ogg", codec="libopus" if to_format != "музыку" else None)

            os.remove(file_path)
            await message.respond(file=output_path)
            os.remove(output_path)

        except Exception as e:
            await call.edit(f"⚠️ Произошла ошибка: {str(e)}")

    @loader.command()
    async def savev(self, message: Message):
        """Сохранить запись: <название>"""
        args = utils.get_args_raw(message)
        if not args or len(args) > 30:
            await message.respond("❗ Укажите название не длиннее 30 символов.")
            return

        reply = await message.get_reply_message()
        if not reply or not (reply.voice or (reply.file and reply.file.name and reply.file.name.endswith('.mp3'))):
            await message.respond("⚠️ Ответьте на голосовое или MP3.")
            return

        status_msg = await message.respond("Сохраняю...")
        file_path = await self.client.download_media(reply.media)

        if self.get_audio_duration(file_path) > 180:
            await status_msg.edit("⚠️ Длительность превышает 3 минуты.")
            os.remove(file_path)
            return

        save_path = os.path.join(self.records_dir, f"{args}.ogg" if reply.voice else f"{args}.mp3")
        os.rename(file_path, save_path)

        self.saved_records[args] = save_path
        self.save_records()
        await status_msg.edit(f"✅ Запись '{args}' сохранена!")

    @loader.command()
    async def getv(self, message: Message):
        """Получить запись: <название> или список"""
        args = utils.get_args_raw(message)
        if not args:
            if not self.saved_records:
                await message.respond("📭 Нет сохраненных записей.")
                return

            saved_list = ""
            for name, path in self.saved_records.items():
                duration = self.get_audio_duration(path)
                emoji = "🎙️" if path.endswith('.ogg') else "🎵"
                saved_list += f"{emoji} <code>{name}</code> - {duration//60}:{duration%60:02}\n"

            await message.respond(f"📜 Сохраненные записи:\n{saved_list}")
            return

        if args not in self.saved_records:
            await message.respond(f"❌ Запись '{args}' не найдена.")
            return

        await message.respond(file=self.saved_records[args])

    @loader.command()
    async def delv(self, message: Message):
        """Удалить запись: <название> или все"""
        args = utils.get_args_raw(message)

        if not args:
            if len(self.saved_records) == 1:
                name = next(iter(self.saved_records))
                await self.inline.form(
                    f"❓ Удалить запись '{name}'?",
                    message,
                    [
                        {"text": "Да", "callback": self.confirm_delete, "args": (name,)},
                        {"text": "Нет", "callback": self.cancel_delete}
                    ]
                )
            else:
                await self.inline.form(
                    "❓ Удалить все записи?",
                    message,
                    [
                        {"text": "Да", "callback": self.confirm_delete},
                        {"text": "Нет", "callback": self.cancel_delete}
                    ]
                )
        elif args in self.saved_records:
            await self.inline.form(
                f"❓ Удалить запись '{args}'?",
                message,
                [
                    {"text": "Да", "callback": self.confirm_delete, "args": (args,)},
                    {"text": "Нет", "callback": self.cancel_delete}
                ]
            )
        else:
            await message.respond(f"❌ Запись '{args}' не найдена.")

    async def confirm_delete(self, call: InlineCall, name=None):
        """Обрабатывает подтверждение удаления"""
        if name:
            path = self.saved_records.get(name)
            if path and os.path.exists(path):
                os.remove(path)
            self.saved_records.pop(name, None)
            await call.edit(f"🗑️ Запись '{name}' удалена.")
        else:
            for path in self.saved_records.values():
                if os.path.exists(path):
                    os.remove(path)
            self.saved_records.clear()
            await call.edit("🗑️ Все записи удалены.")

        self.save_records()

    async def cancel_delete(self, call: InlineCall):
        """Отмена удаления"""
        await call.edit("❌ Удаление отменено.")

    @loader.command()
    async def conv(self, message: Message):
        """Конвертировать медиафайл"""
        if message.is_reply:
            reply = await message.get_reply_message()
            if self.is_unsupported(reply):
                await message.respond("⚠️ Неподдерживаемый тип файла. Поддерживаются только голосовые сообщения, MP3 и видео.")
                return
            if reply.voice:
                await self.convert_to_mp3(reply)
            elif reply.file and reply.file.name and reply.file.name.endswith('.mp3'):
                await self.convert_to_voice(reply)
            elif reply.video:
                await self.inline.form(
                    "❓ Конвертировать видео в:",
                    message,
                    [
                        {"text": "Музыку", "callback": self.convert_video, "args": (reply, "музыку")},
                        {"text": "Голосовое", "callback": self.convert_video, "args": (reply, "голосовое")}
                    ]
                )
            else:
                await message.respond("⚠️ Неподдерживаемый тип файла. Поддерживаются только голосовые сообщения, MP3 и видео.")
        else:
            await message.respond("⚠️ Ответьте на медиафайл.")
