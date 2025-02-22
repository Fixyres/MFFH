# meta developer: @kotcheat

from .. import loader, utils
from telethon import events
import speech_recognition as sr
from pydub import AudioSegment
import io

@loader.tds
class KOTvoicetotextMod(loader.Module):
    """Модуль преобразования голосовых сообщений в текст (by @kotcheat)"""
    strings = {"name": "KOTvoicetotext"}

    async def client_ready(self, client, db):
        self.client = client

    @loader.command(ru_doc="<reply> to voice")
    async def texcmd(self, message):
        """Преобразовать голосовое сообщение в текст"""
        if not message.is_reply:
            await utils.answer(message, "<b>Ответить на голосовое сообщение!</b>")
            return

        reply_message = await message.get_reply_message()
        if not reply_message or not reply_message.voice:
            await utils.answer(message, "<b>Ответить на голосовое сообщение!</b>")
            return

        voice_message = await reply_message.download_media()

        # Convert OGG/Opus to WAV
        audio = AudioSegment.from_file(voice_message)
        wav_io = io.BytesIO()
        audio.export(wav_io, format="wav")
        wav_io.seek(0)

        recognizer = sr.Recognizer()

        with sr.AudioFile(wav_io) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data, language="ru-RU")
                await message.edit(f"<b>Итог:</b> {text}")
            except sr.UnknownValueError:
                await message.edit("<b>Не удалось понять звук.</b>")
            except sr.RequestError as e:
                await message.edit(f"<b>Не удалось запросить результаты; {e}</b>")