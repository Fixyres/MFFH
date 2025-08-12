# Name: Searcher
#Description: Searches for various queries in inline bots
# Author: @sansaramods
# Commands:
# .pic | .vid | .gif | .stick
# ---------------------------------------------------------------------------------
# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# ⚠️ All modules is not scam and absolutely safe.
# 👤 https://t.me/exodiast
#-----------------------------------------------------------------------------------
# meta developer: @sansaramods
#-----------------------------------------------------------------------------------

__version__ = (1, 0, 1)

import random
from herokutl.types import Message
from .. import loader, utils
import logging

logger = logging.getLogger(__name__)

async def inline_search(client, query, inline_bot):
    try:
        result = await client.inline_query(inline_bot, query)
        if not result:
            return None
        return result 
    except Exception:
        return None
    

class Searcher(loader.Module):
    """Searches for various queries in inline bots"""

    strings = {
        "name": "Searcher",
        "error": "<emoji document_id=5258318620722733379>❌</emoji>Not found!",
    }

    strings_ru = {
        "error": "<emoji document_id=5258318620722733379>❌</emoji>Не найдено!",
    }

    @loader.command()
    async def pic(self, m: Message):
        """<str> -> search in @pic"""
        args = utils.get_args_raw(m)

        if await m.get_reply_message():
            r = await m.get_reply_message()
        else:
            r = m

        result = await inline_search(self._client, args, "pic")
        if not result:
            return await utils.answer(m, self.strings("error"))
        
        await result[random.randint(0,10)].click(m.to_id, reply_to=r)
        await m.delete()

    @loader.command()
    async def vid(self, m: Message):
        """<str> -> search in @vid"""
        args = utils.get_args_raw(m)

        if await m.get_reply_message():
            r = await m.get_reply_message()

        else:
            r = m

        result = await inline_search(self._client, args, "vid")
        if not result:
            return await utils.answer(m, self.strings("error"))
        
        await result[random.randint(0, 10)].click(m.to_id, reply_to=r)
        await m.delete()

    @loader.command()
    async def gif(self, m: Message):
        """<str> -> search in @gif"""
        args = utils.get_args_raw(m)

        if await m.get_reply_message():
            r = await m.get_reply_message()

        else:
            r = m

        result = await inline_search(self._client, args, "gif")
        if not result:
            return await utils.answer(m, self.strings("error"))
        
        await result[random.randint(0, 10)].click(m.to_id, reply_to=r)
        await m.delete()

    @loader.command()
    async def stik(self, m: Message):
        """<emoji> -> search in @sticker"""
        args = utils.get_args_raw(m)

        if await m.get_reply_message():
            r = await m.get_reply_message()

        else:
            r = m

        result = await inline_search(self._client, args, "sticker")
        if not result:
            return await utils.answer(m, self.strings("error"))
        
        await result[random.randint(0, 10)].click(m.to_id, reply_to=r)
        await m.delete()
