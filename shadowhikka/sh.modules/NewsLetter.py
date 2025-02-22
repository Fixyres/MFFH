# █▀ █░█ ▄▀█ █▀▄ █▀█ █░█░█
# ▄█ █▀█ █▀█ █▄▀ █▄█ ▀▄▀▄▀

# Copyright 2023 t.me/shadow_modules
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
from .. import loader, utils
from telethon.tl.types import Message  # type: ignore
from ..inline.types import InlineCall  # type: ignore

# meta developer: @shadow_modules
# scope: hikka_only
# scope: hikka_min 1.3.0
# meta banner: https://i.imgur.com/Hy9ABNY.jpeg


@loader.tds
class NewsLetterMod(loader.Module):
    """newsletter for chats"""

    strings = {
        "name": "NewsLetter",
        "succnews": (
            "<b><emoji document_id=5776375003280838798>✅</emoji> Newsletter successfully sent</b>\n<b><emoji document_id=5228686859663585439>👁‍🗨</emoji> Id сhats that were"
            " sent:</b>\n{}"
        ),
        "nochat": "<emoji document_id=5350311258220404874>❗️</emoji> <b>You did not specify chats for mailing</b>",
        "warnform": (
            "<b>⚠️ Attention!</b>\n<b>😰 When sending a newsletter to a lot of chats,"
            " there may be a flood</b>\n<b>✅ If you agree that you can get a flood,"
            " click on the button below</b>"
        ),
        "noargs": "<b><emoji document_id=5350311258220404874>❗️</emoji> There are no messages to send</b>",
        "yes": "✅ Yes",
        "no": "❌ No",
        "off": "<emoji document_id=5350311258220404874>❗️</emoji> <b>Mailing disabled</b>",
        "on": "<emoji document_id=5776375003280838798>✅</emoji> <b>Mailing enabled</b>",
        "no_delay": "<emoji document_id=5350311258220404874>❗️</emoji> <b>You did not indicate the delay between shipments</b>",
        "no_text": "<emoji document_id=5350311258220404874>❗️</emoji> <b>You did not indicate the text that will be written in the newsletter</b>",
    }
    strings_ru = {
        "succnews": (
            "<b><emoji document_id=5776375003280838798>✅</emoji> Рассылка успешно отправлена</b>\n<b><emoji document_id=5228686859663585439>👁‍🗨</emoji> Айди чатов в которые была"
            " отправлена рассылка:</b>\n{}"
        ),
        "warnform": (
            "<b>⚠️ Внимание!</b>\n<b>😰 При отправке рассылки во многое количество чатов"
            " может быть флудвейт</b>\n<b>✅ Если вы согласны с тем что можете получить"
            " флудвейт - нажмите на кнопку ниже</b>"
        ),
        "noargs": "<b><emoji document_id=5350311258220404874>❗️</emoji> Нет сообщения что-бы рассылать</b>",
        "nochat": "<emoji document_id=5350311258220404874>❗️</emoji> <b>Вы не указали чаты для рассылки</b>",
        "yes": "✅ Да",
        "no": "❌ Нет",
        "off": "<emoji document_id=5350311258220404874>❗️</emoji> <b>Рассылка выключена</b>",
        "on": "<emoji document_id=5776375003280838798>✅</emoji> <b>Рассылка включена</b>",
        "no_delay": "<emoji document_id=5350311258220404874>❗️</emoji> <b>Вы не указали задержку между отправками</b>",
        "no_text": "<emoji document_id=5350311258220404874>❗️</emoji> <b>Вы не указали текст который будет писать в рассылке</b>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "chats",
                [],
                lambda: "Chat for newsletter",
                validator=loader.validators.Series(
                    validator=loader.validators.TelegramID()
                ),
            ),
            loader.ConfigValue(
                "delay",
                5,
                lambda: "Delay for send message",
                validator=loader.validators.Integer(minimum=0),
            ),
            loader.ConfigValue(
                "url",
                "https://github.githubassets.com/assets/GitHub-Mark-ea2971cee799.png",
                lambda: "Url for photo",
                validator=loader.validators.Link(),
            ),
            loader.ConfigValue(
                "text",
                "",
                lambda: "Text for send",
                validator=loader.validators.String(),
            ),
        )

    async def sendnewscmd(self, message: Message):
        """<message> or reply"""
        if not self.db.get(__name__, "warn", False):
            await self.inline.form(
                message=message,
                text=self.strings("warnform"),
                reply_markup=[
                    [
                        {
                            "text": self.strings("yes"),
                            "callback": self.inline__callAnswer,
                            "args": ("yes",),
                        },
                    ],
                    [
                        {
                            "text": self.strings("no"),
                            "callback": self.inline__callAnswer,
                            "args": ("no",),
                        },
                    ],
                ],
            )
            return
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        chats = self.config["chats"]
        if not chats:
            await utils.answer(message, self.strings("nochat"))
            return
        try:
            if reply:
                for chat in chats:
                    await self.client.send_message(chat, reply)
            if not reply:
                for chat in chats:
                    await self.client.send_message(chat, args)
        except ValueError:
            await utils.answer(message, self.strings("noargs"))
            return

        await utils.answer(
            message,
            self.strings("succnews").format(
                "\n".join([f"<code>{s}</code>" for s in list(map(str, chats))])
            ),
        )

    async def newsdelaycmd(self, message: Message):
        """Delayed mailing and photos"""
        if not self.config["delay"]:
            return await utils.answer(message, self.strings("no_delay"))
        if not self.config["text"]:
            return await utils.answer(message, self.strings("no_text"))
        if self.get("status"):
            await utils.answer(message, self.strings("off"))
            return self.set("status", False)
        else:
            await utils.answer(message, self.strings("on"))
            self.set("status", True)
        while True:
            if not self.get("status"):
                break
            for chat in self.config["chats"]:
                await self.client.send_file(chat, self.config["url"], caption=self.config["text"])
                await asyncio.sleep(self.config["delay"])

    async def inline__callAnswer(self, call: InlineCall, value: str):
        self.db.set(__name__, "warn", True)
        await call.delete()
