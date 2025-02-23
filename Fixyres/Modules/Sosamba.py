version = (1, 4, 8, 8)
#meta developer: @moduleslist

from .. import loader, utils
from telethon.tl.types import Message
from telethon.tl.functions.channels import JoinChannelRequest
import re

@loader.tds
class SosambaModule(loader.Module):
    """сосал?"""

    strings = {
        "name": "Sosamba",
        "enabled": "✅ <b>Модуль включен</b>",
        "disabled": "🚫 <b>Модуль выключен</b>",
        "config_changed": "✅ <b>Конфигурация обновлена</b>"
    }

    trigger_words = [
        "да", "конечно", "естественно", "каждый день", "ага",
        "Да", "Конечно", "Естественно", "Каждый день", "Ага",
        "До", "до"
    ]

    defaults = {
        "replacement_text": "сосал?"
    }

    def init(self):
        self._db = None
        self._client = None

    async def client_ready(self, client, db):
        self._db = db
        self._client = client

        await client(JoinChannelRequest(channel="@moduleslist"))

    def _is_enabled(self) -> bool:
        return self._db.get(self.strings["name"], "enabled", False)

    def _check_trigger(self, text: str) -> bool:
        """Проверка текста на триггер-слова"""
        return any(text.strip().startswith(word) for word in self.trigger_words)

    @loader.command()
    async def sosamba(self, message: Message):
        """👻 Включить/выключить модуль"""
        current_state = self._is_enabled()
        new_state = not current_state
        self._db.set(self.strings["name"], "enabled", new_state)
        await utils.answer(
            message,
            self.strings["enabled"] if new_state else self.strings["disabled"]
        )

    @loader.watcher()
    async def watcher(self, message: Message):
        if not self._is_enabled():
            return

        if not message.is_reply:
            return

        try:
            replied = await message.get_reply_message()
            me = await message.client.get_me()

            if not replied.sender_id == me.id:
                return

            if not message.text or not self._check_trigger(message.text):
                return

            await message.client.edit_message(
                replied.chat_id,
                replied.id,
                self.get("replacement_text")
            )
        except Exception:
            pass

    @loader.command()
    async def sostext(self, message: Message):
        """📝 Изменить текст замены. Использование: .sostext <текст>"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(
                message,
                f"🔧 <b>Текущий текст замены:</b> <code>{self.get('replacement_text')}</code>"
            )
            return

        self.set("replacement_text", args)
        await utils.answer(message, self.strings["config_changed"])