# meta developer: @Eraminel01
from .. import loader, utils
from telethon.tl.types import Message

@loader.tds
class VivoMod(loader.Module):
    strings = {
        "name": "📱 Смартфон vivo"
    }

    async def client_ready(self, client, db):
        self.db = db
        self._client = client
        self.enabled = self.db.get("vivophone", "enabled", False)

    async def tvivocmd(self, message: Message):
        """Включить или отключить ВИВО"""
        self.enabled = not self.enabled
        self.db.set("vivophone", "enabled", self.enabled)
        
        if self.enabled:
            return await utils.answer(
                message=message,
                response="<b>📱 Vivo успешно включен. Дай бог тебе накажет. Смартфон vivo</b>"
            )
        else:
            return await utils.answer(
                message=message,
                response="❌ <b>Vivo отключен</b>"
            )

    async def watcher(self, message: Message):
        if self.enabled and message.out:
            new_text = (message.text or "") + "\nСмартфон vivo"
            await self._client.edit_message(message.peer_id, message.id, new_text)