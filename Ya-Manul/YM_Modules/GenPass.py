# meta developer: @YA_ManuI

import random
import string
from .. import loader, utils

@loader.tds
class PasswordGeneratorMod(loader.Module):
    """Генератор безопасных паролей"""
    strings = {"name": "GenPass"}

    @loader.command()
    async def ghelp(self, message):
        """- показать опции генерации"""
        text = (
            "⚙️ <b>Доступные настройки:</b>\n\n"
            "▫️ Укажи число после команды для длины пароля\n"
            "▫️ Пример: <code>.genpass 16</code>\n"
            "▫️ Диапазон: <b>4-999 символов</b>\n"
            "▫️ Используемые символы:\n"
            "<code>A-Z a-z 0-9 !@#$%^&*()</code>"
        )
        await utils.answer(message, text)

    @loader.command()
    async def genpass(self, message):
        """[длина] - сгенерировать пароль"""
        args = utils.get_args_raw(message)
        try:
            length = int(args) if args.isdigit() else 8
        except:
            length = 8
        
        length = max(4, min(999, length))
        
        chars = string.ascii_letters + string.digits + "!@#$%^&*()"
        password = "".join(random.SystemRandom().choice(chars) for _ in range(length))
        
        await utils.answer(message, f"🔐 Пароль ({length} символов):\n<code>{password}</code>")