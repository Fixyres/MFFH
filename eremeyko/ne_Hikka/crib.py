# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# Original repository: https://github.com/eremeyko/ne_Hikka
#
# ©️ Dan Gazizullin, 2021-2024
# This file is a part of Hikka Userbot
# 🌐 https://github.com/hikariatama/Hikka
# 🔑 https://www.gnu.org/licenses/agpl-3.0.html
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
