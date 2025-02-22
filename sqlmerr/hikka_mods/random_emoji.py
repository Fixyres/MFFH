"""
░██████╗░██████╗░██╗░░░░░███╗░░░███╗███████╗██████╗░██████╗░
██╔════╝██╔═══██╗██║░░░░░████╗░████║██╔════╝██╔══██╗██╔══██╗
╚█████╗░██║██╗██║██║░░░░░██╔████╔██║█████╗░░██████╔╝██████╔╝
░╚═══██╗╚██████╔╝██║░░░░░██║╚██╔╝██║██╔══╝░░██╔══██╗██╔══██╗
██████╔╝░╚═██╔═╝░███████╗██║░╚═╝░██║███████╗██║░░██║██║░░██║
╚═════╝░░░░╚═╝░░░╚══════╝╚═╝░░░░░╚═╝╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝
"""


# meta banner: https://github.com/sqlmerr/sqlmerr/blob/main/assets/hikka_mods/sqlmerrmodules_randomemoji.png?raw=true
# meta icon: https://github.com/sqlmerr/hikka_mods/blob/main/assets/icons/random_emoji.png?raw=true
# meta developer: @sqlmerr_m

import requests

from .. import loader, utils
from hikkatl.tl.types import Message


@loader.tds
class RandomEmoji(loader.Module):
    """Just random emojis"""

    strings = {"name": "RandomEmoji"}

    @loader.command()
    async def random_emoji(self, message: Message):
        """Random emoji"""
        url = "https://emojihub.yurace.pro/api/random"
        emoji = await utils.run_sync(requests.get, url)
        emoji = emoji.json()

        await utils.answer(message, "".join(html for html in emoji["htmlCode"]))
