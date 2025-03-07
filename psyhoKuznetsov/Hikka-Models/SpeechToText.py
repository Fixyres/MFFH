__version__ = (1, 1, 0)
# meta developer: @psyho_Kuznetsov

from .. import loader, utils
import asyncio
import logging
import os
import tempfile
import speech_recognition as sr
import subprocess

logger = logging.getLogger(__name__)

@loader.tds
class SpeechToText(loader.Module):
    """Speech to text conversion via Google Speech Recognition (supports multiple languages)"""

    strings = {
        "name": "SpeechToText",
        "processing": "🔮 <b>Processing...</b>",
        "no_reply": "🚫 <b>Reply to a voice or video message!</b>",
        "result": "📜 <b>Result:</b>\n\n{}",
        "error": "❌ <b>Error processing the message.</b>",
        "downloading": "⏳ <b>Downloading file...</b>",
        "converting": "🔄 <b>Converting audio...</b>",
        "recognizing": "🎯 <b>Recognizing speech...</b>"
    }
    
    strings_ru = {
        "name": "SpeechToText",
        "processing": "🔮 <b>Обработка...</b>",
        "no_reply": "🚫 <b>Ответьте на голосовое или видеосообщение!</b>",
        "result": "📜 <b>Результат:</b>\n\n{}",
        "error": "❌ <b>Ошибка при обработке сообщения.</b>",
        "downloading": "⏳ <b>Скачивание файла...</b>",
        "converting": "🔄 <b>Конвертация аудио...</b>",
        "recognizing": "🎯 <b>Распознавание речи...</b>"
    }
    
    def __init__(self):
        self.name = self.strings["name"]
        self.recognizer = sr.Recognizer()
        self.config = loader.ModuleConfig(
            "language", "ru-RU", "Default language for speech recognition"
        )
    
    async def convert_to_wav(self, input_file, output_file):
        try:
            cmd = [
                'ffmpeg', '-y', '-i', input_file, 
                '-acodec', 'pcm_s16le', '-ac', '1', '-ar', '16000', 
                output_file
            ]
            process = await asyncio.create_subprocess_exec(
                *cmd, 
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await process.communicate()
            return True
        except Exception as e:
            logger.error(f"Audio conversion error: {e}", exc_info=True)
            return False
    
    async def recognize_audio(self, file_path, language):
        try:
            return await asyncio.to_thread(self._perform_recognition, file_path, language)
        except Exception as e:
            logger.error(f"Recognition error: {e}", exc_info=True)
            return None
    
    def _perform_recognition(self, file_path, language):
        with sr.AudioFile(file_path) as source:
            audio_data = self.recognizer.record(source)
            return self.recognizer.recognize_google(audio_data, language=language)

    @loader.command()
    async def atxt(self, message):
        """Usage: Reply to a voice message with .atxt [language code]"""
        args = utils.get_args_raw(message)
        language = args.strip() if args else self.config["language"]
        
        reply = await message.get_reply_message()
        
        if not reply or not reply.media:
            return await utils.answer(message, self.strings["no_reply"])
            
        msg = await utils.answer(message, self.strings["processing"])
        
        temp_original = tempfile.NamedTemporaryFile(suffix=".ogg", delete=False).name
        temp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
        
        try:
            await utils.answer(msg, self.strings["downloading"])
            await reply.download_media(temp_original)
            
            await utils.answer(msg, self.strings["converting"])
            if not await self.convert_to_wav(temp_original, temp_wav):
                return await utils.answer(msg, self.strings["error"])
            
            await utils.answer(msg, self.strings["recognizing"])
            text = await self.recognize_audio(temp_wav, language)
            
            if text:
                await utils.answer(msg, self.strings["result"].format(text))
            else:
                await utils.answer(msg, self.strings["error"])
                
        except Exception as e:
            logger.error(f"Error in atxt: {e}", exc_info=True)
            await utils.answer(msg, self.strings["error"])
        finally:
            for temp_file in [temp_original, temp_wav]:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
    
    @loader.command()
    async def stxtcfg(self, message):
        """Configure default language: .stxtcfg [language code]"""
        args = utils.get_args_raw(message)
        if not args:
            return await utils.answer(
                message, f"Current default language: <code>{self.config['language']}</code>\n"
                "To change, use: <code>.stxtcfg [language code]</code>\n"
                "Example language codes: en-US, ru-RU, fr-FR, de-DE, zh-CN, ja-JP, es-ES"
            )
        
        self.config["language"] = args.strip()
        await utils.answer(
            message, f"Default language set to: <code>{self.config['language']}</code>"
      )
