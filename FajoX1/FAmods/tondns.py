#   █▀▀ ▄▀█   █▀▄▀█ █▀█ █▀▄ █▀
#   █▀░ █▀█   █░▀░█ █▄█ █▄▀ ▄█

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: TonDNS
# Description: Модуль для работы с TON DNS
# meta developer: @FAmods
# meta banner: https://github.com/FajoX1/FAmods/blob/main/assets/banners/tondns.png?raw=true
# requires: aiohttp
# ---------------------------------------------------------------------------------

import logging
import aiohttp
import asyncio
from datetime import datetime

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class TonDNS(loader.Module):
    """Модуль для работы с Ton DNS"""

    strings = {
        "name": "TonDNS",

        "waiting": "<b><emoji document_id=6334391057186293707>🕑</emoji> Собираю информацию...</b>",
        "waiting_shot": "<b><emoji document_id=6334391057186293707>📸</emoji> Делаю скриншот TON DNS сайта...</b>", 
        
        "shot_ton_dns": "<b>💎 Скриншот TON DNS сайта <code>{}</code></b>",

        "ton_shot_link": "https://mini.s-shot.ru/1920x1080/JPEG/1024/Z100/?{}",
    }


    async def client_ready(self, client, db):
        self.db = db
        self._client = client

    @loader.command()
    async def itondns(self, message):
        """Информация о TON DNS"""
        address = utils.get_args_raw(message)

        if not address:
            return await utils.answer(message, f"<emoji document_id=5019523782004441717>❌</emoji> <b>Должно быть</b> <code>{self.get_prefix()}itondns тон_домен</code>")
        
        await utils.answer(message, self.strings["waiting"])

        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://tonapi.io/v2/dns/{address}") as res:
               response = await res.json()

        try:
          response['error']
          if "can't decode address" in response['error']:
            return await utils.answer(message, f"<b>❌ Это не адрес кошелька!</b>")

          return await utils.answer(message, f"""<b>❌ Ошибка!\n\n
<code>{response['error']}</code>                                
</b>""")
        except:
           pass

        await utils.answer(message, f"""<b>
<emoji document_id=5854713299794398583>💎</emoji> Ton DNS

Имя: <code>{response['name']}</code>
Адрес: <code>{response['item']['address']}</code>

⌛️ Истекает: <i>{datetime.fromtimestamp(response['expiring_at'])}</i>

🧑‍💻 Владелец
Адресс: <code>{response['item']['owner']['address']}</code>

🌐 DNS адрес: <code>{response['item']['dns']}</code>

<a href="https://tonscan.org/address/{address}">Tonscan</a> • <a href="{response['item']['previews'][2]['url']}">Image</a> • <a href="https://tonscan.org/address/{address}#source">Contract</a>
</b>""")
        
    @loader.command()
    async def tonshot(self, message):
        """Скриншот TON DNS сайта"""
        address = utils.get_args_raw(message)

        if not address:
            return await utils.answer(message, f"<emoji document_id=5019523782004441717>❌</emoji> <b>Должно быть</b> <code>.tonshot тон_домен</code>")
        
        await utils.answer(message, self.strings["waiting_shot"])

        address = address.replace("https://", "")
        address = address.replace("http://", "")

        ton_dns = address

        address += f"-s.cam"

        try:
            await message.client.send_file(message.chat_id, self.strings['ton_shot_link'].format(address), caption=self.strings['shot_ton_dns'].format(ton_dns))
            await message.delete()
        except:
            address = address.replace("-s.cam", ".run")
            await message.client.send_file(message.chat_id, self.strings['ton_shot_link'].format(address), caption=self.strings['shot_ton_dns'].format(ton_dns))
            await message.delete()
