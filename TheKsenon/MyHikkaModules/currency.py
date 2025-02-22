from .. import loader, utils
import requests

@loader.tds
class CurrencyMod(loader.Module):
    """Get current currency exchange rates"""

    strings = {
        "name": "K:Currency",
        "usage": "<emoji document_id=5465665476971471368>❌</emoji> <b>Usage: .rate USD EUR.</b>",
        "error": "<emoji document_id=5467890025217661107>‼️</emoji> <b>Error getting exchange rate.</b>",
        "searching": "<emoji document_id=5188311512791393083>🔎</emoji> <b>Searching for exchange rate...</b>",
        "result": "<emoji document_id=5359785904535774578>💼</emoji> <b>1 {} = {} {}</b>"
    }

    strings_ru = {
        "name": "K:Currency",
        "usage": "<emoji document_id=5465665476971471368>❌</emoji> <b>Использование: .rate USD EUR.</b>",
        "error": "<emoji document_id=5467890025217661107>‼️</emoji> <b>Ошибка получения курса валют.</b>",
        "searching": "<emoji document_id=5188311512791393083>🔎</emoji> <b>Ищу курс валют...</b>",
        "result": "<emoji document_id=5359785904535774578>💼</emoji> <b>1 {} = {} {}</b>"
    }

    @loader.command()
    async def rate(self, message):
        """<from> <to> - Get exchange rate"""
        args = utils.get_args_raw(message)
        if not args or len(args.split()) != 2:
            await utils.answer(message, self.strings["usage"])
            return

        base, target = args.upper().split()
        await utils.answer(message, self.strings["searching"])
        try:
            response = requests.get(f"https://open.er-api.com/v6/latest/{base}")
            data = response.json()
            rate = data["rates"][target]
            await utils.answer(message, self.strings["result"].format(base, rate, target))
        except Exception:
            await utils.answer(message, self.strings["error"])
