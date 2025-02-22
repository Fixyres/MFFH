from hikkatl.types import Message
from hikkatl.errors.rpcerrorlist import WebpageCurlFailedError
from .. import loader, utils
import aiohttp
from ..inline.types import InlineCall
import logging

"""
    ███    ███ ██    ██ ██████  ██    ██ ██       ██████  ███████ ███████
    ████  ████ ██    ██ ██   ██ ██    ██ ██      ██    ██ ██      ██  
    ██ ████ ██ ██    ██ ██████  ██    ██ ██      ██    ██ ███████ █████
    ██  ██  ██ ██    ██ ██   ██ ██    ██ ██      ██    ██      ██ ██  
    ██      ██  ██████  ██   ██  ██████  ███████  ██████  ███████ ███████ 


    RandomDog
    📜 Licensed under the GNU AGPLv3	
"""

# meta banner: https://0x0.st/HYVq.jpg
# meta desc: desc
# meta developer: @BruhHikkaModules

# requires: aiohttp

logger = logging.getLogger(__name__)


@loader.tds
class RandomDogs(loader.Module):
    """Get random pictures with dogs"""

    strings = {
        "name": "RandomDogs",
        "dog": "🐶 <b>There's your doggy!</b>",
        "update": "🔄 Update",
        "close": "❌ Close",
        "wait": "⌚ <b>Wait a little while and you'll see a doggie</b>",
        "error": "😢 Looks like the API returned a non-existent image :(\n\n🦉 Tip: Try update the image",
    }
    strings_ru = {
        "dog": "🐶 <b>Вот твоя собачка!</b>",
        "update": "🔄 Обновить",
        "close": "❌ Закрыть",
        "wait": "⌚ <b>Подождите немного, и вы увидите собачку</b>",
        "error": "😢 Похоже что API вернул несуществующую картинку :(\n\n🦉 Совет: Попробуйте обновить картинку",
    }

    def __init__(self):
        self.api = "https://random.dog/"

        self.markup = [
            [
                {"text": self.strings["update"], "callback": self.update},
                {"text": self.strings["close"], "action": "close"},
            ]
        ]

    async def get_data(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.api + "woof.json") as res:
                data = await res.json()

        return data

    @loader.command(
        ru_doc=" - Просто возращает картинку собачки",
    )
    async def catchdog(self, message: Message):
        """- Just return the picture of the dog"""

        await utils.answer(message, self.strings["wait"])

        data = await self.get_data()

        try:
            await self.inline.form(
                message=message,
                text=self.strings["dog"],
                photo=data["url"],
                reply_markup=self.markup,
            )
        except WebpageCurlFailedError:
            await self.inline.form(
                message=message, text=self.strings["error"], reply_markup=self.markup
            )

    async def update(self, call: InlineCall):
        await call.edit(text=self.strings["wait"])

        data = await self.get_data()

        try:
            await call.edit(
                text=self.strings["dog"], photo=data["url"], reply_markup=self.markup
            )
        except WebpageCurlFailedError:
            await call.edit(text=self.strings["error"], reply_markup=self.markup)
