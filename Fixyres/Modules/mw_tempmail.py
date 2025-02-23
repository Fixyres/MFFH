# meta developer: @mwmodules
# meta desc: 🌐 TempMail - Disposable temporary email addresses generator for private and secure communication
# by @mwmodules
# 🔒 Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# meta link: .dlm http://mwmodules.ftp.sh/tempmail.py


from .. import loader, utils
import aiohttp
import random
import string
import time
from telethon.tl.types import Message

__version__ = (1, 0, 0)

@loader.tds
class TempMailMod(loader.Module):
    """Управление временной почтой от @mwoffice"""
    strings = {
        "name": "TempMail",
        "_cmd_doc_tempmail": "Показать меню управления временной почтой",
        "_cls_doc": "Модуль для работы с временной почтой от @mwoffice",
        "no_email": "🚫 Почтовый ящик не создан",
        "email_created": "📫 Создан новый ящик: <code>{}</code>",
        "email_deleted": "🗑 Почтовый ящик удален",
        "no_messages": "📭 Нет новых сообщений",
        "loading": "⏳ Загрузка...",
        "dev": """
👨‍💻 <b>Разработчик:</b> @mwoffice

<b>📝 О модуле:</b>
└ Версия: <code>{}</code>
└ Лицензия: GNU GPL v3

<b>⚡️ Возможности:</b>
└ Создание временного ящика
└ Проверка входящих сообщений 
└ Чтение писем
└ Удаление ящика

<b>📢 Канал:</b> @mwmodules"""
    }

    async def client_ready(self, client, db):
        self._db = db
        self._client = client
        self.email = None
        self.messages = []
        
    def get_markup(self):
        """Основное меню"""
        return [
            [
                {"text": "📫 Создать ящик", "callback": self.create_callback},
                {"text": "🗑 Удалить ящик", "callback": self.delete_callback},
            ],
            [
                {"text": "📨 Проверить почту", "callback": self.check_callback},
                {"text": "📝 Список сообщений", "callback": self.list_callback},
            ],
            [
                {"text": "ℹ️ Информация", "callback": self.info_callback},
                {"text": "👨‍💻 Разработчик", "callback": self.dev_callback},
            ],
        ]
        
    def get_back_markup(self):
        """Кнопка назад"""
        return [
            [
                {"text": "⬅️ Назад", "callback": self.tempmail_callback},
            ],
        ]

    async def create_email(self):
        """Создание временного ящика"""
        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.1secmail.com/api/v1/?action=genRandomMailbox') as response:
                if response.status == 200:
                    email = await response.json()
                    return email[0]
        return None

    async def get_messages(self):
        """Получение списка сообщений"""
        if not self.email:
            return []
            
        login, domain = self.email.split('@')
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}'
            ) as response:
                if response.status == 200:
                    return await response.json()
        return []

    async def get_message(self, message_id):
        """Получение содержимого письма"""
        if not self.email:
            return None
            
        login, domain = self.email.split('@')
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'https://www.1secmail.com/api/v1/?action=readMessage&login={login}&domain={domain}&id={message_id}'
            ) as response:
                if response.status == 200:
                    return await response.json()
        return None

    async def tempmail_callback(self, call):
        """Основное меню"""
        text = "📧 <b>Управление временной почтой</b>\n\n"
        
        if self.email:
            text += f"📫 Текущий ящик: <code>{self.email}</code>"
        else:
            text += "📭 Почтовый ящик не создан"
            
        await call.edit(text=text, reply_markup=self.get_markup())

    async def create_callback(self, call):
        """Создание ящика"""
        self.email = await self.create_email()
        text = self.strings['email_created'].format(self.email)
        await call.edit(text=text, reply_markup=self.get_back_markup())

    async def delete_callback(self, call):
        """Удаление ящика"""
        self.email = None
        self.messages = []
        await call.edit(text=self.strings['email_deleted'], reply_markup=self.get_back_markup())

    async def check_callback(self, call):
        """Проверка почты"""
        if not self.email:
            await call.edit(text=self.strings['no_email'], reply_markup=self.get_back_markup())
            return

        await call.edit(text=self.strings['loading'])
        self.messages = await self.get_messages()
        
        text = f"📫 Ящик: <code>{self.email}</code>\n\n"
        if self.messages:
            text += f"📨 Новых сообщений: {len(self.messages)}"
        else:
            text += "📭 Нет новых сообщений"
            
        await call.edit(text=text, reply_markup=self.get_back_markup())

    async def list_callback(self, call):
        """Список сообщений"""
        if not self.email:
            await call.edit(text=self.strings['no_email'], reply_markup=self.get_back_markup())
            return

        await call.edit(text=self.strings['loading'])
        self.messages = await self.get_messages()
        
        if not self.messages:
            await call.edit(text=self.strings['no_messages'], reply_markup=self.get_back_markup())
            return
            
        text = f"📫 Ящик: <code>{self.email}</code>\n\n"
        for msg in self.messages:
            text += f"📩 От: {msg['from']}\n"
            text += f"📋 Тема: {msg['subject']}\n"
            text += f"🕐 Дата: {msg['date']}\n\n"
            
        markup = self.get_back_markup()
        # Добавляем кнопки для каждого сообщения
        for msg in self.messages:
            markup.insert(0, [
                {"text": f"📩 {msg['subject'][:30]}", "callback": self.read_callback, "args": (msg['id'],)}
            ])
            
        await call.edit(text=text, reply_markup=markup)

    async def read_callback(self, call, message_id):
        """Чтение сообщения"""
        if not self.email:
            await call.edit(text=self.strings['no_email'], reply_markup=self.get_back_markup())
            return

        await call.edit(text=self.strings['loading'])
        message = await self.get_message(message_id)
        
        if not message:
            await call.edit(text="🚫 Сообщение не найдено", reply_markup=self.get_back_markup())
            return
            
        text = f"📫 Ящик: <code>{self.email}</code>\n\n"
        text += f"📩 От: {message['from']}\n"
        text += f"📋 Тема: {message['subject']}\n"
        text += f"🕐 Дата: {message['date']}\n\n"
        text += f"📝 Сообщение:\n{message['textBody']}\n"
        
        await call.edit(text=text, reply_markup=self.get_back_markup())

    async def info_callback(self, call):
        """Информация о модуле"""
        text = """📧 <b>TempMail</b>

Модуль для работы с временной почтой.

<b>Возможности:</b>
└ Создание временного почтового ящика
└ Проверка входящих сообщений
└ Чтение писем
└ Удаление ящика

<b>Использование:</b>
└ Используйте кнопки меню для управления временной почтой

<b>Разработчик:</b> @mwoffice"""
        await call.edit(text=text, reply_markup=self.get_back_markup())

    async def dev_callback(self, call):
        """Информация о разработчике"""
        version = f"{__version__[0]}.{__version__[1]}.{__version__[2]}"
        await call.edit(
            text=self.strings["dev"].format(version),
            reply_markup=self.get_back_markup()
        )

    @loader.command()
    async def tempmail(self, message: Message):
        """Показать меню управления временной почтой"""
        text = "📧 <b>Управление временной почтой</b>\n\n"
        
        if self.email:
            text += f"📫 Текущий ящик: <code>{self.email}</code>"
        else:
            text += "📭 Почтовый ящик не создан"
            
        await self.inline.form(
            text=text,
            message=message,
            reply_markup=self.get_markup(),
        )