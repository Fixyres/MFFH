import random
from .. import loader
from telethon.tl.types import Message


@loader.tds
class catt(loader.Module):
    """Подпишись на канал @modwini"""

    strings = {"name": "catt"}

    async def cattcmd(self, message: Message):
        """Скидывает видео с котиком (работает в чатах где отключено медиa)"""
        if message.out:
            await message.delete()

        await message.respond(
            f'<a href="https://t.me/radiofmonline/{random.randint(282, 283)}">­</a>',
        )
