# Copyright 2025, werpyock
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
__version__ = (1, 9, 0)
# meta developer: @wmodules

from .. import loader, utils
import random
from telethon.tl.types import InputMessagesFilterGif

class KomaruMod(loader.Module):
    """Достает рандомную гифку из @komarumodd, мили камарек"""

    strings = {"name": "KomaruMod"}

    async def client_ready(self, client, db):
        self.client = client

    async def komarugifcmd(self, message):
        """Рандомная гифка"""
        channel = "@komarumodd"
        gifs = [msg async for msg in self.client.iter_messages(channel, filter=InputMessagesFilterGif)]
        if not gifs:
            await message.edit("<b>Нет доступных GIF-ов в канале!</b>")
            return

        random_gif = random.choice(gifs)
        reply_to = message.reply_to_msg_id

        await self.client.send_file(
            message.chat_id,
            random_gif,
            reply_to=reply_to
        )

        await message.delete()
