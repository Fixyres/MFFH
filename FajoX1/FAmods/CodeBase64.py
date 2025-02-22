#   █▀▀ ▄▀█   █▀▄▀█ █▀█ █▀▄ █▀
#   █▀░ █▀█   █░▀░█ █▄█ █▄▀ ▄█

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: CodeBase64
# Description: Encode and decode base64
# meta developer: @FAmods
# meta banner: https://github.com/FajoX1/FAmods/blob/main/assets/banners/CodeBase64.png?raw=true
# ---------------------------------------------------------------------------------

import base64
import asyncio
import logging

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class CodeBase64(loader.Module):
    """Encode and decode base64"""

    strings = {
        "name": "CodeBase64",

        "only_base64": "<b><emoji document_id=5019523782004441717>🚫</emoji> Only <code>base64</code></b>",

        "enc_txt": "<b><emoji document_id=6334316848741352906>⌨️</emoji> You encoded text into base64:</b>\n<code>{}</code>",
        "de_txt": "<b><emoji document_id=6334316848741352906>⌨️</emoji> You decoded text from base64:</b>\n<code>{}</code>",
    }


    async def client_ready(self, client, db):
        self.db = db
        self._client = client

    @loader.command()
    async def cbase64(self, message):
        """Кодирование в base64"""
        enc_bytes = base64.b64encode(utils.get_args_raw(message).encode('utf-8'))
        enc_text = enc_bytes.decode('utf-8')  # Декодируем байты в строку

        await utils.answer(message, self.strings["enc_txt"].format(enc_text))

    @loader.command()
    async def dbase64(self, message):
        """Декодирование из base64"""
        try:
            de_bytes = base64.b64decode(utils.get_args_raw(message))
        except:
            return await utils.answer(message, self.strings['only_base64'])
        de_text = de_bytes.decode('utf-8')  # Декодируем байты в строку

        await utils.answer(message, self.strings["de_txt"].format(de_text))
