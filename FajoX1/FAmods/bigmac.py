#   █▀▀ ▄▀█   █▀▄▀█ █▀█ █▀▄ █▀
#   █▀░ █▀█   █░▀░█ █▄█ █▄▀ ▄█

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: BigMac
# Description: Авто-фарм в @BigMacMetreBot
# meta developer: @FAmods
# meta banner: https://github.com/FajoX1/FAmods/blob/main/assets/banners/bigmac.png?raw=true
# ---------------------------------------------------------------------------------

import hikkatl

import re
import random
import asyncio
import logging

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class BigMac(loader.Module):
    """Авто-фарм в @BigMacMetreBot"""

    strings = {
        "name": "BigMac",

        "checking_profile": "<b><emoji document_id=5424885441100782420>👀</emoji> Смотрю профиль...</b>",
        "getting_top": "<b><emoji document_id=5424885441100782420>👀</emoji> Смотрю статистику...</b>",

        "e_on": "<emoji document_id=5239948040575393823>🍔</emoji> <b>Авто-фарм включен!</b>",
        "e_off": "<b><emoji document_id=5854929766146118183>🚫</emoji> Авто-фарм выключен!</b>",
    }


    async def client_ready(self, client, db):
        self.db = db
        self._client = client

    async def _eat(self):
        while True:
            try:
                async with self._client.conversation("@BigMacMetreBot") as conv:
                    msg = await conv.send_message("/bigmac")
                    r = await conv.get_response()
                    await msg.delete()
                    await r.delete()
                break
            except hikkatl.errors.common.AlreadyInConversationError:
                await asyncio.sleep(5.67)

    async def _getprofme(self):
        while True:
            try:
                async with self._client.conversation("@BigMacMetreBot") as conv:
                    msg = await conv.send_message("/profile")
                    r = await conv.get_response()
                    await msg.delete()
                    await r.delete()
                    return f"""<b>{r.text}</b>"""

                break
            except hikkatl.errors.common.AlreadyInConversationError:
                await asyncio.sleep(5.67)

    async def _gettop(self):
        while True:
            try:
                async with self._client.conversation("@BigMacMetreBot") as conv:
                    msg = await conv.send_message("/top")
                    r = await conv.get_response()
                    await msg.delete()
                    await r.delete()
                    return f"<b>{r.text}</b>"
                break
            except hikkatl.errors.common.AlreadyInConversationError:
                await asyncio.sleep(5.67)

    @loader.command()
    async def bigmacs(self, message):
        """Включить/выключить авто-фарм"""

        if self.db.get(self.name, "eat_bigmac", False):
            self.db.set(self.name, "eat_bigmac", False)
            return await utils.answer(message, self.strings["e_off"])

        self.db.set(self.name, "eat_bigmac", True)

        await utils.answer(message, self.strings["e_on"])

        await self._eat()
        
    @loader.command()
    async def bp(self, message):
        """Посмотреть свой профиль"""

        await utils.answer(message, self.strings["checking_profile"])

        await utils.answer(message, await self._getprofme())

    @loader.command()
    async def btop(self, message):
        """Посмотреть топ"""

        await utils.answer(message, self.strings["getting_top"])

        await utils.answer(message, await self._gettop())

    @loader.loop(interval=60*60, autostart=True)
    async def loop(self):
      if self.db.get(self.name, "eat_bigmac", False):
        await self._eat()
        await asyncio.sleep(random.randint(65, 90))
