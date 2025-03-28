"""
888    d8P   .d8888b.  888    888     888b     d888  .d88888b.  8888888b.   .d8888b.  
888   d8P   d88P  Y88b 888    888     8888b   d8888 d88P" "Y88b 888  "Y88b d88P  Y88b 
888  d8P    Y88b.      888    888     88888b.d88888 888     888 888    888 Y88b.      
888d88K      "Y888b.   8888888888 d8b 888Y88888P888 888     888 888    888  "Y888b.   
8888888b        "Y88b. 888    888 Y8P 888 Y888P 888 888     888 888    888     "Y88b. 
888  Y88b         "888 888    888     888  Y8P  888 888     888 888    888       "888 
888   Y88b  Y88b  d88P 888    888 d8b 888   "   888 Y88b. .d88P 888  .d88P Y88b  d88P 
888    Y88b  "Y8888P"  888    888 Y8P 888       888  "Y88888P"  8888888P"   "Y8888P" 
                                                           
(C) 2025 t.me/kshmods
Licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
"""
# meta developer: @kshmods

import os
from .. import loader, utils

@loader.tds
class CFile(loader.Module):
    """creates a file from a reply or text"""

    strings = {"name": "C File"}

    async def cfilecmd(self, message):
        """— <reply/text> create file."""
        penis = utils.get_args_raw(message)
        pidor = await message.get_reply_message()

        if "|" in penis:
            text, filename = map(str.strip, penis.split("|", 1))
        elif pidor and penis:
            text = pidor.raw_text
            filename = penis.strip()
        elif pidor:
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
            await message.client.send_file(message.chat_id, filename, reply_to=pidor.id if pidor else None)
        except Exception as e:
            await utils.answer(message, f"Oopsies: {e}")
        finally:
            try:
                os.remove(filename)
            except:
                pass