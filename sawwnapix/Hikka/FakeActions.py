# meta developer: @angellmodules

from telethon import events
from .. import loader
import asyncio

@loader.tds
class FakeActionsMod(loader.Module):
    """Модуль для имитации различных действий в чате."""
    strings = {"name": "FakeActions"}

    async def ftcmd(self, message):
        """<время в секундах>.
        Симулирует набор текста в чате указанное количество секунд."""
        await self.fake_action(message, "typing")

    async def ffcmd(self, message):
        """<время в секундах>.
        Симулирует отправку файла."""
        await self.fake_action(message, "document")

    async def fgcmd(self, message):
        """<время в секундах>.
        Симулирует запись голосового сообщения."""
        await self.fake_action(message, "record-audio")

    async def fvgcmd(self, message):
        """ <время в секундах>.
        Симулирует запись видео-сообщения."""
        await self.fake_action(message, "record-round")

    async def fpgcmd(self, message):
        """ <время в секундах>.
        Симулирует игру."""
        await self.fake_action(message, "game")

    async def fake_action(self, message, action):
        args = message.raw_text.split()
        if len(args) != 2 or not args[1].isdigit():
            await message.edit(f"Использование: .{message.raw_text.split()[0][1:]} <время в секундах>")
            return

        duration = int(args[1])
        await message.delete()
        async with message.client.action(message.chat_id, action):
            await asyncio.sleep(duration) 





#made by @sawwnapix
