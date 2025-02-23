"""

    █▀▀ ▄▀█ █▄▀ █▀▀ █▀ ▀█▀ █░█░█ █ ▀▄▀
    █▄▄ █▀█ █░█ ██▄ ▄█ ░█░ ▀▄▀▄▀ █ █░█

    Copyleft 2022 t.me/shadow_geektg                                                           
    This program is free software; you can redistribute it and/or modify 

"""

__version__ = (1, 0, 1)

# requires: requests
# meta pic: https://cdn-icons-png.flaticon.com/512/1005/1005340.png
# meta developer: @shadow_geektg, @cakestwix_mods
# scope: inline
# scope: hikka_only

import requests
import random
from .. import loader, utils
from telethon.tl.types import Message

async def photofox() -> str:
    """Fox photo handler"""
    return (await utils.run_sync(requests.get, "https://randomfox.ca/floof")).json()["image"]

async def photodog() -> str:
    """Dog photo handler"""
    return (await utils.run_sync(requests.get, "https://random.dog/woof.json")).json()["url"]


async def randomapi():
    randomapis = random.choice(["https://randomfox.ca/floof", "https://random.dog/woof.json", "http://aws.random.cat/meow"])
    if randomapis == "https://randomfox.ca/floof":
        return (await utils.run_sync(requests.get, "https://randomfox.ca/floof")).json()["image"]
    else:
        return (await utils.run_sync(requests.get, "https://random.dog/woof.json")).json()["url"]


@loader.tds
class FoxGalerryMod(loader.Module):
    """🦊 Foxes, Dogs 🐶 and cats 🐱"""
    strings = {"name": "FoxGallery"}

    async def foxescmd(self, message: Message) -> None:
        """🦊 Sending photos with foxes"""    
        await self.inline.gallery(
        message,
        photofox,
        )

    async def dogscmd(self, message: Message) -> None:
        """🐶 Sending photos with dogs"""    
        await self.inline.gallery(
        message,
        photodog,
        )

    async def randomcdfcmd(self, message: Message) -> None:
        """Photos of dogs 🐶 and foxes 🦊"""       
        await self.inline.gallery(
        message,
        randomapi,
        )
