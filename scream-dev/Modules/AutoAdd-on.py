#           __..--''``---....___   _..._    __
# /// //_.-'    .-/";  `        ``<._  ``.''_ `. / // /
#///_.-' _..--.'_    \                    `( ) ) // //
#/ (_..-' // (< _     ;_..__               ; `' / ///
# / // // //  `-._,_)' // / ``--...____..-' /// / //
# 🐈 Module writed @ScreamDev 
# 👌 Channel @ScreamModules
# 🧨 Blog: @ScreamDevBlog

# meta developer: @ScreamDev
# meta banner: https://raw.githubusercontent.com/scream-dev/Modules/refs/heads/main/images/AutoAddon.png
# meta pic: https://raw.githubusercontent.com/scream-dev/Modules/refs/heads/main/images/AutoAddon.png

import asyncio

from .. import loader, utils


@loader.tds
class AutoEdit(loader.Module):
    """Добавляет к сообщению канала ватемарку"""

    strings = {
        "name": "AutoAdd-On",
    }

    @loader.watcher(out=True)
    async def watcher(self, message):
        if self.get("autoedit"):
            if message.chat_id != self.config["channel_id"]:
                return

            watermark_text = self.config["watermark"]
            edit_msg = f"{message.text}\n\n{watermark_text}"
            await message.edit(edit_msg)

    async def client_ready(self, client, db):
        self._db = db
        self._me = await client.get_me()

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "watermark",
                "<b>========\nЗамените текст в конфиге .cfg AutoAdd-On</b>",
                doc="Текст ватемарки, добавляемой к сообщениям."
            ),
            loader.ConfigValue(
                "channel_id",
                0,  # Замените 0 на идентификатор канала по умолчанию
                doc="ID канала, где будет работать модуль."
            )
        )

    @loader.command()
    async def autoedit(self, message):
        "- включить/выключить AutoAdd-On."
        if self.get("autoedit") == True:
            self.set("autoedit", False)
            await utils.answer(message, "<b>🎈Авто Дополнение выключено</b>")
            return
        elif self.get("autoedit") == False or self.get("autoedit") is None:
            self.set("autoedit", True)
            await utils.answer(message, "<b>😶‍🌫️Авто Дополнение включено</b>")
