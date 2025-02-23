"""

    █▀▀ ▄▀█ █▄▀ █▀▀ █▀ ▀█▀ █░█░█ █ ▀▄▀
    █▄▄ █▀█ █░█ ██▄ ▄█ ░█░ ▀▄▀▄▀ █ █░█

    Copyleft 2022 t.me/CakesTwix
    This program is free software; you can redistribute it and/or modify

"""

__version__ = (2, 0, 1)

# meta pic: http://assets.stickpng.com/images/5cb78671a7c7755bf004c14b.png
# meta developer: @cakestwix_mods
# scope: hikka_only
# requires: httpx

import logging
import re

import httpx
from aiogram.utils.markdown import hlink
from telethon.errors.rpcerrorlist import BotResponseTimeoutError

from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class TikTokMod(loader.Module):
    """Yet Another TikTok Downloader"""

    strings = {
        "name": "YATikTok-DL",
        "no_args": "🚫 Not found args, pls check help",
        "no_item": "Couldn't find it("
    }

    strings_ru = {
        "name": "YATikTok-DL",
        "no_args": "🚫 Аргументы не найдены, пожалуйста, проверьте справку",
        "no_item": "Не нашел(("
    }

    async def client_ready(self, client, db) -> None:
        self._db = db
        self._client = client

    async def ttdlcmd(self, message):
        """Download video/music from tiktok"""
        args = utils.get_args_raw(message)
        if not args:
            return await utils.answer(message, self.strings["no_args"])

        elif "www.tiktok.com" in args or "vm.tiktok.com" in args:
            async with httpx.AsyncClient() as client:
                if tik_info := re.findall(r'\/.*\/([\d]*)?', (await client.head(args)).headers["Location"] if "vm.tiktok.com" in args else args):
                    tik_get = (await client.get("http://api.tiktokv.com/aweme/v1/multi/aweme/detail/?aweme_ids=[" + tik_info[0])).json()
                    logger.debug(tik_get)
                    await self.inline.form(
                        message=message,
                        text=hlink(tik_get["aweme_details"][0]["share_info"]["share_title"], tik_get["aweme_details"][0]["share_info"]["share_url"]),
                        reply_markup=[[{"text":"Without watermark", "callback": self.download__callback, "args": (tik_get["aweme_details"][0]["video"]["play_addr"]["url_list"][0], message.to_id)}, {"text":"With watermark", "callback": self.download__callback, "args": (tik_get["aweme_details"][0]["video"]["download_addr"]["url_list"][0], message.to_id)}], [{"text":"Audio", "callback": self.download__callback, "args": (tik_get["aweme_details"][0]["music"]["play_url"]["url_list"][0], message.to_id)}]],
                        photo=tik_get["aweme_details"][0]["video"]["origin_cover"]["url_list"][0]
                    )
                else:
                    await utils.answer(message, "")
                

    async def download__callback(self, call, url, id_):
        await self._client.send_file(id_, url)
        await call.delete()
