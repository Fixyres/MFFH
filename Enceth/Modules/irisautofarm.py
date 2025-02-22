# meta developer: @Enceth
from datetime import datetime, timedelta
from telethon.tl.types import Message
from .. import loader, utils

@loader.tds
class IrisFarm(loader.Module):
    """Автофарм Iris с помощью автоотправки """

    strings = {
        "name": "IrisFarm",
    }

    async def client_ready(self, client, db):
        self.client = client
        self.iris_bot = 5443619563  

    @loader.command()
    async def autofarm(self, message: Message):
        """Запускает автофарм"""
        await utils.answer(message, "Запускаю автофарм...")
        
        for i in range(100):  
            schedule_time = datetime.now() + timedelta(hours=4 * (i + 1))
            await self.client.send_message(self.iris_bot, "Ферма", schedule=schedule_time)
        
        await utils.answer(message, "Автофарм запущен.")
