#   █▀▀ ▄▀█   █▀▄▀█ █▀█ █▀▄ █▀
#   █▀░ █▀█   █░▀░█ █▄█ █▄▀ ▄█

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: FAbusiness
# Description: Бесплатный Telegram business
# meta developer: @FAmods
# meta banner: https://github.com/FajoX1/FAmods/blob/main/assets/banners/fabusiness.png?raw=true
# ---------------------------------------------------------------------------------

import time
import asyncio 
import logging

from telethon.tl.types import Message, PeerUser

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class FAbusiness(loader.Module):
    """Бесплатный Telegram business"""

    strings = {
        "name": "FAbusiness",

        "loading_cfg": "<b><emoji document_id=5334904192622403796>🔄</emoji> Открываю настройку...</b>",

        "business_on": "<b><emoji document_id=5431376038628171216>💻</emoji> FAbusiness включен!</b>",
        "business_off": "<b><emoji document_id=5854929766146118183>🚫</emoji> FAbusiness выключен!</b>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "not_here",
                False,
                lambda: "Ты на месте?",
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "hello_text",
                "<b>👋 Привет</b>",
                lambda: "Текст приветствия",
            ),
            loader.ConfigValue(
                "not_here_text",
                "<b>❌ Нет на месте</b>",
                lambda: "Текст если вас нету на месте",
            )
        )


    async def client_ready(self, client, db):
        self.db = db
        self._client = client

        self.last_message_time = {}

    async def _check_message_rate(self, user_id: int) -> bool:
        if user_id in self.last_message_time:
            last_time = self.last_message_time[user_id]
        
            if time.time() - last_time < 30:
                return False

        self.last_message_time[user_id] = time.time()
        return True

    @loader.command()
    async def business(self, message):
        """Включить/выключить FAbusiness"""

        if self.db.get(self.name, "business", False):
            self.db.set(self.name, "business", False)
            return await utils.answer(message, self.strings["business_off"])

        self.db.set(self.name, "business", True)

        await utils.answer(message, self.strings["business_on"])

    @loader.command()
    async def bsettings(self, message):
        """Настройка FAbusiness"""

        msg = await utils.answer(message, self.strings['loading_cfg'])

        await self.invoke("config", "FAbusiness", message.peer_id)

        await msg.delete()

    async def watcher(self, event):
        if (
            getattr(event, "out", False)
            or not isinstance(event, Message)
            or not isinstance(event.peer_id, PeerUser)
            or not self.db.get(self.name, "business")
            or utils.get_chat_id(event)
            in {
                1271266957,  # @replies
                777000,  # Telegram Notifications
                self._tg_id,  # Self
            }
        ):
            return
        
        try:
            if (
                event.sender.bot
                or event.sender.support
                or event.sender.contact
            ):
                return
        except:
            pass
    
        said_users = self.db.get(self.name, "said_users")

        if not said_users:
            said_users = []

        if not self.config['not_here']:
            if event.from_id not in said_users:
                said_users.append(event.from_id)
                self.db.set(self.name, "said_users", said_users)
            else:
                return
            
        else:
            if not await self._check_message_rate(event.from_id):
                return
        
        if self.config['not_here']:
            text = self.config['not_here_text']
        else:
            text = self.config['hello_text']

        await utils.answer(event, text)