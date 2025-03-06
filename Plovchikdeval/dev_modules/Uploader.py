__version__ = (3, 0, 0)

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
# requires: aiohttp

import logging
import io
import os
import random
import aiohttp
import json

from telethon.tl.types import Message

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class UploaderMod(loader.Module):
    """Модуль для загрузки файлов"""

    strings = {
        "name": "Uploader",
        "_cfg_token": "Paste the received API key from @kshteam_uploader_token_bot",
        "no_token": "<emoji document_id=5872829476143894491>🚫</emoji> <b>Invalid token!</b>\n<emoji document_id=5879785854284599288>ℹ️</emoji> <b>Get token in</b> @kshteam_uploader_token_bot",
        "ban": "<blockquote><emoji document_id=5458779239941681169>😔</emoji> <b>You have been banned</b></blockquote><blockquote>\n<emoji document_id=5879785854284599288>ℹ️</emoji> <b>If this is a mistake, write to</b> @dev3quest</blockquote>\n<blockquote><emoji document_id=5873121512445187130>❓</emoji>Reason: {reason} </blockquote>",
        "uploading": "<blockquote><emoji document_id=5872756762347573066>⏲</emoji> <b>Uploading...</b></blockquote>",
        "noargs": "<blockquote><emoji document_id=5208434048753484584>⛔</emoji> <b>No file specified</b></blockquote>",
        "err": "<blockquote><emoji document_id=5208434048753484584>⛔</emoji> <b>Upload error</b><blockquote>",
        "uploaded": "<blockquote><emoji document_id=5208547229731669225>⚡</emoji> <b>File uploaded!</b>\n\n<code>{link_to_file}</code></blockquote>",
    }

    strings_ru = {
        "_cfg_token": "Вставьте полученный ключ API от @kshteam_uploader_token_bot",
        "no_token": "<blockquote><emoji document_id=5872829476143894491>🚫</emoji><b> Недействительный токен!</b></blockquote>\n<blockquote><emoji document_id=5879785854284599288>ℹ️</emoji> <b>Получите токен в</b> @kshteam_uploader_token_bot</blockquote>",
        "ban": "<blockquote><emoji document_id=5458779239941681169>😔</emoji> <b>Вас забанили</b></blockquote>\n<blockquote><emoji document_id=5879785854284599288>ℹ️</emoji> <b>Если это ошибка, напишите</b> @dev3quest</blockquote>\n<blockquote><emoji document_id=5873121512445187130>❓</emoji>Причина: {reason} </blockquote>",
        "uploading": "<blockquote><emoji document_id=5872756762347573066>⏲</emoji> <b>Загрузка...</b></blockquote>",
        "noargs": "<blockquote><emoji document_id=5208434048753484584>⛔</emoji> <b>Файл не указан</b></blockquote>",
        "err": "<blockquote><emoji document_id=5208434048753484584>⛔</emoji> <b>Ошибка загрузки</b></blockquote>",
        "uploaded": "<blockquote><emoji document_id=5208547229731669225>⚡</emoji> <b>Файл загружен!</b>\n\n<code>{link_to_file}</code></blockquote>",
    }

    def __init__(self):
      self.config = loader.ModuleConfig(
          loader.ConfigValue(
              "token",
              "None",
              lambda: self.strings("_cfg_token"),
              validator=loader.validators.Hidden(),
              ),
          )

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

    @loader.command(en_doc="Upload file", ru_doc="Загрузить файл", ua_doc="Завантажити файл")
    async def oxload(self, message: Message):
        if not self.config["token"] or self.config["token"] == "None":
            await utils.answer(message, self.strings("no_token"))
            return

        file = await self.get_media(message)
        if not file:
            return
        
        await utils.answer(message, self.strings("uploading"))
        
        try:
            headers = {
                "x-api-key": self.config["token"]
            }

            async with aiohttp.ClientSession() as session:
                form_data = aiohttp.FormData() 
                form_data.add_field("file", file)
                async with session.post("https://upload.kshteam.top/upload", headers=headers, data=form_data) as response:
                    response_text = await response.text()

                    if response.status == 403:
                        try:
                            error_data = json.loads(response_text)
                            ban_reason = error_data.get("reason", "Unknown")
                        except json.JSONDecodeError:
                            ban_reason = "Unknown"
                        await utils.answer(message, self.strings("ban").format(reason=ban_reason))
                        return

                    response.raise_for_status()

                    try:
                        data = json.loads(response_text)
                        file_url = data.get("url")
                    except json.JSONDecodeError:
                        file_url = response_text.strip()

        except aiohttp.ClientResponseError:
            await utils.answer(message, self.strings("err"))
            return
        except Exception:
            await utils.answer(message, self.strings("err"))
            return

        await utils.answer(message, self.strings("uploaded").format(link_to_file=file_url))
