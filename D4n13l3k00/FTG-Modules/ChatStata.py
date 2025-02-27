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


from telethon.tl.types import (
    InputMessagesFilterPhotos,
    InputMessagesFilterVideo,
    InputMessagesFilterVoice,
    InputMessagesFilterMusic,
    InputMessagesFilterDocument,
    InputMessagesFilterContacts,
    InputMessagesFilterGeo,
    InputMessagesFilterRoundVideo,
    InputMessagesFilterUrl,
    InputMessagesFilterGif,
)

from .. import loader  # type: ignore


@loader.tds
class ChatStatisticMod(loader.Module):
    "Статистика чата"
    strings = {"name": "ChatStatistic"}

    @loader.owner
    async def statacmd(self, m):
        await m.edit("<b>Считаем...</b>")
        al = str((await m.client.get_messages(m.to_id, limit=0)).total)
        ph = str(
            (
                await m.client.get_messages(
                    m.to_id, limit=0, filter=InputMessagesFilterPhotos()
                )
            ).total
        )
        vi = str(
            (
                await m.client.get_messages(
                    m.to_id, limit=0, filter=InputMessagesFilterVideo()
                )
            ).total
        )
        mu = str(
            (
                await m.client.get_messages(
                    m.to_id, limit=0, filter=InputMessagesFilterMusic()
                )
            ).total
        )
        vo = str(
            (
                await m.client.get_messages(
                    m.to_id, limit=0, filter=InputMessagesFilterVoice()
                )
            ).total
        )
        vv = str(
            (
                await m.client.get_messages(
                    m.to_id, limit=0, filter=InputMessagesFilterRoundVideo()
                )
            ).total
        )
        do = str(
            (
                await m.client.get_messages(
                    m.to_id, limit=0, filter=InputMessagesFilterDocument()
                )
            ).total
        )
        urls = str(
            (
                await m.client.get_messages(
                    m.to_id, limit=0, filter=InputMessagesFilterUrl()
                )
            ).total
        )
        gifs = str(
            (
                await m.client.get_messages(
                    m.to_id, limit=0, filter=InputMessagesFilterGif()
                )
            ).total
        )
        geos = str(
            (
                await m.client.get_messages(
                    m.to_id, limit=0, filter=InputMessagesFilterGeo()
                )
            ).total
        )
        cont = str(
            (
                await m.client.get_messages(
                    m.to_id, limit=0, filter=InputMessagesFilterContacts()
                )
            ).total
        )
        await m.edit(
            (
                "<b>Всего сoообщений</b> {}\n"
                + "<b>Фоток:</b> {}\n"
                + "<b>Видосов:</b> {}\n"
                + "<b>Попсы:</b> {}\n"
                + "<b>Голосовых:</b> {}\n"
                + "<b>Кругляшков:</b> {}\n"
                + "<b>Файлов:</b> {}\n"
                + "<b>Ссылок:</b> {}\n"
                + "<b>Гифок:</b> {}\n"
                + "<b>Координат:</b> {}\n"
                + "<b>Контактов:</b> {}"
            ).format(al, ph, vi, mu, vo, vv, do, urls, gifs, geos, cont)
        )
