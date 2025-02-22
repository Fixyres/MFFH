# meta developer: @xdesai

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
