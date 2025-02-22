# meta developer: @codeer_kot
# не меняйте мой код, пожалуйста, указывая что вы создатель этого модуля.
from .. import loader, utils
import asyncio

@loader.tds
class KOTdick(loader.Module):
    """каждый час отправляю дик в чат"""
    strings = {'name': 'KOTdick'}

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.running = False 

    @loader.command()
    async def dick(self, message):
        """запустить дик"""
        chat_id = message.chat_id

        if self.running:
            await message.reply("Отправка /dick уже запущена!")
            return

        self.running = True 
        await message.reply(f"Отправка /dick в чат {chat_id} запущена.")
        asyncio.create_task(self.кот(chat_id))

    @loader.command()
    async def stopdick(self, message):
        """Останавливает отправку /dick"""
        if not self.running:
            await message.reply("Отправка /dick не запущена.")
            return

        self.running = False
        await message.reply("Отправка /dick остановлена.")

    async def кот(self, chat_id):
        await asyncio.sleep(3600)

        if not self.running: 
            return

        await self.client.send_message(chat_id, '/dick')
        await self.кот(chat_id)
