__version__ = (1, 2, 8)

#            © Copyright 2024
#           https://t.me/HikkTutor 
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
#┏┓━┏┓━━┏┓━━┏┓━━┏━━━━┓━━━━━┏┓━━━━━━━━━━━━
#┃┃━┃┃━━┃┃━━┃┃━━┃┏┓┏┓┃━━━━┏┛┗┓━━━━━━━━━━━
#┃┗━┛┃┏┓┃┃┏┓┃┃┏┓┗┛┃┃┗┛┏┓┏┓┗┓┏┛┏━━┓┏━┓━━━━
#┃┏━┓┃┣┫┃┗┛┛┃┗┛┛━━┃┃━━┃┃┃┃━┃┃━┃┏┓┃┃┏┛━━━━
#┃┃━┃┃┃┃┃┏┓┓┃┏┓┓━┏┛┗┓━┃┗┛┃━┃┗┓┃┗┛┃┃┃━━━━━
#┗┛━┗┛┗┛┗┛┗┛┗┛┗┛━┗━━┛━┗━━┛━┗━┛┗━━┛┗┛━━━━━
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# load from: t.me:HikkTutor 
# meta developer:@HikkTutor 
# author: vsakoe
# name: Fping

import time
import random
import asyncio
from datetime import datetime
from .. import loader, utils

