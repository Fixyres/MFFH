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

# Thanks to OnlySQ team <3

import requests as req
from .. import loader, utils

@loader.tds
class NeuroMod(loader.Module):
    strings = {
        "name": "Neuro",
        "no_prompt": "<emoji document_id=5873121512445187130>❓</emoji> <b>Where your prompt?</b>",
        "error": "<emoji document_id=5872829476143894491>🚫</emoji> <b>This error occured:</b>\n{}",
        "wait": "<emoji document_id=5791714113906282664>⚡️</emoji> <b>Wait, answer to your prompt on generation...</b>",
        "success": "<emoji document_id=5776375003280838798>✅</emoji> <b>Successful!</b>\n\n<emoji document_id=5879770735999717115>👤</emoji> <b>Your prompt:</b>\n<code>{}</code>\n\n<emoji document_id=5931415565955503486>🤖</emoji> <b>Neuro's answer:</b>\n<code>{}</code>",
    }
    strings_ru = {
        "no_prompt": "<emoji document_id=5873121512445187130>❓</emoji> <b>Где твой запрос?</b>",
        "error": "<emoji document_id=5872829476143894491>🚫</emoji> <b>Произошла эта ошибка:</b>\n{}",
        "wait": "<emoji document_id=5791714113906282664>⚡️</emoji> <b>Подожди, ответ на твой вопрос на генерации...</b>",
        "success": "<emoji document_id=5776375003280838798>✅</emoji> <b>Успешно!</b>\n\n<emoji document_id=5879770735999717115>👤</emoji> <b>Твой вопрос:</b>\n<code>{}</code>\n\n<emoji document_id=5931415565955503486>🤖</emoji> <b>Ответ Neuro:</b>\n<code>{}</code>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "model",
                "gemini",
                "Choose model",
                validator=loader.validators.Choice(["gpt-3.5-turbo", "gemini", "claude-3.5-sonnet", "claude-3-haiku", "copilot", "gpt-4o-mini", "searchgpt"]),
            ),
        )

    @loader.command(
        ru_doc="[запрос] - спросить Neuro"
    )
    async def neurocmd(self, message):
        """[prompt] - ask Neuro"""

        question = utils.get_args_raw(message)

        if not question:
            await utils.answer(message, self.strings("no_prompt"))
            return

        await utils.answer(message, self.strings("wait"))

        dictToSend = {"model": self.config['model'], "request": {"messages": [{"role": "user", "content": question}]}}
        res = req.post('http://api.onlysq.ru/ai/v2', json=dictToSend)
        response = res.json()

        try:
            await utils.answer(message, self.strings("success").format(question, response['answer']))

        except Exception as e:
            await utils.answer(message, self.strings("error").format(e))
