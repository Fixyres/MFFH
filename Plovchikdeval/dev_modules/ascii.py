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

from .. import loader, utils
import pyfiglet

@loader.tds
class AsciiMod(loader.Module):
    """Пишет ASCII шрифтом"""
    strings = {"name": "Ascii"}

    @loader.owner
    async def asciicmd(self, event):
        """Пишет ASCII шрифтом. Использование: .ascii <текст>"""
        if len(event.text.split(" ", maxsplit=1)) > 1:
            text = event.text.split(" ", maxsplit=1)[1]
        else:
            await utils.answer(event, "❌ Пожалуйста, укажите текст для генерации.")
            return
        art = pyfiglet.figlet_format(text)
        await utils.answer(event, f"```\n⁠{art}\n```", parse_mode="markdown")
