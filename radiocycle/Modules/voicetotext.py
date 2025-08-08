# meta developer: bio.kezuhiro.fun

from .. import loader, utils
import os
import speech_recognition as sr
from pydub import AudioSegment

@loader.tds
class VoiceToTextMod(loader.Module):
    strings = {
        "name": "VoiceToText",
        "process_text": "<emoji document_id=4911241630633165627>✨</emoji> <b>Recognizing the message text...</b>",
        "vtt_success": "<emoji document_id=5116110535565247270>🔥</emoji> <b>Recognized text:</b>\n<blockquote expandable>{}</blockquote>",
        "vtt_failure": "<emoji document_id=5116151848855667552>🚫</emoji> <b>Failed to recognize the message.</b>",
        "vtt_request_error": "<emoji document_id=5116151848855667552>🚫</emoji> <b>Error when contacting the recognition service:</b>\n<code>{}</code>",
        "vtt_invalid": "<emoji document_id=5116151848855667552>🚫</emoji> <b>Please reply to a voice or video message with the command</b> <code>{self.get_prefix}vtt</code>",
        "vtt_successful": "<emoji document_id=4916036072560919511>✅</emoji> <b>Text recognized successfully</b>",
    }

    strings_ru = {
        "process_text": "<emoji document_id=4911241630633165627>✨</emoji> <b>Распознаю текст сообщения...</b>",
        "vtt_success": "<emoji document_id=5116110535565247270>🔥</emoji> <b>Распознанный текст:</b>\n<blockquote expandable>{}</blockquote>",
        "vtt_failure": "<emoji document_id=5116151848855667552>🚫</emoji> <b>Не удалось распознать сообщение.</b>",
        "vtt_request_error": "<emoji document_id=5116151848855667552>🚫</emoji> <b>Ошибка при обращении к сервису распознавания:</b>\n<code>{}</code>",
        "vtt_invalid": "<emoji document_id=5116151848855667552>🚫</emoji> <b>Пожалуйста, ответьте на голосовое или видеосообщение командой</b> <code>.vtt</code>",
        "vtt_successful": "<emoji document_id=4916036072560919511>✅</emoji> <b>Текст успешно распознан</b>",
    }

    @loader.command(
        ru_doc="- распознает текст из голосового или видеосообщения.",
    )
    async def vttcmd(self, message):
        """- recognizes text from voice or video messages."""
        await self._vtt_process(message)

    async def _vtt_process(self, message):
        """processing voice/video messages to text"""
        reply = await message.get_reply_message()

        if not reply or not (reply.voice or reply.video_note):
            await message.respond(self.strings["vtt_invalid"])
            return

        waiting_message = await utils.answer(
            message, self.strings["process_text"], reply_to=message.id
        )

        media_file = await reply.download_media()
        wav_file = media_file.replace('.mp4', '.wav') if reply.video_note else media_file.replace('.oga', '.wav')

        try:
            AudioSegment.from_file(media_file).export(wav_file, format='wav')
            recognizer = sr.Recognizer()
            with sr.AudioFile(wav_file) as source:
                audio_data = recognizer.record(source)
                try:
                    text = recognizer.recognize_google(audio_data, language='ru-RU')
                    await reply.reply(self.strings["vtt_success"].format(text))
                    await waiting_message.edit(self.strings["vtt_successful"])
                except sr.UnknownValueError:
                    await waiting_message.delete()
                    await reply.reply(self.strings["vtt_failure"])
                except sr.RequestError as e:
                    await waiting_message.delete()
                    await reply.reply(self.strings["vtt_request_error"].format(e))
        finally:
            os.remove(media_file)
            os.remove(wav_file)