@loader.tds
class FpingMod(loader.Module):
    """Модуль для настройки и отображения фейкового пинга"""

    strings = {
        "name": "Fping",
        "results_ping_old": (
            "<emoji document_id=5431449001532594346>⚡️</emoji> <b>{} ping:</b> <b><code>{}</code> ms</b>\n"
            "<emoji document_id=5445284980978621387>🚀</emoji> <b>Uptime:</b> <b>{}</b>"
        ),
        "results_ping_new": (
            "<emoji document_id=5920515922505765329>⚡️</emoji> <b>𝙿𝚒𝚗𝚐: </b><code>{}</code><b> 𝚖𝚜 </b>\n"
            "<emoji document_id=5900104897885376843>🕓</emoji><b> 𝚄𝚙𝚝𝚒𝚖𝚎: </b><code>{}</code>"
        ),
        "moon": "🌘",
        "additional_info": (
            "<emoji document_id=5472146462362048818>💡</emoji> <i>Telegram ping mostly depends on Telegram servers latency and other external factors and has nothing to do with the parameters of server on which userbot is installed</i>"
        ),
        "future_messages": [
            "Honestly, I'm just from the future and live right on the satellite",
            "The provider is so afraid of {username}, that they give him negative ping",
            "Your internet is faster than the speed of light, {username}!",
            "It seems your connection has outrun time, {username}!",
            "<b>Error:</b> <i>You have broken the space-time continuum.</i>"
        ],
        "future_messages_double_minus": [
            "You have torn the universe, {username}!",
            "Your connection has reached infinity and beyond!",
            "Your internet is so fast it outran itself, {username}!",
            "You are ahead of all times, {username}!",
            "<b>Error:</b> <i>You have created a new timeline.</i>",
            "Time and space no longer matter for your internet, {username}!",
            "Your ping is so negative you can see the future, {username}!",
            "Your signal reached antimatter and returned, {username}!",
            "You are so fast that even light can't keep up, {username}!",
            "Your connection is the new definition of speed, {username}!",
            "<b>Error:</b> You accidentally slowed down YouTube."
        ],
        "invalid_input": "<b>Please specify a valid ping value in milliseconds.</b>",
        "infinity_error": "<b>Error:</b> Infinity is the limit!"
    }

    strings_ru = {
        "name": "Fping",
        "results_ping_old": (
            "<emoji document_id=5431449001532594346>⚡️</emoji> <b>Скорость отклика {}:</b> <b><code>{}</code> ms</b>\n"
            "<emoji document_id=5445284980978621387>🚀</emoji> <b>Прошло с последней перезагрузки:</b> <b>{}</b>"
        ),
        "results_ping_new": (
            "<emoji document_id=5920515922505765329>⚡️</emoji> <b>𝙿𝚒𝚗𝚐: </b><code>{}</code><b> 𝚖𝚜 </b>\n"
            "<emoji document_id=5900104897885376843>🕓</emoji><b> 𝚄𝚙𝚝𝚒𝚖𝚎: </b><code>{}</code>"
        ),
        "moon": "🌘",
        "additional_info": (
            "<emoji document_id=5472146462362048818>💡</emoji> <i>Скорость отклика Telegram в большей степени зависит от загруженности серверов Telegram и других внешних факторов и никак не связана с параметрами сервера, на который установлен юзербот</i>"
        ),
        "future_messages": [
            "Честно, я просто из будущего и живу прямо на спутнике",
            "Провайдер так боится {username}, что дает ему отрицательный пинг",
            "Ваш интернет быстрее скорости света, {username}!",
            "Кажется, ваше соединение опередило время, {username}!",
            "<b>Ошибка:</b> <i>Вы нарушили пространственно-временной континуум.</i>"
        ],
        "future_messages_double_minus": [
            "Вы разорвали вселенную, {username}!",
            "Ваше соединение достигло бесконечности и за ее пределы!",
            "Ваш интернет настолько быстр, что обогнал сам себя, {username}!",
            "Вы опередили все времена, {username}!",
            "<b>Ошибка:</b> <i>Вы создали новую временную линию.</i>",
            "Время и пространство больше не имеют значения для вашего интернета, {username}!",
            "Ваш пинг настолько отрицательный, что вы видите будущее, {username}!",
            "Ваш сигнал достиг антиматерии и вернулся, {username}!",
            "Вы настолько быстры, что даже свет не может угнаться, {username}!",
            "Ваше соединение — новое определение скорости, {username}!",
            "<b>Ошибка:</b> Вы случайно замедлили YouTube."
        ],
        "invalid_input": "<b>Пожалуйста, укажите корректное значение пинга в миллисекундах.</b>",
        "infinity_error": "<b>Ошибка:</b> Бесконечность — предел!"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "style",
                "old",
                lambda: "Выбери стиль:\n"
                "new - кастомное оформление из Hikka 1.6.7\n"
                "old - стандартное оформление Hikka\n",
                validator=loader.validators.Choice(["old", "new"])
            ),
            loader.ConfigValue(
                "show_ping",
                True,
                lambda: "Отображать .ping перед стартом",
                validator=loader.validators.Boolean()
            )
        )

    @loader.command()
    async def fping(self, message):
        """Устанавливает и отображает фейковый пинг"""
        args = utils.get_args(message)
        if not args or not args[0].lstrip('-').isdigit():
            await utils.answer(message, self.strings["invalid_input"])
            return

        if args[0].startswith('---'):
            await utils.answer(message, self.strings["infinity_error"])
            return

        base_ping = int(args[0].lstrip('-'))
        double_minus = args[0].startswith('--')

        if double_minus:
            base_ping = min(max(base_ping, -10000), 25000)
        else:
            base_ping = min(max(base_ping, 0), 25000)

        if args[0].startswith('-'):
            minus_prefix = '--' if double_minus else '-'
            realistic_ping_with_decimal = f"{minus_prefix}{base_ping}.{random.randint(0, 9)}"
            initial_delay = final_delay = 0.5
        else:
            deviation = int(base_ping / 25)
            realistic_ping = base_ping + random.randint(-deviation, deviation)
            decimal_places = random.choice([1, 2, 3])
            realistic_ping_with_decimal = f"{realistic_ping}.{random.randint(10**(decimal_places-1), 10**decimal_places-1)}"
            initial_delay = random.uniform(0.3, 0.5)
            final_delay = max(0, realistic_ping / 1000 - initial_delay)

        if self.config["show_ping"]:
            await message.edit(".ping")
        time.sleep(initial_delay)
        await utils.answer(message, self.strings["moon"])
        time.sleep(final_delay)

        formatted_uptime = utils.formatted_uptime()

        if self.config["style"] == "old":
            response = self.strings["results_ping_old"].format("Telegram", realistic_ping_with_decimal, formatted_uptime)
        else:
            response = self.strings["results_ping_new"].format(realistic_ping_with_decimal, formatted_uptime)

        result_message = await utils.answer(message, response)

        if args[0].startswith('-'):
            await asyncio.sleep(2)
            sender = await message.get_sender()
            first_name = sender.first_name.strip() if sender.first_name else ""
            last_name = sender.last_name.strip() if sender.last_name else ""
            if first_name or last_name:
                username = f"{first_name} {last_name}".strip()
            else:
                username = "user" if self.strings == self.strings["en"] else "пользователь"
            future_message_list = self.strings["future_messages_double_minus"] if double_minus else self.strings["future_messages"]
            future_message = random.choice(future_message_list).format(username=username)
            await message.client.send_message(message.chat_id, future_message, reply_to=result_message.id)
