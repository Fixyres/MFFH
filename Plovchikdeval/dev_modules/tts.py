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
