#---------------------------------------------------------------------------------
# Name: Hohol Text Modifier 
# Description: Заменяет сообщения на хрю
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
        "name": "Hohol Text Modifier"
    }

    async def client_ready(self, client, db):
        self.db = db
        self._client = client
        self.enabled = self.db.get("Hoholmod", "enabled", False)

    async def hoholcmd(self, message: Message):
        """Включить или отключить режим свинки"""
        args = utils.get_args_raw(message)
        self.enabled = not self.enabled
        self.db.set("hoholmod", "enabled", self.enabled)

        if self.enabled:
            response = "🐖Режим свинки успешно включен."
        else:
            response = "🚫 Режим свинки отключен"

        await utils.answer(message=message, response=response)

    async def watcher(self, message: Message):
        if self.enabled and message.out:
            message_text = message.text
            replaced_text = ' '.join(['хрю' + 'ю' * (len(word) - 3) for word in message_text.split()])
            await message.edit(replaced_text)