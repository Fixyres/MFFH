
__version__ = (1, 0, 0)
# meta developer: @psyhomodules

from .. import loader, utils
from telethon import types
import datetime
import re
import logging

logger = logging.getLogger(__name__)

@loader.tds
class ДатаЗачатияMod(loader.Module):
    """Модуль для определения примерной даты зачатия по дате рождения"""
    
    strings = {
        "name": "ДатаЗачатия",
        "no_args": "❌ <b>Пожалуйста, укажите дату рождения в формате:</b> <code>.зачали [год] [месяц] [день]</code>",
        "invalid_date": "❌ <b>Неверный формат даты. Используйте:</b> <code>.зачали [год] [месяц] [день]</code>",
        "date_error": "❌ <b>Ошибка! Проверьте правильность введенной даты</b>",
        "result": "🔍 <b>Примерная дата зачатия:</b> <code>{}</code>",
        "future_date": "❌ <b>Дата рождения не может быть в будущем!</b>"
    }
    
    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        
    def validate_date(self, year, month, day):
        try:
            date = datetime.date(year, month, day)

            if date > datetime.date.today():
                return False, "future"
            return True, date
        except ValueError:
            return False, "invalid"
    
    @loader.command(ru_doc="Примерная дата зачатия: .зачали [год] [месяц] [день]")
    async def зачалиcmd(self, message: types.Message):
        """Вычисляет примерную дату зачатия по формату: .зачали [год] [месяц] [день]"""
        
        args = utils.get_args(message)
        
        if not args or len(args) != 3:
            await utils.answer(message, self.strings["no_args"])
            return
        
        try:
            year = int(args[0].strip())
            month = int(args[1].strip())
            day = int(args[2].strip())
            
            valid, result = self.validate_date(year, month, day)
            if not valid:
                if result == "future":
                    await utils.answer(message, self.strings["future_date"])
                else:
                    await utils.answer(message, self.strings["invalid_date"])
                return
            
            birth_date = result
            
            pregnancy_duration = datetime.timedelta(days=266)
            
            conception_date = birth_date - pregnancy_duration
            
            formatted_date = conception_date.strftime("%d.%m.%Y")
            
            await utils.answer(message, self.strings["result"].format(formatted_date))
            
        except Exception as e:
            logger.error(f"Ошибка в модуле ДатаЗачатия: {e}")
            await utils.answer(message, self.strings["date_error"])
            return
