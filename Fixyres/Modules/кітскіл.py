# meta developer: @QzKat
from .. import loader, utils
from telethon.tl.types import Message

@loader.tds
class meinkita(loader.Module):
    """Модуль чтобы стать настоящим мэйном кіта(упрощенная версия чтобы юзать на постоянку)."""
    strings = {"name": "MainKita"}

    # Словарь для замены слов
    translate_map = {
        "и": "і",
        "И": "і",
        "что": "шо",
        "Что": "шо",
        "че": "шо",
        "Че": "шо",
        "чо": "шо",
        "Чо": "шо",
        "Э": "є",
        "е": "є",
        "е": "є",
        "э": "є",
    }

    async def client_ready(self, client, db):
        """Инициализация клиента и базы данных."""
        self.db = db
        self._client = client
        self.enabled = self.db.get("meinkita", "enabled", False)

    async def китcmd(self, message: Message):
        """Команда для включения или Bыключения модуля."""
        self.enabled = not self.enabled
        self.db.set("meinkita", "enabled", self.enabled)
        response_text = (
            "<b>ученик мэйна қіта включен💀</b>"
            if self.enabled
            else "❌ <b>Я больше не мэйн қіта </b>"
        )
        return await utils.answer(message=message, response=response_text)

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
                await self._client.edit_message(
                    message.peer_id, 
                    message.id, 
                    translated_text
                )