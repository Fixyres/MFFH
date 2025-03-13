# meta developer: @xdesai
# requires: pyfiglet

from .. import loader, utils
import pyfiglet

@loader.tds
class AsciiMod(loader.Module):
    """Пишет ASCII шрифтом"""
    strings = {"name": "Ascii"}

    @loader.owner
    async def asciicmd(self, event):
        """<текст> | Пишет ASCII шрифтом."""
        if len(event.text.split(" ", maxsplit=1)) > 1:
            text = event.text.split(" ", maxsplit=1)[1]
        else:
            return await utils.answer(event, "❌ Пожалуйста, укажите текст для генерации.")
        art = pyfiglet.figlet_format(text)
        await utils.answer(event, f"```\n⁠{art}\n```", parse_mode="markdown")
