import random
from .. import loader
from telethon.tl.types import Message


@loader.tds
class amogus(loader.Module):
    """Подпишись на канал @modwini"""

    strings = {"name": "amogus"}

    async def amoguscmd(self, message: Message):
        """Скидывает видео с амогусом (работает в чатах где отключено медиa)"""
        if message.out:
            await message.delete()

        await message.respond(
            f'<a href="https://t.me/radiofmonline/{random.randint(233, 236)}">­</a>',
        )
