from .. import loader, utils
import wikipedia
import logging

# meta developer: @kmodules
__version__ = (1, 0, 0)

@loader.tds
class WikiSearchMod(loader.Module):
    """Поиск информации в Википедии"""

    strings = {
        "name": "WikiSearch",
        "no_args": "Please specify search query",
        "no_result": "Nothing found for this query",
        "header": "<b>[</b><emoji document_id=5122983123188974322>👁</emoji><b>] Wikipedia - Search</b>\n\n",
        "searching": "<emoji document_id=5116414868357907335>🔥</emoji> <b>Ищу в Wikipedia...</b>"
    }
    
    strings_ru = {
        "name": "WikiSearch", 
        "no_args": "Укажите поисковый запрос",
        "no_result": "По данному запросу ничего не найдено",
        "header": "<b>[</b><emoji document_id=5122983123188974322>👁</emoji><b>] Wikipedia - Search</b>\n\n",
        "searching": "<emoji document_id=5116414868357907335>🔥</emoji> <b>Ищу в Wikipedia...</b>"
    }

    async def client_ready(self, client, db):
        self.client = client
        
    @loader.command()
    async def wksearch(self, message):
        """Поиск в Википедии - .wksearch <запрос>"""
        args = utils.get_args_raw(message)
        
        if not args:
            await utils.answer(message, self.strings["no_args"])
            return

        await utils.answer(message, self.strings["searching"])

        try:
            wikipedia.set_lang('ru')
            result = wikipedia.summary(args, sentences=10)
            
            await utils.answer(
                message,
                self.strings["header"] + f"<b>{result}</b>"
            )
            
        except wikipedia.exceptions.DisambiguationError:
            await utils.answer(message, self.strings["no_result"])
        except wikipedia.exceptions.PageError:
            await utils.answer(message, self.strings["no_result"])
        except Exception as e:
            logging.exception(e)
            await utils.answer(message, self.strings["no_result"])
          
