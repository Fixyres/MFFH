# ---------------------------------------------------------------------------------
# Author: @shiro_hikka
# Name: PMStat
# Description: Defines how many messages did you and your chat partner write
# Commands: stat
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

@loader.tds
class PMStat(loader.Module):
    """Defines how many messages did you and your chat partner write"""

    strings = {
        "name": "PMStat",
        "q": "<emoji document_id=5444965061749644170>👨‍💻</emoji> All in all, {} messages were counted from <b>{}</b>",
        "pm": "<emoji document_id=5233657262106485430>🤨</emoji> Use in PM only"
    }

    async def statcmd(self, message: Message):
        """ [-p] [-s] - (-p - counts your chat partner messages) (-s - send result to the saved messages)"""
        args = utils.get_args_raw(message)
        if not message.is_private:
            return await utils.answer(message, self.strings["pm"])

        await message.delete()

        chat = await self.client.get_entity(message.peer_id.user_id)
        target = "you" if "-p" not in args else f"<a href='tg://user?id={chat.id}'>{chat.first_name}</a>"
        s = chat.id if "-s" not in args else self.tg_id
        count = 0
        messagesList = []

        async for i in self.client.iter_messages(chat.id):
            if "-p" in args:
                if i.from_id != self.tg_id:
                    messagesList.append(i)
            else:
                if i.from_id == self.tg_id:
                    messagesList.append(i)

        await message.client.send_message(s, self.strings["q"].format(len(messagesList), target))
