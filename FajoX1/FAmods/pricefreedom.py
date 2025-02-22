#   █▀▀ ▄▀█   █▀▄▀█ █▀█ █▀▄ █▀
#   █▀░ █▀█   █░▀░█ █▄█ █▄▀ ▄█

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: PriceFreedom
# Description: Автоматизированная работа с @rabstvo_game_bot
# meta developer: @FAmods
# meta banner: https://github.com/FajoX1/FAmods/blob/main/assets/banners/pricefreedom.png?raw=true
# ---------------------------------------------------------------------------------

import hikkatl

import re
import asyncio
import logging

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class PriceFreedom(loader.Module):
    """Автоматизированная работа с @rabstvo_game_bot"""

    strings = {
        "name": "PriceFreedom",

        "checking_profile": "<b><emoji document_id=5424885441100782420>👀</emoji> Смотрю профиль...</b>",
        "searching_us": "<b><emoji document_id=5424885441100782420>👀</emoji> Поиск пользователя...</b>",

        "no_usid": "<emoji document_id=5019523782004441717>🚫</emoji> <b>Нужно <code>{}{} [айди]</code></b>",

        "promo_on": "<b><emoji document_id=5852779353330421386>🎁</emoji> Авто-промо включен!</b>\n\n<i>Что бы получать промокоды вы должны быть подписаним <a href='{}'>здесь</a>.</i>",
        "promo_off": "<b><emoji document_id=5854929766146118183>🚫</emoji> Авто-промо выключен!</b>",
    }

    promo_channel = "https://t.me/+1eLPUMl51a5mOWQy"


    async def client_ready(self, client, db):
        self.db = db
        self._client = client

  #      while True:
  #       try:
  #          async with self._client.conversation("@rabstvo_game_bot") as conv:
  #              msg = await conv.send_message("/start 44088")
  #              r = await conv.get_response()
  #              await msg.delete()
  #              await r.delete()
  #              break
  #       except hikkatl.errors.common.AlreadyInConversationError:
  #          await asyncio.sleep(5.67)
  #       except Exception:
  #          break

    async def _active_promo(self, prom):
     while True:
      try:
        async with self._client.conversation("@rabstvo_game_bot") as conv:
            msg = await conv.send_message(f"/start {prom}")
            r = await conv.get_response()
            await r.delete()
            r = await conv.get_response()
            await r.delete()
            await msg.delete()
            break
      except hikkatl.errors.common.AlreadyInConversationError:
          await asyncio.sleep(5.67)

    async def _spfus_s(self, query):
     while True:
      try:
        async with self._client.conversation("@rabstvo_game_bot") as conv:
            msg = await conv.send_message(f"/start {query}")
            r = await conv.get_response()
            await r.delete()
            await msg.delete()
            o = await conv.get_response()
            await o.delete()
            if not "Зарабатывает:" in r.text:
               return f"🚫 <b>Пользователь не найден!</b>"
            return f"<b>👾 Информация о игроке\n\n{r.text}</b>\n\n<b><a href='https://t.me/rabstvo_game_bot?start={query}'>🔗 Ссылка</a></b>"
      except hikkatl.errors.common.AlreadyInConversationError:
          await asyncio.sleep(5.67)

    async def _getprofme(self):
     while True:
      try:
        async with self._client.conversation("@rabstvo_game_bot") as conv:
            msg = await conv.send_message("🫅 Профиль")
            r = await conv.get_response()
            await msg.delete()
            await r.delete()

            pattern = r'#(\w+).*?Баланс:'
            result = re.search(pattern, r.text, re.DOTALL)
            my_id = result.group(1)

            return f"<b>📁 Ваши данные\n\n{r.text}\n\n<a href='https://t.me/rabstvo_game_bot?start={my_id}'>🔗 Ссылка</a></b>"
      except hikkatl.errors.common.AlreadyInConversationError:
          await asyncio.sleep(5.67)

    @loader.command()
    async def pfpromo(self, message):
        """Включить/выключить автоматически активирование промокода"""

        if self.db.get(self.name, "promo_s", False):
            self.db.set(self.name, "promo_s", False)
            return await utils.answer(message, self.strings["promo_off"])

        self.db.set(self.name, "promo_s", True)

        await utils.answer(message, self.strings["promo_on"].format(self.promo_channel))

    @loader.command()
    async def spfus(self, message):
        """Посмотреть профиль пользователя"""

        query = utils.get_args_raw(message)

        if not query:
            return await utils.answer(message, self.strings['no_usid'].format(self.get_prefix(), 'spfus'))

        await utils.answer(message, self.strings["searching_us"])

        await utils.answer(message, await self._spfus_s(query))

    @loader.command()
    async def spfme(self, message):
        """Посмотреть свой профиль"""

        await utils.answer(message, self.strings["checking_profile"])

        await utils.answer(message, await self._getprofme())

    async def watcher(self, event):
        chat = utils.get_chat_id(event)
        
        if chat != 1726199153:
            return
        
        if all(keyword in event.raw_text for keyword in ["ПРОМОКОД", "Активируй"]):
          if self.db.get(self.name, "promo_s", False):
            await self._active_promo(event.reply_markup.rows[0].buttons[0].url.split("?start=")[1])
