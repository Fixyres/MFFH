# ©️ qq_shark, 2025
# 🌐 https://github.com/qqshark/Modules/blob/main/always-online.py
# Licеnsed under GNU AGPL v3.0
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

# meta developer: @qq_shark && @SharkHostBot

__version__ = (1, 0, 1)

import asyncio
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from telethon.tl.types import InputNotifyPeer, InputPeerNotifySettings
from .. import loader, utils

@loader.tds
class AlwaysOnline(loader.Module):
    """Always Online - модуль вечного онлайна (by @qq_shark)."""

    strings = {
        "name": "Always Online",
        "reqj": "This is a chat for always online mode by reading messages!",
        "online_on": "<blockquote><emoji document_id=5278411813468269386>✅</emoji> <b>Online mode enabled!</b></blockquote>",
        "online_off": "<blockquote><emoji document_id=5278578973595427038>🚫</emoji> <b>Online mode disabled!</b></blockquote>",
    }

    strings_ru = {
        "name": "Always Online",
        "reqj": "Это чат для вечного онлайна посредством чтения сообщений!",
        "online_on": "<blockquote><emoji document_id=5278411813468269386>✅</emoji> <b>Режим онлайн включен!</b></blockquote>",
        "online_off": "<blockquote><emoji document_id=5278578973595427038>🚫</emoji> <b>Режим онлайн выключен!</b></blockquote>",
    }

    strings_ua = {
        "name": "Always Online",
        "reqj": "Це чат для вічного онлайну за допомогою читання повідомлень!",
        "online_on": "<blockquote><emoji document_id=5278411813468269386>✅</emoji> <b>Режим онлайн увімкнено!</b></blockquote>",
        "online_off": "<blockquote><emoji document_id=5278578973595427038>🚫</emoji> <b>Режим онлайн вимкнено!</b></blockquote>",
    }

    strings_de = {
        "name": "Always Online",
        "reqj": "Dies ist ein Chat für ewiges Online-Sein durch das Lesen von Nachrichten!",
        "online_on": "<blockquote><emoji document_id=5278411813468269386>✅</emoji> <b>Online-Modus aktiviert!</b></blockquote>",
        "online_off": "<blockquote><emoji document_id=5278578973595427038>🚫</emoji> <b>Online-Modus deaktiviert!</b></blockquote>",
    }

    def __init__(self):
        self.online_mode = False
        self.target_chat_id = -1002870102083

    async def client_ready(self, client, db):
        self.db = db
        self.online_mode = self.db.get("AlwaysOnline", "online_mode", False)
        await self.request_join(
            "@infinite_online",
            self.strings['reqj'],
        )
        await asyncio.sleep(2)
        try:
            entity = await client.get_entity("@infinite_online")
            await client.edit_folder(entity, 1)
            await client(UpdateNotifySettingsRequest(
                peer=InputNotifyPeer(entity),
                settings=InputPeerNotifySettings(
                    mute_until=2147483647, 
                    sound=""
                )
            ))
        except Exception:
            pass

    @loader.watcher()
    async def watcher(self, message):
        """Автоматически читает сообщения в целевом чате когда режим включен"""
        try:
            if self.online_mode and message.chat_id == self.target_chat_id:
                await self.client.send_read_acknowledge(
                    message.chat_id, 
                    clear_mentions=True
                )
        except Exception:
            pass

    @loader.command()
    async def onlinecmd(self, message):
        """- переключатель режима онлайн"""
        self.online_mode = not self.online_mode
        self.db.set("AlwaysOnline", "online_mode", self.online_mode)
        if self.online_mode:
            await utils.answer(message, self.strings["online_on"])
        else:
            await utils.answer(message, self.strings["online_off"])
