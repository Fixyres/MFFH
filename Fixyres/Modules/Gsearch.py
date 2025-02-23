#   █▀▀ ▄▀█   █▀▄▀█ █▀█ █▀▄ █▀
#   █▀░ █▀█   █░▀░█ █▄█ █▄▀ ▄█

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: Gsearch
# Description: Поиск в Google
# meta developer: @FAmods
# meta banner: https://github.com/FajoX1/FAmods/blob/main/assets/banners/gsearch.png?raw=true
# requires: aiohttp google BeautifulSoup4
# ---------------------------------------------------------------------------------

import time
import asyncio
import logging
import aiohttp

from bs4 import BeautifulSoup
from googlesearch import search
from urllib.parse import unquote

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class Gsearch(loader.Module):
    """Поиск в Google"""

    strings = {
        "name": "Gsearch",

        "no_q": "<emoji document_id=5854929766146118183>❌</emoji> <b>Должно быть </b><code>{}gsearch [запрос]</code>",
        "no_result": "<b>😕 Ничего не нашёл по этому запросу</b>",

        "searching": "<emoji document_id=5326015457155620929>🔄</emoji> <b>Поиск в google.com...</b>",
        "searched": """<b>
<emoji document_id=5308054573938647180>🔎</emoji> Результаты поиска

<emoji document_id=5188311512791393083>🔎</emoji> Запрос:</b> <code>{}</code>
{}

<i>{} результатов за {} сек</i>
</b>""",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "results",
                5,
                lambda: "Количество результатов",
            ),
            loader.ConfigValue(
                "safe_search",
                False,
                lambda: "Безопастный поиск",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "lang",
                "ru",
                lambda: "Язык результатов",
            ),
            loader.ConfigValue(
                "emoji",
                "<emoji document_id=5098187078693290864>▪️</emoji>",
                lambda: "Эмодзи в результатах поиска",
            ),
            loader.ConfigValue(
                "user_agent",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
                lambda: "Ваш User-Agent"
            ),
            loader.ConfigValue(
                "show_title",
                True,
                lambda: "Заголовки в результате",
                validator=loader.validators.Boolean()
            )
        )


    async def client_ready(self, client, db):
        self.db = db
        self._client = client

    @loader.command()
    async def gsearch(self, message):
        """Поиск в Google"""

        q = utils.get_args_raw(message)
        if not q:
            return await utils.answer(message, self.strings["no_q"].format(self.get_prefix()))

        await utils.answer(message, self.strings['searching'])

        safe_s = "off"

        if self.config["safe_search"]:
            safe_s = "on"

        count_s = 0

        start_time = time.time()

        searched_result = ""

        emojii = self.config["emoji"]

        for url in search(q, stop=self.config["results"], lang=self.config["safe_search"], safe=safe_s):
            if self.config['show_title']:
                try:
                  async with aiohttp.ClientSession() as session:
                    async with session.get(url, headers={"User-Agent": self.config['user_agent']}) as response:
                        html = await response.read()
                  soup = BeautifulSoup(html, 'html.parser')
                  title = soup.find('title').text
                  searched_result += f"\n{emojii} <i><a href='{unquote(url)}'>{title}</a></i>"
                except:
                    searched_result += f"\n{emojii} <i>{unquote(url)}</i>"
            else:
                searched_result += f"\n{emojii} <i>{unquote(url)}</i>"
            count_s += 1

        end_time = time.time()
        execution_time = end_time - start_time
        
        if count_s == 0:
            return await utils.answer(message, self.strings['no_result'])

        return await utils.answer(message, self.strings['searched'].format(q, searched_result, count_s, execution_time))