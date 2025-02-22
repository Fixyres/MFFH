#   █▀▀ ▄▀█   █▀▄▀█ █▀█ █▀▄ █▀
#   █▀░ █▀█   █░▀░█ █▄█ █▄▀ ▄█

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: EvalAliases
# Description: Алиаси для eval
# meta developer: @FAmods
# meta banner: https://github.com/FajoX1/FAmods/blob/main/assets/banners/evalaliases.png?raw=true
# ---------------------------------------------------------------------------------

import hikkatl

import re
import random
import asyncio
import logging

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class EvalAliases(loader.Module):
    """Алиаси для eval"""

    strings = {
        "name": "EvalAliases",

        "no_args": "<emoji document_id=5854929766146118183>❌</emoji> <b>Нужно </b><code>{}{} {}</code>",

        "already_created": "<emoji document_id=5854929766146118183>❌</emoji> <b>Алиас <code>{}</code> уже существует!</b>",
        "alias_created": """<emoji document_id=5429633836684157942>⚡️</emoji> <b>Алиас <code>{}</code> создан!</b>
        
<i>Используй его с помощью <code>{}v{}</code></i>""",

        "alias_not_found": "<emoji document_id=5854929766146118183>❌</emoji> <b>Алиас <code>{}</code> не найден!</b>",
        "alias_deleted": "<emoji document_id=5854929766146118183>❌</emoji> <b>Алиас <code>{}</code> удален!</b>",

        "no_aliases": "<emoji document_id=5854929766146118183>❌</emoji> <b>Вы ещё не создали алиасов!</b>",
        "aliases": """<emoji document_id=4985626654563894116>🖥</emoji> <b>Список алиасов</b>
        
{}""",
    }

    async def client_ready(self, client, db):
        self.db = db
        self._client = client

    @loader.command()
    async def addea(self, message):
        """Добавить алиас"""

        args = utils.get_args_raw(message)
        try:
            name, code = args.split(" ")
        except:
            return await utils.answer(message, self.strings["no_args"].format(self.get_prefix(), "addea", "[имя] [код]"))

        aliases = self.db.get(self.name, "aliases", [])

        if any(alias['name'] == name for alias in aliases):
            return await utils.answer(message, self.strings["already_created"].format(name))

        aliases.append({"name": name, "code": code})

        self.db.set(self.name, "aliases", aliases)

        await utils.answer(message, self.strings["alias_created"].format(name, self.get_prefix(), name))

    @loader.command()
    async def removea(self, message):
        """Удалить алиас"""

        name = utils.get_args_raw(message)
        if not name:
            return await utils.answer(message, self.strings["no_args"].format(self.get_prefix(), "removea", "[имя]"))

        aliases = self.db.get(self.name, "aliases", [])

        alias_to_remove = next((alias for alias in aliases if alias['name'] == name), None)
        if not alias_to_remove:
            return await utils.answer(message, self.strings["alias_not_found"].format(name))

        aliases.remove(alias_to_remove)

        self.db.set(self.name, "aliases", aliases)

        await utils.answer(message, self.strings["alias_deleted"].format(name))

    @loader.command()
    async def getea(self, message):
        """Получить список алиасов для Eval"""

        aliases = self.db.get(self.name, "aliases", [])

        if not aliases:
            return await utils.answer(message, self.strings["no_aliases"])

        aliases_list = ""
        for alias in aliases:
            aliases_list += f"<emoji document_id=4974259868996207180>▫️</emoji> <code>{self.get_prefix()}v{alias['name']}</code>"

        await utils.answer(message, self.strings["aliases"].format(aliases_list))
    
    async def watcher(self, event):
        try:
            if event.from_id != self.tg_id:
                return
        except:
            return
        if f"{self.get_prefix()}v" not in event.raw_text:
            return 
        alias_name = event.raw_text.split(f"{self.get_prefix()}v")[1]
        logger.info(alias_name)
        aliases = self.db.get(self.name, "aliases", [])

        alias = next((alias for alias in aliases if alias['name'] == alias_name), None)
        if not alias:
            return

        await event.delete()    
        await self.invoke("e", alias['code'], event.peer_id)