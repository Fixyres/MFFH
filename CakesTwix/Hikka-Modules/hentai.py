"""

    █▀▀ ▄▀█ █▄▀ █▀▀ █▀ ▀█▀ █░█░█ █ ▀▄▀
    █▄▄ █▀█ █░█ ██▄ ▄█ ░█░ ▀▄▀▄▀ █ █░█

    Copyleft 2022 t.me/CakesTwix
    This program is free software; you can redistribute it and/or modify

"""

__version__ = (2, 0, 1)

# meta pic: https://seeklogo.com/images/H/hentai-haven-logo-B9D8C4B3B8-seeklogo.com.png
# meta developer: @cakestwix_mods
# requires: NHentai-API

import logging
from typing import Union

from NHentai import NHentaiAsync, CloudFlareSettings

from .. import loader, utils
from ..inline import GeekInlineQuery, rand
from aiogram.utils.markdown import hlink
import asyncio

logger = logging.getLogger(__name__)

# From Hikka https://github.com/hikariatama/Hikka/commit/03f7c71557acd6e14e816df4de932dd55668fd97#diff-b020ffc1f4d0e66f2cfd8724370d8ee28197d945f9d0f2cf7e4358717e71e27cR439-R441
def chunks(_list: Union[list, tuple, set], n: int, /) -> list:
    """Split provided `_list` into chunks of `n`"""
    return [_list[i : i + n] for i in range(0, len(_list), n)]

def StringBuilder(Hentai):
    tags = "".join(f"{hlink(tag.name, tag.url)} " for tag in Hentai.tags)
    langs = "".join(f"{hlink(lang.name, lang.url)} " for lang in Hentai.languages)
    
    text = f"{hlink(Hentai.title.english, Hentai.url)} [{Hentai.id}]\n\n"
    text += f"{tags} \n\n"

    text += f"Language: {langs} \n"
    text += f"❤️ {Hentai.total_favorites} | 📄 {Hentai.total_pages}"
    return text

@loader.tds
class NHentaiMod(loader.Module):
    """🍓 Hentai doujin module 18+"""

    strings = {
        "name": "NHentai",
        "no_tags": "🎞 <b>No hentai by your query :(</b>",
        "no_digit": "1️⃣ <b>Please give me a number.</b>",
    }

    strings_ru = {
        "name": "🍓 NHentai",
        "no_tags": "🎞 <b>Не нашел хентая по твоему запросу :(</b>",
        "no_digit": "1️⃣ <b>Пожалуйста, дайте мне число.</b>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            "CONFIG_CSRFTOKEN",
            "",
            lambda: self.strings("cfg_csrftoken"),
            "CONFIG_CF_CLEARANCE",
            "",
            lambda: self.strings("cfg_cf_clearance"),
        )

    async def client_ready(self, client, db) -> None:
        self.nhentai_async = NHentaiAsync(request_settings=CloudFlareSettings(csrftoken=self.config["CONFIG_CSRFTOKEN"],
                                                                              cf_clearance=self.config["CONFIG_CF_CLEARANCE"]))

    async def nhrandomcmd(self, message):
        """🎲 Random hentai doujin"""
        hentai = await self.nhentai_async.get_random()
        await message.delete()
        await message.client.send_file(message.chat_id, hentai.cover.src, caption=StringBuilder(hentai))

    async def nhlastcmd(self, message):
        """⌚️ Latest hentai doujin"""
        hentai = await self.nhentai_async.get_doujin((await self.nhentai_async.get_page(page=1)).doujins[0].id)
        await message.delete()
        await message.client.send_file(message.chat_id, hentai.cover.src, caption=StringBuilder(hentai))

    async def nhidcmd(self, message):
        """1️⃣ Hentai doujin by id"""
        if args:= utils.get_args_raw(message):
            if not args.isdigit():
                return await message.answer(message, self.strings["no_digit"])

            hentai = await self.nhentai_async.get_doujin(args)
            await message.client.send_file(message.chat_id, hentai.cover.src, caption=StringBuilder(hentai))

    async def nhsearchcmd(self, message):
        """🔎 Search hentai doujin"""
        if args:= utils.get_args_raw(message):
            hentai = await self.nhentai_async.search(args)
            markup = [[{"text":"Link", "url":hentai.doujins[0].url}]]
            if len(hentai.doujins) != 1:
                markup.append([{"text":"➡️","callback": self.hentai_pagination__callback, "args": (hentai.doujins, 0, "+")}])
            await self.inline.form(
                text=StringBuilder(hentai.doujins[0]),
                message=message,
                photo=hentai.doujins[0].cover.src,
                reply_markup=markup,
            )

    # Just callbacks

    async def hentai_pagination__callback(self, call, list_doujins, index, type_button):
        markup = [[{"text":"Link", "url": list_doujins[index].url}],[]]
        if type_button == "+":
            index += 1
            markup[1].append({"text":"⬅️","callback": self.hentai_pagination__callback, "args": (list_doujins, index, "-")})
            if index != len(list_doujins) - 1:
                markup[1].append({"text":"➡️","callback": self.hentai_pagination__callback, "args": (list_doujins, index, "+")})
        else:
            index -= 1
            if index != 0:
                markup[1].append({"text":"⬅️","callback": self.hentai_pagination__callback, "args": (list_doujins, index, "-")})

            markup[1].append({"text":"➡️","callback": self.hentai_pagination__callback, "args": (list_doujins, index, "+")})
        await call.edit(text=StringBuilder(list_doujins[index]), reply_markup=markup, photo=list_doujins[index].cover.src)