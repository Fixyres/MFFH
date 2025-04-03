#meta developer @ManulMods

from typing import Dict, List, Set
import re
from hikkatl.types import Message
from .. import loader, utils

@loader.tds
class AutoResponderMod(loader.Module):
    """Автоматические ответы с управлением"""

    strings = {
        "name": "AutoResponder",
        "added": "✅ <b>Автоответ добавлен!</b>\n▸ <code>{}</code> → <code>{}</code>",
        "removed": "✅ Автоответ на <code>{}</code> удалён",
        "not_found": "❌ Автоответ на <code>{}</code> не найден",
        "list": "📊 <b>Список автоответов ({}):</b>\n\n{}",
        "empty": "🚫 Нет сохранённых автоответов",
        "syntax": "❌ <b>Неверный синтаксис!</b>\n▸ Для добавления: <code>{}aa ключ\\nответ</code>",
        "global_status": "🌍 <b>Глобальный статус:</b> {}\n▸ Активен в {} чатах",
        "chat_enabled": "✅ Автоответы включены в этом чате",
        "chat_disabled": "❌ Автоответы отключены в этом чате",
    }

    def __init__(self):
        self._responses: Dict[str, str] = {}
        self._active_chats: Set[int] = set()
        self._global_enabled = True
        self._db = None
        self._client = None

    async def client_ready(self, client, db):
        self._db = db
        self._client = client
        
        # Инициализация из базы данных
        self._responses = self._db.get("AutoResponder", "responses", {})
        self._active_chats = set(self._db.get("AutoResponder", "active_chats", []))
        self._global_enabled = self._db.get("AutoResponder", "global_enabled", True)

    def _save(self):
        self._db.set("AutoResponder", "responses", self._responses)
        self._db.set("AutoResponder", "active_chats", list(self._active_chats))
        self._db.set("AutoResponder", "global_enabled", self._global_enabled)

    @loader.command(ru_doc="<ключ>\\n<ответ> - Добавить автоответ")
    async def aa(self, message: Message):
        """Добавить автоответ"""
        try:
            args = utils.get_args_raw(message)
            if not args or "\n" not in args:
                raise ValueError
            
            keyword, response = args.split("\n", 1)
            keyword = keyword.strip().lower()
            response = response.strip()

            if not keyword or not response:
                raise ValueError

            self._responses[keyword] = response
            self._save()

            await utils.answer(
                message,
                self.strings("added").format(
                    utils.escape_html(keyword),
                    utils.escape_html(response)
                )
            )
        except:
            await utils.answer(
                message,
                self.strings("syntax").format(self.get_prefix())
            )

    @loader.command(ru_doc="<ключ> - Удалить автоответ")
    async def ar(self, message: Message):
        """Удалить автоответ"""
        args = utils.get_args_raw(message)
        if not args:
            return await utils.answer(message, "❌ Укажите ключевое слово")

        keyword = args.strip().lower()
        if keyword in self._responses:
            del self._responses[keyword]
            self._save()
            await utils.answer(
                message,
                self.strings("removed").format(utils.escape_html(keyword))
            )
        else:
            await utils.answer(
                message,
                self.strings("not_found").format(utils.escape_html(keyword))
            )

    @loader.command(ru_doc="Показать все автоответы")
    async def al(self, message: Message):
        """Список автоответов"""
        if not self._responses:
            return await utils.answer(message, self.strings("empty"))

        response_list = "\n".join(
            f"▸ <code>{k}</code>: {v}" 
            for k, v in self._responses.items()
        )
        await utils.answer(
            message,
            self.strings("list").format(len(self._responses), response_list)
        )

    @loader.command(ru_doc="Включить/выключить глобально")
    async def aatoggle(self, message: Message):
        """Вкл/выкл Глобального управления"""
        self._global_enabled = not self._global_enabled
        self._save()
        status = "✅ Включён" if self._global_enabled else "❌ Выключен"
        await utils.answer(
            message,
            self.strings("global_status").format(status, len(self._active_chats))
        )

    @loader.command(ru_doc="Включить в текущем чате")
    async def aaon(self, message: Message):
        """Вкл автоответы в чате"""
        chat_id = utils.get_chat_id(message)
        if chat_id in self._active_chats:
            return await utils.answer(message, "ℹ️ Уже включено в этом чате")
        
        self._active_chats.add(chat_id)
        self._save()
        await utils.answer(message, self.strings("chat_enabled"))

    @loader.command(ru_doc="Выключить в текущем чате")
    async def aaoff(self, message: Message):
        """Выкл автоответы в чате"""
        chat_id = utils.get_chat_id(message)
        if chat_id not in self._active_chats:
            return await utils.answer(message, "ℹ️ Уже выключено в этом чате")
        
        self._active_chats.remove(chat_id)
        self._save()
        await utils.answer(message, self.strings("chat_disabled"))

    async def watcher(self, message: Message):
        """Обработчик сообщений"""
        try:
            # Проверка условий
            if not isinstance(message, Message):
                return
            
            if message.out or not message.text:
                return
                
            if not self._global_enabled:
                return
                
            chat_id = utils.get_chat_id(message)
            if chat_id not in self._active_chats:
                return
                
            # Проверка на свои сообщения
            if message.sender_id == (await self._client.get_me()).id:
                return

            # Поиск ключевых слов
            text = message.text.lower()
            for keyword, response in self._responses.items():
                if re.search(rf'\b{re.escape(keyword)}\b', text):
                    await utils.answer(message, response)
                    break
                    
        except Exception as e:
            logger.exception("Ошибка в watcher: %s", e)