#   █▀▀ ▄▀█   █▀▄▀█ █▀█ █▀▄ █▀
#   █▀░ █▀█   █░▀░█ █▄█ █▄▀ ▄█

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: AnonSMS
# Description: Анонимное сообщение
# meta developer: @FAmods
# meta banner: https://github.com/FajoX1/FAmods/blob/main/assets/banners/anonsms.png?raw=true
# ---------------------------------------------------------------------------------

import time
import asyncio
import logging

from .. import loader, utils

from ..inline.types import InlineCall, BotInlineMessage

logger = logging.getLogger(__name__)

@loader.tds
class AnonSMS(loader.Module):
    """Анонимное сообщение"""

    strings = {
        "name": "AnonSMS",

        "enter_message": "<b>📩 Отправьте сообщение</b>",

        "new_anon_msg": "<b>📨 Вам пришло новое анонимное сообщение:</b>",
        "opening_settings": "<b><emoji document_id=5327902038720257153>🔄</emoji> Открываю настройки...</b>",

        "only_one": "<b>❌ Отправлять сообщение можно раз в {} секунд!</b>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "start_text",
                "<b>👋 Привет!\nТы можешь написать мне анонимное сообщение</b>",
                lambda: "Текст после перехода по ссылке",
            ),
            loader.ConfigValue(
                "sent_text",
                "<b>✅ Сообщение отправлено</b>",
                lambda: "Текст пользователю после отправки сообщения",
            ),
            loader.ConfigValue(
                "error_send_text",
                "<b>❌ Не удалось отправить сообщение</b>",
                lambda: "Текст пользователю если не удалось отправить сообщение",
            ),
            loader.ConfigValue(
                "floodwait",
                15,
                lambda: "Раз в сколько секунд можно отправить сообщение",
            ),
        )


    async def client_ready(self, client, db):
        self.db = db
        self._client = client

    async def _check_message_rate(self, user_id: int) -> bool:
        if user_id in self.last_message_time:
            last_time = self.last_message_time[user_id]
        
            if time.time() - last_time < self.config['floodwait']:
                return False

        self.last_message_time[user_id] = time.time()
        return True

    @loader.command()
    async def getanonlink(self, message):
        """Получить ссылку на получение анонимного сообщения"""

        await utils.answer(message, f"<emoji document_id=5271604874419647061>🔗</emoji> <b>Твоя ссылка для получение анонимного смс:\n<code>https://t.me/{self.inline.bot_username}?start=anonsms</code></b>")

    @loader.command()
    async def anonsettings(self, message):
        """Настроят модуль"""

        await utils.answer(message, self.strings['opening_settings'])
        await self.invoke("config", "AnonSMS", message.peer_id)
        await message.delete()

    @loader.inline_everyone
    @loader.callback_handler()
    async def anon_sms(self, call: InlineCall):
        if call.data == "anon_cancel":
            self.inline.ss(call.from_user.id, False)
            await self.inline.bot.delete_message(
                call.message.chat.id,
                call.message.message_id,
            )
            return

        if call.data != "leave_anonsms":
            return

        self.inline.ss(call.from_user.id, "send_anonsms")
        await self.inline.bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=self.strings['enter_message'],
            parse_mode="HTML",
            disable_web_page_preview=True,
            reply_markup=self.inline.generate_markup(
            {"text": "🚫 Отменить", "data": "anon_cancel"}
        ),
        )

    async def aiogram_watcher(self, message: BotInlineMessage):
        if message.text == "/start anonsms":
            return await message.answer(
                self.config["start_text"],
                reply_markup=self.inline.generate_markup(
            {"text": "✍️ Написать", "data": "leave_anonsms"}
        ),
            )
        if self.inline.gs(message.from_user.id) == "send_anonsms":
            if not await self._check_message_rate(message.from_user.id):
                await message.answer(self.strings['only_one'].format(self.config['floodwait']))
                return
            try:
                await self.inline.bot.send_message(self._tg_id, self.strings['new_anon_msg'])
                await message.send_copy(self._tg_id)
            except:
                return await message.answer(self.config['error_send_text'])
            return await message.answer(self.config["sent_text"])