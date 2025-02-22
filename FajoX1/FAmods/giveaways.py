#   █▀▀ ▄▀█   █▀▄▀█ █▀█ █▀▄ █▀
#   █▀░ █▀█   █░▀░█ █▄█ █▄▀ ▄█

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: Giveaways
# Description: Авто-участие в розыгрышах Telegram Premium (Hikka 1.6.4+)
# meta developer: @FAmods
# meta banner: https://github.com/FajoX1/FAmods/blob/main/assets/banners/giveaways.png?raw=true
# scope: hikka_min 1.6.4
# ---------------------------------------------------------------------------------

import asyncio
import logging

from telethon.tl.types import MessageMediaGiveaway

from .. import loader, utils

from telethon.tl.functions.channels import JoinChannelRequest

logger = logging.getLogger(__name__)

@loader.tds
class Giveaways(loader.Module):
    """Авто-участие в розыгрышах Telegram Premium"""

    strings = {
        "name": "Giveaways",

        "giveaways_on": "<b><emoji document_id=5852779353330421386>🎁</emoji> Авто-участие включено!</b>",
        "giveaways_off": "<b><emoji document_id=5854929766146118183>🚫</emoji> Авто-участие выключено!</b>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "log",
                True,
                lambda: "Писать в логи о участии в новом розыгрыше",
                validator=loader.validators.Boolean()
            )
        )


    async def client_ready(self, client, db):
        self.db = db
        self._client = client

    @loader.command()
    async def gwtg(self, message):
        """Включить/выключить автоматическое участие в розыгрышах Telegram Premium"""

        if self.db.get(self.name, "giveaways_status", False):
            self.db.set(self.name, "giveaways_status", False)
            return await utils.answer(message, self.strings["giveaways_off"])

        self.db.set(self.name, "giveaways_status", True)

        await utils.answer(message, self.strings["giveaways_on"])

    async def watcher(self, event):
        try:
            if not isinstance(event.media, MessageMediaGiveaway):
                return
        except:
            return

        if not self.db.get(self.name, "giveaways_status"):
           return
        
        for c_id in event.media.channels:
            try:
                channel = await self.client.get_entity(c_id)
                await self.client(JoinChannelRequest(channel))
                await asyncio.sleep(2.343982493248932)
            except:
                return

        if self.config['log']:
            logging.info("Joined to new giveaway")
