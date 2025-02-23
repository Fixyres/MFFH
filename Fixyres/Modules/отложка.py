__version__ = (1, 3)

# meta developer: @lorcyt

from hikka import loader, utils
import asyncio
from datetime import datetime, timedelta

@loader.tds
class ScheduledMessagesMod(loader.Module):
    """отправка отложенных сообщений более простым и гибким способом"""
    strings = {"name": "otl"}
    
    async def client_ready(self, client, db):
        self.db = db
        self.client = client

    async def отлcmd(self, message):
        """Используй .otl <время в минутах> <кол-во сообщений> <текст сообщения>"""
        args = utils.get_args_raw(message).split(' ', 2)

        if len(args) < 3:
            await message.edit("Пожалуйста, укажи время в минутах, количество сообщений и текст.")
            return

        if not args[0].isdigit() or not args[1].isdigit():
            await message.edit("Пожалуйста, укажи числовые значения для времени и количества сообщений.")
            return

        interval = int(args[0]) * 60  
        message_count = int(args[1])   
        text = args[2]                 
        chat_id = message.chat_id

        await message.edit("Сообщения будут запланированы.")

        for i in range(message_count):
            send_time = datetime.now() + timedelta(seconds=interval * i)
            await self.client.send_message(chat_id, text, schedule=send_time)

        await message.respond(f"{message_count} сообщений запланированы на отправку с интервалом {interval // 60} минут.")