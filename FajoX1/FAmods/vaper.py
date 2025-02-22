#   █▀▀ ▄▀█   █▀▄▀█ █▀█ █▀▄ █▀
#   █▀░ █▀█   █░▀░█ █▄█ █▄▀ ▄█

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: Vaper
# Description: Авто-фарм в @vapeusebot
# meta developer: @FAmods
# meta banner: https://github.com/FajoX1/FAmods/blob/main/assets/banners/vaper.png?raw=true
# ---------------------------------------------------------------------------------

import hikkatl

import re
import random
import asyncio
import logging

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class Vaper(loader.Module):
    """Авто-фарм в @vapeusebot"""

    strings = {
        "name": "Vaper",

        "checking_profile": "<b><emoji document_id=5424885441100782420>👀</emoji> Смотрю профиль...</b>",
        "getting_top": "<b><emoji document_id=5424885441100782420>👀</emoji> Смотрю статистику...</b>",

        "v_on": "<b><emoji document_id=5429633836684157942>⚡️</emoji> Авто-фарм включен!</b>",
        "v_off": "<b><emoji document_id=5854929766146118183>🚫</emoji> Авто-фарм выключен!</b>",
    }


    async def client_ready(self, client, db):
        self.db = db
        self._client = client

        if self.db.get(self.name, "vape", False):
           asyncio.create_task(self._vape())

    async def _vape(self):
        while True:
            try:
                async with self._client.conversation("@vapeusebot") as conv:
                    msg = await conv.send_message("/vape")
                    r = await conv.get_response()
                    await msg.delete()
                break
            except hikkatl.errors.common.AlreadyInConversationError:
                await asyncio.sleep(5.67)

    async def _getprofme(self):
        while True:
            try:
                async with self._client.conversation("@vapeusebot") as conv:
                    msg = await conv.send_message("/vape")
                    r = await conv.get_response()
                    await msg.delete()
                    await r.delete()
                    match = re.search(r'Всего затягов: (\d+)', r.text)
                    total_puffs = int(match.group(1))
                    await asyncio.sleep(2.4211112)
                    msg = await conv.send_message("/ref")
                    r = await conv.get_response()
                    await msg.delete()
                    await r.delete()
                    match = re.search(r'рефералов: (\d+)', r.text)
                    referrals = int(match.group(1))
                    return f"""<b><emoji document_id=5433653135799228968>📁</emoji> Профиль
                    
🌫 Затяжек: <code>{total_puffs}</code>
👥 Приглашено: <code>{referrals}</code>

<emoji document_id=5271604874419647061>🔗</emoji> Реферальная ссылка: <code>http://t.me/vapeusebot?start=ref_{self.tg_id}</code></b>"""

                break
            except hikkatl.errors.common.AlreadyInConversationError:
                await asyncio.sleep(5.67)

    async def _gettop(self):
        while True:
            try:
                async with self._client.conversation("@vapeusebot") as conv:
                    msg = await conv.send_message("/global_top")
                    r = await conv.get_response()
                    await msg.delete()
                    await r.delete()
                    return r.text.replace("&lt;i&gt;/vape&lt;/i&gt", "<code>/vape</code>")
                break
            except hikkatl.errors.common.AlreadyInConversationError:
                await asyncio.sleep(5.67)

    @loader.command()
    async def vape(self, message):
        """Включить/выключить авто-фарм"""

        if self.db.get(self.name, "vape", False):
            self.db.set(self.name, "vape", False)
            return await utils.answer(message, self.strings["v_off"])

        self.db.set(self.name, "vape", True)

        await utils.answer(message, self.strings["v_on"])

        await self._vape()
        
    @loader.command()
    async def vp(self, message):
        """Посмотреть свой профиль"""

        await utils.answer(message, self.strings["checking_profile"])

        await utils.answer(message, await self._getprofme())

    @loader.command()
    async def vtop(self, message):
        """Посмотреть топ"""

        await utils.answer(message, self.strings["getting_top"])

        await utils.answer(message, await self._gettop())

    @loader.loop(interval=60*60, autostart=True)
    async def loop(self):
      if self.db.get(self.name, "vape", False):
        await self._vape()
        await asyncio.sleep(random.randint(65, 90))
