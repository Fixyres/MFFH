#   Coded by D4n13l3k00    #
#     t.me/D4n13l3k00      #
# This code under AGPL-3.0 #

import os

from .. import loader, utils  # type: ignore


@loader.tds
class TesseractMod(loader.Module):
    strings = {"name": "Tesseract"}

    @loader.owner
    async def ocrcmd(self, m):
        "Распознать текст с картинки"
        reply = await m.get_reply_message()
        if not reply:
            return await m.edit("[OCR] Реплай на пикчу")
        await m.edit("[OCR] Распознаём")
        file = await reply.download_media()
        rec = os.popen(f"tesseract -l rus+eng {file} stdout").read()
        await m.edit(
            "[OCR]\n" + (("<code>" + rec + "</code>") if rec != "" else "НЕ_РАСПОЗНАНО")
        )
        os.remove(file)
