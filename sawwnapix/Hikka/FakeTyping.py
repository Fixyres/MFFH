# meta developer: @angellmodules

from telethon import events
from .. import loader
import asyncio

@loader.tds
class FakeTypingMod(loader.Module):
    """Модуль для имитации набора текста!"""
    strings = {"name": "FakeTyping"}

    async def fpcmd(self, message):
        """<время в секундах>.
        """
        args = message.raw_text.split()
        if len(args) != 2 or not args[1].isdigit():
            await message.edit("Использование: .fp <время в секундах>")
            return
        
        duration = int(args[1])
        await message.delete()
        async with message.client.action(message.chat_id, "typing"):
            await asyncio.sleep(duration)




#made by @sawwnapix
