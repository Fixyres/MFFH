__version__ = (1, 0, 0)
#          █  █ █▄ █ █▄ █ █▀▀ ▀▄▀ █▀█ █▄ █
#          ▀▄▄▀ █ ▀█ █ ▀█ ██▄  █  █▄█ █ ▀█ ▄
#                © Copyright 2025
#            ✈ https://t.me/unneyon

# 🔒 Licensed under CC-BY-NC-ND 4.0 unless otherwise specified.
# 🌐 https://creativecommons.org/licenses/by-nc-nd/4.0
# + attribution
# + non-commercial
# + no-derivatives

# You CANNOT edit, distribute or redistribute this file without direct permission from the author.

# meta banner: https://mods.unneyon.ru/banners/warpigs.png
# meta pic: https://static.unneyon.ru/mods/warpigs_icon.png
# meta developer: @unneyon_hmods
# scope: hikka_only
# scope: hikka_min 1.6.3

import asyncio
import logging
import traceback

from telethon import types

from .. import loader, utils


logger = logging.getLogger(__name__)


@loader.tds
class WarPigsMod(loader.Module):
    """Some auto-functions for your pig in @warpigs_bot"""

    strings = {
        "name": "WarPigs",
        "dforpm": "<emoji document_id=5312526098750252863>❌</emoji> <b>This command cannot be used in PM.</b>",
        "af_started": "<emoji document_id=5454014806950429357>⚔️</emoji> <b>Autofight was enabled for this chat.</b>",
        "af_stopped": "<emoji document_id=5462990652943904884>😴</emoji> <b>Autofight was disabled for this chat.</b>",
        "ag_started": "<emoji document_id=5463081281048818043>🍕</emoji> <b>Autogrow was enabled for this chat.</b>",
        "ag_stopped": "<emoji document_id=5462990652943904884>😴</emoji> <b>Autogrow was disabled for this chat.</b>",
        "no_name": "<emoji document_id=5312526098750252863>❌</emoji> <b>You have not specified a new name for your pig.</b>",
        "new_name": "<emoji document_id=5463071033256848094>👑</emoji> <b>Now your pig's new name is:</b> {name}"
    }

    strings_ru = {
        "_cls_doc": "Немного авто-функций для вашего хряка в @warpigs_bot",
        "dforpm": "<emoji document_id=5312526098750252863>❌</emoji> <b>Эту команду нельзя использовать в ЛС.</b>",
        "af_started": "<emoji document_id=5454014806950429357>⚔️</emoji> <b>Автобой был включён для этого чата.</b>",
        "af_stopped": "<emoji document_id=5462990652943904884>😴</emoji> <b>Автобой был отключён для этого чата.</b>",
        "ag_started": "<emoji document_id=5463081281048818043>🍕</emoji> <b>Автокормёжка была включена для этого чата.</b>",
        "ag_stopped": "<emoji document_id=5462990652943904884>😴</emoji> <b>Автокормёжка была отключена для этого чата.</b>",
        "no_name": "<emoji document_id=5312526098750252863>❌</emoji> <b>Вы не указали новое имя для вашего хряка.</b>",
        "new_name": "<emoji document_id=5463071033256848094>👑</emoji> <b>Теперь новое имя вашего хряка:</b> {name}"
    }

    bot = "@warpigs_bot"
    bot_id = 2028629176


    async def client_ready(self, client, db):
        self.client = client
        self.logger = logging.getLogger(__name__)
        self.autofight.start()
        self.autogrow.start()


    async def message_q(
        self,
        text: str,
        chat_id: int,
        mark_read: bool = False,
        delete: bool = False,
    ):
        async with self.client.conversation(chat_id, exclusive=False) as conv:
            msg = await conv.send_message(text)
            while True:
                await asyncio.sleep(1)
                response = await conv.get_response()
                if response.from_id != self.bot_id:
                    continue
                if mark_read:
                    await conv.mark_read()
                if delete:
                    await msg.delete()
                    await response.delete()
                return response
            await conv.cancel_all()


    @loader.loop(interval=86400)
    async def autofight(self):
        chats = self.get("chats", {})
        for i in chats.keys():
            if chats[i].get("autofight"):
                try:
                    r = await self.message_q(
                        chat_id=int(i),
                        text=f"/fight{self.bot}"
                    )
                except Exception as e:
                    self.logger.error(f"Ошибка отправки сообщения в чат {i}:\n{traceback.format_exc()}")
                    continue
            await asyncio.sleep(1)


    @loader.loop(interval=86400)
    async def autogrow(self):
        chats = self.get("chats", {})
        for i in chats.keys():
            if chats[i].get("autogrow"):
                try:
                    r = await self.message_q(
                        chat_id=int(i),
                        text=f"/grow{self.bot}"
                    )
                except Exception as e:
                    self.logger.error(f"Ошибка отправки сообщения в чат {i}:\n{traceback.format_exc()}")
                    continue
            await asyncio.sleep(1)


    @loader.command(
        ru_doc="- Включить/отключить автобой"
    )
    async def afightcmd(self, message: types.Message):
        """- Enable/disable autofight"""
        if message.is_private:
            await utils.answer(message, self.strings("dforpm"))
            return

        chats = self.get("chats", {})
        chat = chats.get(str(message.chat_id), {"autofight": False, "autogrow": False})
        chat['autofight'] = not chat.get('autofight', False)
        chats[str(message.chat_id)] = chat
        self.set("chats", chats)

        self.autofight.stop()
        await asyncio.sleep(1)
        self.autofight.start()

        await utils.answer(
            message, self.strings("af_started") if chat['autofight'] else self.strings("af_stopped")
        )


    @loader.command(
        ru_doc="- Включить/отключить автокормёжку"
    )
    async def agrowcmd(self, message: types.Message):
        """- Enable/disable autogrow"""
        if message.is_private:
            await utils.answer(message, self.strings("dforpm"))
            return

        chats = self.get("chats", {})
        chat = chats.get(str(message.chat_id), {"autofight": False, "autogrow": False})
        chat['autogrow'] = not chat.get('autogrow', False)
        chats[str(message.chat_id)] = chat
        self.set("chats", chats)

        self.autogrow.stop()
        await asyncio.sleep(1)
        self.autogrow.start()

        await utils.answer(
            message, self.strings("ag_started") if chat['autogrow'] else self.strings("ag_stopped")
        )


    @loader.command(
        ru_doc="<имя> - Меняет имя вашего хряка"
    )
    async def setnamecmd(self, message: types.Message):
        """<name> - Changes your pig's name"""
        args = utils.get_args_raw(message)
        if not args:
            return await utils.answer(message, self.strings("no_name"))

        r = await self.message_q(chat_id=message.chat_id, text=f"/name{self.bot} {args}")
        await utils.answer(message, self.strings("new_name").format(name=args))