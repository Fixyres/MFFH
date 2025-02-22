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
# meta banner: https://i.imgur.com/KiCMAfX.jpg

from .. import loader, utils
from telethon.tl.types import Message  # type: ignore


async def convert(self, message, args):
    days, remainder = divmod(args, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes = divmod(remainder, 60)
    seconds = divmod(remainder, 60)

    time_parts = [
        f"<emoji document_id=5469947168523558652>☀️</emoji><b> {days} Days</b>"
        if days > 0
        else None,
        f"<emoji document_id=6334620339720423126>🕛</emoji> <b> {hours} Hours</b>"
        if hours > 0
        else None,
        f"<emoji document_id=6334540900005315791>🕰️</emoji><b> {minutes[0]} Minutes</b>"
        if minutes[0] > 0
        else None,
        f"<emoji document_id=6334768915524093741>⏲️</emoji><b> {seconds[0]} Seconds</b>",
    ]

    time_string = "\n".join(part for part in time_parts if part is not None)
    if not args:
        await utils.answer(message, self.strings("no_args"))

    await utils.answer(message, time_string)


@loader.tds
class ConvertTimeMod(loader.Module):
    """Convert time in days, hours, minutes and seconds"""

    strings = {
        "name": "ConvertTime",
        "no_args": "<emoji document_id=5350311258220404874>❗️</emoji> <b>Arguments entered incorrectly</b>",
    }
    strings_ru = {
        "no_args": "<emoji document_id=5350311258220404874>❗️</emoji> <b>Не правильно введены аргументы</b>",
    }

    async def ctimecmd(self, message: Message):
        """ctime <int: time for convert>"""
        args = utils.get_args_raw(message)
        time_values = int(args)
        await convert(self, message, time_values)
