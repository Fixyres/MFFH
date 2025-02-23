"""

    █▀▀ ▄▀█ █▄▀ █▀▀ █▀ ▀█▀ █░█░█ █ ▀▄▀
    █▄▄ █▀█ █░█ ██▄ ▄█ ░█░ ▀▄▀▄▀ █ █░█

    # Copyleft 2022 t.me/CakesTwix                                                            
    This program is free software; you can redistribute it and/or modify 

"""

__version__ = (1, 0, 1)

# requires: requests hentai
# meta pic: https://seeklogo.com/images/H/hentai-haven-logo-B9D8C4B3B8-seeklogo.com.png
# meta developer: @cakestwix_mods

import asyncio
import logging

from hentai import Hentai, Utils
from requests.exceptions import HTTPError

from .. import loader, utils

logger = logging.getLogger(__name__)

# Utils
def StringBuilder(Hentai):
    id_nh = Hentai.id
    eng_name = Hentai.title()
    link = Hentai.url
    total_pages = Hentai.num_pages
    total_favorites = Hentai.num_favorites
    tags = "".join(f"{tag.name} " for tag in Hentai.tag)
    text = f"<a href={link}>{eng_name}</a> [{id_nh}]\n\n"
    text += f"{tags} \n"
    text += f"❤️ {total_favorites} | 📄 {total_pages}"
    return text


def ListHentaiBuilder(Hentais):
    text = ""
    for i, Hentai in enumerate(Hentais, start=1):
        id_nh = Hentai.id
        eng_name = Hentai.title()
        link = Hentai.url
        total_pages = Hentai.num_pages
        total_favorites = Hentai.num_favorites

        text += f"{i}: <a href={link}>{eng_name}</a> [{id_nh}] / "
        text += f"❤️ {total_favorites} | 📄 {total_pages} \n"
    return text


@loader.unrestricted
@loader.ratelimit
@loader.tds
class NHentaiMod(loader.Module):
    """Hentai module 18+ Legacy"""

    strings = {
        "name": "NHentai",
    }

    @loader.unrestricted
    @loader.ratelimit
    async def nhrandomcmd(self, message):
        """Random hentai manga"""
        await message.delete()
        hentai_info = Utils.get_random_hentai()
        text = StringBuilder(hentai_info)

        await message.client.send_file(message.chat_id, hentai_info.cover, caption=text)

    @loader.unrestricted
    @loader.ratelimit
    async def nhtagcmd(self, message):
        """Search hentai manga by tag"""
        if args := utils.get_args(message):
            hentai_info = Utils.search_by_query(args)
            text = ListHentaiBuilder(hentai_info)

            await utils.answer(message, text)
        else:
            await utils.answer(message, "Pls tags")
            await asyncio.sleep(5)
            await message.delete()

    @loader.unrestricted
    @loader.ratelimit
    async def nhidcmd(self, message):
        """Search hentai manga by id"""
        args = utils.get_args(message)
        if args[0].isdigit():
            try:
                hentai_info = Hentai(args[0])
                text = StringBuilder(hentai_info)
                await message.client.send_file(
                    message.chat_id, hentai_info.cover, caption=text
                )
            except HTTPError as e:
                await utils.answer(message, str(e))
                await asyncio.sleep(5)
                await message.delete()
        else:
            await utils.answer(message, "Pls id")
            await asyncio.sleep(5)
            await message.delete()
