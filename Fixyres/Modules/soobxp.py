from telethon import events
from .. import loader, utils
import asyncio

class soobxp(loader.Module):
    """
    Модуль для рассылки сообщений по заданным чатам от @Apostol_prince.
    """
    strings = {"name": "soobxp"}

    def __init__(self):
        self.chats = []
        self.message_to_send = None
        self.interval = 5  # Интервал по умолчанию в минутах
        self.running = False

    async def client_ready(self, client, db):
        self.client = client

    @loader.command()
    async def soob(self, message):
        """- сохранить сообщение для рассылки (использовать в ответ на сообщение)"""
        reply = await message.get_reply_message()
        if not reply:
            await message.edit("<b>Нет сообщения для сохранения. Используйте эту команду в ответ на сообщение.</b>")
            return
        self.message_to_send = reply
        await message.edit("<b>Сообщение сохранено для рассылки.</b>")

    @loader.command()
    async def slist(self, message):
        """- показать сохраненное сообщение для рассылки"""
        if not self.message_to_send:
            await message.edit("<b>Сообщение для рассылки не сохранено.</b>")
        else:
            await self.client.send_message(message.chat_id, self.message_to_send)

    @loader.command()
    async def dobchat(self, message):
        """- добавить чат в список для рассылки (использовать только с @username)"""
        args = utils.get_args_raw(message)
        if not args:
            await message.edit("<b>Укажите @username чата для добавления.</b>")
            return
        self.chats.append(args)
        await message.edit(f"<b>Чат {args} добавлен в список для рассылки.</b>")

    @loader.command()
    async def chatlist(self, message):
        """- показать список чатов для рассылки"""
        if not self.chats:
            await message.edit("<b>Список чатов для рассылки пуст.</b>")
        else:
            chat_list = "\n".join(self.chats)
            await message.edit(f"<b>Список чатов для рассылки:</b>\n{chat_list}")

    @loader.command()
    async def delchat(self, message):
        """- удалить чат из списка для рассылки (использовать только через @username)"""
        args = utils.get_args_raw(message)
        if not args:
            await message.edit("<b>Укажите @username чата для удаления.</b>")
            return
        if args in self.chats:
            self.chats.remove(args)
            await message.edit(f"<b>Чат {args} удален из списка для рассылки.</b>")
        else:
            await message.edit(f"<b>Чат {args} не найден в списке для рассылки.</b>")

    @loader.command()
    async def setinterval(self, message):
        """- установить интервал рассылки (в минутах)"""
        args = utils.get_args_raw(message)
        if not args or not args.isdigit():
            await message.edit("<b>Укажите интервал в минутах.</b>")
            return
        self.interval = int(args)
        await message.edit(f"<b>Интервал рассылки установлен на {self.interval} минут.</b>")

    @loader.command()
    async def startr(self, message):
        """- разослать сохраненное сообщение по указанным чатам через интервал времени"""
        if not self.message_to_send:
            await message.edit("<b>Нет сообщения для рассылки.</b>")
            return
        if not self.chats:
            await message.edit("<b>Список чатов для рассылки пуст.</b>")
            return

        await message.edit(f"<b>Начинаю рассылку каждые {self.interval} минут...</b>")
        self.running = True
        
        while self.running:
            for chat in self.chats:
                try:
                    await self.client.send_message(chat, self.message_to_send)
                except Exception as e:
                    await message.edit(f"<b>Ошибка при отправке в чат {chat}: {e}</b>")
            await asyncio.sleep(self.interval * 60)

    @loader.command()
    async def stopr(self, message):
        """- остановить рассылку сообщений"""
        if self.running:
            self.running = False
            await message.edit("<b>Рассылка сообщений остановлена.</b>")
        else:
            await message.edit("<b>Рассылка сообщений не активна.</b>")