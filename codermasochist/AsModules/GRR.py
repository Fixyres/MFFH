# meta developer: @codermasochist

from .. import loader, utils

@loader.tds
class GRR(loader.Module):
    """генератор рандомных паролей"""
    
    strings = {"name": "GRR"}
    
    async def grrcmd(self, message):
        """ — <число> — макс. символов."""
        args = message.text.split()
        
        if len(args) < 2:
            await utils.answer(message, "<b>че за хуйню ты высрал?</b>")
            return
        
        try:
            length = int(args[1])
        except ValueError:
            return
        
        password = utils.rand(length)
        await utils.answer(message, f"<blockquote>✅ <b>ваш пароль:</b>\n\n<code>{password}</code></blockquote>")	
