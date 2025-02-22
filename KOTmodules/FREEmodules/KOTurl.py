# meta developer: @kotcheat

import requests
from .. import loader, utils

class URLShortenerMod(loader.Module):
    """Модуль для быстрого и безопастного сокращения URL (by @kotcheat)"""

    strings = {"name": "KOTURLShortener"}

    def __init__(self):
        self.name = self.strings["name"]

    async def urlsoccmd(self, message):
        """Сокращает URL"""
        args = utils.get_args_raw(message)
        if not args:
            await message.edit("Пожалуйста, предоставьте URL для сокращения.")
            return

        url = args.strip()
        shorten_url = await self.shorten_url(url)

        if shorten_url:
            await message.edit(f"Сокращённый URL: {shorten_url}")
        else:
            await message.edit("Не удалось сократить URL. Пожалуйста, проверьте правильность введённого URL.")

    async def shorten_url(self, url):
        response = requests.get(f"https://clck.ru/--?url={url}")

        if response.status_code == 200:
            return response.text
        else:
            return None
