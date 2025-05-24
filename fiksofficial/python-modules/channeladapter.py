# На модуль распространяется лицензия "GNU General Public License v3.0"
# https://github.com/all-licenses/GNU-General-Public-License-v3.0

# meta developer: @PyModule
import json
import os
from telethon.tl.types import Message
from .. import loader

@loader.tds
class ChannelAdapterMod(loader.Module):
    """Модуль для добавления переходника в сообщения каналов"""
    strings = {"name": "ChannelAdapter"}

    def __init__(self):
        self.adapters_file = "adapters.json"
        self.adapters = self.load_adapters()

    def load_adapters(self):
        """Загружает адаптеры из файла, если он существует."""
        if os.path.exists(self.adapters_file):
            with open(self.adapters_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def save_adapters(self):
        """Сохраняет адаптеры в файл."""
        with open(self.adapters_file, "w", encoding="utf-8") as f:
            json.dump(self.adapters, f, ensure_ascii=False, indent=4)

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        if not self.adapters:
            self.adapters = {}

    @loader.command()
    async def addadaptercmd(self, message: Message):
        """[CHANNEL ID] [Текст] - Добавить канал и переходник."""
        args = message.raw_text.split()
        if len(args) < 2:
            await message.edit("<emoji document_id=6030563507299160824>❗️</emoji> <b>Укажите ID канала.</b>")
            return

        chat_id = args[1]
        adapter_text = " ".join(args[2:])

        if not adapter_text:
            await message.edit("<emoji document_id=6030563507299160824>❗️</emoji> <b>Укажите текст переходника.</b>")
            return

        self.adapters[chat_id] = adapter_text
        self.save_adapters()

        await message.edit(f"<emoji document_id=5774022692642492953>✅</emoji> <b>Переходник добавлен для канала:</b> <code>{chat_id}</code> - {adapter_text}")

    async def deladaptercmd(self, message: Message):
        """[CHANNEL ID] - Удалить переходник для канала."""
        args = message.raw_text.split()
        if len(args) < 2:
            await message.edit("<emoji document_id=6030563507299160824>❗️</emoji> <b>Укажите ID канала.</b>")
            return

        chat_id = args[1]

        if chat_id not in self.adapters:
            await message.edit("<emoji document_id=5774077015388852135>❌</emoji> <b>Этот канал не найден в списке.</b>")
            return

        del self.adapters[chat_id]
        self.save_adapters() 

        await message.edit(f"<emoji document_id=5774022692642492953>✅</emoji> <b>Переходник для канала <code>{chat_id}</code> удалён.</b>")

    async def listadapterscmd(self, message: Message):
        """- Показать список всех переходников."""
        if not self.adapters:
            await message.edit("<emoji document_id=5774077015388852135>❌</emoji> <b>Нет сохранённых переходников.</b>")
            return

        text = "<blockquote><emoji document_id=5253959125838090076>👁</emoji> <b>Список сохранённых переходников</b></blockquote>\n\n\n"
        for chat_id, adapter_text in self.adapters.items():
            text += f"<emoji document_id=6032924188828767321>➕</emoji> <b><code>{chat_id}</code>:</b> {adapter_text}\n\n"

        await message.edit(text)

    async def clearadapterscmd(self, message: Message):
        """- Удалить все переходники."""
        if not self.adapters:
            await message.edit("<emoji document_id=5774077015388852135>❌</emoji> <b>Нет переходников для удаления.</b>")
            return

        self.adapters = {}
        self.save_adapters()

        await message.edit("<emoji document_id=5774022692642492953>✅</emoji> <b>Все адаптеры были удалены.</b>")

    async def watcher(self, message: Message):
        """Автоматически добавляет переходник в сообщения каналов"""
        if not message or not message.out:
            return
        
        adapter_text = self.adapters.get(str(message.chat_id), None)

        if not adapter_text:
            return

        try:
            if message.text:
                modified_text = f"{message.text}\n\n{adapter_text}"
                await message.edit(modified_text, parse_mode='html')
            elif message.media:
                modified_caption = f"{message.text}\n\n{adapter_text}" if message.text else adapter_text
                await message.edit(text=modified_caption, parse_mode='html')
        except Exception as e:
            me = await self.client.get_me()
            await self.client.send_message(me.id, f"<emoji document_id=6030563507299160824>❗️</emoji> <b>Ошибка в ChannelAdapter:</b>\n`{str(e)}`")
