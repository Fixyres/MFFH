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


import os
import random
import string

from .. import loader, utils  # type: ignore


@loader.tds
class VSHAKALMod(loader.Module):
    strings = {"name": "Video Shakal"}

    @loader.owner
    async def vshcmd(self, m):
        ".vsh <реплай на видео> <уровень от 1 до 6 (по умолчанию 3)>\n" "Сшакалить видео"
        reply = await m.get_reply_message()
        if not reply:
            return await utils.answer(m, "reply...")
        if reply.file.mime_type.split("/")[0] != "video":
            return await utils.answer(m, "shit...")

        args = utils.get_args_raw(m)
        lvls = {
            "1": "1M",
            "2": "0.5M",
            "3": "0.1M",
            "4": "0.05M",
            "5": "0.01M",
        }
        if args:
            if args in lvls:
                lvl = lvls[args]
            else:
                return await utils.answer(m, "не знаю такого")
        else:
            lvl = lvls["3"]
        m = await utils.answer(m, "[Шакал] Качаю...")
        vid = await reply.download_media(
            "".join(random.choice(string.ascii_letters) for _ in range(25)) + ".mp4"
        )

        out = "".join(random.choice(string.ascii_letters) for _ in range(25)) + ".mp4"

        m = await utils.answer(m, "[Шакал] Шакалю...")
        os.system(
            f'ffmpeg -y -i "{vid}" '
            f"-b:v {lvl} -maxrate:v {lvl} "
            f'-b:a {lvl} -maxrate:a {lvl} "{out}"'
        )
        m = await utils.answer(m, "[Шакал] Отправляю...")
        await utils.answer(m, out)
        os.remove(vid)
        os.remove(out)
