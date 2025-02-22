#   █▀▀ ▄▀█   █▀▄▀█ █▀█ █▀▄ █▀
#   █▀░ █▀█   █░▀░█ █▄█ █▄▀ ▄█

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: Fun
# Description: Module for fun
# meta developer: @FAmods
# meta banner: https://github.com/FajoX1/FAmods/blob/main/assets/banners/fun.png?raw=true
# ---------------------------------------------------------------------------------

import random
import asyncio
import logging

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class Fun(loader.Module):
    """Module for fun..."""

    strings = {
        "name": "Fun",

        "no_us": "<emoji document_id=5854929766146118183>❌</emoji> <b>Должно быть .hacku [юзернейм/ник чела]</b>",
        "no_typing_text": "<emoji document_id=5854929766146118183>❌</emoji> <b>Должно быть .ftype [текст]</b>",

        "hacku_process": "<emoji document_id=6334357625160861194>💻</emoji> <b>Взлом {} в процессе... {}%</b>",
        "hackedu": "<emoji document_id=5854762571659218443>✅</emoji> <b>{} успешно взломан!</b>",
        "collecting_info": "<b><emoji document_id=6334778871258286021>💾</emoji> Сохранение информации о {}... {}%</b>",
        "collected_info": "<emoji document_id=5854762571659218443>✅</emoji> <b>Успешно нашёл и сохранил всю информацию о {}</b>",

        "hackp_process": "<emoji document_id=5370872220149099318>👮‍♀️</emoji> <b>Взлом пентагона в процессе... {}%</b>",
        "hackedp": "🟢 <b>Пентагон успешно взломан!</b>",
        "founding_nlo": "<b><emoji document_id=5371018382181145040>👽</emoji> Поиск секретных данных об НЛО ... {}%</b>",
        "dino_founded": "<emoji document_id=5460873384390830669>🦖</emoji> <b>Найдены данные о существовании динозавров на земле!</b>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "TYPING_SYMBOL",
                "_",
                lambda: "Печатающий символ в .ftype",
            ),
            loader.ConfigValue(
                "WAITING_TIME",
                0.05,
                lambda: "Сколько секунд будет ждать перед печатю каждой буквы в .ftype",
            )
        )


    async def client_ready(self, client, db):
        self.db = db
        self._client = client

    @loader.command()
    async def hacku(self, message):
        """Взлом пользователя"""

        us = utils.get_args_raw(message)
        if not us:
             return await utils.answer(message, self.strings["no_us"])

        perc = 0
 
        while(perc < 100):
                await utils.answer(message, self.strings["hacku_process"].format(us, perc))
                perc += random.randint(1, 3)
                await asyncio.sleep(0.3)
        
        await utils.answer(message, self.strings["hackedu"].format(us))

        await asyncio.sleep(3)

        perc = 0
 
        while(perc < 100):
            await utils.answer(message, self.strings["collecting_info"].format(us, perc))
            perc += random.randint(1, 5)
            await asyncio.sleep(0.33)
 
        await utils.answer(message, self.strings["collected_info"].format(us))

    @loader.command()
    async def hackp(self, message):
        """Взлом пентагона"""
        perc = 0
 
        while(perc < 100):
                await utils.answer(message, self.strings["hackp_process"].format(perc))
                perc += random.randint(1, 3)
                await asyncio.sleep(0.3)
        
        await utils.answer(message, self.strings["hackedp"])

        await asyncio.sleep(3)

        perc = 0
 
        while(perc < 100):
            await utils.answer(message, self.strings["founding_nlo"].format(perc))
            perc += random.randint(1, 5)
            await asyncio.sleep(0.33)
 
        await utils.answer(message, self.strings["dino_founded"])

    @loader.command()
    async def ftype(self, message):
        """Печатать текст"""
        orig_text = utils.get_args_raw(message)
        if not orig_text:
             return await utils.answer(message, self.strings["no_typing_text"])
        
        text = orig_text

        tbp = ""
        typing_symbol = self.config["TYPING_SYMBOL"]
        waiting_seconds = self.config["WAITING_TIME"]

        while(tbp != orig_text):
            await utils.answer(message, tbp + typing_symbol)
            await asyncio.sleep(waiting_seconds)
 
            tbp = tbp + text[0]
            text = text[1:]
 
            await utils.answer(message, tbp)
            await asyncio.sleep(waiting_seconds)