"""

    █▀▀ ▄▀█ █▄▀ █▀▀ █▀ ▀█▀ █░█░█ █ ▀▄▀
    █▄▄ █▀█ █░█ ██▄ ▄█ ░█░ ▀▄▀▄▀ █ █░█

    Copyleft 2022 t.me/CakesTwix
    This program is free software; you can redistribute it and/or modify

"""

__version__ = (1, 0, 0)

# requires: aiohttp
# meta pic: https://www.pngall.com/wp-content/uploads/12/Avatar-Transparent.png
# meta developer: @cakestwix_mods

import logging
from .. import loader, utils
import aiohttp

logger = logging.getLogger(__name__)


@loader.tds
class RandomPeopleMod(loader.Module):
    """Create your new identity"""

    strings = {
        "name": "RandomPeople",
        "id":"Id",
        "uuid":"UUID",
        "firstname":"Firstname",
        "lastname":"Lastname",
        "username":"Username",
        "password":"Password",
        "email":"Email",
        "ip":"IP",
        "macAddress":"MAC-address",
        "website":"Website",
        "image":"Image",
    }

    strings_ru = {
        "name": "RandomPeople",
        "id":"Id",
        "uuid":"UUID",
        "firstname":"Имя",
        "lastname":"Фамилия",
        "username":"Юзернейм",
        "password":"Пароль",
        "email":"Почта",
        "ip":"IP",
        "macAddress":"MAC-адрес",
        "website":"Сайт",
        "image":"Фото",
    }


    async def prandomcmd(self, message):
        """Get random people"""
        async with aiohttp.ClientSession() as session:
            async with session.get("https://fakerapi.it/api/v1/users?_quantity=1") as get:
                b  = (await get.json())["data"][0]
                await session.close()

        string = "".join(f"<b>{self.strings[key]}</b>: <code>{val}</code>\n" for val, key in zip(b.values(), b.keys()))

        await utils.answer(message, string)
        

        
