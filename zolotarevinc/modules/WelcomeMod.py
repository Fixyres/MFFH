# meta pic: https://static.whypodg.me/mods!irisfarm.png
# meta banner: https://mods.whypodg.me/badges/irisfarm.jpg
# meta developer: @zolotarevxc
# scope: hikka_only
# scope: hikka_min 1.2.10

from .. import loader, utils
import asyncio

class WelcomeModule(loader.Module):
    """Модуль для автоматического приветствия новых участников чата"""

    strings = {
        "name": "WelcomeModule",
        "description": "Модуль для автоматического приветствия новых участников чата 🌟",
        "developer": "Разработчик: @zolotarevxc 🫶",
        "welon_cmd": "▫️ .welon Включить автоматическое приветствие новых участников",
        "weloff_cmd": "▫️ .weloff Выключить автоматическое приветствие новых участников"
    }

    def __init__(self):
        self.running = False

    async def weloncmd(self, message):
        """Включить автоматическое приветствие новых участников"""
        if self.running:
            await message.edit("<b>❎Автоматическое приветствие уже включено!</b>")
            return

        self.running = True
        await message.edit("<b>✅Автоматическое приветствие новых участников включено!</b>")

    async def weloffcmd(self, message):
        """Выключить автоматическое приветствие новых участников"""
        if not self.running:
            await message.edit("<b>❎Автоматическое приветствие не включено!</b>")
            return

        self.running = False
        await message.edit("<b>❎Автоматическое приветствие новых участников выключено!</b>")

    async def on_chat_member(self, event):
        """Обработчик новых участников"""
        if self.running and event.new_chat_members:
            for new_member in event.new_chat_members:
                welcome_message = f"👋 Привет, {new_member.full_name}! Добро пожаловать в наш чат! 🌟"
                await event.chat.send_message(welcome_message)

    async def on_load(self):
        """При загрузке модуля выводим описание и информацию о разработчике"""
        await utils.answer(message, f"{self.strings['description']}\n{self.strings['developer']}\n\n{self.strings['welon_cmd']}\n{self.strings['weloff_cmd']}")
