# meta developer: @amm1e & @AmeMods

import requests
import random
from .. import loader, utils
from hikkatl.types import Message

@loader.tds
class uselesswmod(loader.Module):
    """Useless mod for useless sites."""
    strings = {"name": "uselessweb"}
    strings_en = {"Web": "<emoji document_id=5318759457801385682>👍</emoji> <b>Your random site</b>: "}
    strings_ru = {"Web": "<emoji document_id=5318759457801385682>👍</emoji> <b>Ваш рандомный сайт</b>: "}

    @loader.command(
        en_doc = "- Random useless site"
    )
    async def uselessweb(self, message):
        """- Рандомный бесполезный сайт."""
        response = requests.get('https://gist.githubusercontent.com/quest/07bbc6908f84b50a9fc8/raw/d8983a0723d07203816b78953ff52f07423c808d/uselessweb.json')
        file = response.json()
        uselesswebr = random.choice(file['uselessweb'])
        await message.edit(self.strings("Web") + uselesswebr)
