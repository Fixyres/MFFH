# meta developer: @codeer_kot
# не меняйте мой код, пожалуйста, указывая что вы создатель этого модуля.
from .. import loader, utils
import asyncio

@loader.tds
class KOTfarm(loader.Module):
    """автофармит коины в ирисе, самый простой код."""
    strings = {'name': 'KOTfarm'}

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.running = False 

    @loader.command()
    async def rfarm(self, message):
        """запустить автофарм"""
        chat_id = message.chat_id

        if self.running:
            await message.reply("автофарм уже запущен.")
            return

        self.running = True 
        await message.reply(f"автоферма в чате {chat_id} запущена.")
        asyncio.create_task(self.iris(chat_id))

    @loader.command()
    async def rsfarm(self, message):
        """останавливает автофарм"""
        if not self.running:
            await message.reply("автоферма не запущена.")
            return

        self.running = False
        await message.reply("автоферма остановлена.")

    async def iris(self, chat_id):
        await asyncio.sleep(14400)

        if not self.running: 
            return

        await self.client.send_message(chat_id, 'ферма')
        await self.iris(chat_id)
