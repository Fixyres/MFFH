#Name: SeasonsTimer
#Description: Модуль - таймер времен года.
#Author: @nervousmods
#Commands:
#.tosum | .toaut | .towin | .tospr
# ---------------------------------------------------------------------------------
#🔒 Licensed under the GNU GPLv3
#🌐 https://www.gnu.org/licenses/agpl-3.0.html
#⚠️ All modules is not scam and absolutely safe.
#👤 https://t.me/smlgwy
#-----------------------------------------------------------------------------------
#meta developer: @nervousmods, @hikka_mods
#scope: hikka_only 
#scope: hikka_min 1.6.0
#-----------------------------------------------------------------------------------
__version__=(1, 0, 1)

from datetime import datetime
from hikka import loader, utils

@loader.tds
class SeasonsTimer(loader.Module):
    """Модуль таймер до начала времен года."""
    strings = {
        "name": "SeasonsTimer"
    }
    
    @loader.command(ru_doc="-> вывести таймер до зимы")
    async def towincmd(self, message):
        """-> display timer until winter"""
        now=datetime.now()
        winter=datetime(now.year, 12, 1)
        if now.month>12 or (now.month==12 and now.day>1):
            winter=datetime(now.year + 1, 12, 1)
        time_to_winter=abs(winter - now)
        await utils.answer(
            message,
            (
            "<b><emoji document_id=5334788464728612728>❤️</emoji> До зимы:\n</b>\n"
                f"• Дней<emoji document_id=5364179527230564196>⚪️</emoji> {time_to_winter.days}\n"
                f"• Часов<emoji document_id=5364179527230564196>⚪️</emoji> {time_to_winter.seconds // 3600}\n"
                f"• Минут<emoji document_id=5364179527230564196>⚪️</emoji> {time_to_winter.seconds // 60 % 60}\n"              
            ),
        ),
    
    @loader.command(ru_doc="-> вывести таймер до лета")
    async def tosumcmd(self, message):
        """-> display timer until summer"""
        now=datetime.now()
        summer=datetime(now.year, 6, 1)       
        if now.month>6 or (now.month==6 and now.day>1):
            summer=datetime(now.year+1, 6, 1)
        time_to_summer=abs(summer-now)
        await utils.answer(
            message,
            (
            "<b><emoji document_id=5334788464728612728>❤️</emoji> До лета:\n</b>"
                f"• Дней<emoji document_id=5364179527230564196>⚪️</emoji> {time_to_summer.days}\n"
                f"• Часов<emoji document_id=5364179527230564196>⚪️</emoji> {time_to_summer.seconds // 3600}\n"
                f"• Минут<emoji document_id=5364179527230564196>⚪️</emoji> {time_to_summer.seconds // 60 % 60}\n"
            ),
        ),
    
    @loader.command(ru_doc="-> вывести таймер до осени")
    async def toautcmd(self, message):
        """-> display timer until autumn"""
        now=datetime.now()
        autumn=datetime(now.year, 9, 1)
        if now.month>9 or (now.month==9 and now.day>1):
            autumn=datetime(now.year + 1, 9, 1)
        time_to_autumn=abs(autumn-now)
        await utils.answer(
            message,
            (
            "<b><emoji document_id=5334788464728612728>❤️</emoji> До осени:\n</b>"
                f"• Дней<emoji document_id=5364179527230564196>⚪️</emoji> {time_to_autumn.days}\n"
                f"• Часов<emoji document_id=5364179527230564196>⚪️</emoji> {time_to_autumn.seconds // 3600}\n"
                f"• Минут<emoji document_id=5364179527230564196>⚪️</emoji> {time_to_autumn.seconds // 60 % 60}\n"     
            ),
        ),
    
    @loader.command(ru_doc="-> вывести таймер до весны")
    async def tosprcmd(self, message):
        """-> display timer until spring"""
        now=datetime.now()
        spring=datetime(now.year, 3, 1)
        if now.month>3 or (now.month==3 and now.day>1):
            spring=datetime(now.year + 1, 3, 1)
        time_to_spring=abs(spring-now)
        await utils.answer(
            message,
            (
            "<b><emoji document_id=5334788464728612728>❤️</emoji> До весны:\n</b>"
                f"• Дней<emoji document_id=5364179527230564196>⚪️</emoji> {time_to_spring.days}\n"
                f"• Часов<emoji document_id=5364179527230564196>⚪️</emoji> {time_to_spring.seconds // 3600}\n"
                f"• Минут<emoji document_id=5364179527230564196>⚪️</emoji> {time_to_spring.seconds // 60 % 60}\n"
            ),
        )
