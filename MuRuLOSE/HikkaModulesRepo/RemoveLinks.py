from hikkatl.types import Message
from .. import loader, utils
import re

"""
    ███    ███ ██    ██ ██████  ██    ██ ██       ██████  ███████ ███████
    ████  ████ ██    ██ ██   ██ ██    ██ ██      ██    ██ ██      ██  
    ██ ████ ██ ██    ██ ██████  ██    ██ ██      ██    ██ ███████ █████
    ██  ██  ██ ██    ██ ██   ██ ██    ██ ██      ██    ██      ██ ██  
    ██      ██  ██████  ██   ██  ██████  ███████  ██████  ███████ ███████ 


    RemoveLinks
    📜 Licensed under the GNU AGPLv3	
"""

# meta banner: https://0x0.st/HYVc.jpg
# meta desc: desc
# meta developer: @BruhHikkaModules


@loader.tds
class RemoveLinks(loader.Module):
    """Remove links from your messages"""

    strings = {
        "name": "RemoveLinks",
        "link_remove": "[HYPERLINK BLOCKED!]",
        "chat_added": "✅ <b>Chat {} added!</b>",
        "chat_removed": "🗑 <b>Chat {} deleted!</b>",
        "status_enable": "✅ <b>Link removal enabled</b>",
        "status_shutdown": "❌ <b>Removal Links Off</b>",
    }

    strings_ru = {
        "_cls_doc": "Удаляй ссылки из твоих сообщений",
        "link_remove": "[ГИПЕРССЫЛКА ЗАБЛОКИРОВАНА!]",
        "chat_added": "✅ <b>Чат {} добавлен!</b>",
        "chat_removed": "🗑 <b>Чат {} удалён!</b>",
        "status_enable": "✅ <b>Удаление ссылок включено</b>",
        "status_shutdown": "❌ <b>Удаление ссылок выключено</b>",
    }

    async def client_ready(self, db, client):
        self._rmchats = self.pointer("chats", [])

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "status",
                False,
                lambda: "for status",
                validator=loader.validators.Boolean(),
            )
        )

    def removelinks(self, text):
        pattern = r"http[s]?:\/\/\S+|www\.\S+|\b\w+\.\w{2,}\b"
        no_links = re.sub(pattern, self.strings["link_remove"], text)
        return no_links

    async def remove_addchat(self, message, chat_id):
        if chat_id not in self._rmchats:
            self._rmchats.append(chat_id)
            return await utils.answer(
                message, self.strings["chat_added"].format(chat_id)
            )
        else:
            self._rmchats.remove(chat_id)
            return await utils.answer(
                message, self.strings["chat_removed"].format(chat_id)
            )

    @loader.command(
        ru_doc=" [status] - Включить / выключить блокировку ссылок",
    )
    async def rmlink(self, message: Message):
        """[status] - Enable / Shutdown link blocking"""
        self.config["status"] = not self.config["status"]

        status = (
            self.strings["status_enable"]
            if self.config["status"]
            else self.strings["status_shutdown"]
        )

        await utils.answer(message, status)

    @loader.command(
        ru_doc=" [id] - Добавить / Удалить чат где блокируется ссылки (если добавить *, удаление будет глобальным во всех чатах)",
    )
    async def addrmlink(self, message: Message):
        """[id] - Add / Remove chat where blocking links (if add *, removing will be global in all chats)"""

        args = utils.get_args_raw(message)

        chat_id = message.chat_id

        await self.remove_addchat(message, chat_id or args)

    @loader.watcher()
    async def remove_link(self, message: Message):
        me = await self.client.get_me(id)
        try:
            if message.from_id == me.user_id and message.chat_id in self._rmchats:
                edit_msg = self.removelinks(text=message.raw_text)

                if edit_msg != message.raw_text:
                    await utils.answer(message, edit_msg)
        except AttributeError:
            pass  # Just excepted events or not text messages
