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

import io

from telethon import types

from .. import loader, utils  # type: ignore


@loader.tds
class SaverMod(loader.Module):
    strings = {"name": "Saver"}

    async def client_ready(self, client, db):
        self.db = db

    @loader.owner
    async def бляcmd(self, m: types.Message):
        ".бля <reply> - скачать самоуничтожающееся фото"
        reply = await m.get_reply_message()
        if not reply or not reply.media or not reply.media.ttl_seconds:
            return await m.edit("бля")
        await m.delete()
        new = io.BytesIO(await reply.download_media(bytes))
        new.name = reply.file.name
        await m.client.send_file("me", new)

    @loader.owner
    async def swбляcmd(self, m: types.Message):
        "Переключить режим автозагрузки фото в лс"
        new_val = not self.db.get("Saver", "state", False)
        self.db.set("Saver", "state", new_val)
        await utils.answer(m, f"<b>[Saver]</b> <pre>{new_val}</pre>")

    async def watcher(self, m: types.Message):
        if (
            m
            and m.media
            and m.media.ttl_seconds
            and self.db.get("Saver", "state", False)
        ):
            new = io.BytesIO(await m.download_media(bytes))
            new.name = m.file.name
            await m.client.send_file(
                "me",
                new,
                caption=f"<b>[Saver] Фото от</b> {f'@{m.sender.username}' if m.sender.username else m.sender.first_name} | <pre>{m.sender.id}</pre>\n"
                f"Время жизни: <code>{m.media.ttl_seconds}sec</code>",
            )
