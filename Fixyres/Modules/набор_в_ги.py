# meta developer: @Yaukais, @Shadow_red1
__version__ = (7, 7, 7)
from .. import loader, utils
from telethon.tl.types import Message
from telethon import Button
import asyncio
import json
import os
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@loader.tds
class AutoKitGi(loader.Module):
    '''Автоматический спам сообщениями: набор в гильдию!'''
    strings = {
        'name': "AutoKit"
    }

    def __init__(self):
        self.chat_id = None
        self.spam_enabled = False
        self.message_ids = []  # Список ID сообщений для спама
        self.messages_file = "messages.json"
        self.messages = {}

        # Загружаем существующие сообщения из JSON
        if os.path.exists(self.messages_file):
            with open(self.messages_file, 'r', encoding='utf-8') as f:
                self.messages = json.load(f)

    async def client_ready(self, client, db):
        self.client = client

    @loader.command()
    async def setchat(self, message: Message):
        """Установить ID чата для спама."""
        self.chat_id = message.to_id  # Установка текущего чата
        await utils.answer(message, f'Чат установлен: {self.chat_id}')

    @loader.command()
    async def набор(self, message: Message):
        """Начать спамить сообщение каждые 10 минут."""
        try:
            if not self.chat_id:
                await utils.answer(message, 'Сначала установите чат с помощью команды <code>.setchat</code>.')
                return
            
            if not self.message_ids:
                await utils.answer(message, 'Не выбраны сообщения для спама. Используйте команду <code>.инстаил</code> для установки сообщений.')
                return

            self.spam_enabled = True
            await utils.answer(message, '<emoji document_id=5292160660912748253>⚫️</emoji>AutoKit<emoji document_id=5289977374417368794>⚫️</emoji> включен!')

            while self.spam_enabled:
                for msg_id in self.message_ids:
                    try:
                        await self.client.send_message(self.chat_id, self.messages[str(msg_id)])
                    except Exception as e:
                        logger.error(f'Ошибка при отправке сообщения: {str(e)}')
                        await utils.answer(message, f'Ошибка при отправке сообщения: {str(e)}')
                        break
                await asyncio.sleep(600)  # Ждать 10 минут
        except Exception as e:
            logger.exception("Ошибка в команде набор")
            await utils.answer(message, 'Произошла ошибка. Проверьте логи.')

    @loader.command()
    async def стоп(self, message: Message):
        """Остановить спам."""
        self.spam_enabled = False
        await utils.answer(message, '<emoji document_id=5292160660912748253>⚫️</emoji>AutoKit<emoji document_id=5289977374417368794>⚫️</emoji> выключен!')

    @loader.command()
    async def showchat(self, message: Message):
        """Показать текущий ID чата."""
        if self.chat_id:
            await utils.answer(message, f'Текущий ID чата: {self.chat_id}')
        else:
            await utils.answer(message, 'Чат еще не установлен.')

    @loader.command()
    async def lod_message(self, message: Message):
        """Сохранить сообщение для спама. Используйте команду с текстом или реплаем."""
        await message.delete()  # Удаляем команду
        reply = await message.get_reply_message()  # Получаем реплай
        msg = reply.text if reply else utils.get_args_raw(message)  # Получаем текст

        if not msg:
            await utils.answer(message, 'Не удалось получить сообщение для сохранения. Убедитесь, что вы реплаите на сообщение или передаете текст.')
            return

        # Сохранение в JSON
        if len(self.messages) < 20:  # Максимум 20 сообщений
            msg_id = len(self.messages) + 1
            self.messages[str(msg_id)] = msg
            with open(self.messages_file, 'w', encoding='utf-8') as f:
                json.dump(self.messages, f, ensure_ascii=False, indent=4)
            await utils.answer(message, f'<emoji document_id=5292160660912748253>⚫️</emoji>AutoKit<emoji document_id=5289977374417368794>⚫️</emoji> Сохранил сообщение под номером {msg_id}!')
        else:
            await utils.answer(message, 'Достигнуто максимальное количество сохранённых сообщений (20).')

    @loader.command()
    async def список(self, message: Message):
        """Показать список сохранённых сообщений."""
        if not self.messages:
            await utils.answer(message, 'Список сообщений пуст!')
            return

        buttons = []
        message_text = "Выберите сообщение для спама:\n"
        for i in range(1, len(self.messages) + 1):
            msg_content = self.messages[str(i)]
            buttons.append(Button.inline(f'Сообщение {i}: {msg_content[:20]}...', data=str(i)))  # Отображаем первые 20 символов сообщения
            message_text += f"{i}: {msg_content[:50]}...\n"  # Отображаем первые 50 символов сообщения

        # Отправляем сообщение с инлайн-кнопками
        await utils.answer(message, message_text, buttons=buttons)

    @loader.command()
    async def инстаил(self, message: Message):
        """Установить сообщения для спама. Используйте команду с номерами сообщений через запятую."""
        args = utils.get_args_raw(message).split(',')
        self.message_ids = []

        for arg in args:
            msg_id = arg.strip()
            if msg_id.isdigit() and msg_id in self.messages:
                self.message_ids.append(msg_id)
            else:
                await utils.answer(message, f'Сообщение с номером {msg_id} не найдено.')

        if self.message_ids:
            await utils.answer(message, f'<emoji document_id=5292160660912748253>⚫️</emoji>AutoKit<emoji document_id=5289977374417368794>⚫️</emoji> Установил сообщения для спама: {", ".join(self.message_ids)}.')

    @loader.command()
    async def un_инстаил(self, message: Message):
        """Убрать сообщение из установленных для спама. Используйте команду с номером сообщения."""
        args = utils.get_args(message)
        if not args:
            await utils.answer(message, 'Укажите номер сообщения для убирания из списка установленных.')
            return

        msg_id = args[0]
        if msg_id in self.message_ids:
            self.message_ids.remove(msg_id)
            await utils.answer(message, f'<emoji document_id=5292160660912748253>⚫️</emoji>AutoKit<emoji document_id=5289977374417368794>⚫️</emoji> Сообщение под номером {msg_id} убрано из установленных.')
        else:
            await utils.answer(message, f'<emoji document_id=5292160660912748253>⚫️</emoji>AutoKit<emoji document_id=5289977374417368794>⚫️</emoji> Сообщение с номером {msg_id} не найдено в установленных.')

    @loader.command()
    async def удалить(self, message: Message):
        """Удалить сообщение по номеру. Используйте команду: .удалить <номер>."""
        args = utils.get_args(message)
        if not args:
            await utils.answer(message, 'Укажите номер сообщения для удаления.')
            return

        msg_id = args[0]
        if msg_id in self.messages:
            del self.messages[msg_id]
            with open(self.messages_file, 'w', encoding='utf-8') as f:
                json.dump(self.messages, f, ensure_ascii=False, indent=4)
            await utils.answer(message, f'Сообщение под номером {msg_id} удалено!')
        else:
            await utils.answer(message, f'Нет сообщения с номером {msg_id}.')

    async def callback_handler(self, callback):
        """Обработчик для инлайн-кнопок."""
        msg_id = callback.data.decode("utf-8")  # Получаем ID сообщения из callback
        if msg_id in self.messages:
            self.message = self.messages[msg_id]
            await utils.answer(callback.message, f'Сообщение для спама установлено: {self.message}')
        else:
            await utils.answer(callback.message, f'Нет сообщения с номером {msg_id}.')

    @loader.command()
    async def show_bot_ids(self, message: Message):
        """Показать ID всех ботов в чате."""
        chat = await self.client.get_entity(message.to_id)
        bots = [user for user in await self.client.get_participants(chat) if user.bot]
        if bots:
            bot_ids = "\n".join([f"Имя: {bot.first_name}, ID: <code>{bot.id}</code>" for bot in bots])
            await utils.answer(message, f'Боты в чате:\n{bot_ids}')
        else:
            await utils.answer(message, 'В этом чате нет ботов.')

    @loader.command()
    async def show_user_ids(self, message: Message):
        """Показать ID всех пользователей в чате."""
        chat = await self.client.get_entity(message.to_id)
        users = [user for user in await self.client.get_participants(chat) if not user.bot]  # Получаем всех пользователей, исключая ботов
        if users:
            user_ids = "\n".join([f"Имя: {user.first_name}, ID: <code>{user.id}</code>" for user in users])
            await utils.answer(message, f'Пользователи в чате:\n{user_ids}')
        else:
            await utils.answer(message, 'В этом чате нет пользователей.')
