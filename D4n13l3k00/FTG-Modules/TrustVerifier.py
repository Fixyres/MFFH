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

import hashlib

import aiohttp
from telethon.tl import types

from .. import loader, utils  # type: ignore


@loader.tds
class TrustVerifierMod(loader.Module):
    """TrustVerifier"""

    strings = {
        "name": __doc__,
        "pref": "<b>[TrustVerifier]</b> ",
        "need_args": "{}Reply to a module or enter link to check if it's a trusted module",
        "reply_to_file": "{}This is not a file",
        "invalid_file": "{}This is not a valid module",
        "trust_result": "{0}✅ This is a trusted module!\n\n"
        + "🔗 <b>Source:</b> {1}\n"
        + "💯 <b>Original filename:</b> <code>{3}</code>\n"
        + "#️⃣ <b>Hash:</b> <code>{2}</code>\n"
        + "📅 <b>Added at:</b> <code>{4}</code>\n",
        "untrust_result": "{0}❌ This is not a trusted module <code>[not_found_in_db err]</code>!\n<b>Hash:</b> <code>{1}</code>",
    }

    async def cmcmd(self, m: types.Message):
        "<reply to module | link> - Check if the module is trusted"
        text = None
        reply = await m.get_reply_message()
        args = utils.get_args_raw(m)
        if not reply and not args:
            return await utils.answer(
                m, self.strings("need_args", m).format(self.strings("pref", m))
            )
        elif reply:
            if not reply.file:
                return await utils.answer(
                    m, self.strings("reply_to_file", m).format(self.strings("pref", m))
                )
            file = await reply.download_media(bytes)
            try:
                text = file.decode("utf-8")
            except UnicodeDecodeError:
                return await utils.answer(
                    m, self.strings("invalid_file", m).format(self.strings("pref", m))
                )
        else:
            async with aiohttp.ClientSession() as session:
                async with session.get(args) as resp:
                    try:
                        text = await resp.text()
                    except UnicodeDecodeError:
                        return await utils.answer(
                            m,
                            self.strings("invalid_file", m).format(
                                self.strings("pref", m)
                            ),
                        )
        _hash = hashlib.sha256(text.encode("utf-8")).hexdigest()

        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.d4n13l3k00.ru/ftg/module/check",
                json={"hash": _hash},
            ) as response:
                j = await response.json(content_type=None)
            if j["success"]:
                if j["trust"]:
                    await utils.answer(
                        m,
                        self.strings("trust_result", m).format(
                            self.strings("pref", m),
                            j["source"],
                            j["hash"],
                            j["orig_name"],
                            j["added_at"],
                        ),
                    )
                else:
                    await utils.answer(
                        m,
                        self.strings("untrust_result", m).format(
                            self.strings("pref", m), _hash
                        ),
                    )
