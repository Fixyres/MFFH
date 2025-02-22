#   Coded by D4n13l3k00    #
#     t.me/D4n13l3k00      #
# This code under AGPL-3.0 #

import random

from .. import loader, utils  # type: ignore


@loader.tds
class TryMod(loader.Module):
    """Try"""

    strings = {"name": "Try"}

    @loader.owner
    async def trycmd(self, message):
        """.try действие"""
        do = utils.get_args_raw(message)
        rnd = random.choice(
            [
                "Удачно",
                "Удачно",
                "Неудачно",
                "Неудачно",
                "Удачно",
                "Неудачно",
                "Удачно",
                "Неудачно",
                "Удачно",
                "Неудачно",
            ]
        )
        await message.edit(f"<b>{do}</b>\n\n<code>{rnd}</code>")
