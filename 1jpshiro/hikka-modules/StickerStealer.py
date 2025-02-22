# ---------------------------------------------------------------------------------
# Author: @shiro_hikka
# Name: Sticker stealer
# Description: Emoji / Sticker pickpocket
# Commands: steal
# ---------------------------------------------------------------------------------
#              © Copyright 2025
#
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# ---------------------------------------------------------------------------------
# scope: hikka_only
# meta developer: @shiro_hikka
# meta banner: https://0x0.st/s/FIR0RnhUN5pZV5CZ6sNFEw/8KBz.jpg
# ---------------------------------------------------------------------------------

__version__ = (1, 0, 1)

from .. import loader, utils
from telethon.tl.types import Message
import asyncio

@loader.tds
class StickerStealer(loader.Module):
    """Emoji / Sticker pickpocket"""

    strings = {
        "name": "StickerStealer",
        "incorrect": "<emoji document_id=5233657262106485430>🤨</emoji> It's not a sticker or emoji"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "Emoji pack",
                "emsaved",
                lambda: "Specify a name of your emoji pack",
            ),
            loader.ConfigValue(
                "Animated sticker pack",
                "vssaved",
                lambda: "Specify a name of your animated sticker pack"
            ),
            loader.ConfigValue(
                "Static sticker pack",
                "sssaved",
                lambda: "Specify a name of your static sticker pack"
            )
        )


    def checkType(self, reply, message):
        if hasattr(reply, "media"):
            if hasattr(reply.media, "document"):
                mime_type = reply.media.document.mime_type.split('/')
                if mime_type[1] == "webp":
                    return 3
                elif mime_type[1] == "webm":
                    return 2

        if reply.entities:
            return 1

        else:
            return 0


    async def stealcmd(self, message: Message):
        """ <reply / quote reply> - add an emoji or sticker to your pack
        Emoji: one type of emoji only is possible to be used at time"""
        await utils.answer(message, "....")
        reply = await message.get_reply_message()
        bot = "Stickers"

        cfg_ref = {
            1: self.config["Emoji pack"],
            2: self.config["Animated sticker pack"],
            3: self.config["Static sticker pack"]
        }
        entity_type = {
            1: "An emoji",
            2: "A sticker",
            3: "A sticker"
        }

        async with self.client.conversation(bot) as bot:
            _entity_type = self.checkType(reply, message)
            if _entity_type == 0:
                return await utils.answer(message, self.strings["incorrect"])

            elif _entity_type == 1:
                outgoing = await bot.send_message("/addemoji")
            else:
                outgoing = await bot.send_message("/addsticker")
            response = await bot.get_response()

            await asyncio.sleep(2)
            await outgoing.delete()
            await response.delete()

            if _entity_type == 1:
                outgoing = await bot.send_message(self.config["emoji"])
            elif _entity_type == 2:
                outgoing = await bot.send_message(self.config["video_sticker"])
            else:
                outgoing = await bot.send_message(self.config["static_sticker"])

            response = await bot.get_response()
            await asyncio.sleep(2)
            await response.delete()
            await outgoing.delete()

            if response.text == "Не выбран набор стикеров.":
                return await utils.answer(message, f"Create {entity_type[_entity_type].lower()} pack with a public name <b>{cfg_ref[_entity_type]}</b>")

            if _entity_type == 1:
                emoji = reply.message
                toSend = reply
            else:
                emoji = reply.media.document.attributes[1].alt
                toSend = reply

            outgoing = await bot.send_message(toSend)
            response = await bot.get_response()
            await asyncio.sleep(2)
            await outgoing.delete()
            await response.delete()

            outgoing = await bot.send_message(emoji)
            response = await bot.get_response()
            await asyncio.sleep(2)
            await outgoing.delete()
            await response.delete()

            await utils.answer(message, f"<b>{entity_type[_entity_type]} added</b>")
