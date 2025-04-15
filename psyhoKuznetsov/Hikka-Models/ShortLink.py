__version__ = (1, 0, 0)
# meta developer: @psyhomodules

from .. import loader, utils
import aiohttp
import asyncio
import urllib.parse
import re

@loader.tds
class ShortLinkMod(loader.Module):
    """Сократитель ссылок"""

    strings = {
        "name": "ShortLink",
        "shortened": "<b>✅ Короткая ссылка:</b> <code>{}</code>",
        "error": "<b>❌ Ошибка сокращения:</b> {}",
        "invalid_url": "<b>🤔 Введите действительную ссылку (начинается с http:// или https://)</b>",
    }

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    async def shorten_tinyurl(self, url):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://tinyurl.com/api-create.php?url={urllib.parse.quote(url)}", headers={"User-Agent": "Mozilla/5.0"}) as response:
                    if response.status == 200:
                        return await response.text()
                    return None, f"Ошибка: статус {response.status}"
        except Exception as e:
            return None, str(e)

    async def shorten_l8nu(self, url):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post("https://l8.nu/", data={"url": url}, headers={"User-Agent": "Mozilla/5.0"}) as response:
                    if response.status == 200:
                        text = await response.text()
                        match = re.search(r"https://l8\.nu/[a-zA-Z0-9]+", text)
                        return match.group(0) if match else None, "Ошибка: ссылка не найдена в ответе"
                    return None, f"Ошибка: статус {response.status}"
        except Exception as e:
            return None, str(e)

    async def shorten_clckru(self, url):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://clck.ru/--?url={urllib.parse.quote(url)}", headers={"User-Agent": "Mozilla/5.0"}) as response:
                    if response.status == 200:
                        return await response.text()
                    return None, f"Ошибка: статус {response.status}"
        except Exception as e:
            return None, str(e)

    async def shorten_kuttit(self, url):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post("https://kutt.it/api/v2/links", json={"target": url}, headers={"User-Agent": "Mozilla/5.0"}) as response:
                    if response.status in (200, 201):
                        data = await response.json()
                        return data.get("link"), "Ошибка: ссылка не найдена в JSON"
                    return None, f"Ошибка: статус {response.status}"
        except Exception as e:
            return None, str(e)

    async def shorten_isgd(self, url):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://is.gd/create.php?format=simple&url={urllib.parse.quote(url)}", headers={"User-Agent": "Mozilla/5.0"}) as response:
                    if response.status == 200:
                        return await response.text()
                    return None, f"Ошибка: статус {response.status}"
        except Exception as e:
            return None, str(e)

    @loader.command()
    async def tiny(self, message):
        """Сократить ссылку через TinyURL: .tiny <ссылка>"""
        await self.shorten(message, self.shorten_tinyurl)

    @loader.command()
    async def l8nu(self, message):
        """Сократить ссылку через L8.nu: .l8nu <ссылка>"""
        await self.shorten(message, self.shorten_l8nu)

    @loader.command()
    async def clckru(self, message):
        """Сократить ссылку через Clck.ru: .clckru <ссылка>"""
        await self.shorten(message, self.shorten_clckru)

    @loader.command()
    async def kuttit(self, message):
        """Сократить ссылку через Kutt.it: .kuttit <ссылка>"""
        await self.shorten(message, self.shorten_kuttit)

    @loader.command()
    async def isgd(self, message):
        """Сократить ссылку через Is.gd: .isgd <ссылка>"""
        await self.shorten(message, self.shorten_isgd)

    async def shorten(self, message, shortener_func):
        """Общая логика сокращения"""
        args = utils.get_args_raw(message)
        if not args or not args.startswith(("http://", "https://")):
            await utils.answer(message, self.strings["invalid_url"])
            return

        result = await shortener_func(args)
        if isinstance(result, tuple):
            result, error = result
            if result:
                await utils.answer(message, self.strings["shortened"].format(result))
            else:
                await utils.answer(message, self.strings["error"].format(error))
        else:
            if result:
                await utils.answer(message, self.strings["shortened"].format(result))
            else:
                await utils.answer(message, self.strings["error"].format("Не удалось сократить ссылку"))
