#     ___    __ __ ____
#    /   |  / //_//  _/
#   / /| | / ,<   / /  
#  / ___ |/ /| |_/ /   
# /_/  |_/_/ |_/___/   
#                      
#     __  _______  ____  _____
#    /  |/  / __ \/ __ \/ ___/
#   / /|_/ / / / / / / /\__ \ 
#  / /  / / /_/ / /_/ /___/ / 
# /_/  /_/\____/_____//____/
#
# meta developer: @aki_modules

from .. import loader, utils

class SearcherMod(loader.Module):
    """Модуль для поиска в различных поисковых системах"""
    strings = {"name": "Searcher"}

    async def searchcmd(self, message):
        """Поиск по запросу в различных системах"""
        query = utils.get_args_raw(message) or (await message.get_reply_message()).raw_text
        if not query:
            await utils.answer(message, "<b>Нужно указать запрос или ответить на сообщение.</b>")
            return

        query_encoded = utils.escape_html(query).replace(' ', '+')

        search_engines = {
            "Google": f"https://www.google.com/search?q={query_encoded}",
            "Bing": f"https://www.bing.com/search?q={query_encoded}",
            "DuckDuckGo": f"https://duckduckgo.com/?q={query_encoded}",
            "Yahoo": f"https://search.yahoo.com/search?p={query_encoded}",
            "Yandex": f"https://yandex.com/search/?text={query_encoded}"
        }

        links = "\n".join([f"{name}: <a href='{url}'>Link</a>" for name, url in search_engines.items()])

        result_message = f"🔍 <b>Links for your request:</b> {utils.escape_html(query)}\n{links}"

        await utils.answer(message, result_message, parse_mode="html")
