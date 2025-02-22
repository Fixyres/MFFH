import random
from .. import loader
from telethon.tl.types import Message


@loader.tds
class кругляш(loader.Module):
    """Подпишись на канал @modwini"""

    strings = {"name": "кругляш"}

    async def krcmd(self, message: Message):
        """Кидает рандом видео сообщение из канала @kruglishik"""
        if message.out:
            await message.delete()

        await message.respond(
            f'<a href="https://t.me/kruglishik/{random.randint(6, 44)}">­</a>',
        )
