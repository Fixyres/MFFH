# meta developer: @kotcheat

from .. import loader, utils
import speech_recognition as sr
from pydub import AudioSegment
import io
import os
import asyncio
import concurrent.futures

@loader.tds
class KOTvoicetotextMod(loader.Module):
    """Модуль преобразования голосовых и видео сообщений в текст (by @kotcheat)"""
    
    strings = {"name": "KOTvoicetotext"}
    
    def __init__(self):
        self.processing_messages = {}
    
    async def client_ready(self, client, db):
        self.client = client
    
    def _process_audio(self, audio_file_path):
        """Блокирующая функция для обработки аудио"""
        try:
            
            audio = AudioSegment.from_file(audio_file_path)
            wav_io = io.BytesIO()
            audio.export(wav_io, format="wav")
            wav_io.seek(0)
            
            
            if os.path.exists(audio_file_path):
                os.remove(audio_file_path)
            
            
            recognizer = sr.Recognizer()
            with sr.AudioFile(wav_io) as source:
                audio_data = recognizer.record(source)
                
            text = recognizer.recognize_google(audio_data, language="ru-RU")
            return {"success": True, "text": text}
            
        except sr.UnknownValueError:
            return {"success": False, "error": "<emoji document_id=5800887979366944343>#⃣</emoji> Не удалось распознать речь."}
        except sr.RequestError as e:
            return {"success": False, "error": f"<emoji document_id=5800887979366944343>#⃣</emoji> Ошибка запроса к сервису распознавания: {e}"}
        except Exception as e:
            return {"success": False, "error": f"<emoji document_id=5800887979366944343>#⃣</emoji> Произошла ошибка при обработке: {e}"}
    
    @loader.command(ru_doc="Преобразовать голосовое/видео сообщение в текст")
    async def texcmd(self, message):
        """Преобразовать голосовое или видео сообщение в текст"""
        if not message.is_reply:
            await utils.answer(message, "<emoji document_id=6037630738545774536>❓</emoji> Ответьте на голосовое или видео сообщение!")
            return
        
        reply_message = await message.get_reply_message()
        if not reply_message or (not reply_message.voice and not reply_message.video_note and not reply_message.video):
            await utils.answer(message, "<emoji document_id=6037630738545774536>❓</emoji> Ответьте на голосовое или видео сообщение!")
            return
        
        
        msg_id = reply_message.id
        if msg_id in self.processing_messages:
            await utils.answer(message, "<emoji document_id=5325787248363314644>🫥</emoji> Это сообщение уже обрабатывается...")
            return
        
        
        media_type = "голосовое сообщение"
        if reply_message.video_note:
            media_type = "видеосообщение"
        elif reply_message.video:
            media_type = "видео"
        
        
        self.processing_messages[msg_id] = True
        
        
        processing_msg = await utils.answer(message, f"<emoji document_id=5325787248363314644>🫥</emoji> Подождите немного...")
        
        try:
            
            media_file = await reply_message.download_media()
            
            
            loop = asyncio.get_event_loop()
            with concurrent.futures.ThreadPoolExecutor() as executor:
                result = await loop.run_in_executor(executor, self._process_audio, media_file)
            
            
            if result["success"]:
                await utils.answer(processing_msg, f"<emoji document_id=5316899638177964496>☁️</emoji>: {result['text']}")
            else:
                await utils.answer(processing_msg, f"<emoji document_id=5800887979366944343>#⃣</emoji> Не удалось распознать речь.")
                
        except Exception as e:
            await utils.answer(processing_msg, f"<emoji document_id=5800887979366944343>#⃣</emoji> Произошла ошибка: {e}")
            
        finally:
            
            if msg_id in self.processing_messages:
                del self.processing_messages[msg_id]
