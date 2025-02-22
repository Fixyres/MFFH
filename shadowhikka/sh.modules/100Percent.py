# █▀ █░█ ▄▀█ █▀▄ █▀█ █░█░█
# ▄█ █▀█ █▀█ █▄▀ █▄█ ▀▄▀▄▀

# Copyleft 2022 t.me/shadow_modules
# This module is free software
# You can edit this module

# meta developer: @shadow_modules
# scope: hikka_only
# scope: hikka_min 1.3.0
# meta banner: https://i.imgur.com/g7yk55s.jpeg

from .. import loader, utils
from telethon.tl.types import Message  # type: ignore


@loader.tds
class PercentMod(loader.Module):
    """Create your text with inline percentages"""

    strings = {"name": "Percent", "no_args": "❗ You didn't provide arguments"}

    strings_ru = {
        "_cls_doc": "Создайте свой текст с инлайн процентами",
        "no_args": "❗ Вы не указали аргументы",
    }

    @loader.command(
        ru_doc="<Текст с процентами> <Текст в конце> [интервал] -> Для создания"
    )
    async def percentcmd(self, message: Message):
        """<Text with percentages> <Text at the end> [interval] -> For creating"""
        args = utils.get_args(message)
        if len(args) not in {2, 3}:
            await utils.answer(message, self.strings("no_args"))
            return

        interval = args[-1] if args[-1].isdigit() else 0.2
        await self.animate(
            message,
            [f"{args[0]} {x}%" for x in range(100)] + [args[1]],
            interval=int(interval),
            inline=True,
        )
