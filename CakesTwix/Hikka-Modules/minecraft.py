"""

    █▀▀ ▄▀█ █▄▀ █▀▀ █▀ ▀█▀ █░█░█ █ ▀▄▀
    █▄▄ █▀█ █░█ ██▄ ▄█ ░█░ ▀▄▀▄▀ █ █░█

    Copyleft 2022 t.me/CakesTwix                                                            
    This program is free software; you can redistribute it and/or modify 

"""

__version__ = (1, 1, 0)

# requires: aiohttp
# meta pic: https://icons.iconarchive.com/icons/blackvariant/button-ui-requests-2/1024/Minecraft-2-icon.png
# meta developer: @cakestwix_mods

import logging
import aiohttp
from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class InlineMinecraftInfoMod(loader.Module):
    """Information about players and server status"""

    strings = {
        "name": "MinecraftInfo",
        "error_message": "🚫 This entity does not exist or you entered it incorrectly",
        "about_user": "<b>Available player information</b> <code>{}</code>:'\n",
        "about_server": "<b>Available server information</b> <code>{}</code>:'\n",
        "username": "<b>Username:</b> <code>{}</code>\n",
        "id": "<b>Id:</b> <code>{}</code>\n",
        "description": "<b>Description</b>: {}\n",
        "latency": "<b>Latency</b>: {}\n",
        "players": "<b>Players</b>: {} in {}\n",
        "versions": "<b>Versions</b>: {}\n",
    }

    strings_ru = {
        "error_message": "🚫 Этот объект не существует или вы ввели его неправильно",
        "about_user": "<b>Доступная информация об игроке</b> <code>{}</code>:'\n",
        "about_server": "<b>Доступная информация о сервере</b> <code>{}</code>:'\n",
        "username": "<b>Имя игрока:</b> <code>{}</code>\n",
        "id": "<b>Id:</b> <code>{}</code>\n",
        "description": "<b>Описание</b>: {}\n",
        "latency": "<b>Задержка</b>: {}\n",
        "players": "<b>Игроки</b>: {} in {}\n",
        "versions": "<b>Версии</b>: {}\n",
    }

    base_url = "https://api.minetools.eu"

    async def mucheckcmd(self, message):
        """Check user by username"""
        if args := utils.get_args_raw(message):
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/uuid/{args}") as get:
                    data = await get.json()
                    if data["status"] == "ERR":
                        return await utils.answer(
                            message, self.strings["error_message"]
                        )

                async with session.get(f"{self.base_url}/profile/{data['id']}") as get:
                    user = await get.json()

            text = self.strings["about_user"].format(user["decoded"]["profileName"])
            text += self.strings["id"].format(user["decoded"]["profileId"])
            text += self.strings["username"].format(user["decoded"]["profileName"])

            for texture in user["decoded"]["textures"]:
                text += f"<b>{texture}</b>: <a href={user['decoded']['textures'][texture]['url']}>URL</a>\n"

            await utils.answer(message, text)

    async def mpingcmd(self, message):
        """Ping minecraft server"""
        if args := utils.get_args_raw(message):
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/ping/{args}") as get:
                    data = await get.json()
                    if "error" in data:
                        return await utils.answer(
                            message, self.strings["error_message"]
                        )

            text = self.strings["about_user"].format(args)
            text += self.strings["description"].format(data["description"])
            text += self.strings["latency"].format(data["latency"])
            text += self.strings["players"].format(
                data["players"]["online"], data["players"]["max"]
            )
            text += self.strings["versions"].format(data["version"]["name"])

            await utils.answer(message, text)
