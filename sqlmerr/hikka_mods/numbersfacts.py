from hikkatl.types import Message
from .. import loader, utils
import requests

# meta developer: @sqlmerr_m
# meta icon: https://github.com/sqlmerr/hikka_mods/blob/main/assets/icons/numberfacts.png?raw=true
# meta banner: https://github.com/sqlmerr/sqlmerr/blob/main/assets/hikka_mods/sqlmerrmodules_numberfacts.png?raw=true


@loader.tds
class NumbersFacts(loader.Module):
    """Interesting facts about numbers | Check the config"""

    strings = {
        "name": "NumbersFacts",
        "noargs": "<emoji document_id=5240241223632954241>🚫</emoji> <b>You didn't enter any arguments</b>",
        "indexerror": "<emoji document_id=5240241223632954241>🚫</emoji> <b>You have not entered enough arguments</b>",
        "type": "Type of facts about numbers. Trivia is a fact from life, math is a mathematical fact, date and year is a question about a date",
    }

    string_ru = {
        "noargs": "<emoji document_id=5240241223632954241>🚫</emoji> <b>Вы не ввели аргументы</b>",
        "indexerror": "<emoji document_id=5240241223632954241>🚫</emoji> <b>Вы ввели недостаточно аргументов</b>",
        "type": "Тип фактов о числах. Trivia — факт из жизни, math — математический факт, date и year — вопрос про дату",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "type",
                "math",
                lambda: self.strings("type"),
                validator=loader.validators.Choice(["date", "math", "year", "trivia"]),
            ),
        )

    @loader.command(ru_doc="[число] - получить факт об этом числе")
    async def numberfact(self, message: Message):
        """[number] - get fact about number"""
        if not (args := utils.get_args_raw(message).split()):
            return await utils.answer(message, self.strings("no_args"))
        number = args[0]
        _type = self.config["type"]

        url = f"http://numbersapi.com/{number}/{_type}"
        response = await utils.run_sync(requests.get, url)
        data = response.text
        await utils.answer(
            message,
            await self._client.translate(
                message.peer_id,
                message,
                to_lang=self._db.get("hikka.translations", "lang")[0:2],
                raw_text=data,
                entities=message.entities,
            ),
        )
