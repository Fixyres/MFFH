# meta developer: @VahueykoMod
# * |           V A H U E Y K O                        
# * |           © 2024 Vahueyko
from hikkatl.types import Message
from .. import loader, utils

@loader.tds
class CheatingUptime(loader.Module):
    """накручивает аптайм"""
    strings = {"name": "CheatingUptime"}

    async def addumcmd(self, message: Message):
        """.addum <минуты>"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "Недостаточно аргументов")        
        try:
            args = float(args)
        except (ValueError, TypeError):
            await utils.answer(message, "Толко числа")
        
        utils.init_ts -= args * 60
        await utils.answer(message, "Готово")
        
    async def adduhcmd(self, message: Message):
        """.adduh <часы>"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "Недостаточно аргументов")        
        try:
            args = float(args)
        except (ValueError, TypeError):
            await utils.answer(message, "Только числа")
        
        utils.init_ts -= args * 60 * 60
        await utils.answer(message, "готово")
        
    async def delumcmd(self, message: Message):
        """.delum <минуты>"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "Недостаточно аргументов")        
        try:
            args = float(args)
        except (ValueError, TypeError):
            await utils.answer(message, "Только числа")
        
        utils.init_ts += args * 60
        await utils.answer(message, "готово")
        
    async def deluhcmd(self, message: Message):
        """.deluh <часы>"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "Недостаточно аргументов")        
        try:
            args = float(args)
        except (ValueError, TypeError):
            await utils.answer(message, "Только числа")
        
        utils.init_ts += args * 60 * 60
        await utils.answer(message, "Готово")
