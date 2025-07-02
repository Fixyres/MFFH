# ©️ qq_shark, 2025
# 🌐 https://github.com/qqshark/always-online
# Licensed under GNU AGPL v3.0
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

__version__ = (1, 0, 0)

import asyncio
from telethon.tl.functions.contacts import UnblockRequest
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from telethon.tl.types import InputNotifyPeer, InputPeerNotifySettings
from .. import loader, utils

@loader.tds
class AlwaysOnline(loader.Module):
    """Always Online - модуль вечного онлайна (by @qq_shark)."""

    strings = {
        "name": "Always Online",
        "reqj": "Это чат для вечного онлайна посредством чтения сообщений!",
        "online_on": "Online mode turn on",
        "online_off": "Online mode turn off",
    }

    strings_ru = {
        "name": "Always Online",
        "reqj": "Это чат для вечного онлайна посредством чтения сообщений!",
        "online_on": "Режим онлайн включен",
        "online_off": "Режим онлайн выключен",
    }

    strings_ua = {
        "name": "Always Online",
        "reqj": "Це чат для вічного онлайну за допомогою читання повідомлень!",
        "online_on": "Режим онлайн увімкнено",
        "online_off": "Режим онлайн вимкнено",
    }

    strings_de = {
        "name": "Always Online",
        "reqj": "Dies ist ein Chat für ewiges Online-Sein durch das Lesen von Nachrichten!",
        "online_on": "Online-Modus eingeschaltet",
        "online_off": "Online-Modus ausgeschaltet",
    }

    strings_tr = {
        "name": "Always Online",
        "reqj": "Bu, mesajları okuyarak sürekli çevrimiçi olmak için bir sohbettir!",
        "online_on": "Çevrimiçi modu açık",
        "online_off": "Çevrimiçi modu kapalı",
    }

    strings_tt = {
        "name": "Always Online",
        "reqj": "Бу хәбәрләрне укып мәңгелек онлайн булу өчен чат!",
        "online_on": "Онлайн режимы кабызылган",
        "online_off": "Онлайн режимы сүндерелгән",
    }

    strings_es = {
        "name": "Always Online",
        "reqj": "¡Este es un chat para estar siempre en línea mediante la lectura de mensajes!",
        "online_on": "Modo en línea activado",
        "online_off": "Modo en línea desactivado",
    }

    strings_kk = {
        "name": "Always Online",
        "reqj": "Бұл хабарларды оқу арқылы мәңгілік онлайн болу үшін чат!",
        "online_on": "Онлайн режимі қосылды",
        "online_off": "Онлайн режимі өшірілді",
    }

    strings_yz = {
        "name": "Always Online",
        "reqj": "Бул билдирүүлөрдү окуу аркылуу түбөлүккө онлайн болуу үчүн чат!",
        "online_on": "Онлайн режими күйгүзүлдү",
        "online_off": "Онлайн режими өчүрүлдү",
    }

    strings_fr = {
        "name": "Always Online",
        "reqj": "Ceci est un chat pour être toujours en ligne en lisant les messages!",
        "online_on": "Mode en ligne activé",
        "online_off": "Mode en ligne désactivé",
    }

    strings_it = {
        "name": "Always Online",
        "reqj": "Questa è una chat per essere sempre online leggendo i messaggi!",
        "online_on": "Modalità online attivata",
        "online_off": "Modalità online disattivata",
    }

    def __init__(self):
        self.online_mode = False
        self.target_chat_id = -1002870102083

    async def client_ready(self, client, db):
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
        
        if self.online_mode:
            await utils.answer(message, self.strings["online_on"])
        else:
            await utils.answer(message, self.strings["online_off"])
