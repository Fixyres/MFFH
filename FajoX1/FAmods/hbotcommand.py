#   █▀▀ ▄▀█   █▀▄▀█ █▀█ █▀▄ █▀
#   █▀░ █▀█   █░▀░█ █▄█ █▄▀ ▄█

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: HbotCommand
# Description: Дополнительная команда для твоего inline бота
# meta developer: @FAmods
# meta banner: https://github.com/FajoX1/FAmods/blob/main/assets/banners/hbotcommand.png?raw=true
# ---------------------------------------------------------------------------------

import re
import asyncio 
import logging

from aiogram import types
from .. import loader, utils
from ..inline.types import BotInlineMessage

logger = logging.getLogger(__name__)

@loader.tds
class HbotCommand(loader.Module):
    """Дополнительная команда для твоего inline бота"""

    strings = {
        "name": "HbotCommand",

        "loading_cfg": "<b><emoji document_id=5334904192622403796>🔄</emoji> Открываю настройку...</b>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "command_text",
                "<b>Этот текст можно изменить в .cfg HbotCommand</b>",
                lambda: "Текст сообщения",
            ),
            loader.ConfigValue(
                "command_image",
                "https://2.bp.blogspot.com/-wkYFtsM9jf8/XD9CK8-u-rI/AAAAAAAAArI/OWAfpxubCXA4H7sG72YPDEqR8I_yR7AeACKgBGAs/w4096-h2304-c/shooting-star-sunset-anime-horizon-30-4k.jpg",
                lambda: "Картинка сообщения",
            ),
            loader.ConfigValue(
                "command_button",
                """FAmods, https://t.me/famods""",
                lambda: "Кнопки сообщения",
            ),
            loader.ConfigValue(
                "command_name",
                "/famods",
                lambda: "Команда для кастомного сообщения",
            ),
            loader.ConfigValue(
                "command_work",
                True,
                lambda: "Кастомное сообщение",
                validator=loader.validators.Boolean()
            ),
        )


    async def client_ready(self, client, db):
        self.db = db
        self._client = client

    @loader.command()
    async def busername(self, message):
        """Посмотреть юзернейм бота"""

        await utils.answer(message, f"<b><emoji document_id=5785175271011259591>🌀</emoji> Username бота: @{self.inline.bot_username}</b>")
        
    @loader.command()
    async def bcsettings(self, message):
        """Настройка команды бота"""

        msg = await utils.answer(message, self.strings['loading_cfg'])

        await self.invoke("config", "HbotCommand", message.peer_id)

        await msg.delete()

    async def aiogram_watcher(self, message: BotInlineMessage):
        if self.config['command_work'] and message.text == self.config['command_name']:
            markup = None
            if self.config['command_button']:
                markup = types.InlineKeyboardMarkup()
                pattern = r'(\w+),\s(https?://\S+)'
                matches = re.findall(pattern, self.config['command_button'])
                if matches:
                    title, url = matches[0]
                    button = types.InlineKeyboardButton(text=title, url=url)
                    markup.add(button)

            if self.config['command_image']:
                return await message.answer_photo(photo=self.config['command_image'], caption=self.config['command_text'], reply_markup=markup)

            await message.answer(
                self.config['command_text'],
                reply_markup=markup
            )