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
import traceback as tb

@loader.tds
class SearchMod(loader.Module):

    strings = {
        "name": "Search",
        "result": "<emoji document_id=5188217332748527444>🔍</emoji> <b>There is link with your query:</b>\n{}",
        "no_args": "<emoji document_id=5467910507916697142>💢</emoji> <b>You should specify query!</b>",
        "error": "<emoji document_id=5465665476971471368>❌</emoji> <b>An error occured:</b>\n{}",
    }

    strings_ru = {
        "result": "<emoji document_id=5188217332748527444>🔍</emoji> <b>Вот ссылка с твоим запросом:</b>\n{}",
        "no_args": "<emoji document_id=5467910507916697142>💢</emoji> <b>Ты должен указать запрос!</b>",
        "error": "<emoji document_id=5465665476971471368>❌</emoji> <b>Произошла ошибка:</b>\n{}",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "engine",
                "google",
                "Choose search engine/Выбери поисковую систему",
                validator=loader.validators.Choice(["google", "yandex", "microsoft-bing", "duckduckgo"]),
            ),
        )

    @loader.command(
        ru_doc="[запрос] - получить ссылку на поисковую систему с указанным запросом. (Указать поисковую систему можно через .cfg Search)"
    )
    async def searchcmd(self, message):
        """[query] - get link to search engine with your query. (You can specify search engine via .cfg Search)"""

        query = utils.get_args_raw(message) or (await message.get_reply_message()).raw_text

        if not query:
            await utils.answer(message, self.config("no_args"))
            return

        query_encoded = utils.escape_html(query).replace(' ', '+')

        get_search_engine = self.config["engine"]

        try:
            if str(get_search_engine) == "google":
                await utils.answer(message, self.strings("result").format(f"https://www.google.com/search?q={query_encoded}"))
            
            if str(get_search_engine) == "yandex":
                await utils.answer(message, self.strings("result").format(f"https://yandex.com/search/?text={query_encoded}"))

            if str(get_search_engine) == "duckduckgo":
                await utils.answer(message, self.strings("result").format(f"https://duckduckgo.com/?q={query_encoded}"))

            if str(get_search_engine) == "microsoft-bing":
                await utils.answer(message, self.strings("result").format(f"https://www.bing.com/search?q={query_encoded}"))

        except Exception:
            await utils.answer(message, self.strings("error").format(tb.format_exc()))