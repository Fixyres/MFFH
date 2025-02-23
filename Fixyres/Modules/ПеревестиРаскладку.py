#meta developer: @xuduk
"""
██████████████████████████████████████████████████████████████████████████████████
█░░░░░░░░██░░░░░░░░█░░░░░░██░░░░░░█░░░░░░░░░░░░███░░░░░░██░░░░░░█░░░░░░██░░░░░░░░█
█░░▄▀▄▀░░██░░▄▀▄▀░░█░░▄▀░░██░░▄▀░░█░░▄▀▄▀▄▀▄▀░░░░█░░▄▀░░██░░▄▀░░█░░▄▀░░██░░▄▀▄▀░░█
█░░░░▄▀░░██░░▄▀░░░░█░░▄▀░░██░░▄▀░░█░░▄▀░░░░▄▀▄▀░░█░░▄▀░░██░░▄▀░░█░░▄▀░░██░░▄▀░░░░█
███░░▄▀▄▀░░▄▀▄▀░░███░░▄▀░░██░░▄▀░░█░░▄▀░░██░░▄▀░░█░░▄▀░░██░░▄▀░░█░░▄▀░░██░░▄▀░░███
███░░░░▄▀▄▀▄▀░░░░███░░▄▀░░██░░▄▀░░█░░▄▀░░██░░▄▀░░█░░▄▀░░██░░▄▀░░█░░▄▀░░░░░░▄▀░░███
█████░░▄▀▄▀▄▀░░█████░░▄▀░░██░░▄▀░░█░░▄▀░░██░░▄▀░░█░░▄▀░░██░░▄▀░░█░░▄▀▄▀▄▀▄▀▄▀░░███
███░░░░▄▀▄▀▄▀░░░░███░░▄▀░░██░░▄▀░░█░░▄▀░░██░░▄▀░░█░░▄▀░░██░░▄▀░░█░░▄▀░░░░░░▄▀░░███
███░░▄▀▄▀░░▄▀▄▀░░███░░▄▀░░██░░▄▀░░█░░▄▀░░██░░▄▀░░█░░▄▀░░██░░▄▀░░█░░▄▀░░██░░▄▀░░███
█░░░░▄▀░░██░░▄▀░░░░█░░▄▀░░░░░░▄▀░░█░░▄▀░░░░▄▀▄▀░░█░░▄▀░░░░░░▄▀░░█░░▄▀░░██░░▄▀░░░░█
█░░▄▀▄▀░░██░░▄▀▄▀░░█░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀▄▀▄▀▄▀░░░░█░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀░░██░░▄▀▄▀░░█
█░░░░░░░░██░░░░░░░░█░░░░░░░░░░░░░░█░░░░░░░░░░░░███░░░░░░░░░░░░░░█░░░░░░██░░░░░░░░█
██████████████████████████████████████████████████████████████████████████████████
"""
from .. import loader, utils

@loader.tds
class TranslateLayout(loader.Module):
    """Переводит русский текст введённый на английской раскладке"""
    strings = {'name': 'Перевести раскладку'}

    @loader.command(alias='перевестираскладку')
    async def trlayout(self, message):
        """[text or replay] - Перевести на RU раскладку"""
        original_text = "<emoji document_id=5350722806281676158>✅</emoji><b> Изначальный текст:</b>"
        transformed_text = "<emoji document_id=5974438511057570894>⌨</emoji><b> Преобразованный текст:</b>"
        space = " "
        args = utils.get_args_raw(message)
        if not args and message.is_reply:
            reply_message = await message.get_reply_message()
            args = reply_message.raw_text
        
        if not args:
            await message.edit("<b><emoji document_id=5465665476971471368>❌</emoji> Пожалуйста, укажите текст для преобразования в киррилицу или ответьте на сообщение с ним.</b>")
            return
        await message.edit(original_text + space + args + "\n" + transformed_text + space + args.replace("`", "ё").replace("~", "Ё").replace("q", "й").replace("Q", "Й").replace("w", "ц").replace("W", "Ц").replace("e", "у").replace("E", "У").replace("r", "к").replace("R", "К").replace("t", "е").replace("T", "Е").replace("y", "н").replace("Y", "Н").replace("u", "г").replace("U", "Г").replace("i", "ш").replace("I", "Ш").replace("o", "щ").replace("O", "Щ").replace("p", "з").replace("P", "З").replace("a", "ф").replace("A", "Ф").replace("s", "ы").replace("S", "Ы").replace("d", "в").replace("D", "В").replace("f", "а").replace("F", "А").replace("g", "п").replace("G", "П").replace("h", "р").replace("H", "Р").replace("j", "о").replace("J", "О").replace("k", "л").replace("K", "Л").replace("l", "д").replace("L", "Д").replace("z", "я").replace("Z", "Я").replace("x", "ч").replace("X", "Ч").replace("c", "с").replace("C", "С").replace("v", "м").replace("V", "М").replace("b", "и").replace("B", "И").replace("n", "т").replace("N", "Т").replace("m", "ь").replace("M", "Ь").replace(",", "б").replace("<", "Б").replace(".", "ю").replace(">", "Ю").replace("/", ".").replace("?", ",").replace(";", "ж").replace(":", "Ж").replace("'", "э").replace("&", "?").replace("^", ":").replace("$", ";").replace("[", "х").replace("{", "Х").replace("]", "ъ").replace("}", "Ъ"))
