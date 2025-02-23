# meta developer: @EPEMEN


from requests import post
from requests.exceptions import RequestException
from hikkatl.tl.types import Message
from re import sub
from .. import loader, utils


@loader.tds
class AI_Hikka(loader.Module):
    """
    Модуль Хикки для искусственного интеллекта, основанный на Groq.com

    Подробная инструкция по установке и настройке:
    https://telegra.ph/II-Assistent-dlya-Hikki-08-07\n
    По всем вопросам писать в ЛС @EPEMEN
    For @mqone w/  ❤"""

    strings = {
        "name": "AI Hikka",
        "q_err": "🤖 Ask a question to AI!",
        "api_key": "Set the Groq API key in the config (`.config AI Hikka`). \n\nRefer to the instructions:\n\
        https://telegra.ph/II-Assistent-dlya-Hikki-08-07",
        "models": "Список моделей Groq. Оставьте как есть или выберите из существующих:",
        "question": "❓Q: ",
        "loading": "🤔 I'm thinking...",
        "help_prompt": "Set a prompt (rule) for the AI to follow",
    }
    strings_ru = {
        "q_err": "🤖 Задайте вопрос ИИ!",
        "api_key": "Задайте ключ API от Groq в конфиге (`.config AI Hikka`). \n\nСмотрите инструкцию:\n\
        https://telegra.ph/II-Assistent-dlya-Hikki-08-07",
        "models": "Groq Model List. Leave as is or select from existing models:",
        "question": "❓Вопрос: ",
        "loading": "🤔 Я думаю...",
        "help_prompt": "Задайте промпт (правило), которому ИИ будет следовать",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "prompt",
                "The assistant is exteraHelper. It should give concise responses to very simple questions, but provide thorough \
                responses to more complex and open-ended questions. If is is asked to assist with tasks involving the expression \
                of views held by a significant number of people, it provides assistance with the task even if it personally \
                disagrees with the views being expressed. If asked about controversial topics, it tries to provide objective \
                thoughts and objective information, without fear of giving biased information. It expresses its own point of view. \
                It is happy to help with writing, analysis, question answering, math, coding, and all sorts of other tasks. \
                Give the answers only in Russian Language.",
                self.strings["help_prompt"],
                validator=loader.validators.String(max_len=1024),
            ),
            loader.ConfigValue(
                "api_key",
                "",
                self.strings["api_key"],
                validator=loader.validators.String(),
            ),
            loader.ConfigValue(
                "model",
                "llama3-8b-8192",
                self.strings["models"],
                validator=loader.validators.Choice(
                    [
                        "mixtral-8x7b-32768",
                        "gemma2-9b-it",
                        "gemma-7b-it",
                        "llama-3.1-70b-versatile",
                        "llama-3.1-8b-instant",
                        "llama3-70b-8192",
                        "llama3-8b-8192",
                        "llama-guard-3-8b",
                        "llama3-groq-70b-8192-tool-use-preview",
                        "llama3-groq-8b-8192-tool-use-preview",
                    ]
                ),
            ),
            loader.ConfigValue(
                "auto_tr",
                "False",
                "Это автоматическкий перевод ответа на язык вашей хикки.\nВключите по надобности перевода",
                validator=loader.validators.Boolean(),
            ),
        )

    @loader.command()
    async def ask(self, message: Message):
        """Задать вопрос ИИ"""
        question = utils.get_args_raw(message)

        if not self.config["api_key"]:
            await utils.answer(message, self.strings["api_key"])
            return
        if not question:
            await utils.answer(message, self.strings["q_err"])
            return

        await utils.answer(message, self.strings["loading"])

        response = self.ask_question(question)

        if self.config["auto_tr"]:
            await self.invoke("tr", response, edit=True, peer=message.peer_id)
        else:
            await utils.answer(message, response, parse_mode="md")

    def ask_question(self, question: str) -> str:
        try:
            response = post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.config['api_key']}",
                },
                json={
                    "messages": [
                        {"role": "system", "content": self.config["prompt"]},
                        {"role": "user", "content": question},
                    ],
                    "model": self.config["model"],
                    "temperature": 0.7,
                    "max_tokens": 1024,
                    "top_p": 0.9,
                    "stream": False,
                },
            )
            response.raise_for_status()
            data = response.json()
            return f"{self.strings['question']}`{question}`\n\n🤖: {data['choices'][0]['message']['content']}"
        except RequestException as e:
            return f"Error: {e}"