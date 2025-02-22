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
__version__ = (1, 4, 1)
# meta developer: @wmodules
from .. import loader, utils
import asyncio
import shlex

class WSpamMod(loader.Module):
    """Гибкий спам-модуль."""

    strings = {
        "name": "WSpamMod",
        "no_args": "❌ Укажите количество, задержку и текст (текст обязательно в кавычках) или используйте ответ на сообщение.",
        "spamming": "✅ Начинаю спам...",
        "stopped": "🛑 Задачи приостановлены.",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            "DEFAULT_COUNT", 10, "Количество сообщений по умолчанию",
            "DEFAULT_DELAY", 1.0, "Задержка между сообщениями по умолчанию (в секундах)",
            "DEFAULT_TEXT", "Привет, мир!", "Текст по умолчанию для спама",
            "DELETE_SPAM_ANNOUNCE", "false", "Удалять сообщение о начале спама: 'true' или 'false'"
        )
        self.spam_tasks = set()

    async def spamcmd(self, message):
        """Запуск спама.
Использование: .spam [кол-во сообщений] [задержка] "текст" (или ответ на сообщение)."""
        await self._start_spam(message, delete_after_send=False)

    async def dspamcmd(self, message):
        """Запуск спама с удалением отправленных сообщений.
Использование: .dspam [кол-во сообщений] [задержка] "текст" (или ответ на сообщение)."""
        await self._start_spam(message, delete_after_send=True)

    async def _start_spam(self, message, delete_after_send):
        args_raw = utils.get_args_raw(message)
        reply = await message.get_reply_message()

        count = self.config["DEFAULT_COUNT"]
        delay = self.config["DEFAULT_DELAY"]
        text = self.config["DEFAULT_TEXT"] if not reply else ""

        if args_raw:
            try:
                args_list = shlex.split(args_raw)
            except Exception:
                return await message.edit(self.strings["no_args"])

            if args_list and args_list[0].isdigit():
                count = int(args_list[0])
                args_list = args_list[1:]

            if args_list:
                try:
                    delay = float(args_list[0])
                    args_list = args_list[1:]
                except ValueError:
                    pass

            if args_list:
                text = " ".join(args_list)
        elif not reply:
            return await message.edit(self.strings["no_args"])

        delete_announce = str(self.config["DELETE_SPAM_ANNOUNCE"]).lower() == "true"
        if delete_announce:
            await message.delete()
        else:
            await message.edit(self.strings["spamming"])

        async def spam_task():
            for _ in range(count):
                if reply and reply.media:
                    sent = await message.client.send_file(
                        message.chat_id,
                        reply.media,
                        caption=text or None,
                        reply_to=reply.id
                    )
                else:
                    sent = await message.respond(text)
                if delete_after_send:
                    await sent.delete()
                await asyncio.sleep(delay)

        task = asyncio.create_task(spam_task())
        self.spam_tasks.add(task)
        task.add_done_callback(self.spam_tasks.discard)

    async def stopspamcmd(self, message):
        """Останавливает все активные задачи .spam."""
        await self._stop_spam(message)

    async def stopdspamcmd(self, message):
        """Останавливает все активные задачи .dspam."""
        await self._stop_spam(message)

    async def _stop_spam(self, message):
        for task in self.spam_tasks:
            task.cancel()
        self.spam_tasks.clear()
        await message.edit(self.strings["stopped"])
