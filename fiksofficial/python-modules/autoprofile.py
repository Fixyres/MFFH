# На модуль распространяется лицензия "GNU General Public License v3.0"
# https://github.com/all-licenses/GNU-General-Public-License-v3.0

# meta developer: @pymodule

from hikkatl.types import Message
from telethon.tl.functions.account import UpdateProfileRequest
from .. import loader, utils
import asyncio
import random


@loader.tds
class AutoProfileMod(loader.Module):
    """Automatically update your profile description"""

    strings = {
        "name": "AutoProfile",
        "no_desc": "<b>[AutoProfile] No saved descriptions!</b>",
        "error": "<b>[AutoProfile] Auto bio update error:</b> {}",
        "enabled": "<b>[AutoProfile] Auto bio enabled!</b>",
        "disabled": "<b>[AutoProfile] Auto bio disabled!</b>",
        "usage": "<b>[AutoProfile] Usage:</b> .autodesc on/off",
        "desc_added": "<b>[AutoProfile] Description added:</b> {}",
        "desc_removed": "<b>[AutoProfile] Description removed:</b> {}",
        "invalid_number": "<b>[AutoProfile] Invalid number!</b>",
        "enter_number": "<b>[AutoProfile] Enter a description number to delete!</b>",
        "desc_list": "<b>[AutoProfile] Description list:</b>\n{}",
        "desc_empty": "<b>[AutoProfile] No descriptions saved!</b>",
        "enter_text": "<b>[AutoProfile] Enter text to add!</b>",
        "set_interval": "<b>[AutoProfile] Update interval set:</b> {} sec.",
        "enter_interval": "<b>[AutoProfile] Enter interval in seconds!</b>",
    }

    strings_ru = {
        "no_desc": "<b>[AutoProfile] Нет сохранённых описаний!</b>",
        "error": "<b>[AutoProfile] Ошибка автообновления описания:</b> {}",
        "enabled": "<b>[AutoProfile] Автоописание включено!</b>",
        "disabled": "<b>[AutoProfile] Автоописание отключено!</b>",
        "usage": "<b>[AutoProfile] Использование:</b> .autodesc on/off",
        "desc_added": "<b>[AutoProfile] Описание добавлено:</b> {}",
        "desc_removed": "<b>[AutoProfile] Описание удалено:</b> {}",
        "invalid_number": "<b>[AutoProfile] Некорректный номер!</b>",
        "enter_number": "<b>[AutoProfile] Введите номер описания для удаления!</b>",
        "desc_list": "<b>[AutoProfile] Список описаний:</b>\n{}",
        "desc_empty": "<b>[AutoProfile] Список описаний пуст!</b>",
        "enter_text": "<b>[AutoProfile] Введите текст для добавления!</b>",
        "set_interval": "<b>[AutoProfile] Интервал смены установлен:</b> {} сек.",
        "enter_interval": "<b>[AutoProfile] Введите интервал в секундах!</b>",
    }

    def __init__(self):
        self._task = None

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

        self.config = loader.ModuleConfig(
            "enabled", False, "Auto bio enabled",
            "interval", 3600, "Interval in seconds",
            "descriptions", [], "List of descriptions"
        )

        if self.config["enabled"]:
            self._task = asyncio.create_task(self._update_bio())

    async def _update_bio(self):
        while self.config["enabled"]:
            descs = self.config["descriptions"]
            if not descs:
                await self.client.send_message("me", self.strings("no_desc"))
                return

            try:
                new_bio = random.choice(descs)
                await self.client(UpdateProfileRequest(about=new_bio[:70]))
            except Exception as e:
                await self.client.send_message("me", self.strings("error").format(str(e)))

            await asyncio.sleep(self.config["interval"])

    @loader.command(
        ru_doc="Включить или отключить автоописание",
        en_doc="Enable or disable auto bio updates"
    )
    async def autodesccmd(self, message: Message):
        """Toggle auto bio"""
        arg = utils.get_args_raw(message)
        if arg not in ["on", "off"]:
            await utils.answer(message, self.strings("usage"))
            return

        enabled = arg == "on"
        self.config["enabled"] = enabled

        if enabled:
            self._task = asyncio.create_task(self._update_bio())
            await utils.answer(message, self.strings("enabled"))
        else:
            await utils.answer(message, self.strings("disabled"))

    @loader.command(
        ru_doc="Добавить описание: .adddesc <текст>",
        en_doc="Add a description: .adddesc <text>"
    )
    async def adddesccmd(self, message: Message):
        """Add description"""
        text = utils.get_args_raw(message)
        if not text:
            await utils.answer(message, self.strings("enter_text"))
            return

        self.config["descriptions"].append(text)
        await utils.answer(message, self.strings("desc_added").format(text))

    @loader.command(
        ru_doc="Удалить описание по номеру: .deldesc <номер>",
        en_doc="Delete description by number: .deldesc <number>"
    )
    async def deldesccmd(self, message: Message):
        """Delete description"""
        args = utils.get_args_raw(message)
        if not args.isdigit():
            await utils.answer(message, self.strings("enter_number"))
            return

        index = int(args) - 1
        descs = self.config["descriptions"]
        if 0 <= index < len(descs):
            removed = descs.pop(index)
            await utils.answer(message, self.strings("desc_removed").format(removed))
        else:
            await utils.answer(message, self.strings("invalid_number"))

    @loader.command(
        ru_doc="Показать список описаний",
        en_doc="Show list of descriptions"
    )
    async def listdesccmd(self, message: Message):
        """List descriptions"""
        descs = self.config["descriptions"]
        if not descs:
            await utils.answer(message, self.strings("desc_empty"))
            return

        text = "\n".join([f"{i + 1}. {d}" for i, d in enumerate(descs)])
        await utils.answer(message, self.strings("desc_list").format(text))

    @loader.command(
        ru_doc="Установить интервал обновления: .setinterval <сек>",
        en_doc="Set update interval: .setinterval <seconds>"
    )
    async def setintervalcmd(self, message: Message):
        """Set update interval"""
        args = utils.get_args_raw(message)
        if not args.isdigit():
            await utils.answer(message, self.strings("enter_interval"))
            return

        self.config["interval"] = int(args)
        await utils.answer(message, self.strings("set_interval").format(args))