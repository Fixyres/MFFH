__version__ = (1, 0)
#  meta developer: @Enceth
# change-log: Pisunf7
from deep_translator import GoogleTranslator
from .. import loader, utils

class Translate(loader.Module):
    """Переводчик"""

    strings = {"name": "ETranslate"}

    async def translatecmd(self, message):
        """Репли на сообщение"""
        reply = await message.get_reply_message()
        if not reply or not reply.text:
            await utils.answer(message, "Так не работает")
            return

        args = utils.get_args_raw(message)
        target_lang = args if args else "ru"  

        try:
            translated = GoogleTranslator(target=target_lang).translate(reply.text)
            await utils.answer(message, f"**Перевод ({target_lang}):**\n\n{translated}")
        except Exception as e:
            await utils.answer(message, f"Ошибка, хз заплачь: {str(e)}")