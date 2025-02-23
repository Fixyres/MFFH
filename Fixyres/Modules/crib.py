# meta developer: @eremod
__version__ = (1, 0, 3)

from hikkatl.types import Message
from .. import loader, utils

@loader.tds
class CribModule(loader.Module):
    """Модуль для замены гласных на 'i'"""
    strings = {"name": "Crib"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "exclude_letters",
                ["о", "я"], 
                "Буквы, которые не будут заменяться на 'i'",
                validator=loader.validators.Series(loader.validators.String()),
            ),
        )

    async def client_ready(self, client, db):
        self.client = client

    async def watcher(self, message: Message):
        """Функция, которая обрабатывает все сообщения владельца"""
        if not self.get("crib_enabled", False):
            return

        if message.out:
            text = message.text
            exclude = self.config["exclude_letters"]
            new_text = ''.join(
                char if (
                    char.lower() in exclude or char.lower() not in "aeiouаеёиоуыэюя"
                ) else ("I" if char.isupper() else "i")
                for char in text
            )
            await utils.answer(message, new_text)

    @loader.command(ru_doc="Меняет гласные на i (команда на вкл и выкл)")
    async def cribcmd(self, message: Message):
        """Включает или выключает замену"""
        state = not self.get("crib_enabled", False)
        self.set("crib_enabled", state)
        await utils.answer(
            message, f"Скрипт {'включен' if state else 'выключен'}."
        )
