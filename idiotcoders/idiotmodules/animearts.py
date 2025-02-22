# meta pic: https://static.whypodg.me/mods!animearts.png
# meta banner: https://mods.whypodg.me/badges/animearts.jpg
# meta developer: @idiotcoders
# scope: hikka_only
# scope: hikka_min 1.2.10

import asyncio
import functools

import requests
from telethon.tl.types import Message

from .. import loader, utils

async def photo():
    link = "https://api.waifu.pics/sfw/waifu"
    response = await utils.run_sync(requests.get, link)
    img = response.json()
    if "error" not in img:
        return img["url"]

async def nsfwphoto():
    link = "https://api.waifu.pics/nsfw/waifu"
    response = await utils.run_sync(requests.get, link)
    img = response.json()
    if "error" not in img:
        return img["url"]

@loader.tds
class animeartsMod(loader.Module):
    """Sends cute anime art"""

    strings = {
        "name": "AnimeArts"
    }
    strings_ru = {"_cls_doc": "Отправляет милые аниме-арты"}

    @loader.command(
        ru_doc="— Отправит милые аниме-арты"
    )
    async def artcmd(self, message: Message):
        """Sends cute anime-art"""
        await self.inline.gallery(
            caption=lambda: f"<i>{utils.ascii_face()}</i>",
            message=message,
            next_handler=functools.partial(
                photo,
            ),
            preload=5,
        )

    @loader.command(
        ru_doc="— Отправит nsfw аниме-арты"
    )
    async def nsfwartcmd(self, message: Message):
        """Sends nsfw anime-art"""
        await self.inline.gallery(
            caption=lambda: f"<i>{utils.ascii_face()}</i>",
            message=message,
            next_handler=functools.partial(
                nsfwphoto,
            ),
            preload=5,
        )
