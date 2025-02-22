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


# requires: pornhub-api

from random import choice

from pornhub_api import PornhubApi
from telethon import types

from .. import loader, utils  # type: ignore


@loader.tds
class PhSrchMod(loader.Module):
    strings = {"name": "PornHub"}

    @loader.owner
    async def sphcmd(self, m: types.Message):
        "Найти видео на pornhub"
        if args := utils.get_args_raw(m):
            srch = args
        else:
            return await m.delete()
        api = PornhubApi()
        data = api.search.search(srch, ordering="mostviewed")
        video = choice(data.videos)
        await utils.asnwer(
            m,
            f'<b>Нашёл кое-что по запросу</b> <code>{srch}</code>: <a href="{video.url}">{video.title}</a>',
        )
