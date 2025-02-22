# ---------------------------------------------------------------------------------
# Author: @shiro_hikka
# Name: Message Eraser
# Description: Delete your messages in the current chat
# Commands: purge, stoppurge
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

__version__ = (1, 2, 3)

from .. import loader, utils
from telethon.tl.types import Message
import asyncio
import random

@loader.tds
class MessageEraser(loader.Module):
    """Delete your messages in the current chat"""

    strings = {
        "name": "MessageEraser",
        "enabled": "<emoji document_id=5289755247298747469>😒</emoji> It's not operational now anyway",
        "disabled": "<emoji document_id=5237870268541582966>❄️</emoji> Operation status changed to disabled",
        "interrupted": "<emoji document_id=5233717529087581343>😀</emoji> The deletion was interrupted because you changed your mind",
        "none": "<emoji document_id=5291954734410767857>👁️</emoji> You didn't even intend to delete anything here, but anyway it's disabled now"
    }

    async def client_ready(self):
        status = self.db.get(__name__, "status", None)
        if status is None:
            self.db.set(__name__, "status", {})


    async def stoppurgecmd(self, message: Message):
        """
        Interrupt the deletion process
        Use in the chat where you've previously started deletion
        """
        chat_id = utils.get_chat_id(message)

        status = self.db.get(__name__, "status", {})
        _status = status.get(chat_id, None)
        status[chat_id] = False
        self.db.set(__name__, "status", status)

        if _status is True:
            await utils.answer(message, self.strings["disabled"])
        elif _status is False:
            await utils.answer(message, self.strings["enabled"])
        else:
            await utils.answer(message, self.strings["none"])

    async def purgecmd(self, message: Message):
        """
        [reply] [10s / 10m / 10h / 10d] [-all] - delete all your messages in the current chat or only ones up to the message you replied to
        Possible to do with a delay
        -all - to delete messages from each topic if this is a forum otherwise flag'll just be ignored
        Example: 10h 3d
        """
        args = (utils.get_args_raw(message)).split()
        if "-all" in args:
            is_each = True
            args.remove("-all")
        else:
            is_each = False

        reply = await message.get_reply_message()
        chat_id = utils.get_chat_id(message)
        delay = 0

        is_last = False
        is_forum = (await self.client.get_entity(chat_id)).forum

        status = self.db.get(__name__, "status", {})
        status[chat_id] = True
        self.db.set(__name__, "status", status)

        if args:
            for i in args:
                if len(i) < 2 or not i[:-1].isdigit():
                    continue

                delay += (
                    {"d": 86400, "h": 3600, "m": 60, "s": 1}.get(i[-1], 0) * i[:-1]
                )


        await asyncio.sleep(delay)

        batch = []
        async for _message in self.client.iter_messages(chat_id):
            status = self.db.get(__name__, "status", {})
            if status.get(chat_id, None) is not True:
                return await utils.answer(message, self.strings["interrupted"])

            if _message.from_id != self.tg_id:
                continue

            if is_forum and not is_each and utils.get_topic(message) != utils.get_topic(_message):
                continue

            if len(batch) == 10:
                await asyncio.sleep(self.getRandomDelay)
                await message.client.delete_messages(chat_id, batch)
                batch = []

            if reply:
                if is_last:
                    break
                if _message.id == reply.id:
                    is_last = True

            batch.append(_message.id)

        if len(batch) != 0:
            await message.client.delete_messages(chat_id, batch)
            batch = []

        await utils.answer(message, "<emoji document_id=5292186100004036291>🤩</emoji> Done")


    def getRandomDelay(self):
        """A self-made function, creatively designed for generating a random float"""
        rangeList = random.choice([(2.1, 3.9), (4.4, 6.7), (7.5, 9.1), (9.4, 10.4)])
        randomRange = random.uniform(rangeList[0], rangeList[1])
        randomSubRange = random.uniform(0.800, 1.399)

        randomNum = randomRange * random.random() + (random.random() + 1.0) * randomSubRange
        randomNum *= 3.8 if randomNum < 3 else 2.4 if randomNum < 5 else 1.3

        return round(randomNum, 3)