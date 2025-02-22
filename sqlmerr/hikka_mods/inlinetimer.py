"""
░██████╗░██████╗░██╗░░░░░███╗░░░███╗███████╗██████╗░██████╗░
██╔════╝██╔═══██╗██║░░░░░████╗░████║██╔════╝██╔══██╗██╔══██╗
╚█████╗░██║██╗██║██║░░░░░██╔████╔██║█████╗░░██████╔╝██████╔╝
░╚═══██╗╚██████╔╝██║░░░░░██║╚██╔╝██║██╔══╝░░██╔══██╗██╔══██╗
██████╔╝░╚═██╔═╝░███████╗██║░╚═╝░██║███████╗██║░░██║██║░░██║
╚═════╝░░░░╚═╝░░░╚══════╝╚═╝░░░░░╚═╝╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝
"""
# meta developer: @sqlmerr_m
# meta icon: https://github.com/sqlmerr/hikka_mods/blob/main/assets/icons/inlinetimer.png?raw=true
# meta banner: https://github.com/sqlmerr/sqlmerr/blob/main/assets/hikka_mods/sqlmerrmodules_inlinetimer.png?raw=true

import asyncio


from .. import loader
from ..inline.types import InlineCall


@loader.tds
class InlineTimer(loader.Module):
    """Описание нашего модуля"""

    strings = {
        "name": "InlineTimer",
        "text": "⏲ <b>Inline timer</b>\n⏰ <i>Current time</i>: {} seconds",
        "successful": "Great, in {} seconds the inline bot will send you a message via PM",
        "timer_created": "<b>Timer created!</b>",
        "text_cfg": "The text that your inline bot will send when the timer expires",
        "below_zero": "Time cannot be below zero",
    }
    strings_ru = {
        "text": "⏲ <b>Inline timer</b>\n⏰ <i>Текущее время</i>: {} секунд",
        "successful": "Отлично, через {} секунд инлайн бот отправит вам сообщение в лс",
        "timer_created": "<b>Таймер создан!</b>",
        "text_cfg": "Текст, который будет писать ваш инлайн бот по истечению времени таймера",
        "below_zero": "Время не может быть меньше нуля",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "text",
                "⚠️",
                lambda: self.strings("text_cfg"),
                validator=loader.validators.String(),
            )
        )

    @loader.command(ru_doc="отправить таймер")
    async def timer(self, message):
        """Send timer"""
        timer = self.get("timer", 0)
        await self.inline.form(
            text=self.strings("text").format(timer),
            message=message,
            reply_markup=[
                [
                    {
                        "text": "-1 sec",
                        "callback": self.decrement,
                    },
                    {
                        "text": "✍️ Enter value",
                        "input": "✍️ Enter new time IN SECONDS",
                        "handler": self.input_handler,
                    },
                    {"text": "+1 sec", "callback": self.increment},
                ],
                [
                    {"text": "✅", "callback": self.proceed},
                    {
                        "text": "❌",
                        "action": "close",
                    },
                ],
            ],
        )

    async def proceed(self, call: InlineCall):
        timer = self.get("timer", 1)
        await call.answer(self.strings("successful").format(timer))
        await call.edit(self.strings("timer_created"))
        self.set("timer", 0)

        await asyncio.sleep(timer)
        await self.inline.bot.send_message(self.tg_id, self.config["text"])

    async def decrement(self, call: InlineCall):
        timer = self.get("timer", 0)
        if timer == 0:
            await call.answer(self.strings("below_zero"))
            return
        timer -= 1
        self.set("timer", timer)
        await call.answer()

        await call.edit(
            text=self.strings("text").format(timer),
            reply_markup=[
                [
                    {
                        "text": "-1 sec",
                        "callback": self.decrement,
                    },
                    {
                        "text": "✍️ Enter value",
                        "input": "✍️ Enter new time IN SECONDS",
                        "handler": self.input_handler,
                    },
                    {"text": "+1 sec", "callback": self.increment},
                ],
                [
                    {"text": "✅", "callback": self.proceed},
                    {
                        "text": "❌",
                        "action": "close",
                    },
                ],
            ],
        )

    async def increment(self, call: InlineCall):
        timer = self.get("timer", 0)
        timer += 1
        self.set("timer", timer)
        await call.answer()

        await call.edit(
            text=self.strings("text").format(timer),
            reply_markup=[
                [
                    {
                        "text": "-1 sec",
                        "callback": self.decrement,
                    },
                    {
                        "text": "✍️ Enter value",
                        "input": "✍️ Enter new time IN SECONDS",
                        "handler": self.input_handler,
                    },
                    {"text": "+1 sec", "callback": self.increment},
                ],
                [
                    {"text": "✅", "callback": self.proceed},
                    {
                        "text": "❌",
                        "action": "close",
                    },
                ],
            ],
        )

    async def input_handler(self, call: InlineCall, query: str):
        if not query.isdigit():
            await call.answer("Вы ввели не число!")
            return

        self.set("timer", int(query))

        timer = self.get("timer", int(query))
        await call.answer()

        await call.edit(
            text=self.strings("text").format(timer),
            reply_markup=[
                [
                    {
                        "text": "-1 sec",
                        "callback": self.decrement,
                    },
                    {
                        "text": "✍️ Enter value",
                        "input": "✍️ Enter new time IN SECONDS",
                        "handler": self.input_handler,
                    },
                    {"text": "+1 sec", "callback": self.increment},
                ],
                [
                    {"text": "✅", "callback": self.proceed},
                    {
                        "text": "❌",
                        "action": "close",
                    },
                ],
            ],
        )
