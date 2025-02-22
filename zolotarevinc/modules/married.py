# meta pic: https://static.whypodg.me/mods!irisfarm.png
# meta banner: https://mods.whypodg.me/badges/irisfarm.jpg
# meta developer: @zolotarevxc
# scope: hikka_only
# scope: hikka_min 1.2.10

from .. import loader, utils
import asyncio

class MarriedFarm(loader.Module):
    """Модуль для фарма колец в @MarriedGroupBot 🌘 ʕ·ᴥ· ʔ"""

    strings = {
        "name": "MarriedFarm",
        "description": "Модуль для фарма колец в @MarriedGroupBot 🌘 ʕ·ᴥ· ʔ",
        "developer": "Разработчик: @zolotarevxc 🌟"
    }

    def __init__(self):
        self.running = False 

    async def farmdoncmd(self, message):
        """Включить автоматическую отправку /job 🚀"""
        if self.running:
            await message.edit("<b>❎Процесс уже запущен!</b>")
            return

        self.running = True
        await message.edit("<b>✅Автоматическая отправка /job запущена!</b>")

        while self.running:
            await message.client.send_message(message.chat.id, "/job")
            await asyncio.sleep(1800)  # 30 минут

    async def farmdoffcmd(self, message):
        """Отключить автоматическую отправку /job ⚡️"""
        if not self.running:
            await message.edit("<b>❎Процесс не запущен!</b>")
            return

        self.running = False
        await message.edit("<b>❎Автоматическая отправка /job остановлена!</b>")

    async def on_load(self):
        """При загрузке модуля выводим описание и информацию о разработчике"""
        await utils.answer(message, f"{self.strings['description']}\n{self.strings['developer']}")

