# Name: musicMod
# Description: Module for search music.
# Author: @sansaramods
# Commands:
# .mus
# ---------------------------------------------------------------------------------
# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# ⚠️ All modules is not scam and absolutely safe.
# 👤 https://t.me/exodiast
#-----------------------------------------------------------------------------------
# meta developer: @sansaramods
#-----------------------------------------------------------------------------------

__version__ = (1, 0, 0)

import logging 
from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class musicMod(loader.Module):
    """
    Module for search music.
    
    """
    strings = {
        "name": "musicMod"
    }
    async def muscmd(self, message):
        """- for search music."""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if not args:
            return await message.edit("<b><emoji document_id=5258318620722733379>❌</emoji>No any args!</b>")
        try:
            await message.edit("<b><emoji document_id=5328311576736833844>🔴</emoji>Search..</b>")
            music = await message.client.inline_query("lybot", args)
            await message.delete()
            await message.client.send_file(
                message.to_id,
                music[0].result.document,
                reply_to = reply.id if reply else None, 
            )
        except:
            return await message.client.send_message(
                message.chat_id,
                f"<b><emoji document_id=5980953710157632545>❌</emoji>Track: <code>{args}</code> not found..</b>"
            )
