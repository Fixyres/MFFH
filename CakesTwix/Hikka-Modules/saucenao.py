"""

    █▀▀ ▄▀█ █▄▀ █▀▀ █▀ ▀█▀ █░█░█ █ ▀▄▀
    █▄▄ █▀█ █░█ ██▄ ▄█ ░█░ ▀▄▀▄▀ █ █░█

    Copyleft 2022 t.me/CakesTwix
    This program is free software; you can redistribute it and/or modify

"""

__version__ = (1, 1, 0)

# meta pic: https://img.icons8.com/external-flaticons-lineal-color-flat-icons/512/000000/external-anime-addiction-flaticons-lineal-color-flat-icons.png
# meta developer: @cakestwix_mods
# requires: saucenao_api
# scope: inline
# scope: hikka_only
# scope: hikka_min 1.2.7

import logging
import os
from .. import loader, utils
from saucenao_api import AIOSauceNao
from saucenao_api.errors import ShortLimitReachedError, LongLimitReachedError
from saucenao_api.containers import BasicSauce

logger = logging.getLogger(__name__)


def string_builder(sauce_item):
    string = "Unsupported type, sorry("
    if isinstance(sauce_item, BasicSauce):
        string = f"<b>Similarity</b>: <code>{sauce_item.similarity}</code>\n\n"

        string += f"<b>Title</b>: <code>{sauce_item.title}</code>\n"
        string += f"<b>Author</b>: <code>{sauce_item.author}</code>\n"
        string += f"<b>Urls</b>: {' '.join(sauce_item.urls)}\n"

    return string


@loader.tds
class SauceNaoMod(loader.Module):
    """🔎 SauceNao - image source locator"""

    strings = {
        "name": "SauceNao",
        "cfg_api_key": "https://saucenao.com/user.php?page=search-api",
        "no_args_reply": "🚫 Not found args or reply, pls check help",
        "wrong_url": "🚫 <b>Wrong Url</b>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            "CONFIG_API_KEY",
            None,
            lambda: self.strings("cfg_api_key"),
        )

    async def client_ready(self, client, db) -> None:
        self._db = db
        self._client = client

    # Just commands

    async def saucecmd(self, message):
        """🔗 Search for the source by link/photo"""
        if not self.config["CONFIG_API_KEY"]:
            return await utils.answer(message, "🚫 <b>No API Key</b>")
            
        results = None
        # If message has reply
        if reply := await message.get_reply_message():
            if reply.photo:
                async with AIOSauceNao(self.config["CONFIG_API_KEY"]) as aio:
                    try:
                        file_ = await self._client.download_media(reply.photo)
                        with open(file_, 'rb') as img:
                            results = await aio.from_file(img)
                        os.remove(file_)
                    except ShortLimitReachedError:
                        return await utils.answer(message, "🚫 <b>ShortLimitReachedError</b>")
                    except LongLimitReachedError:
                        return await utils.answer(message, "🚫 <b>LongLimitReachedError</b>")

        # If message not have reply, then get args from message
        if url := utils.get_args_raw(message):
            if utils.check_url(utils.get_args_raw(message)):
                async with AIOSauceNao(self.config["CONFIG_API_KEY"]) as aio:
                    try:
                        results = await aio.from_url(url)
                    except ShortLimitReachedError:
                        return await utils.answer(message, "🚫 <b>ShortLimitReachedError</b>")
                    except LongLimitReachedError:
                        return await utils.answer(message, "🚫 <b>LongLimitReachedError</b>")
            else:
                await utils.answer(message, self.strings["wrong_url"])
        
        if not results:
            return await utils.answer(message, self.strings["no_args_reply"])

        await self.inline.gallery(
            message,
            [url_photo.thumbnail for url_photo in results],
            [
                f"<b>Request limits (per 30 seconds limit)</b>: <code>{results.short_remaining}</code>\n<b>Request limits (per day limit)</b>: <code>{results.long_remaining}</code>\n"
                + string_builder(item)
                for item in results
            ],
        )
