#   █▀▀ ▄▀█   █▀▄▀█ █▀█ █▀▄ █▀
#   █▀░ █▀█   █░▀░█ █▄█ █▄▀ ▄█

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: FAmodsSocket
# Description: Установка модулей через @FAmods_Bot
# meta developer: @FAmods
# requires: BeautifulSoup4
# ---------------------------------------------------------------------------------

import re
import shlex
import aiohttp
import asyncio
import logging

from bs4 import BeautifulSoup

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class FAmodsSocket(loader.Module):
    """Установка модулей через @FAmods_Bot"""

    strings = {"name": "FAmodsSocket"}


    async def client_ready(self, client, db):
        self.db = db
        self._client = client

    async def watcher(self, message):
        chat = utils.get_chat_id(message)
        
        if chat != 7283754755:
            return
        
        if not message.text.startswith('<a href="https://raw.githubusercontent.com/FajoX1/FAmods/main/'):
            return
        
        soup = BeautifulSoup(message.text, 'html.parser')
        link = soup.a['href']

        async with aiohttp.ClientSession() as session:
            async with session.get(link) as response:
                code = await response.text()

        requires_comments = re.findall(r'#\s*requires:\s*(.*)', code)
        all_requires = ''.join(requires_comments).strip()

        if all_requires:
            await message.delete()
            requirements_list = shlex.split(all_requires)
            process = await asyncio.create_subprocess_exec('pip', 'install', *requirements_list)
            await process.wait()

        loader_m = self.lookup("loader")

        await loader_m.download_and_install(link, None)

        if not all_requires:
            await message.delete()