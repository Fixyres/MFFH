#  _____                          
# |_   _|____  ____ _ _ __   ___  
#   | |/ _ \ \/ / _` | '_ \ / _ \ 
#   | | (_) >  < (_| | | | | (_) |
#   |_|\___/_/\_\__,_|_| |_|\___/ 
#                              
# meta banner: https://i.ibb.co/3yNfKRLL/image-10490.jpg
# meta developer: @toxano_modules 
# scope: @toxano_modules

import asyncio
import random
import logging
from telethon import events
from telethon.errors import ChatWriteForbiddenError, UserNotParticipantError, PeerIdInvalidError, ChannelPrivateError
from .. import loader

logger = logging.getLogger(__name__)

@loader.tds
class ImitatorMod(loader.Module):
    """Имитация активности в чате"""

    strings = {"name": "Imitator"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue("DLY", 5, "Задержка между действиями")
        )
        self._tsk = {}
        self._act = {}
        self.MDS = [
            "typing", "voice", "video", "game", "photo",
            "round", "audio", "document", "location", "contact", "mixed"
        ]

    async def _imt(self, cid, mod):
        """Запускает имитацию активности"""
        while self._act.get(cid):
            try:
                await self._client.get_entity(cid)
                async with self._client.action(cid, action="typing"):
                    pass
                act = random.choice(self.MDS[:-1]) if mod == "mixed" else mod
                async with self._client.action(cid, action=act):
                    await asyncio.sleep(self.config["DLY"])
            except (ChatWriteForbiddenError, UserNotParticipantError, PeerIdInvalidError, ChannelPrivateError):
                self._act.pop(cid, None)
                if cid in self._tsk:
                    self._tsk[cid].cancel()
                return
            except Exception as e:
                logger.error(f"Ошибка при имитации в чате {cid}: {e}")
                await asyncio.sleep(2)

    async def imcmd(self, msg):
        """Запускает имитацию активности. Режимы: typing, voice, video, game, photo, round, audio, document, location, contact, mixed"""
        await msg.delete()
        arg = msg.raw_text.split()
        cid = msg.chat_id

        if len(arg) < 2 or arg[1].lower() not in self.MDS:
            return

        mod = arg[1].lower()

        if cid in self._act:
            self._act.pop(cid, None)
            if cid in self._tsk:
                self._tsk[cid].cancel()

        self._act[cid] = mod
        self._tsk[cid] = asyncio.create_task(self._imt(cid, mod))

    async def imstopcmd(self, msg):
        """Останавливает имитацию активности"""
        await msg.delete()
        cid = msg.chat_id

        if cid in self._act:
            self._act.pop(cid, None)
            if cid in self._tsk:
                self._tsk[cid].cancel()
