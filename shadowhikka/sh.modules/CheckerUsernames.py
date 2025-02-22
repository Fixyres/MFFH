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
# meta banner: https://i.imgur.com/aGGx93G.jpeg

import pytz  # type: ignore
from .. import loader, utils
from telethon.tl.types import Message  # type: ignore
from telethon.tl.functions.channels import CreateChannelRequest  # type: ignore
from telethon.tl.functions.channels import UpdateUsernameRequest  # type: ignore
from datetime import datetime


@loader.tds
class CheckerUsernamesMod(loader.Module):
    """Check of avaliable usernames"""

    strings = {
        "name": "CheckerUsernames",
        "off": "<emoji document_id=5350311258220404874>❗️</emoji> <b>Checker disabled</b>",
        "on": "<emoji document_id=5776375003280838798>✅</emoji> <b>Checker enabled</b>",
        "catching": "<b>👍 I caught the username\n🧐 Username: @{user}\n<b>⏰ Catch time: {time}</b>",
    }
    strings_ru = {
        "off": "<emoji document_id=5350311258220404874>❗️</emoji> <b>Проверка юзернеймов выключена</b>",
        "on": "<emoji document_id=5776375003280838798>✅</emoji> <b>Проверка юзернеймов включена</b>",
        "catching": "<b>👍 Я словил юзернейм\n🧐 Юзернейм: @{user}\n<b>⏰ Время ловли: {time}</b>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "usernames",
                ["onetimeusername"],
                lambda: "Usernames for check",
                validator=loader.validators.Series(
                    validator=loader.validators.String()
                ),
            ),
            loader.ConfigValue(
                "text",
                "OCCUPIED BY SH. MODULE",
                lambda: "Usernames for check",
                validator=loader.validators.String(),
            ),
            loader.ConfigValue(
                "delay",
                5,
                lambda: "Delay for check username",
                validator=loader.validators.Integer(minimum=0),
            ),
            loader.ConfigValue(
                "time",
                "Europe/Kiev",
                lambda: "Timezone",
                validator=loader.validators.String(),
            ),
        )

    @loader.loop(30, autostart=True)
    async def checker(self):
        if not self.get("status"):
            return
        current_time = (
            datetime.now(pytz.timezone(self.config["time"]))
            .replace(microsecond=0)
            .time()
        )
        usernames = self.config["usernames"]
        for username in usernames:
            try:
                await self.client.get_entity(username)
            except ValueError:
                chan = await self.client(
                    CreateChannelRequest(
                        title="occupied shadow",
                        about="GEAR SHADOW",
                    )
                )
                await self.client(UpdateUsernameRequest(chan.chats[0].id, username))
                await self.client.send_message(chan.chats[0].id, self.config["text"])
                await self.inline.bot.send_message(
                    self._tg_id,
                    self.strings("catching").format(
                        user=(await self.client.get_entity(chan.chats[0].id)).username,
                        time=current_time,
                    ),
                )
                continue

    async def cusercmd(self, message: Message):
        """Off/On checker username"""
        if self.get("status"):
            await utils.answer(message, self.strings("off"))
            return self.set("status", False)
        else:
            await utils.answer(message, self.strings("on"))
            self.set("status", True)

    async def timezonescmd(self, message: Message):
        """All timezones for config"""
        await message.delete()
        await self.invoke("e", "import pytz; pytz.all_timezones", message.peer_id)
