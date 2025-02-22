# meta developer: @xdesai

import os
from langdetect import detect
import edge_tts
from .. import loader, utils

@loader.tds
class TextToSpeechMod(loader.Module):
    """Text to Speech Module"""
    strings = {"name": "TextToSpeech"}

    @loader.owner
    async def speakcmd(self, event):
        """Текст в речь. Использование: .speak <текст>"""
        await event.delete()
        if len(event.text.split(" ", maxsplit=1)) > 1:
            text = event.text.split(" ", maxsplit=1)[1]
        else:
            await utils.answer(event, "❌ Пожалуйста, укажите текст для генерации.")
            return
        try:
            lang = detect(text)
            voice = "en-US-GuyNeural" if lang == 'en' else "ru-RU-DmitryNeural"
        except Exception as e:
            await utils.answer(event, "Не удалось определить язык текста.")
            return
        communicate = edge_tts.Communicate(text, voice=voice)
        await communicate.save("voice.mp3")
        if event.reply_to_msg_id:
            await event.client.send_file(event.chat_id, "voice.mp3", voice_note=True, reply_to=event.reply_to_msg_id)
        else:
            await event.client.send_file(event.chat_id, "voice.mp3", voice_note=True, reply_to=event.reply_to_msg_id)
        os.remove("voice.mp3")
