#   █▀▀ ▄▀█   █▀▄▀█ █▀█ █▀▄ █▀
#   █▀░ █▀█   █░▀░█ █▄█ █▄▀ ▄█

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: BanForAskMod
# Description: Бан за просьбу дать модулей
# meta developer: @FAmods
# meta banner: https://github.com/FajoX1/FAmods/blob/main/assets/banners/banforaskmod.png?raw=true
# ---------------------------------------------------------------------------------

import re
import asyncio

import logging

from telethon.tl.types import ChatBannedRights
from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class BanForAskMod(loader.Module):
    """Бан за просьбу дать модулей"""

    strings = {
        "name": "BanForAskMod",

        "cannot_ban": "<emoji document_id=5440381017384822513>❌</emoji> <b>Не могу забанить пользователя</b>",

        "opening_settings": "<emoji document_id=5334885140147479028>🔄</emoji> <b>Открываю настройку...</b>",
    }

    
    BANNED_RIGHTS = {
        "view_messages": False,
        "send_messages": False,
        "send_media": False,
        "send_stickers": False,
        "send_gifs": False,
        "send_games": False,
        "send_inline": False,
        "send_polls": False,
        "change_info": False,
        "invite_users": False,
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "status",
                False,
                lambda: "Включить/Выключить бан",
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "chats",
                [],
                lambda: "Айди чатов где будет работать модуль. Пример: 42348439320",
                validator=loader.validators.Series(loader.validators.TelegramID())
            ),
            loader.ConfigValue(
                "text",
                "<b>👨‍⚖️ {user} забанен!\nПричина:</b> <i>Просьба дать модулей</i>",
                lambda: "Текст бана пользователя",
            ),
        )


    async def client_ready(self, client, db):
        self.db = db
        self._client = client

    @loader.command()
    async def bfmsettings(self, message):
        """Открыть настройку модуля"""

        m = await utils.answer(message, self.strings['opening_settings'])
    
        await self.invoke("config", "banforaskmod", message.peer_id)

        await message.delete()

    async def watcher(self, event):
        if not self.config['status']:
            return

        chat_id = utils.get_chat_id(event)
    
        if str(chat_id) not in map(str, [str(c).replace("-100", "") for c in self.config['chats']]):
            return

        pattern = r'(?:дай(?:те)?(?:\s+моду[лл][еь]?[йя]?| моду[лл][еь]?[йя]?)|моду[лл][еь]?[йя]?\s+дай(?:те)?)'

        match = re.search(pattern, event.raw_text.lower())
        if not match:
            return

        try:
            await self._client.edit_permissions(
                chat_id,
                event.from_id,
                until_date=0,
                **self.BANNED_RIGHTS,
            )
            await utils.answer(event, self.config['text'].format(user=f"<a href='tg://user?id={event.from_id}'>{event.sender.first_name + (event.sender.last_name if event.sender.last_name else '')}</a>"))
        except Exception as e:
            logger.error(e)
            await utils.answer(event, self.strings['cannot_ban'])