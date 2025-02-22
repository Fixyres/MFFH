from .. import loader, utils
import requests

# meta developer: @kmodules
__version__ = (1, 0, 0)


@loader.tds
class ShortLinkerMod(loader.Module):
    """Модуль для сокращения ссылок."""
    
    strings = {
        "name": "K:ShortLinker",
        "no_args": "<emoji document_id=5220197908342648622>❗</emoji> <b>Wrong format! Write: .shortlink <url></b>",
        "error": "<emoji document_id=5220046725493828505>✍️</emoji> <b>Error!</b>",
        "success": "<emoji document_id=5219899949281453881>✅</emoji> <b>Shortened URL:</b>\n\n{}"
    }
    
    strings_ru = {
        "name": "K:ShortLinker", 
        "no_args": "<emoji document_id=5220197908342648622>❗</emoji> <b>Неправильный формат! Напишите: .shortlink <url></b>",
        "error": "<emoji document_id=5220046725493828505>✍️</emoji> <b>Ошибка!</b>",
        "success": "<emoji document_id=5219899949281453881>✅</emoji> <b>Сокращённая ссылка:</b>\n\n{}"
    }

    async def shortlinkcmd(self, message):
        """Использование: .shortlink <url>"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings["no_args"])
            return

        try:
            api = f"https://is.gd/create.php?format=json&url={args}"
            short_url = requests.get(api).json()["shorturl"]
            await utils.answer(
                message,
                self.strings["success"].format(short_url)
            )
        except Exception:
            await utils.answer(message, self.strings["error"])
