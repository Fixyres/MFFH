# ---------------------------------------------------------------------------------
# Author: @shiro_hikka
# Name: Counter
# Description: Inline Clicks Counter
# Commands: count, creset
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

__version__ = (1, 0, 1)

from .. import loader, utils
from telethon.tl.types import Message
from ..inline.types import InlineCall
import asyncio

@loader.tds
class Counter(loader.Module):
    """Inline Clicks Counter"""

    strings = {
        "name": "Counter",
        "count": "Counter: {}"
    }

    async def client_ready(self):
        counts = self.db.get(__name__, "c")
        users = self.db.get(__name__, "u")
        if not counts:
            self.db.set(__name__, "c", 0)
        if not users:
            self.db.set(__name__, "u", [])


    async def cresetcmd(self, message: Message):
        """ [-u] [-c] - reset the counter\n-u (users list) -c (counts list)"""
        args = (utils.get_args_raw(message)).split()

        if all(i not in ["-u", "-c"] for i in args):
            return await utils.answer(message, "<emoji document_id=5233657262106485430>🤨</emoji> Incorrect flag")

        if "-u" in args:
            self.db.set(__name__, "u", [])
        if "-c" in args:
            self.db.set(__name__, "c", 0)

        await message.delete()

    async def countcmd(self, message: Message):
        """ Creates an inline button for counting a presses"""
        counts = self.db.get(__name__, "c")

        await self.inline.form(
            text=self.strings["count"].format(counts),
            message=message,
            reply_markup=[
                {
                    "text": "Click",
                    "callback": self.back
                }
            ],
            disable_security=True
        )


    async def back(self, call: InlineCall):
        id = call.from_user.id
        if id in self.db.get(__name__, "u"):
            return

        counts = self.db.get(__name__, "c")
        counts += 1
        self.db.set(__name__, "c", counts)

        users = self.db.get(__name__, "u")
        users.append(id)
        self.db.set(__name__, "u", users)

        await call.edit(
            text=self.strings["count"].format(counts),
            reply_markup=[
                {
                    "text": "Click",
                    "callback": self.back
                }
            ],
            disable_security=True
        )
