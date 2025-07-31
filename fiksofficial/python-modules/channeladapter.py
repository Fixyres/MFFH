# На модуль распространяется лицензия "GNU General Public License v3.0"
# https://github.com/all-licenses/GNU-General-Public-License-v3.0

# meta developer: @PyModule
from telethon.tl.types import Message
from .. import loader

@loader.tds
class ChannelAdapterMod(loader.Module):
    """Модуль для добавления переходника в сообщения каналов"""
    strings = {"name": "ChannelAdapter"}

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        if not self.db.get(__name__, "adapters"):
            self.db.set(__name__, "adapters", {})

    def get_adapters(self):
        """Получает адаптеры из базы данных"""
        return self.db.get(__name__, "adapters", {})

    def save_adapters(self, adapters):
        """Сохраняет адаптеры в базу данных"""
        self.db.set(__name__, "adapters", adapters)

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

        adapters = self.get_adapters()
        adapters[chat_id] = adapter_text
        self.save_adapters(adapters)

        await message.edit(f"<emoji document_id=5774022692642492953>✅</emoji> <b>Переходник добавлен для канала:</b> <code>{chat_id}</code> - {adapter_text}")

    @loader.command()
    async def deladaptercmd(self, message: Message):
        """[CHANNEL ID] - Удалить переходник для канала."""
        args = message.raw_text.split()
        if len(args) < 2:
            await message.edit("<emoji document_id=6030563507299160824>❗️</emoji> <b>Укажите ID канала.</b>")
            return

        chat_id = args[1]
        adapters = self.get_adapters()

        if chat_id not in adapters:
            await message.edit("<emoji document_id=5774077015388852135>❌</emoji> <b>Этот канал не найден в списке.</b>")
            return

        del adapters[chat_id]
        self.save_adapters(adapters)

        await message.edit(f"<emoji document_id=5774022692642492953>✅</emoji> <b>Переходник для канала <code>{chat_id}</code> удалён.</b>")

    @loader.command()
    async def listadapterscmd(self, message: Message):
        """- Показать список всех переходников."""
        adapters = self.get_adapters()
        if not adapters:
            await message.edit("<emoji document_id=5774077015388852135>❌</emoji> <b>Нет сохранённых переходников.</b>")
            return

        text = "<blockquote><emoji document_id=5253959125838090076>👁</emoji> <b>Список сохранённых переходников</b></blockquote>\n\n\n"
        for chat_id, adapter_text in adapters.items():
            text += f"<emoji document_id=6032924188828767321>➕</emoji> <b><code>{chat_id}</code>:</b> {adapter_text}\n\n"

        await message.edit(text)

    @loader.command()
    async def clearadapterscmd(self, message: Message):
        """- Удалить все переходники."""
        adapters = self.get_adapters()
        if not adapters:
            await message.edit("<emoji document_id=5774077015388852135>❌</emoji> <b>Нет переходников для удаления.</b>")
            return

        self.db.set(__name__, "adapters", {})
        await message.edit("<emoji document_id=5774022692642492953>✅</emoji> <b>Все адаптеры были удалены.</b>")

    async def watcher(self, message: Message):
        """Автоматически добавляет переходник в сообщения каналов"""
        if not message or not message.out:
            return
        
        adapters = self.get_adapters()
        adapter_text = adapters.get(str(message.chat_id), None)

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
