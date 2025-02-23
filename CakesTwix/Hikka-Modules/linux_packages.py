"""

    █▄▀ █ █░█░█ █ █▄░█ █ █▀▀ █▀▀ █▀█
    █░█ █ ▀▄▀▄▀ █ █░▀█ █ █▄▄ ██▄ █▀▄

    Copyleft 2022 t.me/KiwiNicer                                                            
    This program is free software; you can redistribute it and/or modify 

"""

__version__ = (1, 1, 0)

# requires: aiohttp
# meta pic: https://img.icons8.com/clouds/512/000000/linux-client.png
# meta developer: @KiwiNicer

import aiohttp
import logging
import asyncio

from aiogram.types import CallbackQuery
from typing import Union
from .. import loader, utils

logger = logging.getLogger(__name__)

# From Hikka https://github.com/hikariatama/Hikka/blob/master/hikka/utils.py#L459-L461
def chunks(_list: Union[list, tuple, set], n: int, /) -> list:
    """Split provided `_list` into chunks of `n`"""
    return [_list[i : i + n] for i in range(0, len(_list), n)]


@loader.tds
class LinuxPackagesMod(loader.Module):
    """Search package for Linux by name"""

    strings = {
        "name": "Packages",
        "no_name": "Pls give me name",
        "general_error": "<b>Unknown error</b> .-.",
        "string_list": "<b>List of packages in the {}</b>\n\n",
        "info_about": "<b>Info about</b> <code>{}</code>\n\n",
        "ver": "<b>Version:</b> {}\n",
        "description": "<b>Description:</b> {}\n",
        "maintainer": "<b>Maintainer:</b> {}\n",
        "no_packages": "<b>No packages</b>...",
    }

    strings_ru = {
        "no_name": "Пожалуйста, дайте мне имя пакета",
        "general_error": "<b>Неизвестная ошибка</b> .-.",
        "string_list": "<b>Список пакетов в {}</b>\n\n",
        "info_about": "<b>Информация о</b> <code>{}</code>\n\n",
        "ver": "<b>Версия:</b> {}\n",
        "description": "<b>Описание:</b> {}\n",
        "maintainer": "<b>Сопровождающий:</b> {}\n",
        "no_packages": "<b>Нет пакетов</b>...",
    }

    async def aurcmd(self, message):
        """Arch User Repository"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings["no_name"])
            return await asyncio.sleep(5)

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://aur.archlinux.org/rpc/?v=5&type=search&arg={args}"
            ) as get:
                if get.ok:
                    packages = await get.json()
                    if packages["resultcount"] == 0:
                        return await utils.answer(message, self.strings["no_packages"])

                    i = 1
                    reply_markup = []
                    string = self.strings["string_list"].format("AUR")
                    for package in packages["results"]:
                        string += f"{i}. {package['Name']}(v{package['Version']})\n"
                        reply_markup.append(
                            {
                                "text": str(i),
                                "callback": self.inline__get_package,
                                "args": [package["Name"], "AUR", args],
                            }
                        )

                        if i >= 10:
                            break

                        i = i + 1

                    await self.inline.form(
                        text=string,
                        message=message,
                        reply_markup=chunks(reply_markup, 5),
                        force_me=False,  # optional: Allow other users to access form (all)
                    )
                else:
                    await utils.answer(message, self.strings["general_error"])
                    return await asyncio.sleep(5)

    async def inline__get_package(
        self, call: CallbackQuery, Name: str, _type: str, search_arg: str
    ) -> None:
        if _type == "AUR":
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"https://aur.archlinux.org/rpc/?v=5&type=info&arg[]={Name}"
                ) as get:
                    if get.ok:
                        package = await get.json()
                    else:
                        await utils.answer(message, self.strings["general_error"])
                        return await asyncio.sleep(5)
            string = self.strings["info_about"].format(Name)
            string += self.strings["ver"].format(package["results"][0]["Version"])
            string += self.strings["description"].format(
                package["results"][0]["Description"]
            )
            string += self.strings["maintainer"].format(
                package["results"][0]["Maintainer"]
            )

            btn = [
                [
                    {
                        "text": "AUR",
                        "url": f"https://aur.archlinux.org/packages/{Name}",
                    },
                    {
                        "text": "Download snapshot",
                        "url": "https://aur.archlinux.org"
                        + package["results"][0]["URLPath"],
                    },
                ],
                [
                    {
                        "text": "Back",
                        "callback": self.inline__back,
                        "args": [search_arg, "AUR"],
                    }
                ],
            ]

        elif _type == "pacman":
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"https://www.archlinux.org/packages/search/json/?q={Name}"
                ) as get:
                    if get.ok:
                        package = await get.json()
                    else:
                        await utils.answer(message, self.strings["general_error"])
                        return await asyncio.sleep(5)
            string = self.strings["info_about"].format(Name)
            string += self.strings["ver"].format(package["results"][0]["pkgver"])
            string += self.strings["description"].format(
                package["results"][0]["pkgdesc"]
            )
            string += self.strings["maintainer"].format(
                package["results"][0]["maintainers"][0]
            )

            btn = [
                [
                    {
                        "text": "Pacman",
                        "url": f"https://archlinux.org/packages/{package['results'][0]['repo']}/{package['results'][0]['arch']}/{package['results'][0]['pkgname']}",
                    },
                ],
                [
                    {
                        "text": "Back",
                        "callback": self.inline__back,
                        "args": [search_arg, "pacman"],
                    }
                ],
            ]

        await call.edit(
            text=string,
            reply_markup=btn,  # optional: Change buttons in message. If not specified, buttons will be removed
            force_me=False,  # optional: Change button privacy mode
        )

    async def inline__back(self, call: CallbackQuery, Name: str, _type: str) -> None:
        if _type == "AUR":
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"https://aur.archlinux.org/rpc/?v=5&type=search&arg={Name}"
                ) as get:
                    if get.ok:
                        packages = await get.json()

                        i = 1
                        reply_markup = []
                        string = self.strings["string_list"].format("AUR")
                        for package in packages["results"]:
                            string += f"{i}. {package['Name']}(v{package['Version']})\n"
                            reply_markup.append(
                                {
                                    "text": str(i),
                                    "callback": self.inline__get_package,
                                    "args": [package["Name"], "AUR", Name],
                                }
                            )

                            if i >= 10:
                                break

                            i = i + 1

                        await call.edit(
                            text=string,
                            reply_markup=chunks(reply_markup, 5),
                            force_me=False,  # optional: Allow other users to access form (all)
                        )
                    else:
                        await utils.answer(message, self.strings["general_error"])
                        return await asyncio.sleep(5)
        elif _type == "pacman":
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"https://www.archlinux.org/packages/search/json/?q={Name}"
                ) as get:
                    if get.ok:
                        packages = await get.json()
                    if len(packages["results"]) == 0:
                        return await utils.answer(message, self.strings["no_packages"])

                    i = 1
                    reply_markup = []
                    string = self.strings["string_list"].format("pacman")
                    for package in packages["results"]:
                        string += f"{i}. {package['pkgname']}(v{package['pkgver']})\n"
                        reply_markup.append(
                            {
                                "text": str(i),
                                "callback": self.inline__get_package,
                                "args": [package["pkgname"], "pacman", Name],
                            }
                        )

                        if i >= 10:
                            break

                        i = i + 1

                await call.edit(
                    text=string,
                    reply_markup=chunks(reply_markup, 5),
                    force_me=False,  # optional: Allow other users to access form (all)
                )

    async def pacmancmd(self, message):
        """Pacman"""
        if not (args := utils.get_args_raw(message)):
            return
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://www.archlinux.org/packages/search/json/?q={args}"
            ) as get:
                if get.ok:
                    packages = await get.json()
                if len(packages["results"]) == 0:
                    return await utils.answer(message, self.strings["no_packages"])

                i = 1
                reply_markup = []
                string = self.strings["string_list"].format("pacman")
                for package in packages["results"]:
                    string += f"{i}. {package['pkgname']}(v{package['pkgver']})\n"
                    reply_markup.append(
                        {
                            "text": str(i),
                            "callback": self.inline__get_package,
                            "args": [package["pkgname"], "pacman", args],
                        }
                    )

                    if i >= 10:
                        break
                    i = i + 1

            await self.inline.form(
                text=string,
                message=message,
                reply_markup=chunks(reply_markup, 5),
                force_me=False,  # optional: Allow other users to access form (all)
            )
