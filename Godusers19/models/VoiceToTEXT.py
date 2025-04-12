# meta developer: @Goduser18
from hikkatl.types import Message
from .. import loader, utils
import speech_recognition as sr
import os
import tempfile
import asyncio
from pydub import AudioSegment

@loader.tds
class VoiceToTextMod(loader.Module):
    strings = {
        "name": "VoiceToText",
        "processing": "🎤 <b>Обрабатываю голосовое сообщение...</b>",
        "result": "📝 <b>Текст из голосового:</b>\n<code>{}</code>",
        "error": "❌ <b>Ошибка:</b> {}",
        "help": "ℹ️ <b>Как использовать:</b>\nОтветьте на голосовое сообщение командой <code>.vgo</code>",
        "not_voice": "⚠️ Это не голосовое сообщение!"
    }

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "language",
                "ru-RU",
                "Язык распознавания",
                validator=loader.validators.Choice(["ru-RU", "en-US", "uk-UA"])
            ),
            loader.ConfigValue(
                "auto_delete",
                True,
                "Автоудаление исходного голосового",
                validator=loader.validators.Boolean()
            )
        )

    async def client_ready(self, client, db):
        self._client = client

    @loader.command()
    async def vgo(self, message: Message):
        reply = await message.get_reply_message()
        if not reply or not reply.voice:
            await utils.answer(message, self.strings["not_voice"])
            return

        await utils.answer(message, self.strings["processing"])

        try:
            voice_file = await reply.download_media(bytes)
            
            with tempfile.NamedTemporaryFile(suffix='.ogg', delete=False) as tmp_ogg:
                tmp_ogg.write(voice_file)
                tmp_ogg_path = tmp_ogg.name
            
            wav_path = await self._convert_to_wav(tmp_ogg_path)
            text = await self._recognize_speech(wav_path)
            
            await utils.answer(
                message,
                self.strings["result"].format(utils.escape_html(text))
            )
            
            if self.config["auto_delete"]:
                await reply.delete()
            
        except Exception as e:
            await utils.answer(message, self.strings["error"].format(str(e)))
        finally:
            if 'tmp_ogg_path' in locals() and os.path.exists(tmp_ogg_path):
                os.unlink(tmp_ogg_path)
            if 'wav_path' in locals() and os.path.exists(wav_path):
                os.unlink(wav_path)

    async def _convert_to_wav(self, ogg_path: str) -> str:
        sound = AudioSegment.from_ogg(ogg_path)
        wav_path = ogg_path.replace('.ogg', '.wav')
        sound.export(wav_path, format="wav")
        return wav_path

    async def _recognize_speech(self, wav_path: str) -> str:
        with sr.AudioFile(wav_path) as source:
            audio = self.recognizer.record(source)
            
        return self.recognizer.recognize_google(
            audio,
            language=self.config["language"]
        )

    async def watcher(self, message: Message):
        if "vgo" in message.text.lower() and message.is_reply:
            await self.vgo(message)
