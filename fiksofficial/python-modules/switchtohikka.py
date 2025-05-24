# На модуль распространяется лицензия "GNU General Public License v3.0"
# https://github.com/all-licenses/GNU-General-Public-License-v3.0

# meta developer: @PyModule

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from hikkatl.types import Message
from .. import loader, utils
import asyncio

@loader.tds
class SwitchToHikka(loader.Module):
    """Auto switching from Heroku to Hikka"""

    strings = {"name": "SwitchToHikka"}

    async def client_ready(self, client, db):
        self._db = db

        if self.get("done"):
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(text='🥷 Support chat', url='https://t.me/hikka_talks')],[
                InlineKeyboardButton(text='📖 Github', url='https://github.com/hikariatama/Hikka')
            ]]
            )
            await self.inline._bot.send_photo(
                self.tg_id, 
                "https://raw.githubusercontent.com/hikariatama/Hikka/refs/heads/master/assets/bot_pfp.png",
                caption="<b>Hello, you switched to Hikka, an advanced Telegram userbot.</b>"
                "\nModule for switching is unloaded.",
                reply_markup=keyboard,
            )

            self.set("done", None)  # Очистка БД для повторного переключения

            await self.invoke('unloadmod', 'SwitchToHikka', self.inline.bot_id)

    @loader.command()
    async def switchtohikka(self, message: Message):
        """ - Automatically switch to Hikka"""

        await utils.answer(message, "Compatibility check... Wait")

        if "hikariatama" in utils.get_git_info()[1]:
            return await utils.answer(message, "You`re already running Hikka.")

        await utils.answer(message, "Everything is okay, I started switching...")

        await asyncio.create_subprocess_shell(
            "git remote set-url origin https://github.com/hikariatama/Hikka.git",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=utils.get_base_dir(),
        )

        await asyncio.create_subprocess_shell(
            "git config --global user.email 'you@example.com'",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=utils.get_base_dir(),
        )

        await asyncio.create_subprocess_shell(
            "git config --global user.name 'Your Name'",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=utils.get_base_dir(),
        )

        await asyncio.create_subprocess_shell(
            "git pull",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=utils.get_base_dir(),
        )

        peer_id = self.inline.bot_id

        await self.invoke('fconfig', 'updater GIT_ORIGIN_URL https://github.com/hikariatama/Hikka', peer_id)

        await utils.answer(message, "Automatically restarting. (after restart, it's all done)")

        self.set("done", True)

        await self.invoke('update', '-f', peer_id)
