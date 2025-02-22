__version__ = (1, 0, 9)

#            © Copyright 2025
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
# name: Cping

import time
from datetime import datetime, timedelta
import re
from .. import loader, utils
from telethon.tl.types import Message
import logging

@loader.tds
class Cping(loader.Module):
    """Кастомный пинг с поддержкой премиум эмодзи и медиа"""

    strings = {
        "name": "Cping",
        "configping": (
            "Ваш кастомный текст.\n"
            "Вы можете использовать аргументы:\n"
            "{ping} - Пинг (в миллисекундах).\n"
            "{up} - Время работы системы.\n"
            "{time} - Текущее время.\n"
            "{date} - Текущая дата.\n"
            "{day} - Текущий день недели.\n"
            "{ny} - До заданной даты (дни или часы).\n"
            "{emoji_line} - Место для ваших премиум эмодзи.\n"
            "{stat} - Эмодзи уровня пинга.\n\n"
            "Используйте теги для форматирования текста:\n"
            "[ж]текст[/ж] - Жирный текст\n"
            "[м]текст[/м] - Моноширинный текст\n"
            "[з]текст[/з] - Зачёркнутый текст\n"
            "[п]текст[/п] - Подчёркнутый текст\n\n"
            "Если в кфг не влазит весь текст, то вы можете использовать: .fcfg Cping ping ваши настройки\n"
        ),
        "countdown_hint": (
            "Формат даты для отсчёта: 'Число месяц время год'\n"
            "- Примеры:\n"
            "  '01 января 12:00 2025' - полная дата с годом и временем.\n"
            "  '01 января 12:00' - год будет автоматически добавлен как текущий или следующий, если дата прошла.\n"
            "  'пятница 15:45' - ближайшая пятница, год и месяц не указываются.\n"
            "  '14 июня' - день и месяц, время будет 00:00.\n\n"
            "- Указание времени обязательно, если не указано - будет 00:00.\n"
            "- Если не указан год, используется текущий год, но если дата уже прошла, будет использован следующий год.\n"
            "- Если не указан день недели, используется ближайший день с указанным временем."
        ),
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "ping",
                (
                    "{emoji_line}\n"
                    "🚀Пинг: {ping} ms {stat}\n"
                    "⏳Аптайм: {up}\n"
                    "⏰Время: {time}, {day}\n"
                    "🗓До нового года: {ny}\n"
                    "{emoji_line}"
                ),
                lambda: self.strings["configping"],
                validator=loader.validators.String(),
            ),
            loader.ConfigValue(
                "daytime",
                "1 января 0:00",
                lambda: self.strings["countdown_hint"],
                validator=loader.validators.String(),
            ),
            loader.ConfigValue(
                "moon",
                "🌘", 
                lambda: "Эмодзи в начале сообщения (может быть пустым)",
                validator=loader.validators.String(),
            ),
            loader.ConfigValue(
                "poyas",
                0,
                lambda: "Добавить или отнять часы.\n"
                "Пункт для тех, у кого платный хостинг находящийся за пределами часового пояса\n "
                "-число чтобы отнять час(ы)\n"
                "+число чтобы добавить час(ы)\n",
                validator=loader.validators.Integer(minimum=-12, maximum=14),
            ),
            loader.ConfigValue(
                "media",
                None,
                lambda: "Ссылка на медиа (фото/видео/гиф), которое будет прикреплено к сообщению с пингом.",
                validator=loader.validators.String(),
            ),
            loader.ConfigValue(
                "stat",
                "🟢|🟡|🔴",
                lambda: "Эмодзи для уровней пинга в формате: хороший|средний|плохой",
                validator=loader.validators.String(),
            ),
        )

    def get_plural(self, number, one, two, five):
        n = abs(number) % 100
        if 11 <= n <= 19:
            return five
        n = n % 10
        if n == 1:
            return one
        elif 2 <= n <= 4:
            return two
        return five

    def parse_date(self, date_str):
        today = datetime.now()
        months = {
            'января': 1, 'февраля': 2, 'марта': 3, 'апреля': 4,
            'мая': 5, 'июня': 6, 'июля': 7, 'августа': 8,
            'сентября': 9, 'октября': 10, 'ноября': 11, 'декабря': 12
        }
        days_of_week = {
            'понедельник': 0, 'вторник': 1, 'среда': 2,
            'четверг': 3, 'пятница': 4, 'суббота': 5, 'воскресенье': 6
        }

        try:
            return datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        except ValueError:
            pass

        for day_name, day_index in days_of_week.items():
            if day_name in date_str.lower():
                time_part = re.search(r'\d{1,2}:\d{2}', date_str)
                target_date = today + timedelta((day_index - today.weekday() + 7) % 7)
                if time_part:
                    target_time = datetime.strptime(time_part.group(), "%H:%M").time()
                    target_date = target_date.replace(hour=target_time.hour, minute=target_time.minute, second=0)
                if target_date < today:
                    target_date += timedelta(weeks=1)
                return target_date

        match = re.match(r'(\d{1,2})\s+([а-я]+)\s*(\d{4})?\s*(\d{1,2}:\d{2})?', date_str.lower())
        if match:
            day, month_name, year, time_part = match.groups()
            month = months.get(month_name)
            year = int(year) if year else today.year
            target_time = datetime.strptime(time_part, "%H:%M").time() if time_part else datetime.min.time()
            target_date = datetime(year, month, int(day), target_time.hour, target_time.minute)
            if target_date < today:
                target_date = target_date.replace(year=year + 1)
            return target_date

        raise ValueError("Неправильный формат даты")

    def days_to_date(self):
        try:
            countdown_date_str = self.config["daytime"]
            target_date = self.parse_date(countdown_date_str)

            hour_offset = self.config["poyas"]
            today = datetime.now() + timedelta(hours=hour_offset)

            time_difference = target_date - today

            if time_difference.total_seconds() < 86400:
                hours, remainder = divmod(time_difference.seconds, 3600)
                minutes = remainder // 60
                return f"{hours} {self.get_plural(hours, 'час', 'часа', 'часов')} и {minutes} {self.get_plural(minutes, 'минута', 'минуты', 'минут')}"
            else:
                days = time_difference.days
                return f"{days} {self.get_plural(days, 'день', 'дня', 'дней')}"
        except ValueError as e:
            logging.error(f"Ошибка в дате: {e}")
            return "Ошибка в дате"

    def format_text(self, text):
        replacements = {
            r"\[ж\]": "<b>", r"\[/ж\]": "</b>",
            r"\[м\]": "<code>", r"\[/м\]": "</code>",
            r"\[з\]": "<s>", r"\[/з\]": "</s>",
            r"\[п\]": "<u>", r"\[/п\]": "</u>",
        }
        for key, value in replacements.items():
            text = re.sub(key, value, text, flags=re.IGNORECASE)
        return text

    def get_stat_emoji(self, ping_time):
        emojis = self.config["stat"].split('|')
        if len(emojis) != 3:
            logging.error("Неверный формат конфигурации stat. Используйте формат: хороший|средний|плохой.")
            return "❓"

        if ping_time <= 150:
            return emojis[0]
        elif ping_time <= 300:
            return emojis[1]
        else:
            return emojis[2]

    @loader.command(
        ru_doc=" - Узнать пинг вашего юзербота",
    )
    async def cping(self, message: Message):
        start = time.perf_counter_ns()

        moon = self.config["moon"] or "🌘"
        await utils.answer(message, moon)

        ping_time = round((time.perf_counter_ns() - start) / 10**6, 3)

        uptime = utils.formatted_uptime()

        hour_offset = self.config["poyas"]
        current_time = (datetime.now() + timedelta(hours=hour_offset)).strftime("%H:%M:%S")
        current_date = (datetime.now() + timedelta(hours=hour_offset)).strftime("%Y-%m-%d")

        day_of_week = (datetime.now() + timedelta(hours=hour_offset)).strftime("%A")
        days_of_week = {
            "Monday": "Понедельник",
            "Tuesday": "Вторник",
            "Wednesday": "Среда",
            "Thursday": "Четверг",
            "Friday": "Пятница",
            "Saturday": "Суббота",
            "Sunday": "Воскресенье",
        }
        day_of_week = days_of_week.get(day_of_week, "Неизвестный день")

        days_to_event = self.days_to_date()

        ping_emoji = self.get_stat_emoji(ping_time)

        response = self.config["ping"].format(
            ping=ping_time,
            up=uptime,
            time=current_time,
            date=current_date,
            day=day_of_week,
            ny=days_to_event,
            emoji_line="",
            moon=moon,
            stat=ping_emoji
        )

        response = self.format_text(response)

        media = self.config["media"]
        
        if media:
            try:
                await utils.answer_file(message, media, caption=response)
            except Exception as e:
                logging.error(f"Ошибка при отправке медиа: {e}")
                await utils.answer(message, response)
        else:
            await utils.answer(message, response)