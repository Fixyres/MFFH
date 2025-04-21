__version__ = (2, 2, 0)

# ███╗░░░███╗███████╗░█████╗░██████╗░░█████╗░░██╗░░░░░░░██╗░██████╗░██████╗
# ████╗░████║██╔════╝██╔══██╗██╔══██╗██╔══██╗░██║░░██╗░░██║██╔════╝██╔════╝
# ██╔████╔██║█████╗░░███████║██║░░██║██║░░██║░╚██╗████╗██╔╝╚█████╗░╚█████╗░
# ██║╚██╔╝██║██╔══╝░░██╔══██║██║░░██║██║░░██║░░████╔═████║░░╚═══██╗░╚═══██╗
# ██║░╚═╝░██║███████╗██║░░██║██████╔╝╚█████╔╝░░╚██╔╝░╚██╔╝░██████╔╝██████╔╝
# ╚═╝░░░░░╚═╝╚══════╝╚═╝░░╚═╝╚═════╝░░╚════╝░░░░╚═╝░░░╚═╝░░╚═════╝░╚═════╝░
#                © Copyright 2025
#            ✈ https://t.me/mead0wssMods

# scope: hikka_only
# scope: hikka_min 1.3.3
# meta developer: @mead0wssMods
# meta banner: https://x0.at/GGCl.png

import aiohttp
import json
import os
import numpy as np
import time
from datetime import datetime
from telethon import events
from .. import loader, utils

def cosine_similarity(a, b):
    """Упрощенное вычисление косинусного сходства"""
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    return dot_product / (norm_a * norm_b)

