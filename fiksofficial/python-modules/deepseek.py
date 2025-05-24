# На модуль распространяется лицензия "GNU General Public License v3.0"
# https://github.com/all-licenses/GNU-General-Public-License-v3.0

# meta developer: @PyModule
from .. import loader, utils
import requests
import json
import asyncio

API_URL = "https://openrouter.ai/api/v1/chat/completions"
TG_MSG_LIMIT = 4096  # Лимит символов в сообщении Telegram

@loader.tds
class DeepSeekModule(loader.Module):
    "Модуль для отправки вопросов к DeepSeek с использованием OpenRouter API."

    strings = {"name": "DeepSeek"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            "ANIMATION", False, "Включить анимацию печати",
            "API_KEY", "", "API ключ OpenRouter"
        )
        self.history = []
    
    async def dsccmd(self, message):
        "Отправить вопрос к DeepSeek. Использование: .dsc <вопрос>"
        args = utils.get_args_raw(message)
        if not args:
            await message.edit("**❌ Ошибка:** Укажите вопрос.", parse_mode="Markdown")
            return
        
        api_key = self.config["API_KEY"].strip()
        if not api_key:
            await message.edit("**❌ Ошибка:** API ключ не установлен.", parse_mode="Markdown")
            return
        
        await message.edit("**🔄 Отправка запроса...**", parse_mode="Markdown")
        
        self.history.append({"role": "user", "content": args})
        
        payload = {
            "model": "deepseek/deepseek-r1:free",
            "messages": self.history
        }
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            data = response.json()
            
            if "choices" in data and len(data["choices"]) > 0:
                reply = data["choices"][0]["message"]["content"]
                self.history.append({"role": "assistant", "content": reply})
                
                if self.config["ANIMATION"]:
                    words = reply.split()
                    displayed_text = "**💬 Ответ:**\n\n"
                    
                    for word in words:
                        displayed_text += word + " "
                        await message.edit(displayed_text, parse_mode="Markdown")
                        await asyncio.sleep(0.2)  # Задержка между словами
                else:
                    await message.edit(f"**💬 Ответ:**\n\n{reply}", parse_mode="Markdown")
            else:
                await message.edit("**❌ Ошибка:** Пустой ответ от API.", parse_mode="Markdown")
        except requests.exceptions.RequestException as e:
            await message.edit(f"**❌ Ошибка запроса:** `{str(e)}`", parse_mode="Markdown")

    async def txtdsccmd(self, message):
        "Отправить содержимое .txt файла в DeepSeek. Использование: !txtdsc (ответ на .txt файл)"
        reply = await message.get_reply_message()
        if not reply or not reply.file or not reply.file.name.endswith(".txt"):
            await message.edit("**❌ Ошибка:** Ответь на `.txt` файл.", parse_mode="Markdown")
            return
        
        api_key = self.config["API_KEY"].strip()
        if not api_key:
            await message.edit("**❌ Ошибка:** API ключ не установлен.", parse_mode="Markdown")
            return

        await message.edit("**🔄 Читаю файл...**", parse_mode="Markdown")

        file_bytes = await reply.download_media(bytes)
        file_text = file_bytes.decode("utf-8").strip()

        if not file_text:
            await message.edit("**❌ Ошибка:** Файл пуст.", parse_mode="Markdown")
            return

        await message.edit("**🔄 Отправка запроса...**", parse_mode="Markdown")

        self.history.append({"role": "user", "content": file_text})

        payload = {
            "model": "deepseek/deepseek-r1:free",
            "messages": self.history
        }

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            data = response.json()

            if "choices" in data and len(data["choices"]) > 0:
                reply_text = data["choices"][0]["message"]["content"]
                self.history.append({"role": "assistant", "content": reply_text})

                if self.config["ANIMATION"]:
                    words = reply_text.split()
                    displayed_text = "**💬 Ответ:**\n\n"

                    for word in words:
                        displayed_text += word + " "
                        await message.edit(displayed_text, parse_mode="Markdown")
                        await asyncio.sleep(0.2)
                else:
                    await message.edit("**💬 Ответ:**", parse_mode="Markdown")
                    await self.send_long_message(message, reply_text)
            else:
                await message.edit("**❌ Ошибка:** Пустой ответ от API.", parse_mode="Markdown")
        except requests.exceptions.RequestException as e:
            await message.edit(f"**❌ Ошибка запроса:** `{str(e)}`", parse_mode="Markdown")
    
    async def cleardsccmd(self, message):
        "Очистить историю диалога с DeepSeek."
        self.history = []
        await message.edit("**✅ История диалога очищена.**", parse_mode="Markdown")

    async def send_long_message(self, message, text):
        "Отправляет длинный текст несколькими сообщениями"
        chunks = [text[i : i + TG_MSG_LIMIT] for i in range(0, len(text), TG_MSG_LIMIT)]
        for chunk in chunks:
            await message.reply(chunk)
