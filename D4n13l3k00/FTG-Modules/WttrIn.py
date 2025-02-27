# .------.------.------.------.------.------.------.------.------.------.
# |D.--. |4.--. |N.--. |1.--. |3.--. |L.--. |3.--. |K.--. |0.--. |0.--. |
# | :/\: | :/\: | :(): | :/\: | :(): | :/\: | :(): | :/\: | :/\: | :/\: |
# | (__) | :\/: | ()() | (__) | ()() | (__) | ()() | :\/: | :\/: | :\/: |
# | '--'D| '--'4| '--'N| '--'1| '--'3| '--'L| '--'3| '--'K| '--'0| '--'0|
# `------`------`------`------`------`------`------`------`------`------'
#
#                     Copyright 2023 t.me/D4n13l3k00
#           Licensed under the Creative Commons CC BY-NC-ND 4.0
#
#                    Full license text can be found at:
#       https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode
#
#                           Human-friendly one:
#            https://creativecommons.org/licenses/by-nc-nd/4.0

# meta developer: @D4n13l3k00


import aiohttp

from .. import loader, utils  # type: ignore


@loader.tds
class WttrInMod(loader.Module):
    """WttrIn"""

    strings = {"name": __doc__}

    @loader.owner
    async def wthrcmd(self, m):
        """.wthr <Город если надо>
        Получить текущую погоду
        """
        rr = utils.get_args_raw(m)

        await utils.answer(
            m,
            "<code>{}</code>".format(
                await (
                    await aiohttp.ClientSession().get(
                        f"https://wttr.in/{rr if rr is not None else ''}?0Tq&lang=ru"
                    )
                ).text()
            ),
        )
