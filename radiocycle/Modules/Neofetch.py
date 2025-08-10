# meta developer: @cachedfiles

import subprocess
from .. import loader, utils

@loader.tds
class NeofetchMod(loader.Module):
    strings = {
        "name": "Neofetch",
        "not_installed": "<b>Please, install</b> <i>Neofetch</i> <b>package</b>",
    }

    strings_ru = {
        "not_installed": "<b>Пожалуйста, установите пакет</b> <i>Neofetch</i>",
    }

    strings_ua = {
        "not_installed": "<b>Будь ласка, встановіть пакет<b> <i>Neofetch</i>",
    }

    @loader.command(
        ru_doc="- запустить команду neofetch",
        ua_doc="- запустити команду neofetch",
    )
    async def neofetchcmd(self, message):
        """- run neofetch command"""
        try:
            result = subprocess.run(["neofetch", "--stdout"], capture_output=True, text=True)
            output = result.stdout
            await utils.answer(message, f"<blockquote expandable>{utils.escape_html(output)}</blockquote>")
            
        except FileNotFoundError:
            await utils.answer(message, self.strings("not_installed"))
    
