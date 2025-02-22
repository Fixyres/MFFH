#   █▀▀ ▄▀█   █▀▄▀█ █▀█ █▀▄ █▀
#   █▀░ █▀█   █░▀░█ █▄█ █▄▀ ▄█

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: xRocket
# Description: Автоматизация базового функционала @xRocket
# meta developer: @FAmods
# meta banner: https://github.com/FajoX1/FAmods/blob/main/assets/banners/xrocket.png?raw=true
# ---------------------------------------------------------------------------------

import hikkatl
import asyncio

import logging

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class xRocket(loader.Module):
    """Автоматизация базового функционала @xRocket"""

    strings = {
        "name": "xRocket",

        "no_args": "<emoji document_id=5440381017384822513>❌</emoji> <b>Нужно <code>{}{}</code></b>",

        "creating": "<emoji document_id=5334904192622403796>🔄</emoji> <b>Создаю {}...</b>",
        "checking_wallet": "<emoji document_id=5334885140147479028>🔄</emoji> <b>Смотрю кошелёк...</b>",

        "no_money": "<emoji document_id=5440381017384822513>❌</emoji> <b>Не достаточно денег</b>",

        "invoice": """<b>💵 Счёт на <code>{} {}</code>

🔗 <a href='{}'>Оплатить</a></b>""",

        "check": """<b>💵 Чек на <code>{} {}</code> {}

🔗 <a href='{}'>Получить</a></b>""",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "testnet",
                False,
                lambda: "Use testnet version of @xRocket",
                validator=loader.validators.Boolean()
            ),
        )

    xrocket_bot = "@xrocket"
    xrocket_testnetbot = "@ton_rocket_test_bot"


    async def client_ready(self, client, db):
        self.db = db
        self._client = client

    def bot(self):
        return self.xrocket_bot if not self.config['testnet'] else self.xrocket_testnetbot
        
    async def _create_invoice(self, amount, crypt):
        q = await self._client.inline_query(self.bot(), f"{amount} {crypt}")
        result = await q[0].click("me")
        await result.delete()
            
        link = result.reply_markup.rows[0].buttons[0].url

        return link
    
    async def _create_check(self, amount, crypt, user):
        q = await self._client.inline_query(self.bot(), f"{amount} {crypt} {user}")
        result = await q[0].click("me")
        await result.delete()

        if "Счёт" in result.message:
            return "no_money"
            
        link = result.reply_markup.rows[0].buttons[0].url

        return link

    async def _get_wallet(self):
     while True:
      try:
        async with self._client.conversation(self.bot()) as conv:
            msg = await conv.send_message("/wallet")
            r = await conv.get_response()
            await msg.delete()
            await r.delete()
            return r
      except hikkatl.errors.common.AlreadyInConversationError:
          await asyncio.sleep(5.67)

    @loader.command()
    async def xwallet(self, message):
        """Посмотреть кошелёк"""

        await utils.answer(message, self.strings['checking_wallet'])

        wm = await self._get_wallet()
    
        return await utils.answer(message, wm.text)
        
    @loader.command()
    async def xinvoice(self, message):
        """Создать счёт"""
        
        args = utils.get_args_raw(message)

        try:
            amount, crypt = args.split(" ")
        except:
            return await utils.answer(message, self.strings['no_args'].format(self.get_prefix(), 'xinvoice [сумма] [криптовалюта]'))

        await utils.answer(message, self.strings['creating'].format("счёт"))

        link = await self._create_invoice(amount, crypt)
    
        return await utils.answer(message, self.strings['invoice'].format(amount, crypt, link))
    
    @loader.command()
    async def xcheck(self, message):
        """Создать чек"""
        
        args = utils.get_args_raw(message)

        user = ""

        try:
            try:
                amount, crypt, user = args.split(" ")
            except:
                amount, crypt = args.split(" ")
        except:
            return await utils.answer(message, self.strings['no_args'].format(self.get_prefix(), 'xcheck [сумма] [криптовалюта] [пользователь(не обязательно)]'))

        await utils.answer(message, self.strings['creating'].format("чек"))

        link = await self._create_check(amount, crypt, user)

        if "no_money" in link:
            return await utils.answer(message, self.strings['no_money'])
    
        return await utils.answer(message, self.strings['check'].format(amount, crypt, (f"для {user}" if user else ""), link))