#meta developer: @hewin
from .. import loader, utils
from telethon.tl.types import Message

@loader.tds
class XoxolskiMod(loader.Module):
    """Модуль для замены текста в сообщениях на 'игривый' диалект."""
    strings = {"name": "Xoxolski"}

    # Словарь для замены слов
    translate_map = {
        "и": "і",
        "И": "і",
        "ы": "і",
        "Ы": "і",
        "что": "шо",
        "Что": "шо",
        "Э": "є",
        "е": "є",
        "пошел": "пішов",
        "Пошел": "пішов",
        "е": "є",
        "э": "є"
    }

    async def client_ready(self, client, db):
        """Инициализация клиента и базы данных."""
        self.db = db
        self._client = client
        self.enabled = self.db.get("Xoxolski", "enabled", False)

    async def xoxolcmd(self, message: Message):
        """Команда для включения или выключения модуля."""
        self.enabled = not self.enabled
        self.db.set("Xoxolski", "enabled", self.enabled)
        response_text = "<b><emoji document_id=5373230968943420212>🖤</emoji> язык украинца успешно включен</b>" if self.enabled else "❌ <b>украинец выключен </b>"
        return await utils.answer(message=message, response=response_text)

    async def xoxolzcmd(self, message: Message):
        """Команда для преобразования текста в ответном сообщении."""
        reply = await message.get_reply_message()
        if reply and reply.text:
            translated_text = self.translate_text(reply.text)
            await utils.answer(message=message, response=translated_text)

    def translate_text(self, text):
        """Преобразование текста с использованием словаря замены."""
        for key, value in self.translate_map.items():
            text = text.replace(key, value)
        return text

    async def watcher(self, message: Message):
        """Наблюдатель, который автоматически заменяет текст в отправленных сообщениях, если модуль активен."""
        if self.enabled and message.out and message.text:
            translated_text = self.translate_text(message.text)
            if message.text != translated_text:
                await self._client.edit_message(message.peer_id, message.id, translated_text),