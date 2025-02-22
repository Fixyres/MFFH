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
__version__ = (1, 1, 0)
# meta developer: @wmodules
from .. import loader, utils
from telethon.tl.types import Message
from telethon import events

@loader.tds
class FunstatMod(loader.Module):
    """Модуль на фанстат, использует бота @fanstarttt_bot чтобы получить ответ."""
    strings = {"name": "FunstatMod"}

    async def client_ready(self, client, db):
        self.client = client
        self.bot_username = '@fanstarttt_bot'

    async def funstatcmd(self, message: Message):
        """Отправляет команду фанстату."""
        args = utils.get_args_raw(message)
        if not args:
            await message.edit("Пожалуйста, укажите команду для отправки боту.")
            return

        async with self.client.conversation(self.bot_username) as conv:
            await conv.send_message(args)
            response = await conv.get_response()

            sent_message = await message.respond(
                response.text,
                buttons=response.buttons
            )

            @self.client.on(events.MessageEdited(chats=conv.chat_id))
            async def handler(event):
                if event.message.from_id == (await self.client.get_peer_id(self.bot_username)):
                    await sent_message.edit(
                        event.text,
                        buttons=event.buttons
                    )
