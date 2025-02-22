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

from .. import loader, utils

from telethon.tl.types import Message  # type: ignore

# meta developer: @shadow_modules
# scope: hikka_only
# scope: hikka_min 1.3.0
# meta banner: https://i.imgur.com/nw5hP8P.jpeg


@loader.tds
class RandomMemesMod(loader.Module):
    """RandomMemes"""

    strings = {"name": "RandomMemes"}
    
    def __init__(self):
        self.bot = "@ffmemesbot"

    async def on_dlmod(self):
        await utils.dnd(self._client, self.bot, True)

    async def randmemescmd(self, message: Message):
        """See random memes"""
        async with self._client.conversation(self.bot) as conv:
            msg = await conv.send_message("/start")
            phtmem = await conv.get_response()
            await msg.delete()
            await phtmem.delete()
            await message.delete()
            await utils.answer(message, phtmem)
