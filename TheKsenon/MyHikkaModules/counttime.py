from .. import loader, utils
import datetime
import time
import random

# meta developer: @kmodules
__version__ = (1, 0, 0)

@loader.tds
class CountTimeModule(loader.Module):
    """Модуль для отслеживания времени до разных событий, ВРЕМЯ может быть неправильное, потому что у вас на сервере такое время. На Termux время правильное..."""
    
    strings = {
        "name": "CountTime",
        "newyear_hints": [
            "Time to make New Year resolutions!",
            "Get ready for the countdown!",
            "New Year, new beginnings!",
            "Time to prepare the champagne!",
            "Ready for midnight magic?"
        ],
        "winter_hints": [
            "Winter wonderland is coming!",
            "Time for hot chocolate!",
            "Snowflakes will fall soon!",
            "Get your winter clothes ready!",
            "Winter magic approaches!"
        ],
        "spring_hints": [
            "Spring flowers are on their way!",
            "Birds will sing again soon!",
            "Nature is preparing to bloom!",
            "Spring rain will refresh everything!",
            "Time for new beginnings!"
        ],
        "summer_hints": [
            "Beach time is coming!",
            "Get ready for sunny days!",
            "Summer adventures await!",
            "Ice cream season approaches!",
            "Time for vacation plans!"
        ],
        "autumn_hints": [
            "Fall colors are coming!",
            "Time for cozy sweaters!",
            "Falling leaves season ahead!",
            "Pumpkin spice everything!",
            "Autumn magic is near!"
        ]
    }
    
    strings_ru = {
        "name": "CountTime",
        "newyear_hints": [
            "Пора загадывать желания!",
            "Готовимся к обратному отсчету!",
            "Новый год = новые возможности!",
            "Пацаны, готовим шампанское!",
            "Держимся, держимся..."
            "Скоро волшебная ночь!"
        ],
        "winter_hints": [
            "Скоро зимняя сказка!",
            "Время горячего шоколада!",
            "Мам, подари шоколад."
            "Скоро пойдет снег!",
            "Готовь теплую одежду!",
            "Зимнее волшебство приближается!"
        ],
        "spring_hints": [
            "Весенние цветы уже в пути!",
            "Скоро запоют птицы!",
            "Еще немного..."
            "Природа готовится к цветению!",
            "Весенние дожди освежат всё вокруг!",
            "Время новых начинаний!"
        ],
        "summer_hints": [
            "Скоро на пляж!",
            "Включаем вентилятор?"
            "Готовься к солнечным дням!",
            "Летние приключения ждут!",
            "Сезон мороженого приближается!",
            "Время планировать отпуск!"
        ],
        "autumn_hints": [
            "Золотая осень!",
            "Время уютных свитеров!",
            "Приближается сезон падающих листьев!",
            "Тыквенный латте уже ждет!",
            "Осеннее волшебство близко!"
        ]
    }

    def __init__(self):
        self.seasons = {
            'winter': (12, 1, 2),
            'spring': (3, 4, 5),
            'summer': (6, 7, 8),
            'autumn': (9, 10, 11)
        }

    def _get_next_date(self, month, day):
        now = datetime.datetime.now()
        year = now.year
        
        target = datetime.datetime(year, month, day)
        if target < now:
            target = datetime.datetime(year + 1, month, day)
            
        return target

    def _get_next_season(self, season):
        now = datetime.datetime.now()
        year = now.year
        
        if season == 'winter':
            return self._get_next_date(12, 1)
        elif season == 'spring':
            return self._get_next_date(3, 1)
        elif season == 'summer':
            return self._get_next_date(6, 1)
        else: 
            return self._get_next_date(9, 1)

    def _format_time_left(self, target):
        now = datetime.datetime.now()
        diff = target - now
        
        days = diff.days
        hours = diff.seconds // 3600
        seconds = diff.seconds % 3600
        
        return f"| {days} дней | {hours} часов | {seconds} секунд |"

    @loader.command()
    async def nytime(self, message):
        """Показывает время до нового года"""
        next_ny = self._get_next_date(1, 1)
        time_left = self._format_time_left(next_ny)
        hint = random.choice(self.strings['newyear_hints'])
        
        await utils.answer(
            message,
            f"<emoji document_id=5287722241709057624>😉</emoji> <b>До нового года осталось:</b>\n\n"
            f"<blockquote>{time_left}</blockquote>\n\n"
            f"<emoji document_id=5463144094945516339>👍</emoji> <b>{hint}</b>"
        )

    @loader.command()
    async def wintertime(self, message):
        """Показывает время до зимы"""
        next_winter = self._get_next_season('winter')
        time_left = self._format_time_left(next_winter)
        hint = random.choice(self.strings['winter_hints'])
        
        await utils.answer(
            message,
            f"<emoji document_id=5201743825441145795>❄️</emoji> <b>До зимы осталось:</b>\n\n"
            f"<blockquote>{time_left}</blockquote>\n\n"
            f"<emoji document_id=5463144094945516339>👍</emoji> <b>{hint}</b>"
        )

    @loader.command()
    async def springtime(self, message):
        """Показывает время до весны"""
        next_spring = self._get_next_season('spring')
        time_left = self._format_time_left(next_spring)
        hint = random.choice(self.strings['spring_hints'])
        
        await utils.answer(
            message,
            f"<emoji document_id=5195140682590722632>🏠</emoji> <b>До весны осталось:</b>\n\n"
            f"<blockquote>{time_left}</blockquote>\n\n"
            f"<emoji document_id=5463144094945516339>👍</emoji> <b>{hint}</b>"
        )

    @loader.command()
    async def summertime(self, message):
        """Показывает время до лета"""
        next_summer = self._get_next_season('summer')
        time_left = self._format_time_left(next_summer)
        hint = random.choice(self.strings['summer_hints'])
        
        await utils.answer(
            message,
            f"<emoji document_id=5472178859300363509>🏖️</emoji> <b>До лета осталось:</b>\n\n"
            f"<blockquote>{time_left}</blockquote>\n\n"
            f"<emoji document_id=5463144094945516339>👍</emoji> <b>{hint}</b>"
        )

    @loader.command()
    async def autumntime(self, message):
        """Показывает время до осени"""
        next_autumn = self._get_next_season('autumn')
        time_left = self._format_time_left(next_autumn)
        hint = random.choice(self.strings['autumn_hints'])
        
        await utils.answer(
            message,
            f"<emoji document_id=5416034540000910728>🤧</emoji> <b>До осени осталось:</b>\n\n"
            f"<blockquote>{time_left}</blockquote>\n\n"
            f"<emoji document_id=5463144094945516339>👍</emoji> <b>{hint}</b>"
        )
      
