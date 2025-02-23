import asyncio
from telethon import events, tl
from .. import loader, utils
import re
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import JoinChannelRequest

class MassSMS(loader.Module):
    """Модуль для рассылок"""

    strings = {"name": "MassSMS"}

    def __init__(self):
        self.chats = []
        self.interval = 60
        self.is_mass = False
        self.mass_task = None
        self.mass_message = None

    async def addchatcmd(self, message):
        """Добавь чат в список дял рассылки. Использование: .addchat <ссылка или @username>"""
        link = utils.get_args_raw(message)

        if not link:
            await message.reply("Ты забыл указать ссылку или юзернейм")
            return

        try:
            if link.startswith('@'):
                chat = await self.client.get_entity(link)
            elif 't.me/' in link or 'telegram.me/' in link:
                username = re.search(r't\.me/(\w+)', link)
                if username:
                    chat = await self.client.get_entity(username.group(1))
                else:
                    invite_hash = re.search(r't\.me/joinchat/([a-zA-Z0-9_-]+)', link)
                    if invite_hash:
                        chat = await self.client(ImportChatInviteRequest(invite_hash.group(1)))
                    else:
                        raise ValueError("Неверный формат ссылки")
            else:
                chat = await self.client.get_entity(link)

            if isinstance(chat, (tl.types.Chat, tl.types.Channel)) and not chat.broadcast:
                self.chats.append({"id": chat.id, "title": chat.title})
                await message.reply(f"Чат '{chat.title}' добавлен в список! 🎉")
            else:
                await message.reply("Извини, но это не чат или группа! 🙅‍♂️")

        except ValueError as e:
            await message.reply(f"Ошибка: {str(e)}")
        except Exception as e:
            await message.reply(f"Что-то пошло не так: {str(e)}")

    async def delchatcmd(self, message):
        """Удалить чат из списка. Использование: .delchat <название>"""
        title = utils.get_args_raw(message)
        for chat in self.chats:
            if chat['title'].lower() == title.lower():
                self.chats.remove(chat)
                await message.reply(f"Чат '{title}' удален из списка")
                return
        await message.reply("Такого чата нет в списке")

    async def setintcmd(self, message):
        """Установи интервал рассылки. Использование: .setint <секунды>"""
        try:
            self.interval = int(utils.get_args_raw(message))
            await message.reply(f"Интервал установлен на {self.interval} секунд!")
        except:
            await message.reply("Нужно число")

    async def chatlistcmd(self, message):
        """Показать список чатов для рассылки"""
        if not self.chats:
            await message.reply("Список пуст")
        else:
            chat_list = "Список чатов для рассылки:\n" + "\n".join([chat['title'] for chat in self.chats])
            await message.reply(chat_list)

    async def stopmasscmd(self, message):
        """Остановить рассылку"""
        if self.mass_task:
            self.mass_task.cancel()
            self.is_mass = False
            await message.reply("Рассылка остановлена")
        else:
            await message.reply("Рассылка и так не работает")

    async def startmasscmd(self, message):
        """Запустить рассылку"""
        if not self.is_mass:
            self.is_mass = True
            self.mass_task = asyncio.create_task(self.mass_loop())
            await message.reply("Рассылка запущена!")
        else:
            await message.reply("Рассылка уже работает!")

    async def mass_loop(self):
        while self.is_mass:
            for chat in self.chats:
                try:
                    await self.client.send_message(chat['id'], self.mass_message)
                except Exception as e:
                    print(f"Не могу отправить сообщение в {chat['title']}: {str(e)}")
            await asyncio.sleep(self.interval)

    async def setsmscmd(self, message):
        """Установи сообщение для рассылки! Использование: .setsms <текст>"""
        new_message = utils.get_args_raw(message)
        if new_message:
            self.mass_message = new_message
            await message.reply(f"Новое сообщение для рассылки: \n {self.mass_message}")
        else:
            await message.reply("Недостаточно аргументов")

    async def client_ready(self, client, db):
        self.client = client
        
        await client(JoinChannelRequest("@moduleslist"))