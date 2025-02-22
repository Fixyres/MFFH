#     ___    __ __ ____
#    /   |  / //_//  _/
#   / /| | / ,<   / /  
#  / ___ |/ /| |_/ /   
# /_/  |_/_/ |_/___/   
#                      
#     __  _______  ____  _____
#    /  |/  / __ \/ __ \/ ___/
#   / /|_/ / / / / / / /\__ \ 
#  / /  / / /_/ / /_/ /___/ / 
# /_/  /_/\____/_____//____/
#
# meta developer: @aki_modules

from .. import loader, utils
import requests

@loader.tds
class BirthdayGreetingMod(loader.Module):

    strings = {
        "name": "BirthdayGreeting",
        "error": "<b>An unexpected error occured...</b>",
        "wait": "<b>Please wait, your greeting on generation...</b>",
    }

    strings_ru = {
        "error": "<b>Произошла непредвиденная ошибка...</b>",
        "wait": "<b>Пожалуйста подождите, ваше поздравление на генерации...</b>",
    }

    @loader.command(
        ru_doc="[имя (необязательно)] - поздравить человека с Днём Рождения"
    )
    async def bdgreetcmd(self, message):
        """[name (optional)] - congratulate a person on Birthday"""

        name = utils.get_args_raw(message)
        prompt = f"""Сгенерируй текст для поздравления с Днем рождения человека под именем {name}. Только текст для поздравления, один вариант."""
        dictToSend = {"model": "gemini", "request": {"messages": [{"role": "user", "content": prompt}]}}

        try:
            waiting_msg = await utils.answer(message, self.strings('wait'))

            res = requests.post('http://api.onlysq.ru/ai/v2', json=dictToSend)
            response = res.json()

            await utils.answer(message, response['answer'])

        except Exception:
            await utils.answer(message, self.strings('error'))
