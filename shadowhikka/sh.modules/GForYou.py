# █▀ █░█ ▄▀█ █▀▄ █▀█ █░█░█
# ▄█ █▀█ █▀█ █▄▀ █▄█ ▀▄▀▄▀

# Copyright 2023 t.me/shadow_modules
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# meta developer: @shadow_modules
# meta banner: https://i.imgur.com/pmh9eAE.jpeg

from .. import loader, utils
from telethon.tl.types import Message  # type: ignore


@loader.tds
class GYForYouMod(loader.Module):
    """Погуглю за тебя"""

    strings = {
        "name": "GYForYou",
        "google": "<emoji document_id=5300882244842300470>👩‍💻</emoji><b> I googled for you</b>\n",
        "no_args": "❌ No args",
    }
    strings_ru = {
        "google": "<emoji document_id=5300882244842300470>👩‍💻</emoji><b> Я погуглил за тебя</b>\n",
        "no_args": "❌ Нет аргументов",
    }

    async def googlecmd(self, message: Message):
        """<args>"""
        args = utils.get_args_raw(message).replace(" ", "+")
        if not args:
            await utils.answer(message, self.strings("no_args"))
            return
        await utils.answer(message, self.strings("google") + f"https://track24.ru/google/?q={args}")
