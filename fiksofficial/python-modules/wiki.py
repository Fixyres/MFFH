#         ______     ___  ___          _       _      
#    ____ | ___ \    |  \/  |         | |     | |     
#   / __ \| |_/ /   _| .  . | ___   __| |_   _| | ___ 
#  / / _` |  __/ | | | |\/| |/ _ \ / _` | | | | |/ _ \
# | | (_| | |  | |_| | |  | | (_) | (_| | |_| | |  __/
#  \ \__,_\_|   \__, \_|  |_/\___/ \__,_|\__,_|_|\___|
#   \____/       __/ |                                
#               |___/                                 

# На модуль распространяется лицензия "GNU General Public License v3.0"
# https://github.com/all-licenses/GNU-General-Public-License-v3.0

# meta developer: @pymodule
# requires: aiohttp

from .. import loader, utils
from ..inline.types import InlineQuery
import aiohttp


@loader.tds
class WikiSearchMod(loader.Module):
    """Search Wikipedia articles"""

    strings = {
        "name": "WikiSearch",
        "no_query": "❗ Please provide a search term.",
        "searching": "🔎 Searching Wikipedia for: <b>{query}</b>",
        "not_found": "🚫 No results found for: <code>{query}</code>",
        "error": "🚫 Error: <code>{error}</code>",
        "article": "<b>{title}</b>\n\n{summary}\n\n🌐 <a href='{url}'>Read more…</a>",
        "inline_title": "📚 {title}",
        "inline_description": "🔍 {summary}",
    }

    strings_ru = {
        "name": "WikiSearch",
        "no_query": "❗ Укажи термин для поиска.",
        "searching": "🔎 Поиск в Википедии по запросу: <b>{query}</b>",
        "not_found": "🚫 Ничего не найдено по запросу: <code>{query}</code>",
        "error": "🚫 Ошибка: <code>{error}</code>",
        "article": "<b>{title}</b>\n\n{summary}\n\n🌐 <a href='{url}'>Читать далее…</a>",
        "inline_title": "📚 {title}",
        "inline_description": "🔍 {summary}",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "lang",
                "en",
                lambda: "Language for Wikipedia search (e.g. en, ru, fr)",
                validator=loader.validators.RegExp(r"^[a-z]{2}$"),
            )
        )

    @loader.command(doc="[term] - Search Wikipedia for a term", ru_doc="[термин] - Поиск статьи в Википедии по запросу")
    async def wiki(self, message):
        query = utils.get_args_raw(message)
        if not query:
            return await utils.answer(message, self.strings("no_query"))

        await utils.answer(message, self.strings("searching").format(query=query))

        article = await self._get_article_async(query)
        if isinstance(article, str):
            return await utils.answer(message, self.strings("error").format(error=article))
        if article is None:
            return await utils.answer(message, self.strings("not_found").format(query=query))

        await utils.answer(
            message,
            self.strings("article").format(
                title=article["title"],
                summary=article["summary"],
                url=article["url"]
            )
        )

    async def _get_article_async(self, query):
        try:
            lang = self.config["lang"]
            search_url = f"https://{lang}.wikipedia.org/w/api.php"
            params = {
                "action": "query",
                "format": "json",
                "list": "search",
                "srsearch": query,
                "srlimit": 1
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(search_url, params=params) as res:
                    data = await res.json()
                    results = data.get("query", {}).get("search", [])
                    if not results:
                        return None

                title = results[0]["title"]
                summary_url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{title.replace(' ', '_')}"
                async with session.get(summary_url) as res:
                    data = await res.json()

                return {
                    "title": data.get("title", title),
                    "summary": data.get("extract", "No summary available"),
                    "url": data.get("content_urls", {}).get("desktop", {}).get("page", f"https://{lang}.wikipedia.org/wiki/{title.replace(' ', '_')}")
                }

        except Exception as e:
            return str(e)

    @loader.inline_everyone
    async def wiki_inline_handler(self, query: InlineQuery):
        """[term] - Inline Wikipedia search"""
        if not query.args:
            return await query.e400()

        article = await self._get_article_async(query.args)
        if isinstance(article, str):
            return await query.e500()
        if article is None:
            return await query.e404()

        return [{
            "title": self.strings("inline_title").format(title=article["title"]),
            "description": article["summary"][:100],
            "message": self.strings("article").format(
                title=article["title"],
                summary=article["summary"],
                url=article["url"]
            )
        }]