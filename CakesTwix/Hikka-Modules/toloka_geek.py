"""

    █▀▀ ▄▀█ █▄▀ █▀▀ █▀ ▀█▀ █░█░█ █ ▀▄▀
    █▄▄ █▀█ █░█ ██▄ ▄█ ░█░ ▀▄▀▄▀ █ █░█

    Copyleft 2022 t.me/CakesTwix                                                            
    This program is free software; you can redistribute it and/or modify 

"""

__version__ = (1, 0, 1)

# scope: inline
# scope: geektg_only
# scope: geektg_min 3.1.15
# meta pic: https://img.icons8.com/external-others-iconmarket/512/000000/external-national-flags-others-iconmarket-5.png
# meta developer: @cakestwix_mods

import asyncio
import aiohttp
import logging
from aiogram.utils.markdown import hlink
from aiogram.types import (
    InlineQueryResultArticle,
    InputTextMessageContent,
)

from ..inline import GeekInlineQuery, rand
from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.unrestricted
@loader.ratelimit
@loader.tds
class HurtomMod(loader.Module):
    """Український торрент трекер"""

    strings = {
        "name": "InlineHurtom",
        "no_args": "🚫 <b>Будь ласка, введіть ключові слова, за якими я знайду Вам тему</b>",
        "no_args_inline": "Будь ласка, введіть ключові слова, за якими я знайду Вам тему",
        "no_args_inline_description": "ℹ Наприклад : Кот",
        "no_torrent": "🚫 Не було знайдено жодного торрента",
        "forum_name": "<b>Назва Розділу</b> : ",
        "comments": "<b>Коментарі</b> : ",
        "size": "<b>Розмір</b> : ",
        "size_inline": "Розмір: ",
        "seeders": "<b>Роздають</b> : ",
        "leechers": "<b>Завантажують</b> : ",
    }

    def stringBuilder(self, json):
        text = "<b>{}</b>\n".format(hlink(json["title"], json["link"]))
        text += (
            self.strings["forum_name"]
            + json["forum_name"]
            + " | "
            + json["forum_parent"]
            + "\n"
        )
        text += self.strings["comments"] + json["comments"] + "\n"
        text += self.strings["size"] + json["size"] + "\n"
        text += self.strings["seeders"] + json["seeders"] + "\n"
        text += self.strings["leechers"] + json["leechers"] + "\n"

        return text

    @loader.unrestricted
    @loader.ratelimit
    async def hsearchcmd(self, message):
        """Пошук по трекеру toloka.to (повертає перший елемент)"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings["no_args"])
            await asyncio.sleep(5)
            await message.delete()
            return

        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://toloka.to/api.php?search={args}") as get:
                if not get.ok:
                    return

                data = await get.json()
                if data == []:
                    await utils.answer(message, self.strings["no_torrent"])
                    return
            await session.close()

        await utils.answer(message, self.stringBuilder(data[0]))

    # Inline
    async def hsearch_inline_handler(self, query: GeekInlineQuery) -> None:
        """
        Пошук по трекеру toloka.to (Inline)
        @allow: all
        """
        text = query.args

        if not text:
            await query.answer(
                [
                    InlineQueryResultArticle(
                        id=1,
                        title=self.strings["no_args_inline"],
                        description=self.strings["no_args_inline_description"],
                        input_message_content=InputTextMessageContent(
                            self.strings["no_args"],
                            "HTML",
                            disable_web_page_preview=True,
                        ),
                        thumb_url="https://img.icons8.com/android/128/26e07f/ball-point-pen.png",
                        thumb_width=128,
                        thumb_height=128,
                    )
                ],
                cache_time=0,
            )
            return

        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://toloka.to/api.php?search={text}") as get:
                if not get.ok:
                    return

                data = await get.json()
                if data == []:
                    return
            await session.close()

        inline_query = [
            InlineQueryResultArticle(
                id=rand(50),
                title=torrent["title"],
                description=self.strings["size_inline"] + torrent["size"],
                input_message_content=InputTextMessageContent(
                    self.stringBuilder(torrent), "HTML", disable_web_page_preview=True
                ),
            )
            for torrent in data
        ]

        await query.answer(inline_query, cache_time=0)
