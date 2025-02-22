# ---------------------------------------------------------------------------------
# Author: @shiro_hikka
# Name: Autotime
# Description: Automatic stuff for your profile
# Commands: autoname, autobio, cfgset
# ---------------------------------------------------------------------------------
#              © Copyright 2025
#
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# ---------------------------------------------------------------------------------
# scope: hikka_only
# meta developer: @shiro_hikka
# meta banner: https://0x0.st/s/FIR0RnhUN5pZV5CZ6sNFEw/8KBz.jpg
# ---------------------------------------------------------------------------------

__version__ = (1, 0, 0)

from telethon.tl.functions.account import UpdateProfileRequest
from telethon.utils import get_display_name
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import Message

from .. import loader, utils
import re
import datetime
import asyncio

@loader.tds
class Autotime(loader.Module):
    """Automatic stuff for your profile"""

    strings = {
        "name": "Autotime",
        "no_time": "<emoji document_id=5289755247298747469>😒</emoji> You didn't place a {time}",
        "cfg": "Positive or negative integer from -12 to 12 inclusively"
    }

    def __init__(self):
        self.bio_on = False
        self.name_on = False

        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "Timezone",
                "0",
                lambda: self.strings["cfg"],
                validator=loader.validators.Integer()
            )
        )

    async def client_ready(self):
        self.me = await self.client.get_me()

    def _time(self):
        offset = datetime.timedelta(hours=self.config["Timezone"])
        tz = datetime.timezone(offset)
        now = datetime.datetime.now(tz)
        time = now.strftime("%H:%M")
        return time


    async def cfgsetcmd(self, message: Message):
        """ <number> - specify a timezone
        Regarding to UTC+0"""
        tz = utils.get_args_raw(message)
        q = await self.invoke(
            "fconfig",
            f"{self.strings('name')} Timezone {tz}",
            message.chat.id
        )

        await self.client.delete_messages(message.chat.id, [message, q])

    async def autonamecmd(self, message: Message):
        """ <text> - autotime in nickname | {time} must be placed in the text
        Write without argument to disable"""
        args = utils.get_args_raw(message)

        if not args:
            self.name_on = False
            regex = r"\d\d:\d\d"
            name = utils.escape_html(get_display_name(self.me))
            name = re.sub(regex, "", name)
            name.replace("  ", "")

            await self.client(UpdateProfileRequest(first_name=name))
            return await message.delete()

        if "{time}" not in args:
            return await utils.answer(message, self.strings["no_time"])

        self.name_on = True
        await message.delete()

        while self.name_on:
            text = args.replace("{time}", self._time())
            await self.client(UpdateProfileRequest(first_name=text))
            await asyncio.sleep(180)

    async def autobiocmd(self, message: Message):
        """ <text> - autotime in bio | {time} must be placed in the text
        Write without argument to disable"""
        args = utils.get_args_raw(message)

        if not args:
            self.bio_on = False
            regex = r"\d\d:\d\d"
            bio = (await self.client(GetFullUserRequest(self.tg_id))).full_user.about
            bio = re.sub(regex, "", bio)
            bio.replace("  ", " ")

            await self.client(UpdateProfileRequest(about=bio))
            return await message.delete()

        if "{time}" not in args:
            return await utils.answer(message, self.strings["no_time"])

        self.bio_on = True
        await message.delete()

        while self.bio_on:
            text = args.replace("{time}", self._time())
            await self.client(UpdateProfileRequest(about=text))
            await asyncio.sleep(180)
