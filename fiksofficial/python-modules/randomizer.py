# На модуль распространяется лицензия "GNU General Public License v3.0"
# https://github.com/all-licenses/GNU-General-Public-License-v3.0

# scope: hikka_only
# meta developer: @pymodule

from .. import loader, utils
import random
from hikkatl.types import Message

@loader.tds
class RandomizerMod(loader.Module):
    """Randomly selects one of the comma-separated values."""

    strings = {
        "name": "Randomizer",
        "too_few_values": "Please provide at least two values separated by commas.",
        "result": "Random choice: {result}"
    }

    strings_ru = {
        "name": "Рандомайзер",
        "too_few_values": "Укажи хотя бы два значения через запятую.",
        "result": "Случайный выбор: {result}"
    }

    @loader.command(
        doc="Picks a random value from those listed (comma-separated)",
        ru_doc="Выбирает случайное значение из перечисленных через запятую"
    )
    async def randomizecmd(self, message: Message):
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings("too_few_values"))
            return

        items = [item.strip() for item in args.split(",") if item.strip()]
        if len(items) < 2:
            await utils.answer(message, self.strings("too_few_values"))
            return

        result = random.choice(items)
        await utils.answer(message, self.strings("result").format(result=result))
