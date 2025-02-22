#   █▀▀ ▄▀█   █▀▄▀█ █▀█ █▀▄ █▀
#   █▀░ █▀█   █░▀░█ █▄█ █▄▀ ▄█

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: GrokAI
# Description: Взаимодействие с Grok AI
# meta developer: @FAmods
# meta banner: https://github.com/FajoX1/FAmods/blob/main/assets/banners/grokai.png?raw=true
# requires: aiohttp openai
# ---------------------------------------------------------------------------------

import asyncio
import logging

from openai import OpenAI

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class GrokAI(loader.Module):
    """Взаимодействие с Grok AI"""

    strings = {
        "name": "GrokAI",

        "no_args": "<emoji document_id=5854929766146118183>❌</emoji> <b>Нужно </b><code>{}{} {}</code>",
        "no_token": "<emoji document_id=5854929766146118183>❌</emoji> <b>Нету токена! Вставь его в </b><code>{}cfg grokai</code>",

        "asking_grok": "<emoji document_id=5325787248363314644>🔄</emoji> <b>Спрашиваю Grok...</b>",

        "answer": """<emoji document_id=5355148941878900494>🌐</emoji> <b>Ответ:</b> {answer}

<emoji document_id=5785419053354979106>❔</emoji> <b>Вопрос:</b> {question}""",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "api_key",
                None,
                lambda: "Токен GrokAI. Получить токен: https://console.x.ai",
                validator=loader.validators.Hidden(loader.validators.String())
            ),
            loader.ConfigValue(
                "model",
                "grok-beta",
                lambda: "Модель Grok AI",
            ),
        )

    async def client_ready(self, client, db):
        self.db = db
        self._client = client

    @loader.command()
    async def grok(self, message):
        """Задать вопрос к Grok"""
        q = utils.get_args_raw(message)
        if not q:
            return await utils.answer(message, self.strings["no_args"].format(self.get_prefix(), "grok", "[вопрос]"))

        if not self.config['api_key']:
            return await utils.answer(message, self.strings["no_token"].format(self.get_prefix()))

        await utils.answer(message, self.strings['asking_grok'])

        # Не тупите, ЭТО НЕ CHATGPT, это ГРОК от илона маска.
        # В документации для грока использовалась либа опенаи, так что меня заставили её юзануть ><

        client = OpenAI(
            api_key=self.config['api_key'],
            base_url="https://api.x.ai/v1" # вот теперь это точно грок
        )

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": q,
                }
            ],
            model=self.config['model'],
        )

        return await utils.answer(
            message,
            self.strings['answer'].format(
                question=q, 
                answer=chat_completion.choices[0].message.content)
            )