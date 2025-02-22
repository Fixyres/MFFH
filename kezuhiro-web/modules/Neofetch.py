#     ___    __ __ ____
#    /   |  / //_//  _/
#   / /| | / ,<   / /  
#  / ___ |/ /| |_/ /   
# /_/  |_/_/ |_/___/   
#                      
#     __  _______  ____  _____
#    /  |/  / __ \/ __ \/ ___/
#   / /|_/ / / / / / / /\__ \ 
#  / /  / / /_/ / /_/ /___/ / 
# /_/  /_/\____/_____//____/
#
# meta developer: @aki_modules

import subprocess
import traceback
from .. import loader, utils

@loader.tds
class NeofetchMod(loader.Module):
    strings = {
        "name": "Neofetch",
        "not_installed": "Please, install <i>Neofetch</i>",
    }

    strings_ru = {
        "not_installed": "Пожалуйста, установите <i>Neofetch</i>",
    }

    strings_ua = {
        "not_installed": "Будь ласка, встановіть <i>Neofetch</i>",
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
            await utils.answer(message, f"<pre>{utils.escape_html(output)}</pre>")
            
        except FileNotFoundError:
            await utils.answer(message, self.strings("not_installed"))
