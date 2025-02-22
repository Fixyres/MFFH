# .------.------.------.------.------.------.------.------.------.------.
# |D.--. |4.--. |N.--. |1.--. |3.--. |L.--. |3.--. |K.--. |0.--. |0.--. |
# | :/\: | :/\: | :(): | :/\: | :(): | :/\: | :(): | :/\: | :/\: | :/\: |
# | (__) | :\/: | ()() | (__) | ()() | (__) | ()() | :\/: | :\/: | :\/: |
# | '--'D| '--'4| '--'N| '--'1| '--'3| '--'L| '--'3| '--'K| '--'0| '--'0|
# `------`------`------`------`------`------`------`------`------`------'
#
#                     Copyright 2022 t.me/D4n13l3k00
#           Licensed under the Creative Commons CC BY-NC-ND 4.0
#
#                    Full license text can be found at:
#       https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode
#
#                           Human-friendly one:
#            https://creativecommons.org/licenses/by-nc-nd/4.0

# meta developer: @D4n13l3k00


from requests import get

from .. import loader, utils  # type: ignore


@loader.tds
class FullApiMod(loader.Module):
    """Фулл"""

    strings = {"name": "FullApi"}

    @loader.owner
    async def rndfullcmd(self, m):
        "получить рандомный фулл :)"
        await utils.answer(
            m,
            '<a href="'
            + get("https://api.d4n13l3k00.ru/shit/random_full").json()["url"]
            + '">Подгончик для братков</a>',
        )
