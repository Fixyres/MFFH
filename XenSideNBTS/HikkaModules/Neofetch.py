import subprocess
import traceback
from .. import loader, utils

#░█░█░█▀▀░█▀█░█▀▀░▀█▀░█▀▄░█▀▀
#░▄▀▄░█▀▀░█░█░▀▀█░░█░░█░█░█▀▀
#░▀░▀░▀▀▀░▀░▀░▀▀▀░▀▀▀░▀▀░░▀▀▀

# 🔒 Licensed under the AGPL-3.0
# 🥱 Im not allowing to edit this module.
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# meta developer: @XenSideMOD

@loader.tds
class NeofetchMod(loader.Module):
    strings = {"name": "Neofetch"}
    
    async def neofetchcmd(self, message):
        try:
            try:
                subprocess.run(["which", "neofetch"], check=True, capture_output=True)
            except subprocess.CalledProcessError:
                await message.edit("<b>Error: neofetch is not installed</b>")
                return
            process = subprocess.run(["neofetch"], capture_output=True, text=True)
            if process.returncode != 0:
                await message.edit(f"<b>Error:</b>\n<pre>{utils.escape_html(process.stderr)}</pre>")
                return
            clean_output = subprocess.run(
                ["sed", "s/\x1B\\[[0-9;?]*[a-zA-Z]//g"],
                input=process.stdout,
                capture_output=True,
                text=True
            )
            await message.edit(f"<pre>{utils.escape_html(clean_output.stdout)}</pre>")
        except Exception:
            await message.edit(f"<b>Error:</b>\n<pre>{traceback.format_exc()}</pre>")