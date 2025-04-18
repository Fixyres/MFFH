__version__ = (1, 1, 4)

# --------------------------------------------------------------------------------
#
# Name: CheckUsername
# Description: пᴘовᴇᴘкᴀ имя пользовᴀтᴇля в ᴛᴇʟᴇɢʀᴀᴍ
# meta developer: @ManulMods
# authors: @llocJlednuy_cepafum, @ManulMods
# version: 1.1.4
#
# █▀▀ █▀▀ █▀█ ▄▀▄ █▀▀ █ █ █▄ ▄█
# █▄▄ ██▄ █▀▀ █▀█ █▀  █▄█ █ ▀ █
#
# ▀▄▀ █▄ ▄█ █▄ ▄█ █▀█ █▀▄ █ █ █   █▀▀ █▀▀
#  █  █ ▀ █ █ ▀ █ █▄█ █▄▀ █▄█ █▄▄ ██▄ ▄██
#
# --------------------------------------------------------------------------------

from telethon.tl import functions
import logging
from .. import loader, utils

logging.basicConfig(level=logging.INFO)

@loader.tds
class CheckUsername(loader.Module):
    """пᴘовᴇᴘкᴀ имя пользовᴀтᴇля в ᴛᴇʟᴇɢʀᴀᴍ"""

    strings = {
        "name": "CheckUsername",
        "description": "пᴘовᴇᴘкᴀ имя пользовᴀтᴇля в ᴛᴇʟᴇɢʀᴀᴍ",
        "authors": "@ManulMods",
        "versions": "1.1.4",
        "error": "<emoji document_id=5237814653010076467>🗓</emoji> <b>нᴇ ʏдᴀлось совᴇᴘшить вᴀши дᴇйствия...</b>",
        "check_true": "<emoji document_id=5237814653010076467>🗓</emoji> <b>юзᴇᴘнᴇйм:</b> @{} <b>(нᴇ достʏпᴇн!)</b>",
        "check_false": "<emoji document_id=5235875883297824772>🗓</emoji> <b>юзᴇᴘнᴇйм:</b> @{} <b>(достʏпᴇн!)</b>",
        "check_false_args": "<emoji document_id=5237814653010076467>🗓</emoji> <b>пожᴀлʏйстᴀ впишитᴇ юзᴇᴘнᴇйм котоᴘый вы хотитᴇ пᴘовᴇᴘить...</b>"
    }

    async def client_ready(self, client, db):
        self._db = db
        self._client = client

    @loader.command()
    async def check(self, message):
        """<юзернейм> - пᴘовᴇᴘяᴇт достʏпность имᴇни пользовᴀтᴇля"""
        args = utils.get_args_raw(message)

        if not args:
            await utils.answer(message, self.strings["check_false_args"])
            return

        username = args.strip()

        result = await self.check_username_availability(username)

        if result:
            await utils.answer(message, self.strings["check_false"].format(username))
        else:
            await utils.answer(message, self.strings["check_true"].format(username))

    async def check_username_availability(self, username: str) -> bool:
        try:
            request = functions.account.CheckUsernameRequest(username=username)
            result = await self._client(request)
            return result
        except Exception as e:
            logging.exception(f"Ошибка при проверке юзернейма {username}: {e}")
            return False
        
