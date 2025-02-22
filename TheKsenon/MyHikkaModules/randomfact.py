from .. import loader, utils
import aiohttp
import logging

# meta developer: @kmodules
__version__ = (1, 0, 0)

@loader.tds
class RandomFactMod(loader.Module):
    """Рандомные факты"""

    strings = {
        "name": "RandomFact",
        "loading": "<emoji document_id=5420239291508868251>⭐️</emoji> <b>Думаю над рандомным фактом...</b>",
        "fact": "<emoji document_id=5422847414694330750>🪙</emoji> <b>{}</b>",
        "error": "Error occurred while fetching fact. Please try again."
    }
    
    strings_ru = {
        "name": "RandomFact",
        "loading": "<emoji document_id=5420239291508868251>⭐️</emoji> <b>Думаю над рандомным фактом...</b>",
        "fact": "<emoji document_id=5422847414694330750>🪙</emoji> <b>{}</b>",
        "error": "Произошла ошибка при получении факта. Пожалуйста, попробуйте снова."
    }

    async def client_ready(self, client, db):
        self.client = client
        
    @loader.command()
    async def randomfact(self, message):
        """Получить случайный факт"""
        await utils.answer(message, self.strings["loading"])
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('http://aeza.theksenon.pro/v1/api/fact', 
                                    headers={'Content-Type': 'application/json'}) as response:
                    if response.status == 200:
                        fact = await response.text()
                        await utils.answer(message, self.strings["fact"].format(fact))
                    else:
                        await utils.answer(message, self.strings["error"])
        except Exception as e:
            logging.exception(e)
            await utils.answer(message, self.strings["error"])
          
