#   █▀▀ ▄▀█   █▀▄▀█ █▀█ █▀▄ █▀
#   █▀░ █▀█   █░▀░█ █▄█ █▄▀ ▄█

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: PicMe
# Description: Кринж модуль
# meta developer: @FAmods
# meta banner: https://github.com/FajoX1/FAmods/blob/main/assets/banners/picme.png?raw=true
# ---------------------------------------------------------------------------------

import hikkatl

import random
import asyncio
import logging

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class PicMe(loader.Module):
    """Кринж модуль"""

    strings = {
        "name": "PicMe",

        "p_on": "<b><emoji document_id=5373189724372474575>😘</emoji> Режим пикми включен!</b>",
        "p_off": "<b><emoji document_id=5370881342659631698>😢</emoji> Режим пикми выключен!</b>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "emojies",
                ["😊", "😂", "🎉", "👍", "🔥", "❤️", "🥳", "😎"],
                lambda: "Эмодзы для вставки в текст",
                validator=loader.validators.Series()
            ),
            loader.ConfigValue(
                "signs",
                ["!", "!!"],
                lambda: "Знаки для вставки в текст",
                validator=loader.validators.Series()
            ),
        )

    async def client_ready(self, client, db):
        self.db = db
        self._client = client

    @loader.command()
    async def picme(self, message):
        """Включить/выключить режим пикми"""

        if self.db.get(self.name, "picme", False):
            self.db.set(self.name, "picme", False)
            return await utils.answer(message, self.strings["p_off"])

        self.db.set(self.name, "picme", True)

        await utils.answer(message, self.strings["p_on"])

    async def watcher(self, event):
        try:
            if event.from_id != self.tg_id:
                return
        except:
            return
        if not self.db.get(self.name, "picme", False):
            return
        
        words = event.raw_text.split()
        modified_text = " ".join(
            word + (f" {random.choice(self.config['emojies'])}" if random.random() > 0.5 else "")
            for word in words
        )
        await event.edit(text=modified_text+random.choice(self.config['signs']))