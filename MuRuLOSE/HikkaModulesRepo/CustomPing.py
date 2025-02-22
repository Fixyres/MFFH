from hikkatl.types import Message
from .. import loader, utils
import time
import random

"""
    ███    ███ ██    ██ ██████  ██    ██ ██       ██████  ███████ ███████
    ████  ████ ██    ██ ██   ██ ██    ██ ██      ██    ██ ██      ██  
    ██ ████ ██ ██    ██ ██████  ██    ██ ██      ██    ██ ███████ █████
    ██  ██  ██ ██    ██ ██   ██ ██    ██ ██      ██    ██      ██ ██  
    ██      ██  ██████  ██   ██  ██████  ███████  ██████  ███████ ███████ 


    CustomPing
    📜 Licensed under the GNU AGPLv3	
"""

# meta banner: https://0x0.st/HYVX.jpg
# meta desc: desc
# meta developer: @BruhHikkaModules


@loader.tds
class CustomPing(loader.Module):
    """Have you seen a customizable ping module in Netfoll? I have, yes, but I find it unacceptable to use Netfoll, so I took the idea of custom ping, and replicated it."""

    strings = {
        "name": "CustomPing",
        "configping": "Your custom text.\n"
        "You can use placeholders:\n"
        "{ping} - That's your ping.\n"
        "{uptime} - It's your uptime.\n"
        "{ping_hint} - This is the same hint as in the hikka module, it is chosen with random chance, also you can specify this hint in the config ",
        "hint": "Set a hint",
    }

    strings_ru = {
        "_cls_doc": "Вы видели настраиваемый модуль ping в Netfoll? Я, да но я считаю недопустимо использовать Netfoll, поэтому я взял за идею кастомный пинг, и повторил его.",
        "configping": "Ваш кастомный текст.\n"
        "Вы можете использовать плейсхолдеры:\n"
        "{ping} - Это ваш пинг\n"
        "{uptime} - Это ваш аптайм\n"
        "{ping_hint} - Это такая же подсказка как и в модуле хикки, оно также будет выбираться случайно, вы также можете это указать в конфиге\n",
        "hint": "Укажите подсказку",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "text",
                "🕐 Задержка юзербота: {ping}",
                lambda: self.strings["configping"],
                validator=loader.validators.String(),
            ),
            loader.ConfigValue(
                "hint",
                "This is example hint!",
                lambda: self.strings["hint"],
                validator=loader.validators.String(),
            ),
        )

    @loader.command(
        ru_doc=" - Узнать пинг вашего юзербота",
    )
    async def cping(self, message: Message):
        """- Find out your userbot ping"""
        start = time.perf_counter_ns()
        message = await utils.answer(message, "🌘")

        await utils.answer(
            message,
            self.config["text"].format(
                ping=round((time.perf_counter_ns() - start) / 10**6, 3),
                uptime=utils.formatted_uptime(),
                ping_hint=(
                    (self.config["hint"]) if random.choice([0, 0, 1]) == 1 else ""
                ),
            ),
        )
