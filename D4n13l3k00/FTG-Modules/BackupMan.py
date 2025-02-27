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


import ast
import io

from .. import loader, utils  # type: ignore


@loader.tds
class BackupManMod(loader.Module):
    """BackupMan"""

    strings = {"name": "BackupMan"}

    async def client_ready(self, _, db):
        self._db = db

    @loader.owner
    async def restmcmd(self, m):
        "Установить все модули из *.bkm файла"
        reply = await m.get_reply_message()
        if not reply or not reply.file or reply.file.name.split(".")[-1] != "bkm":
            return await m.edit("<b>[BackupMan]</b> Reply to <code>*.bkm</code> file")
        modules = self._db.get("friendly-telegram.modules.loader", "loaded_modules", [])
        txt = io.BytesIO(await reply.download_media(bytes))
        valid, already_loaded = 0, 0
        for i in txt.read().decode("utf-8").split("\n"):
            if i not in modules:
                valid += 1
                modules.append(i)
            else:
                already_loaded += 1
        self._db.set("friendly-telegram.modules.loader", "loaded_modules", modules)
        await m.edit(
            "<b>[BackupMan]</b>\n\n"
            "<i>Загружено модулей:</i> <code>{valid}</code>\n"
            "<i>Загружены ранее:</i> <code>{already_loaded}</code>\n\n"
            + (
                "<b>> Юзербот автоматически перезагрузится</b>"
                if valid != 0
                else "<b>> Ничего не загружено</b>"
            )
        )
        if valid != 0:
            await self.allmodules.commands["restart"](await m.respond("_"))

    @loader.owner
    async def backmcmd(self, m):
        "Сделать бэкап модулей в *.bkm файл"
        modules = self._db.get("friendly-telegram.modules.loader", "loaded_modules", [])
        txt = io.BytesIO("\n".join(modules).encode("utf-8"))
        txt.name = f"BackupMan-{(await m.client.get_me()).id}.bkm"
        await m.client.send_file(
            m.to_id,
            txt,
            caption="<b>[BackupMan]</b> <i>Бэкап модулей</i>\n"
            f"<i>Модулей:</i> <code>{len(modules)}</code>\n"
            "<i>Для загрузки бэкапа используй модуль:</i>\n"
            "<code>.dlmod https://d4n13l3k00.ru/modules/BackupMan.py</code>",
        )
        await m.delete()

    @loader.owner
    async def restncmd(self, m):
        "Установить все заметки из *.bkn файла\n<f> - Заменять уже существующие заметки"
        args: list or None = utils.get_args_raw(m)
        force = "f" in args.lower()
        reply = await m.get_reply_message()
        if not reply or not reply.file or reply.file.name.split(".")[-1] != "bkn":
            return await m.edit("<b>[BackupMan]</b> Reply to <code>*.bkn</code> file")
        notes = self._db.get("friendly-telegram.modules.notes", "notes", {})
        txt = io.BytesIO(await reply.download_media(bytes))
        valid, already_loaded = 0, 0
        for k, v in ast.literal_eval(txt.read().decode("utf-8")).items():
            if k not in notes or force:
                notes[k] = v
                valid += 1
            else:
                already_loaded += 1
        self._db.set("friendly-telegram.modules.notes", "notes", notes)
        await m.edit(
            "<b>[BackupMan]</b>\n\n"
            f"<i>Загружено/заменено заметок:</i> <code>{valid}</code>\n"
            f"<i>Загружены ранее:</i> <code>{already_loaded}</code>"
        )

    @loader.owner
    async def backncmd(self, m):
        "Сделать бэкап заметок в *.bkn файл"
        modules = self._db.get("friendly-telegram.modules.notes", "notes", {})
        txt = io.BytesIO(str(modules).encode("utf-8"))
        txt.name = f"BackupMan-{(await m.client.get_me()).id}.bkn"
        await m.client.send_file(
            m.to_id,
            txt,
            caption=f"<b>[BackupMan]</b> <i>Бэкап заметок</i>\n"
            f"<i>Заметок:</i> <code>{len(modules)}</code>\n"
            "<i>Для загрузки бэкапа используй модуль:</i>\n"
            "<code>.dlmod https://d4n13l3k00.ru/modules/BackupMan.py</code>",
        )
        await m.delete()
