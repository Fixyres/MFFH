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

import asyncio
from .. import loader, utils

@loader.tds
class SpeedTestMod(loader.Module):
    """Проверка скорости интернета на сервере."""
    
    strings = {
        "name": "SpeedTest",
        "no_cmd": "❌ Установи speedtest-cli перед использованием модуля: <code>apt install speedtest-cli</code>",
        "checking": "⏱️ Проверка скорости интернета...",
        "error": "❌ Ошибка: <code>{}</code>"
    }

    async def client_ready(self, client, db):
        self._client = client

    @loader.command()
    async def speedtest(self, message):
        """проверить скорость интернета"""
        msg = await utils.answer(message, self.strings["checking"])
        
        try:
            check = await asyncio.create_subprocess_shell("which speedtest-cli", stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            await check.communicate()
            
            if check.returncode != 0:
                await utils.answer(msg, self.strings["no_cmd"])
                return
            proc = await asyncio.create_subprocess_shell("speedtest-cli --simple", stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            stdout, stderr = await proc.communicate()

            if stderr:
                await utils.answer(msg, self.strings["error"].format(stderr.decode().strip()))
                return
            result = stdout.decode().strip()
            result = (result.replace("Ping", "🚀 Пинг").replace("Download", "💽 Скачивание").replace("Upload", "💿 Загрузка")
            )

            await utils.answer(msg, f"📊 Результаты теста:\n<code>{result}</code>")

        except Exception as e:
            await utils.answer(msg, self.strings["error"].format(str(e)))
