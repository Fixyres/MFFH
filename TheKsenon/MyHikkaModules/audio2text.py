# ------------------------------------------------------------
# Module: Audio2Text
# Description: Module for speech-to-text conversion.
# Author: @kmodules
# ------------------------------------------------------------
# Licensed under the GNU AGPLv3
# https:/www.gnu.org/licenses/agpl-3.0.html
# ------------------------------------------------------------
# Author: @MeKsenon
# Commands: .audio2text
# scope: hikka_only
# meta banner: https://i.ibb.co/7k4sJRR/5ad271ae-ec1b-4803-a714-5d6628ee8f50.jpg
# meta developer: @kmodules
# ------------------------------------------------------------

from .. import loader, utils
import requests
import asyncio

__version__ = (1, 0, 1)

@loader.tds
class Audio2TextMod(loader.Module):
    """Module for speech-to-text conversion"""

    strings = {
        "name": "Audio2Text",
        "processing": "<emoji document_id=5332600281970517875>🫥</emoji> <b>Converting audio to text...</b>",
        "success": "<emoji document_id=5897554554894946515>🎤</emoji> <b>Text recognized!</b>\n\n<emoji document_id=6048354593279053992>🗣</emoji> <code>{}</code>",
        "no_reply": "Reply to a voice message!",
        "error": "An error occurred!"
    }

    strings_ru = {
        "name": "Audio2Text",
        "processing": "<emoji document_id=5332600281970517875>🫥</emoji> <b>Распознаю текст из аудио...</b>",
        "success": "<emoji document_id=5897554554894946515>🎤</emoji> <b>Текст распознан!</b>\n\n<emoji document_id=6048354593279053992>🗣</emoji> <code>{}</code>",
        "no_reply": "Ответьте на аудиосообщение!",
        "error": "Произошла ошибка!"
    }

    async def client_ready(self, client, db):
        self.client = client

    @loader.command(ru_doc="Преобразовать аудио в текст (ответом на аудиосообщение)",
                   en_doc="Convert audio to text (reply to voice message)")
    async def audio2text(self, message):
        reply = await message.get_reply_message()
        if not reply or not reply.media:
            await utils.answer(message, self.strings["no_reply"])
            return

        await utils.answer(message, self.strings["processing"])

        try:
            audio_data = await reply.download_media(bytes)
            
            files = {'audio': ('audio.mp3', audio_data, 'audio/mp3')}
            response = requests.post(
                "http://theksenon.pro/api/audio2text/generate",
                files=files
            )

            if response.status_code == 200:
                result = response.json()
                if 'text' in result:
                    await utils.answer(
                        message,
                        self.strings["success"].format(result['text'])
                    )
                else:
                    await utils.answer(message, self.strings["error"])
            else:
                await utils.answer(message, self.strings["error"])
                
        except Exception as e:
            await utils.answer(message, f"{self.strings['error']}: {str(e)}")
