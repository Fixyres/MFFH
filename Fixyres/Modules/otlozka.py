# meta developer: @lorcyt

from hikka import loader, utils
import asyncio
from datetime import datetime, timedelta

@loader.tds
class ScheduledMessagesMod(loader.Module):
    """отправка отложенных сообщений более простым и гибким способо. слито тут - @mqone"""
    strings = {"name": "отложка"}
    
    async def client_ready(self, client, db):
        self.db = db
        self.client = client
        self.interval = 3600  
        self.message_count = 10  

    async def t_cmd(self, message):
        """Используй .t_ <интервал в минутах> """
        args = utils.get_args_raw(message)
        if not args.isdigit():
            await message.edit("Пожалуйста, укажите интервал в минутах используя числа нужные вам")
            return
        
        self.interval = int(args) * 60  
        await message.edit(f"Интервал сообщений установлен на {args} минут")

    async def c_cmd(self, message):
        """Используй .c_ <количество> чтобы установить нужное количество сообщений"""
        args = utils.get_args_raw(message)
        if not args.isdigit():
            await message.edit("Пожалуйста, укажи количество сообщений")
            return
        
        self.message_count = int(args)
        await message.edit(f"Количество сообщений  {args}.")

    async def te_cmd(self, message):
        """Используй .te_ <текст сообщения>"""
        args = utils.get_args_raw(message)
        chat_id = message.chat_id
        
        if not args:
            await message.edit("Пожалуйста, укажи текст сообщения")
            return

        await message.edit("Сообщения будут запланированы")

        for i in range(self.message_count):
            send_time = datetime.now() + timedelta(seconds=self.interval * i)
            await self.client.send_message(chat_id, args, schedule=send_time)

        await message.respond(f"{self.message_count} сообщений запланированы на отправку с интервалом {self.interval // 60} минут.")