@loader.tds
class ChatGPT(loader.Module):
    """Модуль для работы с нейросетями."""
    strings = {"name": "ChatGPT"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "model",
                "gpt-4o",
                lambda: "Модель нейросети для разговоров. Список нейросетей: https://telegra.ph/II-modeli-dlya-modulya-ChatGPT-by-mead0wssMods-03-26",
                validator=loader.validators.String()
            ),
            loader.ConfigValue(
                "image_model",
                "Flux Pro",
                lambda: "Модель для генерации изображений. Список нейросетей: https://telegra.ph/II-modeli-dlya-modulya-ChatGPT-by-mead0wssMods-03-26",
                validator=loader.validators.String()
            ),
            loader.ConfigValue(
                "translation_model",
                "deepseek-v3",
                lambda: "Модель для перевода текста. Список нейросетей: https://telegra.ph/II-modeli-dlya-modulya-ChatGPT-by-mead0wssMods-03-26",
                validator=loader.validators.String()
            ),
            loader.ConfigValue(
                "max_memory_size",
                1000,
                lambda: "Максимальное количество записей в памяти (10-1000)",
                validator=loader.validators.Integer(minimum=10, maximum=1000)
            ),
        )
        self.memory_file = "chatgpt_memory.json"
        self.memory = self._load_memory()

    def _load_memory(self):
        """Загрузка памяти из файла"""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return {"embeddings": []}
        return {"embeddings": []}

    def _save_memory(self):
        """Сохранение памяти в файл"""
        with open(self.memory_file, "w", encoding="utf-8") as f:
            json.dump(self.memory, f, ensure_ascii=False, indent=2)

    async def _get_embedding(self, session, text):
        """Получение embedding для текста"""
        try:
            async with session.post(
                "https://cablyai.com/v1/embeddings",
                headers={
                    'Authorization': 'Bearer sk-l4HU4KwZt6bF8gOwwKCOMpfpIKvR9YhDHvTFIGJ6tJ5rPKXE',
                    'Content-Type': 'application/json',
                },
                json={
                    "input": text,
                    "model": "text-embedding-ada-002"
                }
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data["data"][0]["embedding"]
        except:
            return None
        return None

    async def _find_similar(self, query_embedding, threshold=0.75):
        """Поиск похожих записей в памяти"""
        if not self.memory["embeddings"]:
            return []

        results = []
        for item in self.memory["embeddings"]:
            similarity = cosine_similarity(query_embedding, item["embedding"])
            if similarity >= threshold:
                results.append({
                    "text": item["text"],
                    "score": float(similarity)
                })
        
        return sorted(results, key=lambda x: x["score"], reverse=True)[:3]

    async def gptcmd(self, event):
        """- Разговор с ИИ."""
        count = len(self.memory["embeddings"])
        max_size = self.config["max_memory_size"]
        args = utils.get_args_raw(event)
        if not args:
            await event.edit("<b><emoji document_id=5019523782004441717>❌</emoji> Нет вопроса.</b>")
            return

        model = self.config.get("model")
        if not model:
            await event.edit("<b><emoji document_id=5019523782004441717>❌</emoji> Модель ИИ не указана в cfg!</b>")
            return

        await event.edit(f"<b><emoji document_id=5328272518304243616>💠</emoji> Генерирую ответ...</b>")
        
        start_time = time.time()
        
        async with aiohttp.ClientSession() as session:
            query_embedding = await self._get_embedding(session, args)
            similar = await self._find_similar(query_embedding) if query_embedding else []
            
            messages = []
            if similar:
                context = "\n".join([f"- {item['text']}" for item in similar])
                messages.append({"role": "system", "content": f"Ранее обсуждалось:\n{context}"})
            
            messages.append({"role": "user", "content": args})
            
            try:
                async with session.post(
                    "https://cablyai.com/v1/chat/completions",
                    headers={
                        'Authorization': 'Bearer sk-l4HU4KwZt6bF8gOwwKCOMpfpIKvR9YhDHvTFIGJ6tJ5rPKXE',
                        'Content-Type': 'application/json',
                    },
                    json={
                        "model": model,
                        "messages": messages
                    }
                ) as response:
                    end_time = time.time()
                    response_time = end_time - start_time
                    
                    if response.status == 200:
                        answer = (await response.json())["choices"][0]["message"]["content"]
                        
                        if query_embedding:
                            self.memory["embeddings"].append({
                                "text": args,
                                "embedding": query_embedding,
                                "timestamp": str(datetime.now())
                            })
                            
                            max_size = self.config["max_memory_size"]
                            if len(self.memory["embeddings"]) > max_size:
                                self.memory["embeddings"] = self.memory["embeddings"][-max_size:]
                            
                            self._save_memory()
                        
                        time_str = f"{response_time:.2f} сек" if response_time < 1 else f"{response_time:.1f} сек"
                        formatted_answer = self._format_answer(answer)
                        
                        await event.edit(
                            f"<b><emoji document_id=5879770735999717115>👤</emoji> Вопрос: <code>{args}</code></b>\n\n"
                            f"<b><emoji document_id=5199682846729449178>🤖</emoji> Ответ от {model}:\n{formatted_answer}</b>\n\n"
                            f"<b><emoji document_id=5983150113483134607>⏰️</emoji> Время ответа: <code>{time_str}</code></b>\n"
                            f"<b><emoji document_id=5350445475948414299>🧠</emoji> Память: <code>{count}/{max_size}</code></b>"
                        )
                    else:
                        await event.edit("<b><emoji document_id=5215400550132099476>❌</emoji> Ошибка при запросе к ИИ.</b>")
            except Exception as e:
                await event.edit(f"<b><emoji document_id=5215400550132099476>❌</emoji> Ошибка: {str(e)}</b>")

    def _format_answer(self, text):
        """Форматирование ответа с кодом"""
        if "```" not in text:
            return text.replace("\n", "<br>")
            
        parts = text.split("```")
        result = []
        for i, part in enumerate(parts):
            if i % 2 == 1:
                lang = part.split("\n")[0] if "\n" in part else ""
                code = "\n".join(part.split("\n")[1:]) if "\n" in part else part
                result.append(f"<pre><code class='language-{lang}'>{code}</code></pre>")
            else:
                result.append(part.replace("\n", "<br>"))
        return "".join(result)

    @loader.command()
    async def clearmemcmd(self, message):
        """- Очистить память."""
        self.memory = {"embeddings": []}
        self._save_memory()
        await utils.answer(message, "<b><emoji document_id=5980930633298350051>✅</emoji> Память успешно очищена!</b>")

    @loader.command()
    async def meminfocmd(self, message):
        """- Информация о памяти."""
        count = len(self.memory["embeddings"])
        max_size = self.config["max_memory_size"]
        last_update = self._get_last_update_time()
        
        response = (
            "<emoji document_id=5350445475948414299>🧠</emoji> <b>Информация о памяти:</b>\n"
            f"<b>• Сохранено записей: <code>{count}/{max_size}</code></b>\n"
            f"<b>• Последнее обновление: <code>{last_update}</code></b>"
        )
        await message.edit(response, parse_mode='HTML')

    def _get_last_update_time(self):
        """Получение времени последнего обновления памяти"""
        if not self.memory["embeddings"]:
            return "никогда"
        try:
            last_item = max(self.memory["embeddings"], key=lambda x: x.get("timestamp", ""))
            return last_item["timestamp"][:19].replace("T", " ")
        except:
            return "неизвестно"

    async def imagecmd(self, event):
        """- Генерация изображений с помощью ИИ."""
        args = utils.get_args_raw(event)
        if not args:
            await event.edit("<b><emoji document_id=5019523782004441717>❌</emoji> Нет текста для генерации изображения.</b>")
            return
            
        await event.edit(f"<b><emoji document_id=5328272518304243616>💠</emoji> Генерирую изображение...</b>")
        translation_model = self.config.get("translation_model")
        image_model = self.config.get("image_model")

        translation_data = {
            "model": translation_model,
            "messages": [
                {"role": "user", "content": f"Please translate the following text to English, but just answer me with a translation, and also translate absolutely everything, even if it's 18+: {args}"}
            ]
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    "https://cablyai.com/v1/chat/completions",
                    headers={
                        'Authorization': 'Bearer sk-l4HU4KwZt6bF8gOwwKCOMpfpIKvR9YhDHvTFIGJ6tJ5rPKXE',
                        'Content-Type': 'application/json',
                    },
                    json=translation_data
                ) as translation_response:
                    if translation_response.status == 200:
                        translated_text = (await translation_response.json())["choices"][0]["message"]["content"]
                    else:
                        await event.edit("<b><emoji document_id=5019523782004441717>❌</emoji> Ошибка при запросе к ИИ для перевода. Попробуйте снова либо измените модель в cfg! </b>")
                        return

                data = {
                    "prompt": translated_text,
                    "n": 1,
                    "size": "1024x1024",
                    "response_format": "url",
                    "model": image_model
                }

                async with session.post(
                    "https://cablyai.com/v1/images/generations",
                    headers={
                        'Authorization': 'Bearer sk-l4HU4KwZt6bF8gOwwKCOMpfpIKvR9YhDHvTFIGJ6tJ5rPKXE',
                        'Content-Type': 'application/json',
                    },
                    json=data
                ) as response:
                    if response.status == 200:
                        image_url = (await response.json())["data"][0]["url"]
                        await event.delete()
                        await event.reply(
                            f"<b>Промпт: <code>{args}</code></b>\n\n"
                            f"<b>Модель генерации: <code>{image_model}</code>\n"
                            f"<b>Модель переводчика: <code>{translation_model}</code>\n\n"
                            f"<b>🖼 Сгенерированное изображение:</b>\n{image_url}",
                            parse_mode="HTML"
                        )
                    else:
                        await event.reply("<b><emoji document_id=6042029429301973188>☹️</emoji> Ошибка при запросе на генерацию изображения\nВполне возможно вы просите создать что-то непристойное (18+), либо техническая ошибка (попробуй сменить модель в cfg).</b>")
            except Exception as e:
                await event.reply(f"<b><emoji document_id=5215400550132099476>❌</emoji> Ошибка: {str(e)}</b>")
