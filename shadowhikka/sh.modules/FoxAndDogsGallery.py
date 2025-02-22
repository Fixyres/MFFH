# █▀ █░█ ▄▀█ █▀▄ █▀█ █░█░█
# ▄█ █▀█ █▀█ █▄▀ █▄█ ▀▄▀▄▀

# Copyright 2023 t.me/shadow_modules
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# meta developer: @shadow_modules
# scope: hikka_only
# meta banner: https://i.imgur.com/nZalKg2.jpeg

import requests
import random
from .. import loader, utils
from telethon.tl.types import Message  # type: ignore


async def photofox() -> str:
    """Fox photo handler"""
    return (await utils.run_sync(requests.get, "https://randomfox.ca/floof")).json()[
        "image"
    ]


async def photodog() -> str:
    """Dog photo handler"""
    return (await utils.run_sync(requests.get, "https://random.dog/woof.json")).json()[
        "url"
    ]


async def randomapi():
    randomapis = random.choice(
        ["https://randomfox.ca/floof", "https://random.dog/woof.json"]
    )
    if randomapis == "https://randomfox.ca/floof":
        return (
            await utils.run_sync(requests.get, "https://randomfox.ca/floof")
        ).json()["image"]
    elif randomapis == "https://random.dog/woof.json":
        return (
            await utils.run_sync(requests.get, "https://random.dog/woof.json")
        ).json()["url"]


@loader.tds
class FoxGalerryMod(loader.Module):
    """🦊 Foxes, Dogs 🐶"""

    strings = {"name": "FoxGallery"}

    strings_ru = {
        "_cls_doc": "🦊 Лисички, Песики 🐶",
        "_cmd_doc_foxes": "🦊 Лисички",
        "_cmd_doc_dogs": "🐶 Песики",
        "_cmd_doc_random": "🦊 Лисички и Песики 🐶",
    }

    async def foxescmd(self, message: Message):
        """🦊 Sending photos with foxes"""
        await self.inline.gallery(message, photofox)

    async def dogscmd(self, message: Message):
        """🐶 Sending photos with dogs"""
        await self.inline.gallery(message, photodog)

    async def randomcdfcmd(self, message: Message):
        """Photos of dogs 🐶 and foxes 🦊"""
        await self.inline.gallery(message, randomapi)
