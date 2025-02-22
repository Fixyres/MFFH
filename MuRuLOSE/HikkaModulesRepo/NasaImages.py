from hikkatl.types import Message
from .. import loader, utils
import aiohttp
import random

"""
    ███    ███ ██    ██ ██████  ██    ██ ██       ██████  ███████ ███████
    ████  ████ ██    ██ ██   ██ ██    ██ ██      ██    ██ ██      ██  
    ██ ████ ██ ██    ██ ██████  ██    ██ ██      ██    ██ ███████ █████
    ██  ██  ██ ██    ██ ██   ██ ██    ██ ██      ██    ██      ██ ██  
    ██      ██  ██████  ██   ██  ██████  ███████  ██████  ███████ ███████ 


    NasaImages
    📜 Licensed under the GNU AGPLv3	
"""

# meta banner: https://0x0.st/HgMS.jpg
# meta desc: Images from Nasa website
# meta developer: @BruhHikkaModules
# requires: aiohttp


@loader.tds
class NasaImages(loader.Module):
    """Images from Nasa website"""

    strings = {
        "name": "NasaImages", 
        "your-image": "<b>🌠 Here's your random picture</b>",
        "wait": "🕑 <b>Hold on a bit...</b>"
    }

    strings_ru = {
        "your-image": "<b>🌠 Вот ваша случайная картинка</b>",
        "wait": "🕑 <b>Подождите немного...</b>"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "api-key",
                "DEMO_KEY",
                lambda: "Here is api key, but developer removed it, so put api key yourself (demo key is demo key, its limited)",
                validator=loader.validators.Hidden(),
            ),
        )
        self._api = "https://api.nasa.gov/"
        self._photos_route = f"mars-photos/api/v1/rovers/curiosity/photos?sol=1000&api_key={self.config['api-key']}"
        self._today_astronome_pic_route = f"planetary/apod?api_key={self.config['api-key']}"

    @loader.command(
        ru_doc=" - Получите случайное фото с вебсайта наса ",
    )
    async def randomcosmosphoto(self, message: Message):
        """- Get random photo from Nasa website"""

        await utils.answer(message, self.strings["wait"])

        async with aiohttp.ClientSession() as session:
            async with session.get(self._api + self._photos_route) as response:
                data = await response.json()
                url = data["photos"][random.randint(0, len(data["photos"]))]["img_src"]

                await utils.answer_file(
                    message, file=url, caption=self.strings["your-image"]
                )

    @loader.command(
        ru_doc=" - Сегодняшее астрономическое фото "
    )
    async def todaycosmocpic(self, message: Message):
        ''' - Today astronomic picture'''

        await utils.answer(message, self.strings["wait"])

        async with aiohttp.ClientSession() as session:
            async with session.get(self._api + self._today_astronome_pic_route) as response:
                data = await response.json()
                url = data['url']

                await utils.answer_file(
                    message, file=url, caption=f"<b>{data['title']}</b>"
                )
