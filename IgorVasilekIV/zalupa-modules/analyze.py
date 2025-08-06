# meta developer: @HikkaZPM
# meta version: 1.0.0
# requires: google.generativeai

from .. import loader, utils
import google.generativeai as genai
import asyncio

class AnalyzeMod(loader.Module):
    """Анализ и сокращение сообщения с помощью ИИ (Gemini API)"""
    strings = {"name": "Analyze"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "api_key",
                None,
                lambda: "API ключ для Gemini (https://aistudio.google.com/app/apikey)",
                validator=loader.validators.Hidden()
            ),

            loader.ConfigValue(
                "model",
                "gemini-2.5-flash",
                lambda: "Модель gemini (можете вписать свой вариант)",
                validator=loader.validators.Choice(["gemini-1.5 Pro", "gemini-2.5-pro-exp-03-25", "gemini-2.5-flash", "gemini-2.0-flash"])
            )
        )

    async def client_ready(self, client, db):
        self._client = client
        self.db = db

        api_key = self.config.get("api_key")

        genai.configure(api_key=self.config['api_key'])
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    async def analyzecmd(self, message):
        reply = await message.get_reply_message()
        if not reply or not reply.text:
            await utils.answer(message, "А где реплай?")
            return

        text = reply.text.strip()

        sender = await reply.get_sender()
        user_name = sender.first_name
        user_username = sender.username
        user_link = f"<a href='tg://user?id={sender.id}'>{user_username}</a>"

        waiting = await utils.answer(message, "<emoji document_id=5355051922862653659>🤖</emoji> <b>Анализирую и сокращаю сообщение...</b>")

        response = await self.ask_gemini(text, user_name)
        formatted = (
            f"<emoji document_id=5461114598344129990>📖</emoji> <b>Анализ сообщения от {user_link}:</b>\n\n"
            f"<blockquote expandable><i>{text}</i></blockquote>\n"
            f"—————————————————————————\n"
            f"<blockquote expandable>{response}</blockquote>"
        )

        await waiting.edit(formatted)

    async def ask_gemini(self, text, user_name):
        prompt = f"You are an expert at summarizing messages. You prefer to use clauses instead of complete sentences. You will respond to this user: {user_name}. And you can use html tags if this realy need. Please keep your summary of the input within 4 sentences, fewer than 80 words. You CAN and NEED to answer on language, that you see in this text, and also, you need sumarize it:\n{text}"
        try:
            loop = asyncio.get_running_loop()
            response = await loop.run_in_executor(None, lambda: self.model.generate_content(prompt))
            return response.text.strip()
        except Exception as e:
            return f"<blockquote expandable>⚠️ Ошибка при обращении к Gemini: <code>{e}</code></blockquote>"
