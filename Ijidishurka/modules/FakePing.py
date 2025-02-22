import time
import random
import logging
from .. import loader, utils
from random import randint, choice
from asyncio import sleep

logger = logging.getLogger(__name__)


def register(cb):
    cb(fake_ping())


class fake_ping(loader.Module):
    """Подпишись на канал @modwini"""
    strings = {'name': 'fake ping v4'}

    async def pinjcmd(self, message):
        """Используй .pinj <цифры>."""
        text = utils.get_args_raw(message)
        if not text:
            for pinj in ["<code>🐻 Nofin...</code>"]:
                await message.edit(pinj)
                await sleep(0.3)

            named_tuple = time.localtime()
            time_string = time.strftime("%H:%M:%S", named_tuple)

            await message.edit(f"<b>⏱ Скорость отклика Telegram:</b>\n<code>{random.randint(10, 1999)}.{random.randint(10, 99)}</code> <b>ms</b>\n<b>😎 Прошло с последней перезагрузки: {time_string}</b>")
            return
        else:
            for pinj in ["<code>🐻 Nofin...</code>"]:
                await message.edit(pinj)
                await sleep(0.3)

            named_tuple = time.localtime()
            time_string = time.strftime("%H:%M:%S", named_tuple)
            
            pinj = (f"<b>⏱ Скорость отклика Telegram:</b>\n<code>{text}</code> <b>ms</b>\n<b>😎 Прошло с последней перезагрузки: {time_string}</b>")

            await message.edit(pinj)
