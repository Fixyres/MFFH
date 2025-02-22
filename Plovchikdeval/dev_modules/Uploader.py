__version__ = (1, 1, 3)

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
# scope: hikka_only
# scope: hikka_min 1.3.3
# meta developer: @kshmods
# meta banner: https://kappa.lol/--YNb
# requires: requests

import logging
import io
import os
import random
import json
import requests

from telethon.tl.types import Message

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class UploaderMod(loader.Module):
    """Загрузка на зеркало 0x.at"""

    strings = {
        "name": "Uploader",
        "uploading": "<emoji document_id=5872756762347573066>⏲</emoji> <b>Uploading...</b>",
        "noargs": "<emoji document_id=5208434048753484584>⛔</emoji> <b>No file specified</b>",
        "err": "<emoji document_id=5208434048753484584>⛔</emoji> <b>Upload error</b>",
        "uploaded": "<emoji document_id=5208547229731669225>⚡</emoji> <b>File uploaded!</b>\n\n<code>{link_to_file}</code>",
    }

    strings_ua = {
        "uploading": "<emoji document_id=5872756762347573066>⏲</emoji><b>Завантаження...</b>",
        "noargs": "<emoji document_id=5208434048753484584>⛔</emoji> <b>Файл не вказано</b>",
        "err": "<emoji document_id=5208434048753484584>⛔</emoji> <b>Помилка завантаження</b>",
        "uploaded": "<emoji document_id=5208547229731669225>⚡</emoji> <b>Файл завантажено!</b>\n\n<code>{link_to_file}</code>",
    }

    strings_ru = {
        "uploading": "<emoji document_id=5872756762347573066>⏲</emoji> <b>Загрузка...</b>",
        "noargs": "<emoji document_id=5208434048753484584>⛔</emoji> <b>Файл не указан</b>",
        "err": "<emoji document_id=5208434048753484584>⛔</emoji> <b>Ошибка загрузки</b>",
        "uploaded": "<emoji document_id=5208547229731669225>⚡</emoji> <b>Файл загружен!</b>\n\n<code>{link_to_file}</code>",
    }

    async def client_ready(self, client, _):
        self._client = client
        
    async def get_media(self, message: Message):
        reply = await message.get_reply_message()
        m = None
        if reply and reply.media:
            m = reply
        elif message.media:
            m = message
        elif not reply:
            await utils.answer(message, self.strings("noargs"))
            return False

        if not m:
            file = io.BytesIO(bytes(reply.raw_text, "utf-8"))
            file.name = "file.txt"
        else:
            file = io.BytesIO(await self._client.download_media(m, bytes))
            file.name = (
                m.file.name
                or (
                    "".join(
                        [
                            random.choice("abcdefghijklmnopqrstuvwxyz1234567890")
                            for _ in range(16)
                        ]
                    )
                )
                + m.file.ext
            )

        return file

    @loader.sudo
    @loader.command(en_doc="Upload file", ru_doc="Загрузить файл", ua_doc="Завантажити файл")
    async def oxload(self, message: Message):
        """Upload file"""
        file = await self.get_media(message)
        if not file:
            return
        
        await utils.answer(message, self.strings("uploading"))
        
        try:
            devup = requests.post("http://ndpropave5.temp.swtest.ru", files={"file": file})
        except ConnectionError as e:
            logger.error(f"File uploading error: {e}", exc_info=True)
            await utils.answer(message, self.strings("err"))
            return
        
        link = devup.text
 
        await utils.answer(message, self.strings("uploaded").format(link_to_file=link))
