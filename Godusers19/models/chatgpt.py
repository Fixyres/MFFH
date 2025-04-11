# meta developer: @goduser18
from .. import loader, utils
import logging

logger = logging.getLogger(__name__)

@loader.tds
class GPTModule(loader.Module):
    """ChatGPT"""
    strings = {"name": "GPTCHAT"}

    def __init__(self):
        super().__init__()
        self.chat_states = {}
        self.default_instruction = "Ответ на вопрос."
        self.grok_bot_username = "@GrokAI"

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    @loader.unrestricted
    async def on_gptcmd(self, message):
        """Включить GPT в этом чате"""
        chat_id = message.chat_id
        self.chat_states[chat_id] = {
            "active": True,
            "instruction": self.default_instruction,
            "history": []
        }
        await utils.answer(message, "<b>✅ GPT включен. Используйте .sgpt вопрос</b>")

    @loader.unrestricted
    async def off_gptcmd(self, message):
        """Выключить GPT в этом чате"""
        chat_id = message.chat_id
        if chat_id in self.chat_states:
            del self.chat_states[chat_id]
            await utils.answer(message, "<b>✅ GPT выключен</b>")
        else:
            await utils.answer(message, "<b>❌ GPT не был активирован</b>")

    async def watcher(self, message):
        chat_id = message.chat_id
        if (chat_id not in self.chat_states or 
            not self.chat_states[chat_id]["active"] or 
            not message.text or 
            not message.text.startswith(".sgpt")):
            return

        user_message = message.text[5:].strip()
        if not user_message:
            return

        chat_state = self.chat_states[chat_id]
        prompt = f"{chat_state['instruction']}\n\n"
        
        for msg in chat_state["history"][-3:]:  # Сохраняем только 3 последних сообщения
            role = "Пользователь" if msg["role"] == "user" else "GPT"
            prompt += f"{role}: {msg['content']}\n"

        prompt += f"Пользователь: {user_message}\nGPT:"

        try:
            async with self.client.conversation(self.grok_bot_username) as conv:
                await conv.send_message(prompt)
                reply = (await conv.get_response()).text

            chat_state["history"].append({"role": "user", "content": user_message})
            chat_state["history"].append({"role": "assistant", "content": reply})

            await message.reply(reply)

        except Exception as e:
            logger.exception("GPT request failed")
            await utils.answer(message, f"<b>⚠️ Ошибка:</b> {str(e)}")
            
            
            #да  еблан
            # я спизди вашу сессию ыыы