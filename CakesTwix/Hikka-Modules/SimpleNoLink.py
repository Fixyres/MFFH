"""

    █▀▀ ▄▀█ █▄▀ █▀▀ █▀ ▀█▀ █░█░█ █ ▀▄▀
    █▄▄ █▀█ █░█ ██▄ ▄█ ░█░ ▀▄▀▄▀ █ █░█

    Copyleft 2022 t.me/CakesTwix
    This program is free software; you can redistribute it and/or modify

"""

__version__ = (1, 0, 0)

# meta developer: @cakestwix_mods
# meta pic: https://img.icons8.com/officel/16/000000/broken-link.png

from .. import loader
import re
import logging
from telethon.tl.patched import Message

logger = logging.getLogger(__name__)


class NoLinksMod(loader.Module):
    """A simple link cleaner from your chats"""
    strings = {"name": "SimpleNoLinks", "settings": "Setting for this chat", "add": "Add", "remove": "Remove"}
    strings_ru = {"name": "SimpleNoLinks", "settings": "Настройка для данного чата", "add": "Добавить", "remove": "Убрать"}

    async def linkcmd(self, message):
        """Configuration for chat"""
        await self.inline.form(
            message=message,
            text=self.strings["settings"],
            reply_markup=[
                {
                    "text": self.strings["add"],
                    "callback": self.chat__callback,
                    "args": (
                        True,
                        message.chat.id,
                    ),
                }
            ]
            if message.chat.id not in self.chats
            else [
                {
                    "text": self.strings["remove"],
                    "callback": self.chat__callback,
                    "args": (
                        False,
                        message.chat.id,
                    ),
                }
            ],
        )

    async def client_ready(self, client, db) -> None:
        self._db = db
        self._client = client

        None if self._db.get(self.strings["name"], "chats") else self._db.set(
            self.strings["name"], "chats", []
        )
        self.chats = self._db.get(self.strings["name"], "chats")

    async def chat__callback(self, call, type_, id_):
        if type_:
            self.chats.append(id_)
        else:
            self.chats.remove(id_)

        self._db.set(self.strings["name"], "chats", self.chats)
        await call.edit(
            text=self.strings["settings"],
            reply_markup=[
                {
                    "text": self.strings["add"],
                    "callback": self.chat__callback,
                    "args": (
                        True,
                        id_,
                    ),
                }
            ]
            if id_ not in self.chats
            else [
                {
                    "text": self.strings["remove"],
                    "callback": self.chat__callback,
                    "args": (
                        False,
                        id_,
                    ),
                }
            ],
        )

    async def watcher(self, message):
        if getattr(message, "sender_id", None) != self._client._tg_id and bool(
            re.findall(
                r"""(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))""",
                message.text,
            )
            and message.chat.id in self.chats
        ):
            await message.delete()
