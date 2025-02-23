# ---------------------------------------------------------------------------------
#  /\_/\  🌐 This module was loaded through https://t.me/hikkamods_bot
# ( o.o )  🔐 Licensed under the GNU AGPLv3.
#  > ^ <   ⚠️ Owner of heta.hikariatama.ru doesn't take any responsibilities or intellectual property rights regarding this script
# ---------------------------------------------------------------------------------
# Name: codemanager
# Author: thomasmod
# Commands:
# .tofile | .tofilen | .tomsg
# ---------------------------------------------------------------------------------

__version__ = (1, 0, 0)

#            ▀█▀ █ █ █▀█ █▀▄▀█ ▄▀█ █▀
#             █  █▀█ █▄█ █ ▀ █ █▀█ ▄█
#             https://t.me/netuzb
#
# 🔒 Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# meta desc: Manager bot for working on modules (all Python files in general).
# meta pic: https://te.legra.ph/file/e534f736497cd1b3e711b.png
# meta banner: https://te.legra.ph/file/16c25a32943f74d7a47bf.jpg
# meta developer: @wilsonmods

# scope: hikka_only
# scope: hikka_min 1.4.0

import io
import os
from asyncio import sleep

import pygments
from pygments.formatters import ImageFormatter
from pygments.lexers import Python3Lexer

from .. import loader, utils

# EMOJI PLACE
em_warn = "🚨 "
em_wait = "🕒 "

manage_byte = "utf8"


@loader.tds
class CodeManagerMod(loader.Module):
    """Manager bot for working on modules (all Python files in general)."""

    strings = {
        "name": "👨‍💻 Code-Manager",
        "manager_reply_to_msg": em_warn + "<b>Reply to message.</b>",
        "manager_reply_to_file": em_warn + "<b>Please, reply to file.</b>",
        "manager_pls_wait": em_wait + "<b>Please, wait for end...</b>",
        "manager_code_name": "-code-manager.py",
    }

    strings_ru = {
        "manager_reply_to_msg": (
            em_warn + "<b>Необходимо ответить реплэем на кодовое сообщение...</b>"
        ),
        "manager_reply_to_file": em_warn + "<b>Укажи файл с реплэем...</b>",
        "manager_pls_wait": em_wait + "<b>Пожалуйста, дождитесь окончания...</b>",
    }

    strings_uz = {
        "manager_reply_to_msg": (
            em_warn
            + "<b>Faylga konvertlash uchun kerakli habarga javob tariqasida...</b>"
        ),
        "manager_reply_to_file": em_warn + "<b>Faylga javob tariqasida...</b>",
        "manager_pls_wait": em_wait + "<b>Iltimos, tayyor bo'lguncha kuting...</b>",
    }

    async def client_ready(self, client, db):
        self.client = client

    async def tofilecmd(self, message):
        """Reply to message code"""
        text = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if not reply or not reply.message:
            await message.edit(self.strings("manager_reply_to_file", message))
            return
        text = bytes(reply.raw_text, manage_byte)
        fname = utils.get_args_raw(message) or str(
            message.id + reply.id
        ) + self.strings("manager_code_name")
        file = io.BytesIO(text)
        file.name = fname
        file.seek(0)
        await reply.reply(file=file)
        await message.delete()

    async def tofilencmd(self, message):
        """[name.format] - Reply to message code (enter the name and format)"""
        text = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if not reply or not reply.message:
            await message.edit(self.strings("manager_reply_to_file", message))
            return
        text = bytes(reply.raw_text, manage_byte)
        fname = utils.get_args_raw(message) or str(message.id + reply.id) + f"{text}"
        file = io.BytesIO(text)
        file.name = fname
        file.seek(0)
        await reply.reply(file=file)
        await message.delete()

    async def tomsgcmd(self, message):
        """Reply to file code"""
        reply = await message.get_reply_message()
        if not reply or not reply.file:
            await message.edit(self.strings("manager_reply_to_msg", message))
            return
        await message.edit(self.strings("manager_pls_wait", message))
        await sleep(0.9)
        text = await reply.download_media(bytes)
        text = str(text, manage_byte)
        text = f"{text}"
        await utils.answer(message, utils.escape_html(text))