# meta developer: @kotcheat

import asyncio
import functools
import json
import random
from urllib.parse import quote_plus

import requests
from telethon.tl.types import Message

from .. import loader, utils

phrases = ["Kawaii!", "Daisuki!", "Sugoi!", "Hai!", "Arigato!", "Moe!", "Yoroshiku!", "Oishii!"]

async def get_image_url(api_url: str) -> str:
    try:
        response = await utils.run_sync(requests.get, api_url)
        response.raise_for_status()
        data = response.json()
        if 'url' in data:
            return data['url']
        elif 'images' in data and data['images']:
            return data['images'][0]['url']
        elif 'results' in data and data['results']:
            return data['results'][0]['url']
        else:
            return "No image found."
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

async def photo(self, args: str) -> str:
    apis = [
        f"https://api.waifu.im/search?included_tags={args}",
        f"https://api.waifu.pics/sfw/{args}",
        f"https://waifu.pics/api/{args}"
    ]
    api_url = random.choice(apis)
    return await get_image_url(api_url)

@loader.tds
class KOTaiwaifu(loader.Module):
    """Этот модуль позволяет вам легко получать изображения waifu из различных источников ( @kotcheat )"""

    strings = {"name": "KOTaiwaifu"}

    strings_ru = {
        "_cmd_doc_waf": "Любимая вайфу",
        "_cls_doc": "Этот модуль позволяет вам легко получать изображения waifu из различных источников ( @kotcheat )",
    }

    async def client_ready(self, client, db):
        self.categories = ["maid", "waifu", "marin-kitagawa", "mori-calliope", "raiden-shogun", "oppai", "selfies", "uniform", "kamisato-ayaka", "neko"]

    @loader.pm
    async def wafcmd(self, message: Message):
        """Send anime pic"""
        args = utils.get_args_raw(message)
        args = "waifu" if args not in self.categories else args
        pic = functools.partial(photo, self=self, args=args)
        await self.inline.gallery(
            message=message,
            next_handler=pic,
            caption=lambda: f"<i>{random.choice(phrases)}</i> {utils.ascii_face()}",
        )
