#   █▀▀ ▄▀█   █▀▄▀█ █▀█ █▀▄ █▀
#   █▀░ █▀█   █░▀░█ █▄█ █▄▀ ▄█

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: Hetsu
# Description: Search and install modules easily.
# meta developer: @FAmods
# meta banner: https://github.com/FajoX1/FAmods/blob/main/assets/banners/hetsu.png?raw=true
# requires: aiohttp
# ---------------------------------------------------------------------------------

import re
import asyncio
import aiohttp

import logging

from telethon import types, functions
from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class Hetsu(loader.Module):
    """Search and install modules easily."""

    strings = {
        "name": "Hetsu",

        "no_q": "<emoji document_id=5854929766146118183>❌</emoji> <b>You need to write <code>{}hetsu [query]</code></b>",
        "inline_no_q": "<emoji document_id=5854929766146118183>❌</emoji> <b>Enter query.</b>",

        "no_modules": "<b>❌ No modules founded.</b>",

        "searching": """<emoji document_id=5404630946563515782>🔍</emoji> <b>Hetsu searching...</b>
        
<i><emoji document_id=6028117381690167734>🛡</emoji> Searching above 900+ modules. All modules are safety and clearly moderated.</i>""",

        "module": """<b><emoji document_id=5843843420468024653>⭐️</emoji> Module <code>{module_name}</code></b> {developer}

<emoji document_id=5843862283964390528>🔖</emoji> <b>Ratio:</b> <code>{ratio}</code>
<emoji document_id=5874960879434338403>🔎</emoji> <b>Query:</b> {query}

<emoji document_id=5879785854284599288>ℹ️</emoji> <b>Description:</b> <i>{description}</i>

<emoji document_id=5967816500415827773>💻</emoji> <b>Source code:</b> <a href="{link}">click</a>

<emoji document_id=5899757765743615694>⬇️</emoji> <code>{prefix}dlm {link}</code>""",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "limit",
                5,
                lambda: "Max results of modules.",
            ),
        )


    async def client_ready(self, client, db):
        self.db = db
        self._client = client

    @loader.command()
    async def hetsucmd(self, message):
        """Search module"""

        q = utils.get_args_raw(message)
        if not q:
            return await utils.answer(message, self.strings["no_q"].format(self.get_prefix()))
        
        await utils.answer(message, self.strings['searching'])

        q_default = q

        if not bool(re.fullmatch(r"[A-Za-z\s\d\W]+", q)):
            q = await self._client(
                functions.messages.TranslateTextRequest(
                    peer=False,
                    id=False,
                    text=[
                        types.TextWithEntities(
                            q_default,
                            [],
                        )
                    ],
                    to_lang="en",
                )
            )

            q = q.result[0].text        

        logger.info(q)

        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://hetsu.fajox.one/api/search",
                params={
                    "q": q,
                    "limit": 1,
                }
            ) as response:
                modules = (await response.json())['results']

        if not modules:
            return await utils.answer(message, self.strings['no_modules'])
        
        module = modules[0]

        module_text = self.strings['module'].format(
            module_name=module['name'],
            developer=f"<b>by <code>{module['developer']}</code></b>" if module['developer'] else "",
            ratio=module['ratio'],
            query=q_default,
            description=module['description'] if module['description'] else "No description.",
            link=module['link'],
            prefix=self.get_prefix()
        )

        if module['banner']:
            return await utils.answer_file(
                message,
                module['banner'],
                caption=module_text,
            )
        else:
            return await utils.answer(
                message,
                module_text
            )

    @loader.inline_handler()
    async def hetsu(self, query):
        """Search module"""

        q = query.args

        if not q:
            return {
                "title": "No query",
                "description": "Enter query for search module",
                "thumb": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Flat_cross_icon.svg/1024px-Flat_cross_icon.svg.png",
                "message": self.strings['inline_no_q'],
            }

        q_default = q

        if not bool(re.fullmatch(r"[A-Za-z\s\d\W]+", q)):
            q = await self._client(
                functions.messages.TranslateTextRequest(
                    peer=False,
                    id=False,
                    text=[
                        types.TextWithEntities(
                            q,
                            [],
                        )
                    ],
                    to_lang="en",
                )
            )

        q = str(q)

        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://hetsu.fajox.one/api/search",
                params={
                    "q": q,
                    "limit": self.config['limit'],
                }
            ) as response:
                modules = (await response.json())['results']

        if not modules:
            return {
                "title": "No modules",
                "description": "No modules founded with this query.",
                "thumb": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Flat_cross_icon.svg/1024px-Flat_cross_icon.svg.png",
                "message": self.strings['no_modules'],
            }

        answer = []

        for module in modules:
            answer.append({
                "title": module['name'],
                "description": module['description'] if module['description'] else "No description.",
                "thumb": "https://img.icons8.com/m_outlined/512/FFFFFF/info.png",
                "message": self.strings['module'].format(
                    module_name=module['name'],
                    developer=f"<b>by <code>{module['developer']}</code></b>" if module['developer'] else "",
                    ratio=module['ratio'],
                    query=q_default,
                    description=module['description'] if module['description'] else "No description.",
                    link=module['link'],
                    prefix=self.get_prefix()
                ),
            })

        return answer
