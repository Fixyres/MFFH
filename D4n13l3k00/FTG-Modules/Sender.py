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


import re

from telethon.errors import ChannelInvalidError

from .. import loader, utils  # type: ignore


@loader.tds
class SenderMod(loader.Module):
    strings = {"name": "Sender"}

    @loader.owner
    async def sndcmd(self, m):
        """.snd <канал/чат/id> <reply>
        Отпрпвить сообшение в чат/канал(без авторства)
        """
        args = utils.get_args_raw(m)
        reply = await m.get_reply_message()
        if not args:
            return await m.edit("[Sender] Укажите канал/чат")
        try:
            this = await m.client.get_input_entity(
                int(args) if re.match(r"-{0,1}\d+", args) else args
            )
        except ChannelInvalidError:
            return await m.edit("[Sender] Такого канала/чата не существует!")
        except Exception as e:
            return await m.edit("[Sender] Неизвестная мне ошибка:\n" + " ".join(e.args))
        await m.client.send_message(this, reply)
        await m.edit("[Sender] Сообщение отправлено!")
