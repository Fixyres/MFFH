# meta developer: @VIP_IPru_tw

import asyncio
import logging
import time

from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.events import NewMessage
from telethon.tl.functions.contacts import UnblockRequest
from telethon.tl.functions.messages import ReadMentionsRequest
from telethon.tl.types import Message

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class AniverseCardMod(loader.Module):
    """Фарм в @aniversecard_bot"""

    strings = {"name": "AniverseCard"}

    _request_timeout = 3
    _bot = "@aniversecard_bot"

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "arena",
                True,
                "Автоматически сражаться на арене",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "card",
                True,
                "Автоматически получать карты",
                validator=loader.validators.Boolean(),
            ),
        )

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        try:
            await self._client.send_message(
                self._bot,
                "💫 <i>~модуль автоматизации AniverseCard от VIP_IPru_tw. запущен~~</i>",
            )
        except YouBlockedUserError:
            await self._client(UnblockRequest(self._bot))
            await self._client.send_message(
                self._bot,
                "💫 <i>~модуль автоматизации AniverseCard от VIP_IPru_tw. запущен~~</i>",
            )

    async def _arena(self) -> bool:
        try:
            message = await self._get_msg("☁️ Меню")
            if not message:
                return False
            await message.click(data="arena")
            await asyncio.sleep(3)
            await message.click(data="arena_battle_search")
            await asyncio.sleep(3)
            await message.click(data="arena_battle_skip")
            return True
        except:
            pass

    async def _card(self) -> bool:
        try:
            message = await self._get_msg("🥡 Получить карту")
            return True
        except:
            pass

    async def _get_msg(self, key: str) -> Message:
        async with self._client.conversation(self._bot) as conv:
            await conv.send_message(key)
            r = await conv.get_response()
            return r

    @loader.loop(interval=15, autostart=True)
    async def loop(self):
        any_ = False
        if not self.get("fee_time") or self.get("fee_time") < time.time():
            if self.config["arena"]:
                await self._arena()
                any_ = True
                await asyncio.sleep(5)

            if self.config["card"]:
                await self._card()
                any_ = True
                await asyncio.sleep(5)

            if any_:
                self.set("fee_time", int(time.time() + 60 * 65))

        if any_:
            await self._client(ReadMentionsRequest(self._bot))