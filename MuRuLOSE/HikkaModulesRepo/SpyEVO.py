# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# '''Если вы хотите взять какую то идею, то упомяните меня в коде, спасибо (но функцию пишите сами)'''

# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# Not licensed
# meta developer: @bruhHikkaModules
__version__ = (0, 1, 5)

from telethon.tl.types import Message, ChatAdminRights
from telethon import functions
import asyncio
from .. import loader, utils
import re
from ..inline.types import InlineCall

"""
    ███    ███ ██    ██ ██████  ██    ██ ██       ██████  ███████ ███████
    ████  ████ ██    ██ ██   ██ ██    ██ ██      ██    ██ ██      ██  
    ██ ████ ██ ██    ██ ██████  ██    ██ ██      ██    ██ ███████ █████
    ██  ██  ██ ██    ██ ██   ██ ██    ██ ██      ██    ██      ██ ██  
    ██      ██  ██████  ██   ██  ██████  ███████  ██████  ███████ ███████ 


    SpyEVO
    📜 Licensed under the GNU AGPLv3	
"""

# meta desc: desc
# meta developer: @BruhHikkaModules


@loader.tds
class SpyEVO(loader.Module):
    """Модуль для"""

    strings = {
        "name": "SpyEVO",
    }

    @loader.watcher()
    async def watcher(self, message):
        converts = self.get("converts", 0)
        r_converts = self.get("r_converts", 0)
        case = self.get("case", 0)
        r_case = self.get("r_case", 0)
        mif = self.get("mif", 0)
        crystal = self.get("crystal", 0)
        plasma = self.get("plasma", 0)
        zv = self.get("zv", 0)
        scrap = self.get("scrap", 0)
        medals = self.get("medals", 0)

        if message.chat_id == 5522271758 and message.text == "✉ Ты нашел(ла) конверт.":
            converts += 1
            self.set("converts", converts)
        if (
            message.chat_id == 5522271758
            and message.text == "🧧 Ты нашел(ла) редкий конверт."
        ):
            r_converts += 1
            self.set("r_converts", converts)
        if message.chat_id == 5522271758 and message.text == "📦 Ты нашел(ла) Кейс!":
            case += 1
            self.set("case", case)
        if (
            message.chat_id == 5522271758
            and message.text == "🗳 Ты нашел(ла) Редкий Кейс!"
        ):
            r_case += 1
            self.set("r_case", r_case)
        if (
            message.chat_id == 5522271758
            and message.raw_text == "🕋 Ты нашел(ла) Мифический Кейс!"
        ):
            mif += 1
            self.set("mif", mif)
        if (
            message.chat_id == 5522271758
            and message.raw_text == "💎 Ты нашел(ла) Кристальный Кейс!"
        ):
            crystal += 1
            self.set("crystal", crystal)
        if message.chat_id == 5522271758 and "🎆 Ты нашел(ла) 1 плазму" in message.text:
            plasma += 1
            self.set("plasma", plasma)
        if message.chat_id == 5522271758 and "💫" in message.text:
            zv += 1
            self.set("zv", zv)
        if message.chat_id == 5522271758 and "🎆 Ты нашел(ла) 2 плазмы" in message.text:
            plasma += 2
            self.set("plasma", plasma)
        if message.chat_id == 5522271758 and "Медаль" in message.text:
            pattern = "Медаль +(.*?)</b>"
            match = re.search(pattern, message.text, re.DOTALL)
            if match:
                medali = int(match.group(1))
                medals += medali
                self.set("medals", medals)
        if message.chat_id == 5522271758 and "Скрап" in message.text:
            pattern = "Скрап +(.*?)</b>"
            match = re.search(pattern, message.text, re.DOTALL)
            if match:
                scrapi = int(match.group(1))
                scrap += scrapi
                self.set("scrap", scrap)

    @loader.command()
    async def show_spy(self, message):
        """Показывает кейсы за всё время работы модуля"""
        convert = self.get("converts", 0)
        r_convert = self.get("r_converts", 0)
        case = self.get("case", 0)
        r_case = self.get("r_case", 0)
        mif = self.get("mif", 0)
        crystal = self.get("crystal", 0)
        zv = self.get("zv", 0)
        plasma = self.get("plasma", 0)
        medals = self.get("medals", 0)
        scrap = self.get("scrap", 0)
        await utils.answer(
            message,
            f"<b>💼 Ваши Кейсы (будем расстягивать для красоты):</b>\n\n✉ <b>Конверты:</b> <code>{convert}</code>\n🧧 <b>Редкие конверты:</b> <code>{r_convert}</code>\n📦 <b>Кейсы:</b> <code>{case}</code>\n🗳 <b>Редкие кейсы:</b> <code>{r_case}</code>\n🕋 <b>Мифические кейсы:</b> <code>{mif}</code>\n💎 <b>Кристальные кейсы</b> <code>{crystal}</code>\n🌌<b>Звездные Кейсы:</b> <code>{zv}</code>\n\n<b>🏺 Ресурсы:</b>\n\n🎆 <b>Плазма:</b> <code>{plasma}</code>\n\n<b>👺 Боссы:</b>\n\n🎖 <b>Медали:</b> <code>{medals}</code>\n🔩 <b>Скрап:</b> <code>{scrap}</code>",
        )

    @loader.command()
    async def clear_spy(self, message):
        """Очистка базы данных (всех кейсов и тд)"""
        await self.inline.form(
            text="Вы уверены что хотите очистить базу данных модуля?",
            message=message,
            reply_markup=[
                [
                    {
                        "text": "Да",
                        "callback": self.cleardb,
                    },
                    {
                        "text": "Нет",
                        "action": "close",
                    },
                ]
            ],
        )

    async def cleardb(self, call: InlineCall):
        # пака статистика
        self.set("converts", 0)
        self.set("r_converts", 0)
        self.set("case", 0)
        self.set("r_case", 0)
        self.set("mif", 0)
        self.set("crystal", 0)
        self.set("plasma", 0)
        self.set("zv", 0)
        call.edit(call, "Статистика о кейсах и плазме очищена")
