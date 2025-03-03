# meta developer: @MrAmigoch for @HikkaZPM
#
#
import hikkatl

import random
import asyncio
import logging

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class femboy(loader.Module):
    """Femboy Modul"""

    strings = {
        "name": "FemBoy",

        "p_on": "<b><emoji <emoji document_id=5341813983252851777>🌟</emoji> режим Femboy включен!</b>",
        "p_off": "<b><emoji <emoji document_id=5318833180915027058>😭</emoji> Режим Femboy^^ выключен!</b>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "emojies",
                ["<emoji document_id=5424970378374035950>🕺</emoji>", "<emoji document_id=5429635773714412028>😆</emoji>", "<emoji document_id=5321451749460946626>😘</emoji>", "<emoji document_id=5215496967852936076>🥵</emoji>", "<emoji document_id=5326027259725749455>🤭</emoji>", "<emoji document_id=5402630084509066049>😏</emoji>️", "<emoji document_id=5327760081461190613>😋</emoji>", "<emoji document_id=5235787973907205473>👅</emoji>"],
                lambda: "Эмодзы для вставки в текст",
                validator=loader.validators.Series()
            ),
            loader.ConfigValue(
                "signs",
                [":3", "•⩊•"],
                lambda: "Знаки для вставки в текст",
                validator=loader.validators.Series()
            ),
        )

    async def client_ready(self, client, db):
        self.db = db
        self._client = client

    @loader.command()
    async def femboy(self, message):
        """Включить/выключить режим фембоя """

        if self.db.get(self.name, "femboy", False):
            self.db.set(self.name, "femboy", False)
            return await utils.answer(message, self.strings["p_off"])

        self.db.set(self.name, "femboy", True)

        await utils.answer(message, self.strings["p_on"])

    async def watcher(self, event):
        try:
            if event.from_id  != self.tg_id:
                return
        except:
            return
        if not self.db.get(self.name, "femboy", False):
            return
        
        words = event.raw_text.split()
        modified_text = " ".join(
            word + (f" {random.choice(self.config['emojies'])}" if random.random() > 0.5 else "")
            for word in words
        )
        await event.edit(text=modified_text+random.choice(self.config['signs']))
