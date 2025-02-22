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

import requests
from .. import loader, utils

@loader.tds
class LinkShortenerMod(loader.Module):
    """Модуль для сокращения ссылок через TinyURL"""
    strings = {
        "name": "LinkShortener",
        "no_link": "<b>Please provide a link to shorten or reply to a message with a link.</b>",
        "invalid_link": "<b>Invalid link. It must start with http:// or https://</b>",
        "shortened_link": "<b>Shortened link:</b>",
        "shortening_error": "<b>Error shortening link.</b>",
        "error": "<b>An error occurred:</b>",
    }

    strings_ru = {
        "no_link": "<b>Пожалуйста, укажите ссылку для сокращения или ответьте на сообщение с ссылкой.</b>",
        "invalid_link": "<b>Неверная ссылка. Она должна начинаться с http:// или https://</b>",
        "shortened_link": "<b>Сокращенная ссылка:</b>",
        "shortening_error": "<b>Ошибка при сокращении ссылки.</b>",
        "error": "<b>Произошла ошибка:</b>",
    }

    async def client_ready(self, client, db):
        self.client = client

    @loader.command(
        ru_doc="Сокращает ссылку. Использование: .slink <link or reply>"
    )
    async def slink(self, message):
        """Shortens a link. Usage: .slink <link or reply>"""
        args = utils.get_args_raw(message)
        if not args and message.is_reply:
            reply_message = await message.get_reply_message()
            args = reply_message.raw_text
        
        if not args:
            await utils.answer(message, self.strings["no_link"])
            return
        
        if not args.startswith("http"):
            await utils.asnwer(message, self.strings["invalid_link"])
            return

        try:
            response = requests.get(f"http://tinyurl.com/api-create.php?url={args}")
            if response.status_code == 200:
                short_url = response.text
                await utils.answer(message, f'''{self.strings["shortened_link"]} {short_url}''')
            else:
                await utils.answer(message, self.strings["shortening_error"])
        except Exception as e:
            await utils.answer(message, f'''{self.strings["error"]}\n<code>{str(e)}</code>''')
