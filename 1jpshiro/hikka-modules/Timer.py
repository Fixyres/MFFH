# ---------------------------------------------------------------------------------
# Author: @shiro_hikka
# Name: Timer
# Description: Creates fine adorned timer
# Commands: timer
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

from .. import loader, utils
from telethon.tl.types import Message
import re
import asyncio

@loader.tds
class Timer(loader.Module):
    """Creates fine adorned timer"""

    strings = {
        "name": "Timer",
        "q": "<b>Current Timer for {}</b>\n<emoji document_id=5303396278179210513>👾</emoji> {} <b>left</b>"
    }

    async def parseArgs(self, message, args, parsed):
        for arg in args:
            if arg[-1] not in ["h", "m", "s"]:
                args.remove(arg)

        for arg in args:
            parsed[arg[-1]] = int(re.sub(r"[^0-9]", "", arg))
        return parsed


    async def timercmd(self, message: Message):
        """ [5h 5m 5s] - launch the timer"""
        args = (utils.get_args_raw(message)).split()
        parsed = {"h": None, "m": None, "s": None}
        if not args:
            return await utils.answer(message, "Specify time")

        _parsed = await self.parseArgs(message, args, parsed)
        if all(_parsed[i] is None for i in parsed):
            return await utils.answer(message, "<b>Time isn't specified</b>")

        hours = _parsed["h"] * 3600 if _parsed["h"] else 0
        mins = _parsed["m"] * 60 if _parsed["m"] else 0
        secs = _parsed["s"] if _parsed["s"] else 0
        _time = secs + mins + hours

        c = f"{hours}:{mins}:{secs}"
        pretime = "<i>{}:{}</i>"
        while _time > -1:
            h = f"{_time//3600}"
            m = f"{_time%3600//60}"
            s = f"{_time%3600%60}"
            if _time > 59:
                q = self.strings["q"].format(c, pretime.format(h, m))
            else:
                q = self.strings["q"].format(c, pretime.format(h, f"{m}:{s}"))

            try:
                await utils.answer(message, q)
            except:
                pass

            _time -= 1
            await asyncio.sleep(1)

        regex = r"\..*\<.*?\>.*"
        answer = re.sub(regex, "\n<emoji document_id=5222108309795908493>✨</emoji> <b>Time's over</b>", q.replace("\n", "."))
        await utils.answer(message, answer)
