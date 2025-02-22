#   █▀▀ ▄▀█   █▀▄▀█ █▀█ █▀▄ █▀
#   █▀░ █▀█   █░▀░█ █▄█ █▄▀ ▄█

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: Tonscan
# Description: Информация о TON адресе
# meta developer: @FAmods
# meta banner: https://github.com/FajoX1/FAmods/blob/main/assets/banners/tonscan.png?raw=true
# requires: aiohttp
# ---------------------------------------------------------------------------------

import logging
import aiohttp
import asyncio
from datetime import datetime

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class Tonscan(loader.Module):
    """Информация о TON адресе"""

    strings = {
        "name": "Tonscan",

        "waiting": "<b><emoji document_id=6334391057186293707>🕑</emoji> Собираю информацию...</b>",
    }


    async def client_ready(self, client, db):
        self.db = db
        self._client = client

    @loader.command()
    async def tonwallet(self, message):
        """Информация о TON кошельке"""
        address = utils.get_args_raw(message)

        if not address:
            return await utils.answer(message, f"<emoji document_id=5019523782004441717>❌</emoji> <b>Должно быть</b> <code>.tonwallet адрес_кошелька</code>")
        
        await utils.answer(message, self.strings["waiting"])

        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://tonapi.io/v2/accounts/{address}") as res:
               response = await res.json()

        try:
            response['icon']
            ava = f"""<a href="{response['icon']}">Аватарка</a> • """
        except:
            ava = ""

        try:
           response['name']
           name = f"\nИмя: <code>{response['name']}</code>\n"
        except:
           name = ""

        try:
          response['error']
          if "can't decode address" in response['error']:
            return await utils.answer(message, f"<b>❌ Это не адрес кошелька!</b>")

          return await utils.answer(message, f"""<b>❌ Ошибка!\n\n
```json 
{response['error']}                                    
```</b>""")
        except:
           pass

        scam = "Нет"

        try:
         if response['is_scam'] == "True":
           scam = "Да"
        except:
            pass
        
        try: 
           contract = f"Контракт: <code>{response['interfaces'][0]}</code>\n"
        except: 
           contract = ""

        try: 
           last_activity = f"\nПоследння активность: </b><i>{datetime.fromtimestamp(response['last_activity'])}</i><b>"
        except: 
           last_activity = ""

        await utils.answer(message, f"""<b>
<emoji document_id=5854713299794398583>💎</emoji> Ton wallet
{name}
Адрес: <code>{address}</code>
Баланс: <code>{response['balance']} TON</code>

Скам: </b><i>{scam}</i><b>
Статус: </b><i>{response['status']}</i><b>{last_activity}
{contract}
<a href="https://tonscan.org/address/{address}">Tonscan</a> • {ava}<a href="https://tonscan.org/address/{address}#transactions">История</a> • <a href="https://tonscan.org/address/{address}#nfts">NFT</a> • <a href="https://tonscan.org/address/{address}#tokens">jettons</a> • <a href="https://tonscan.org/address/{address}#source">Contract</a>
</b>""")
        
    @loader.command()
    async def tonjetton(self, message):
        """Информация о TON токене"""
        address = utils.get_args_raw(message)

        if not address:
            return await utils.answer(message, f"<emoji document_id=5019523782004441717>❌</emoji> <b>Должно быть</b> <code>.tonjetton адрес_токена</code>")
        
        await utils.answer(message, self.strings["waiting"])

        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://tonapi.io/v2/jettons/{address}") as res:
               response = await res.json()

        try:
          response['error']
          return await utils.answer(message, f"""<b>❌ Ошибка!\n\n
```json 
{response['error']}                                    
```</b>""")
        except:
           pass
        
        try:
           response['metadata']['description']
           descr = f"\n</b><i>{response['metadata']['description']}</i><b>\n"
        except:
           descr = ""

        try:
           response['metadata']['social']

           socials = """Ссылки:
"""
           for s in response['metadata']['social']:
              socials += s + "\n"
           socials += "\n"
        except:
           socials = ""

        await utils.answer(message, f"""<b>
<emoji document_id=5854713299794398583>💎</emoji> Ton jetton

Имя: <code>{response['metadata']['name']}</code>
Символ: <code>{response['metadata']['symbol']}</code>
{descr}
Адрес: <code>{address}</code>
Общее предложение: <code>{response['total_supply']} TON</code>

Количество держателей: <code>{response['holders_count']}</code>

{socials}<a href="https://tonscan.org/jetton/{address}">Tonscan</a> • <a href="{response['metadata']['image']}">Лого</a> • <a href="https://tonscan.org/jetton/{address}#transactions">История</a> • <a href="https://tonscan.org/jetton/{address}#holders">Топ держателей</a> • <a href="https://tonscan.org/jetton/{address}#source">Contract</a>
</b>""")
        
    @loader.command()
    async def tonnftcol(self, message):
        """Информация о TON NFT коллекции"""
        address = utils.get_args_raw(message)

        if not address:
            return await utils.answer(message, f"<emoji document_id=5019523782004441717>❌</emoji> <b>Должно быть</b> <code>.tonnftcol адрес_коллекции</code>")
        
        await utils.answer(message, self.strings["waiting"])

        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://tonapi.io/v2/nfts/collections/{address}") as res:
               response = await res.json()

        try:
          response['error']
          return await utils.answer(message, f"""<b>❌ Ошибка!\n\n
```json 
{response['error']}                                    
```</b>""")
        except:
           pass
        
        try:
           response['metadata']['description']
           descr = f"\n</b><i>{response['metadata']['description']}</i><b>\n"
        except:
           descr = ""

        try:
           response['metadata']['external_link']
           external_link = f"\nВнешняя ссылка: {response['metadata']['external_link']}\n"
        except:
           external_link = ""

        try:
           response['metadata']['social_links']

           socials = """Ссылки:
"""
           for s in response['metadata']['social']:
              socials += s + "\n"
           socials += "\n"
        except:
           socials = ""

        try:
           response['metadata']['approved_by']

           approved_by = """Одобрено:
"""
           for s in response['metadata']['approved_by']:
              approved_by += s + "\n"
           approved_by += "\n"
        except:
           approved_by = ""

        await utils.answer(message, f"""<b>
<emoji document_id=5854713299794398583>💎</emoji> Ton NFT collection

Имя: <code>{response['metadata']['name']}</code>
Адрес: <code>{address}</code>
{descr}
{external_link}
{approved_by}{socials}<a href="https://tonscan.org/nft/{address}">Tonscan</a> • <a href="https://tonscan.org/nft/{address}">Коллекция</a> • <a href="{response['metadata']['image']}">Лого</a> • <a href="{response['metadata']['cover_image']}">Баннер</a>
</b>""")
        
    @loader.command()
    async def tonnft(self, message):
        """Информация о TON NFT"""
        address = utils.get_args_raw(message)

        if not address:
            return await utils.answer(message, f"<emoji document_id=5019523782004441717>❌</emoji> <b>Должно быть</b> <code>.tonnft адрес_nft</code>")
        
        await utils.answer(message, self.strings["waiting"])

        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://tonapi.io/v2/nfts/{address}") as res:
               response = await res.json()

        try:
          response['error']
          return await utils.answer(message, f"""<b>❌ Ошибка!\n\n
```json 
{response['error']}                                    
```</b>""")
        except:
           pass
        
        try:
           response['metadata']['description']
           descr = f"\n</b><i>{response['metadata']['description']}</i><b>\n"
        except:
           descr = ""

        try:
           response['collection']['name']
           coll = f"\nКолекция: <code>{response['collection']['name']}</code>\n"
        except:
           coll = ""

        try:
           response['metadata']['external_link']
           external_link = f"\nВнешняя ссылка: {response['metadata']['external_link']}\n"
        except:
           external_link = ""

        try:
           response['metadata']['social_links']

           socials = """Ссылки:
"""
           for s in response['metadata']['social']:
              socials += s + "\n"
           socials += "\n"
        except:
           socials = ""

        try:
           response['metadata']['approved_by']

           approved_by = """Одобрено:
"""
           for s in response['metadata']['approved_by']:
              approved_by += s + "\n"
           approved_by += "\n"
        except:
           approved_by = ""

        await utils.answer(message, f"""<b>
<emoji document_id=5854713299794398583>💎</emoji> Ton NFT      
{coll}
Имя: <code>{response['metadata']['name']}</code>
Адрес: <code>{address}</code>
{descr}
{external_link}
{approved_by}{socials}<a href="https://tonscan.org/nft/{address}">Tonscan</a> • <a href="{response['metadata']['image']}">NFT фото</a>
</b>""")
