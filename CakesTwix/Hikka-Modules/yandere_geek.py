"""

    █▀▀ ▄▀█ █▄▀ █▀▀ █▀ ▀█▀ █░█░█ █ ▀▄▀
    █▄▄ █▀█ █░█ ██▄ ▄█ ░█░ ▀▄▀▄▀ █ █░█

    Copyleft 2022 t.me/CakesTwix                                                            
    This program is free software; you can redistribute it and/or modify 

"""

__version__ = (1, 2, 1)

# requires: aiohttp
# scope: inline
# scope: geektg_only
# scope: geektg_min 3.1.15
# meta pic: https://www.seekpng.com/png/full/824-8246338_yandere-sticker-yandere-simulator-ayano-bloody.png
# meta developer: @cakestwix_mods

import logging
import aiohttp
import asyncio
from .. import loader, main, utils
from ..inline import GeekInlineQuery, rand
from aiogram.types import InlineQueryResultPhoto
from aiogram.utils.markdown import quote_html

logger = logging.getLogger(__name__)


@loader.unrestricted
@loader.ratelimit
@loader.tds
class InlineMoebooruMod(loader.Module):
    """Module for obtaining art from the ImageBoard yande.re"""

    strings = {
        "name": "InlineYandere",
        "url": "https://yande.re/post.json",
        "vote_url": "https://yande.re/post/vote.json?login={login}&password_hash={password_hash}",
        "vote_text": "Vote for this art. The buttons are only available to me",
        "vote_ok": "OK!",
        "vote_login": "Login or password incorrect.",
        "vote_error": "ERROR, .logs 40 or .logs error",
        "cfg_yandere_login": "Login from yande.re",
        "cfg_yandere_password_hash": "SHA1 hashed password",
    }

    strings_ru = {
        "vote_text": "Голосуйте за этот арт. Кнопки доступны только мне",
        "vote_login": "Неверный логин или пароль.",
        "vote_error": "ОШИБКА, .logs 40 или .logs error",
        "cfg_yandere_login": "Войти через yande.re",
        "cfg_yandere_password_hash": "Хэшированный пароль SHA1",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            "yandere_login",
            "None",
            lambda m: self.strings("cfg_yandere_login", m),
            "yandere_password_hash",
            "None",
            lambda m: self.strings("cfg_yandere_password_hash", m),
        )
        self.name = self.strings["name"]

    async def client_ready(self, client, db) -> None:
        self.db = db
        self.client = client

    def string_builder(self, json):
        string = f"Tags : {quote_html(json['tags'])}\n"
        string += (
            f"©️ : {quote_html(json['author']) if json['author'] else 'No author'}\n"
        )
        string += (
            f"🔗 : {quote_html(json['source']) if json['source'] else 'No source'}\n\n"
        )
        string += f"🆔 : https://yande.re/post/show/{json['id']}"

        return string

    @loader.unrestricted
    @loader.ratelimit
    async def ylastcmd(self, message):
        """The last posted art"""
        await message.delete()

        async with aiohttp.ClientSession() as session:
            async with session.get(self.strings["url"]) as get:
                art_data = await get.json()
                await session.close()

        await message.client.send_file(
            message.chat_id,
            art_data[0]["sample_url"],
            caption=self.string_builder(art_data[0]),
        )

    @loader.unrestricted
    @loader.ratelimit
    async def yrandomcmd(self, message):
        """The random posted art"""
        await message.delete()

        params = "?tags=order:random"
        async with aiohttp.ClientSession() as session:
            async with session.get(self.strings["url"] + params) as get:
                art_data = await get.json()
                await session.close()

        await message.client.send_file(
            message.chat_id,
            art_data[0]["sample_url"],
            caption=self.string_builder(art_data[0]),
        )

    @loader.unrestricted
    @loader.ratelimit
    async def yvotecmd(self, message) -> None:
        """
        Vote for art

        Bad = -1, None = 0, Good = 1, Great = 2, Favorite = 3
        """
        reply = await message.get_reply_message()
        args = utils.get_args(message)
        if reply and args:
            yandere_id = reply.raw_text.split("🆔")[1].split("/")[5]

            params = {"id": yandere_id, "score": args[0]}
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.strings["vote_url"].format(
                        login=self.config["yandere_login"],
                        password_hash=self.config["yandere_password_hash"],
                    ),
                    data=params,
                ) as post:
                    result_code = post.status
                    await session.close()
            if result_code == 200:
                await utils.answer(message, self.strings("vote_ok"))
            elif result_code == 403:
                await utils.answer(message, self.strings("vote_login"))
            else:
                await utils.answer(message, self.strings("vote_error"))
            await asyncio.sleep(5)
            await message.delete()
            return
        elif reply:
            yandere_id = reply.raw_text.split("🆔")[1][2:]
            kb = [
                [
                    {
                        "text": "Bad",
                        "callback": self.inline__vote,
                        "args": [-1, yandere_id],
                    }
                ],
                [
                    {
                        "text": "Good",
                        "callback": self.inline__vote,
                        "args": [1, yandere_id],
                    }
                ],
                [
                    {
                        "text": "Great",
                        "callback": self.inline__vote,
                        "args": [2, yandere_id],
                    }
                ],
                [
                    {
                        "text": "Favorite",
                        "callback": self.inline__vote,
                        "args": [3, yandere_id],
                    }
                ],
            ]
            await self.inline.form(
                self.strings["vote_text"],
                message=message,
                reply_markup=kb,
                always_allow=self.client.dispatcher.security._owner,
            )
            return

        await utils.answer(message, "Pls code! Check help Yandere")
        await asyncio.sleep(5)
        await message.delete()

    # Inline commands
    async def ylast_inline_handler(self, query: GeekInlineQuery) -> None:
        """
        The last posted art (Inline)
        @allow: all
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(self.strings["url"]) as get:
                arts = await get.json()
                await session.close()

        inline_query = [
            InlineQueryResultPhoto(
                id=rand(20),
                title="Title",
                description="Description",
                caption=self.string_builder(art),
                thumb_url=art["preview_url"],
                photo_url=art["sample_url"],
                parse_mode="html",
            )
            for art in arts
        ]

        await query.answer(
            inline_query,
            cache_time=0,
        )

    async def yrandom_inline_handler(self, query: GeekInlineQuery) -> None:
        """
        The random posted art (Inline)
        @allow: all
        """
        params = "?tags=order:random"
        async with aiohttp.ClientSession() as session:
            async with session.get(self.strings["url"] + params) as get:
                arts = await get.json()
                await session.close()

        inline_query = [
            InlineQueryResultPhoto(
                id=rand(20),
                title="Title",
                description="Description",
                caption=self.string_builder(art),
                thumb_url=art["preview_url"],
                photo_url=art["sample_url"],
                parse_mode="html",
            )
            for art in arts
        ]

        await query.answer(
            inline_query,
            cache_time=0,
        )

    async def ysearch_inline_handler(self, query: GeekInlineQuery) -> None:
        """
        Search art by tags.  (https://yande.re/help)
        @allow: all
        """
        text = query.args

        if not text:
            return

        params = "?tags=order:random " + text
        async with aiohttp.ClientSession() as session:
            async with session.get(self.strings["url"] + params) as get:
                arts = await get.json()
                await session.close()

        inline_query = [
            InlineQueryResultPhoto(
                id=rand(20),
                title="Title",
                description="Description",
                caption=self.string_builder(art),
                thumb_url=art["preview_url"],
                photo_url=art["sample_url"],
                parse_mode="html",
            )
            for art in arts
        ]

        await query.answer(
            inline_query,
            cache_time=0,
        )

    # Inline button handler
    async def inline__close(self, call: "aiogram.types.CallbackQuery") -> None:
        await call.delete()

    async def inline__vote(self, call, score, _id) -> None:
        params = {"id": _id, "score": score}
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.strings["vote_url"].format(
                    login=self.config["yandere_login"],
                    password_hash=self.config["yandere_password_hash"],
                ),
                data=params,
            ) as post:
                result_code = post.status
                await session.close()
        kb = [[{"text": "🚫 Close", "callback": self.inline__close}]]

        if result_code == 200:
            await call.edit(self.strings("vote_ok"), reply_markup=kb)
        elif result_code == 403:
            await call.edit(self.strings("vote_login"), reply_markup=kb)
        else:
            await call.edit(self.strings("vote_error"), reply_markup=kb)
