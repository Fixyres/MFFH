#   █▀▀ ▄▀█   █▀▄▀█ █▀█ █▀▄ █▀
#   █▀░ █▀█   █░▀░█ █▄█ █▄▀ ▄█

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: YTsearch
# Description: Поиск в Youtube
# meta developer: @FAmods
# meta banner: https://github.com/FajoX1/FAmods/blob/main/assets/banners/ytsearch.png?raw=true
# requires: youtube-search-python
# ---------------------------------------------------------------------------------

import time
import asyncio
import logging

from youtubesearchpython import VideosSearch, ChannelsSearch

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class YTsearch(loader.Module):
    """Поиск в Youtube"""

    strings = {
        "name": "YTsearch",

        "no_q": "<emoji document_id=5854929766146118183>❌</emoji> <b>Должно быть <code>{}{} [запрос]</code></b>",
        "no_result": "<b>😕 Ничего не нашёл по этому запросу</b>",

        "searching": "<emoji document_id=5278611117130653414>🔄</emoji> <b>Поиск в youtube.com...</b>",
        "searched": """<b>
<emoji document_id=5278611117130653414>🔎</emoji> Результаты поиска {}

<emoji document_id=5188311512791393083>🔎</emoji> Запрос:</b> <code>{}</code>{}

<i>{} результатов за {} сек</i>
</b>""",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "limit_channels",
                10,
                lambda: "Максимальное количество видео в результате.",
            ),
            loader.ConfigValue(
                "limit_video",
                10,
                lambda: "Максимальное количество видео в результате.",
            ),
            loader.ConfigValue(
                "lang",
                "ru",
                lambda: "Язык поиска.",
            ),
        )


    async def client_ready(self, client, db):
        self.db = db
        self._client = client

    @loader.command()
    async def ytvsearch(self, message):
        """Поиск видео в Youtube"""

        q = utils.get_args_raw(message)
        if not q:
            return await utils.answer(message, self.strings["no_q"].format(self.get_prefix(), "ytvsearch"))

        await utils.answer(message, self.strings['searching'])

        count_s = 0

        start_time = time.time()

        searched_result = ""

        for v in VideosSearch(query=q, limit=self.config['limit_video'], language=self.config['lang']).result()['result']:
            searched_result += f"""
            
<b><a href='{v['link']}'>{v['title']}</a> от <a href='{v['channel']['link']}'>{v['channel']['name']}</a></b>
<i>{v['viewCount']['text'].replace('views', 'просмотров')}</i> (<i>{v['duration']}</i>) <i>{v['publishedTime']}</i>"""
            count_s += 1

        end_time = time.time()
        execution_time = end_time - start_time
        
        if count_s == 0:
            return await utils.answer(message, self.strings['no_result'])

        return await utils.answer(message, self.strings['searched'].format("видео", q, searched_result, count_s, execution_time))
    
    @loader.command()
    async def ytcsearch(self, message):
        """Поиск каналов в Youtube"""

        q = utils.get_args_raw(message)
        if not q:
            return await utils.answer(message, self.strings["no_q"].format(self.get_prefix(), "ytcsearch"))

        await utils.answer(message, self.strings['searching'])

        count_s = 0

        start_time = time.time()

        searched_result = ""

        for c in ChannelsSearch(query=q, limit=self.config['limit_channels'], language=self.config['lang']).result()['result']:
            searched_result += "\n" if count_s == 0 else ""
            searched_result += f"""
<b><a href='{c['link']}'>{c['title']}</a> (<code>{c['subscribers']}</code>)</b>"""
            count_s += 1

        end_time = time.time()
        execution_time = end_time - start_time
        
        if count_s == 0:
            return await utils.answer(message, self.strings['no_result'])

        return await utils.answer(message, self.strings['searched'].format("каналов", q, searched_result, count_s, execution_time))