from hikkatl.types import Message
from .. import loader, utils
import aiohttp
import os

"""
    ███    ███ ██    ██ ██████  ██    ██ ██       ██████  ███████ ███████
    ████  ████ ██    ██ ██   ██ ██    ██ ██      ██    ██ ██      ██  
    ██ ████ ██ ██    ██ ██████  ██    ██ ██      ██    ██ ███████ █████
    ██  ██  ██ ██    ██ ██   ██ ██    ██ ██      ██    ██      ██ ██  
    ██      ██  ██████  ██   ██  ██████  ███████  ██████  ███████ ███████ 


    Compliments
    📜 Licensed under the GNU AGPLv3	
"""


# meta desc: desc
# meta developer: @BruhHikkaModules
# requires: aiohttp


@loader.tds
class compliments(loader.Module):
    """Генерирует комплименты"""

    strings = {"name": "Compliments"}

    @loader.command()
    async def gen_compliment(self, message: Message):
        """- Генерирует комлпимент"""
        async with aiohttp.ClientSession() as session:
            async with session.get("http://complimentr.com/api") as response:
                data = await response.json()
                await utils.answer(
                    message,
                    await self._client.translate(
                        message.peer_id,
                        message,
                        "ru",
                        raw_text=data["compliment"],
                        entities=message.entities,
                    ),
                )
