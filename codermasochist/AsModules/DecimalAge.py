# meta developer: @codermasochist

import datetime
import calendar
from .. import loader, utils

@loader.tds
class decimalage(loader.Module):
    """узнать свой точнейший возраст"""
    
    strings = {
        "name": "Decimal Age?",
        "error": "<blockquote><emoji document_id=5276477287183687194>👎</emoji><b> надо так: </b><code>дд.мм.гг</code></blockquote>",
       "age": "<blockquote><emoji document_id=5336985409220001678>✅</emoji><b> Ваш точный возраст: </b>"
       "<code>{}</code> лет, <code>{}</code> месяцев, <code>{}</code> дней, <code>{}</code> часов, "
       "<code>{}</code> минут и <code>{}</code> секунд.</blockquote>\n<blockquote><emoji document_id=5282845662826739893>🔤</emoji> <b>в десятичной форме:</b><br> <code>{}</code> лет.</blockquote>"
    }
    
    async def exactagecmd(self, m):
        """— дд.мм.гг"""
        args = utils.get_args_raw(m)
        try:
            bd = datetime.datetime.strptime(args, '%d.%m.%Y')
            now = datetime.datetime.now()

            years = now.year - bd.year
            if now.month < bd.month or (now.month == bd.month and now.day < bd.day):
                years -= 1

            months = now.month - bd.month
            if now.day < bd.day:
                months -= 1
            if months < 0:
                months += 12

            days_in_previous_month = calendar.monthrange(now.year, now.month - 1 if now.month > 1 else 12)[1]
            days = now.day - bd.day
            if days < 0:
                days = days_in_previous_month + days

            hours = now.hour - bd.hour
            minutes = now.minute - bd.minute
            seconds = now.second - bd.second
            
            if seconds < 0:
                seconds += 60
                minutes -= 1
            if minutes < 0:
                minutes += 60
                hours -= 1
            if hours < 0:
                hours += 24
            
            total_days = (now - bd).days
            age_decimal = total_days / 365.2425
            
            await utils.answer(m, self.strings["age"].format(years, months, days, hours, minutes, seconds, age_decimal))
        except (IndexError, ValueError):
            await utils.answer(m, self.strings["error"])
