version = (1, 4, 8, 9)

#meta banner: https://envs.sh/gQg.jpg
# meta developer: @moduleslist

from hikka import loader, utils
import asyncio
from datetime import datetime, timedelta
from telethon import functions

@loader.tds
class OtlozhkaMod(loader.Module):
    """Модуль для создания и удаления отложенных сообщений"""
    strings = {
        "name": "Otlozhka",
        "reqj": "🪐 Канал сборник различных модулей!",
        "no_scheduled": "❌ Нет отложенных сообщений для удаления",
        "deleted": "✅ Отложенные сообщения удалены: {}"
    }
    
    async def client_ready(self, client, db):
        self.db = db
        self.client = client
        
        await self.request_join(
            "@moduleslist",
            (
                self.strings['reqj']
            ),
            )

    async def otlozhkacmd(self, message):
        """Используй .otlozhka <время в минутах> <кол-во сообщений> <текст сообщения>"""
        args = utils.get_args_raw(message).split(' ', 2)

        if len(args) < 3:
            await message.edit("❗Пожалуйста, укажи время в минутах, количество сообщений и текст.")
            return

        if not args[0].isdigit() or not args[1].isdigit():
            await message.edit("❗Пожалуйста, укажи числовые значения для времени и количества сообщений.")
            return

        interval = int(args[0]) * 60  
        message_count = int(args[1])   
        text = args[2]                 
        chat_id = message.chat_id

        await message.edit("⌛ Подготовка...")

        for i in range(message_count):
            send_time = datetime.now() + timedelta(seconds=interval * i)
            await self.client.send_message(chat_id, text, schedule=send_time)

        await message.respond(f"✅ {message_count} сообщений запланированы на отправку с интервалом {interval // 60} минут.")

    async def rmotlozhkacmd(self, message):
        """Удаляет все отложенные сообщения в текущем чате"""
        chat_id = message.chat_id
        
        await message.edit("🔄 Поиск отложенных сообщений...")
        
        try:
            # Получаем все отложенные сообщения
            scheduled = await message.client(functions.messages.GetScheduledHistoryRequest(
                peer=chat_id,
                hash=0
            ))
            
            if not scheduled.messages:
                await message.edit(self.strings["no_scheduled"])
                return
            
            # Удаляем все отложенные сообщения
            await message.client(functions.messages.DeleteScheduledMessagesRequest(
                peer=chat_id,
                id=[msg.id for msg in scheduled.messages]
            ))
            
            count = len(scheduled.messages)
            await message.edit(self.strings["deleted"].format(count))
            
        except Exception as e:
            await message.edit(f"❌ Произошла ошибка: {str(e)}")