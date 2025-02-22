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
__version__ = (1, 0, 0)
# meta developer: @wmodules
from .. import loader, utils
import asyncio
from telethon.errors import TimeoutError

@loader.tds
class SpamCheckMod(loader.Module):
    """Модуль для проверки спам-блока."""
    strings = {"name": "SpamCheckMod"}

    async def client_ready(self, client, db):
        self.client = client

    @loader.command()
    async def checkspam(self, message):
        """Проверяет, есть ли у тебя спам-блок."""
        bot_username = "spambot"
        try:
            async with self.client.conversation(bot_username, timeout=15) as conv:
                await conv.send_message("/start")
                response = await conv.get_response()
                await message.edit(response.text)
        except TimeoutError:
            await message.edit("<b>❌ Бот не ответил в течение 15 секунд</b>")
        except Exception as e:
            await message.edit(f"<b>❌ Ошибка: {e}</b>")
