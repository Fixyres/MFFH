# █▀ █░█ ▄▀█ █▀▄ █▀█ █░█░█
# ▄█ █▀█ █▀█ █▄▀ █▄█ ▀▄▀▄▀

# Copyright 2023 t.me/shadow_modules
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# meta developer: @shadow_modules
# scope: hikka_only
# scope: hikka_min 1.3.0
# meta banner: https://i.imgur.com/1UnAXNf.jpeg

from .. import loader, utils
from telethon.tl.types import Message  # type: ignore


@loader.tds
class StickerDownloadMod(loader.Module):
    """Sticker Downloader"""

    strings = {
        "name": "StickerDownload",
        "filerr": "<b>😥 Specify a sticker replay to it</b>",
    }
    strings_ru = {"filerr": "<b>😥 Укажи стикер реплаем на него</b>"}

    def __init__(self):
        self.bot = "@Stickerdownloadbot"

    async def on_dlmod(self):
        await utils.dnd(self._client, self.bot, True)

    async def stickdowncmd(self, message: Message):
        """stickdown <reply for sticker>"""
        reply = await message.get_reply_message()
        if not getattr(reply, "sticker", None):
            await utils.answer(message, self.strings("filerr"))
            return

        try:
            async with self._client.conversation(self.bot) as conv:
                reply = await message.get_reply_message()
                await conv.send_message(reply)
                phtmem = await conv.get_response()
                await conv.mark_read()
                await message.delete()
                await utils.answer(message, phtmem)
        except ValueError:
            await utils.answer(message, self.strings("filerr"))
