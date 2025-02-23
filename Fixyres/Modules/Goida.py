#---------------------------------------------------------------------------------
# Name: Hohol Text Modifier 
# Description: Заменяет сообщения на ГОЙДА
# Author: @skillzmeow
# Commands:
# .hohol
# ---------------------------------------------------------------------------------


# module by:
# █▀ █▄▀ █ █░░ █░░ ▀█
# ▄█ █░█ █ █▄▄ █▄▄ █▄

# █▀▄▀█ █▀▀ █▀█ █░█░█
# █░▀░█ ██▄ █▄█ ▀▄▀▄▀
# you can edit this module
# 2024

# meta developer: @skillzmeow
from .. import loader, utils
from telethon.tl.types import Message

@loader.tds
class HoholMod(loader.Module):
    strings = {
        "name": "Goida"
    }

    async def client_ready(self, client, db):
        self.db = db
        self._client = client
        self.enabled = self.db.get("Goidamod", "enabled", False)

    async def goidacmd(self, message: Message):
        """Включить или отключить режим гойды"""
        args = utils.get_args_raw(message)
        self.enabled = not self.enabled
        self.db.set("goidamod", "enabled", self.enabled)

        if self.enabled:
            response = "<emoji document_id=5276232525587428621>🏴</emoji>Режим тотальной гойды успешно включен."
        else:
            response = "🚫 Режим тотальной гойды отключен"

        await utils.answer(message=message, response=response)

    async def watcher(self, message: Message):
        if self.enabled and message.out:
            message_text = message.text
            replaced_text = ' '.join(['ГОЙДА' + 'А' + ' ZOV БРАТЬЯ' * (len(word) - 5) for word in message_text.split()])
            await message.edit(replaced_text)