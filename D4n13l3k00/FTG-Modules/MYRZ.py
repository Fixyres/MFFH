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


import requests

from .. import loader, utils  # type: ignore


@loader.tds
class MailSearcherMod(loader.Module):
    "AntiPublic MYRZ"
    strings = {"name": "AntiPublic MYRZ"}

    def __init__(self):
        self.name = self.strings["name"]

    async def client_ready(self, client, db):
        self.db = db

    async def myrz_keycmd(self, m):
        self.db.set("myrz", "key", str(m.raw_text.split(" ", 1)[1]))
        await m.edit("[AntiPublic MYRZ] Токен установлен")

    @loader.owner
    async def msrchcmd(self, m):
        "Получить пароли почты/логина"
        key = self.db.get("myrz", "key", None)
        if not key:
            await m.edit(
                "<b>Укажите ключ из антипаблика myrz!</b>\n\n<code>.myrz_key [KEY]</code>"
            )
            return
        if args := utils.get_args_raw(m):
            await m.edit("Делаю запрос...")
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"
            }
            data = requests.post(
                "https://myrz.org/api/email_search.php",
                data={"key": key, "email": args},
                headers=headers,
            ).json()
            try:
                if data["success"] is True:
                    psswds = "\n".join(
                        f"<code>{i['line']}</code>" for i in data["results"]
                    )
                    psswds += f"\n\nОсталось запросов: {data['awailableQueries']}\nНайдено: {data['resultCount']}\nЗапрос: <code>{args}</code>"
                    await utils.answer(m, str(psswds))
                else:
                    await m.edit(
                        f"Ничего не найдено по запросу <code>{args}</code>\nОсталось запросов: {data['awailableQueries']}"
                    )
            except Exception:
                await m.edit(str(data))
        else:
            await m.edit("shit...")
