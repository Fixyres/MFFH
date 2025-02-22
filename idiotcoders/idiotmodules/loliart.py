# meta pic: https://static.whypodg.me/mods!loliart.png
# meta banner: https://mods.whypodg.me/badges/loliart.jpg
# meta developer: @idiotcoders
# scope: hikka_only
# scope: hikka_min 1.2.10

import asyncio
import functools

import requests
from telethon.tl.types import Message

from .. import loader, utils


async def photo():
        link = "https://api.lolicon.app/setu/v2?tag=loli"
        img = (
            await utils.run_sync(
                requests.get,
                link
            )
        ).json()
        if img["error"] == "":
            return img["data"][0]["urls"]["original"]
                        
@loader.tds
class loliartMod(loader.Module):
    """Sends cute anime loli-art ☺"""

    strings = {
        "name": "LoliArt"
    }
    strings_ru = {"_cls_doc": "Отправляет милые лоли-арты ☺"}

    @loader.command(
        ru_doc="— Отправит милый лоли-арт"
    )
    async def lolicmd(self, message: Message):
        """— Send cute loli-art"""
        await self.inline.gallery(
            caption=lambda: f"<i>{utils.ascii_face()}</i>",
            message=message,
            next_handler=functools.partial(
                photo,
            ),
            preload=5,
        )
