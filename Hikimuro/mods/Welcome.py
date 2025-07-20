# meta developer: @Hikimuro
# ver. 1.0.5
# scope: hikka_only

from .. import loader, utils
from telethon.events import ChatAction
import time

@loader.tds
class WelcomeModule(loader.Module):
    strings = {"name": "WelcomeMessage"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue("welcome_chat", None, ""),
            loader.ConfigValue("welcome_text", "Добро пожаловать!", "")
        )
        self._last_sent = 0

    async def client_ready(self, client, db):
        self._client = client
        self._chat_id = self.config.get("welcome_chat")
        self._text = self.config.get("welcome_text")

        @client.on(ChatAction)
        async def handler(e):
            if not self._chat_id:
                return
            if e.chat_id != int(self._chat_id):
                return
            if not (e.user_joined or e.user_added):
                return
            if time.time() - self._last_sent < 120:
                return

            try:
                await self._client.send_message(int(self._chat_id), self._text)
                self._last_sent = time.time()
            except Exception as err:
                await utils.answer(e, f"Ошибка отправки: {err}")

    @loader.command()
    async def setwelcome(self, m):
        """Настроить приветствие. Используй в чате:

.setwelcome Текст приветствия
"""
        args = utils.get_args_raw(m)
        if not args:
            return await utils.answer(m, "Укажи текст приветствия.")

        cid = m.chat_id
        self.config["welcome_chat"] = cid
        self.config["welcome_text"] = args
        self._chat_id = cid
        self._text = args

        await utils.answer(m, f"✅ Установлено для чата `{cid}`")
