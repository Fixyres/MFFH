
# meta developer: @AssaMods

import os
from .. import loader, utils

@loader.tds
class CFile(loader.Module):
    """creates a file from a reply or text"""

    strings = {"name": "C File"}

    async def cfilecmd(self, message):
        """— <reply/text> create file."""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()

        if "|" in args:
            text, filename = map(str.strip, args.split("|", 1))
        elif reply and args:
            text = reply.raw_text
            filename = args.strip()
        elif reply:
            await utils.answer(message, "<i>Where is the file name? </i><emoji document_id=5431527977391237948>🤔</emoji>")
            return
        else:
            await utils.answer(message, """<blockquote><emoji document_id=5368809197032971971>🤔</emoji><b> how to use?</b></blockquote><b>

</b><blockquote><b>.cfile &lt;reply&gt; file name.
.cfile &lt;text&gt; | file name.</b></blockquote><b>

</b><blockquote><emoji document_id=6325540336475047747>😯</emoji><b> example: .cfile hello | main.txt</b></blockquote>""")
            return

        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(text)
            await message.client.send_file(message.chat_id, filename, reply_to=reply.id if reply else None)
        except Exception as e:
            await utils.answer(message, f"Oopsies: {e}")
        finally:
            try:
                os.remove(filename)
            except:
                pass
