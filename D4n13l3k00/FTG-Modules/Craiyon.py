# .------.------.------.------.------.------.------.------.------.------.
# |D.--. |4.--. |N.--. |1.--. |3.--. |L.--. |3.--. |K.--. |0.--. |0.--. |
# | :/\: | :/\: | :(): | :/\: | :(): | :/\: | :(): | :/\: | :/\: | :/\: |
# | (__) | :\/: | ()() | (__) | ()() | (__) | ()() | :\/: | :\/: | :\/: |
# | '--'D| '--'4| '--'N| '--'1| '--'3| '--'L| '--'3| '--'K| '--'0| '--'0|
# `------`------`------`------`------`------`------`------`------`------'
#
#                     Copyright 2023 t.me/D4n13l3k00
#           Licensed under the Creative Commons CC BY-NC-ND 4.0
#
#                    Full license text can be found at:
#       https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode
#
#                           Human-friendly one:
#            https://creativecommons.org/licenses/by-nc-nd/4.0

# meta developer: @D4n13l3k00

import base64
import io
from typing import List

import aiohttp
from PIL import Image
from telethon import types

from .. import loader, utils  # type: ignore


@loader.tds
class CraiyonMod(loader.Module):
    "Craiyon - Mini DALL-E for FTG"
    strings = {
        "name": "Craiyon",
        "preparing": "<b>[Craiyon] 📥 Preparing...</b>",
        "generating": "<b>[Craiyon] ✨ Generating images...</b>",
        "uploading": "<b>[Craiyon] 📤 Uploading images...</b>",
        "result_with_url": "<b>[Craiyon] 🎉 Generated images:</b>\n{}",
        "error": "<b>[Craiyon]\n❌ Python error:</b>\n<code>{}</code>\n<b> 📜 Response of server:</b>\n<code>{}</code>",
    }

    async def client_ready(self, client, db):
        self.me = await client.get_me()
        self.telegraph_short_name = "Craiyon-FTG"
        self.telegraph_author_name = (
            f"@{self.me.username or self.me.id} via Craiyon-FTG by @DekFTGModules"
        )
        self.telegraph_author_url = "https://t.me/DekFTGModules"
        self.db = db

    class NullResponseError(Exception):
        """Raised when the response is null or has no 'images' key"""

        pass

    @loader.owner
    async def craiyoncmd(self, m: types.Message):
        ".craiyon <text> - Generate images with text using Craiyon (Mini DALL-E)"

        args = utils.get_args_raw(m)

        async with aiohttp.ClientSession() as session:
            m = await utils.answer(m, self.strings("preparing", m))
            async with session.post(
                "https://api.telegra.ph/createAccount",
                json={
                    "short_name": self.telegraph_short_name,
                    "author_name": self.telegraph_author_name,
                    "author_url": self.telegraph_author_url,
                },
            ) as resp:
                try:
                    data = await resp.json(content_type=None)
                    if "error" in data:
                        raise self.NullResponseError(
                            "No images in response (has no 'images' key)"
                        )
                except Exception as e:
                    err_json = await resp.text()
                    await utils.answer(
                        m, self.strings("error", m).format(str(e), err_json)
                    )
                    return
                try:
                    self.author_name = data["result"]["author_name"]
                    self.author_url = data["result"]["author_url"]
                    self.access_token = data["result"]["access_token"]
                except KeyError:
                    await utils.answer(
                        m,
                        self.strings("error", m).format(
                            "No author_name, author_url or access_token in response",
                            data,
                        ),
                    )
                    return

            m = await utils.answer(m, self.strings("generating", m))
            async with session.post(
                "https://backend.craiyon.com/generate",
                json={
                    "prompt": args,
                },
                headers={
                    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0",
                },
            ) as resp:
                try:
                    data = await resp.json(content_type=None)
                    if "images" not in data:
                        raise self.NullResponseError(
                            "No images in response (has no 'images' key)"
                        )
                except Exception as e:
                    err_json = await resp.text()
                    await utils.answer(
                        m, self.strings("error", m).format(str(e), err_json)
                    )
                    return
                imgs: List[io.BytesIO] = []
                uploaded_imgs = []
                await utils.answer(m, self.strings("uploading", m))
                for i in data["images"]:
                    image_data = base64.b64decode(i.encode())
                    image = Image.open(io.BytesIO(image_data))
                    image_buffer = io.BytesIO()
                    image.save(image_buffer, format="JPEG")
                    imgs.append(image_buffer)
                for i, img in enumerate(imgs, 1):
                    img.name = f"craiyon-{i}.jpg"
                    file = aiohttp.FormData()
                    file.add_field("file", img.getvalue(), content_type="image/jpeg")
                    async with session.post(
                        "https://telegra.ph/upload", data=file
                    ) as resp:
                        try:
                            data = await resp.json(content_type=None)
                            if "error" in data:
                                raise self.NullResponseError(
                                    "Error API: {}".format(data)
                                )
                            uploaded_imgs.append(data[0]["src"])
                        except Exception as e:
                            err_json = await resp.text()
                            await utils.answer(
                                m, self.strings("error", m).format(str(e), err_json)
                            )
                            return

            async with session.post(
                "https://api.telegra.ph/createPage",
                json={
                    "title": "Craiyon-FTG",
                    "content": [
                        {
                            "tag": "img",
                            "attrs": {"src": i},
                        }
                        for i in uploaded_imgs
                    ],
                    "access_token": self.access_token,
                },
            ) as resp:
                if resp.status != 200:
                    await utils.answer(
                        self.strings("error", m).format(
                            f"Status code: {resp.status}", await resp.text()
                        )
                    )
                    return
                try:
                    data: dict = await resp.json(content_type=None)
                except Exception as e:
                    err_json = await resp.text()
                    await utils.answer(
                        m, self.strings("error", m).format(str(e), err_json)
                    )
                    return
                page_url = data["result"]["url"]

            await utils.answer(m, self.strings("result_with_url", m).format(page_url))
