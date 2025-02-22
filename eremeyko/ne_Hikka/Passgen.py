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

from .. import loader, utils
from random import sample, choice, shuffle
from string import digits, ascii_letters, punctuation

@loader.tds
class PassGen(loader.Module):
    """Генерирует пароли. Да."""
    strings = {
        'name': 'PassGenerator',
        'error5': "<emoji document_id=5843952899184398024>🚫</emoji> <b>Ваш пароль не может быть короче 5 знаков!</b>",
        'error2000': "<emoji document_id=5843952899184398024>🚫</emoji> <b>Ваш пароль не может быть длинее 2000 знаков!</b>"
    }

    def __init__(self):
        self.length = 0

        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "digits",
                True,
                "Использовать цифры в пароле?",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "ascii_letters",
                True,
                "Использовать буквы в пароле?",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "punctuation",
                True,
                "Использовать символы в пароле?",
                validator=loader.validators.Boolean(),
            )
            )

    @loader.command()
    async def pgen(self, message) -> None:
        """длина — генерирует пароль на заданную длину символов. Например: .pgen 7"""
        error:str = "\n\n"
        all_chars:str = ""
        pass_char: list = []

        args = utils.get_args(message)
        if not args:
            self.length = 7
        else:
            self.length = int(args[0])

            if self.length < 5 and self.length < 2000:
                self.length = 5
                error += self.strings["error5"]
            elif self.length > 2000 and self.length > 5:
                self.length = 2000
                error += self.strings["error2000"]

        if self.config["digits"]:
            pass_char.append(choice(digits))
            all_chars += digits
        if self.config["ascii_letters"]:
            pass_char.append(choice(ascii_letters))
            all_chars += ascii_letters
        if self.config["punctuation"]:
            pass_char.append(choice(punctuation))
            all_chars += punctuation
        if not pass_char:
            return await message.edit(("<b>И из чего я тебе должен пароль лепить, умник?</b><emoji document_id=5472152561215618810>🤓</emoji>\n\n"
                                       "Открывай <code>.cfg PassGen</code> и включи хоть что-то"
                                    ))

        while len(pass_char) < self.length:
            pass_char += sample(all_chars, min(self.length - len(pass_char), len(all_chars)))

        shuffle(pass_char)
        password = ''.join(pass_char)

        return await message.edit("Ваш пароль: <code>{}</code>{}".format(password, error))
