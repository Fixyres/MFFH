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

# meta developer: @shadow_modules, @dan_endy
# scope: hikka_only
# meta banner: https://i.imgur.com/8prGakZ.jpeg


@loader.tds
class VKInlineMod(loader.Module):
    """Your vk in inline"""

    strings = {
        "name": "MyVKInline",
        "myvk": "<b>👾 My VK</b>",
        "clickvk": "🦢 Click",
        "novk": "<b>😰 You didn't enter your VK</b>",
    }

    strings_ru = {
        "myvk": "<b>👾 Мой VK</b>",
        "clickvk": "🦢 Нажми",
        "novk": "<b>😰 Вы не ввели свой вк</b>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "VK",
                None,
                lambda: "Your VK",
                validator=loader.validators.Link(),
            )
        )

    @loader.unrestricted
    async def myvkcmd(self, message: Message):
        """The command to display your VK"""
        if not self.config["VK"]:
            await utils.answer(message, self.strings("novk", message))
            return
        elif "https://" in self.config["VK"]:
            await self.inline.form(
                text=self.strings("myvk"),
                message=message,
                reply_markup={
                    "text": self.strings("clickvk"),
                    "url": self.config["VK"],
                },
            )
