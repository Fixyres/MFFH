# meta developer: @procot1 & @devjmodules
import json
import os

import aiohttp
import requests
from telethon import events
from .. import loader, utils
import re
from time import sleep
from bs4 import BeautifulSoup

@loader.tds
class AIsupport(loader.Module):
    """
    AI - помощник по Hikka.
    🌘Version: 5.1 | Data set: 4
    ⚡Разработчик: @procot1
    💚Оригинальный модуль
    ВНИМАНИЕ! 
    поддержка этого модуля завершена. Этот модуль теперь часть функционала другого крупного модуля.
    Установить: .dlmod https://raw.githubusercontent.com/Chaek1403/VAWEIRR/refs/heads/main/Zetta%20-%20AI%20models.py
    просьба перейти на современное решение что бы получать обновления и улучшенный функционал.
    """
    strings = {"name": "AI-sup Hikka"}

    def __init__(self):
        super().__init__()
        self.default_model = "gpt-4o-mini"
        self.instructions = self.get_instructions()
        self.error_instructions = self.get_error_instructions()
        self.module_instructions = self.get_module_instruction()
        self.double_instructions = self.get_double_instruction()
        self.allmodule_instruction = self.get_allmodule_instruction()
        self.module_instruction2 = self.get_module_instruction2()
        self.module_instruction3 = self.get_module_instruction3()
        self.allmodule_instruction2 = self.get_allmodule_instruction2()
        self.metod = "on"
        self.provider = 'onlysq'
        self.api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"


    @loader.unrestricted
    async def aisupcmd(self, message):
        """
        Спросить у AI помощника.
        Использование: `.aisup <запрос>` или ответить на сообщение с `.aisup`
        
        🧠Скормлены знания: 
        • Установки | команды встроенных модулей | Внешние модули(40 модулей) | чаты Хикки | нюнсы Хикки | официальные тгк с модулями | меры безопасности | Список советов по устранению ошибок | Данные о хикке
        
        """
        r = "sup"
        await self.process_request(message, self.instructions, r)

    @loader.unrestricted
    async def aierrorcmd(self, message):
        """
        Спросить у AI помощника об ошибке модуля.
        Использование: `.aierror <запрос>` или ответить на сообщение с `.aierror`
        
        🧠Скормлены знания(old data set):
        • команды встроенных модулей | чаты Хикки | больше нюансов и принципов работы Хикки | примеры ошибок и их решений | большой список советов по устранению ошибок
        
        """
        r = "error"
        await self.process_request(message, self.error_instructions, r)

    def get_instructions(self):
        url = 'https://raw.githubusercontent.com/Chaek1403/VAWEIRR/refs/heads/main/instruction.txt'
        response = requests.get(url)
        return response.text

    def get_error_instructions(self):
        url = 'https://raw.githubusercontent.com/Chaek1403/VAWEIRR/refs/heads/main/error_instruction.txt'
        response = requests.get(url)
        return response.text

    def get_module_instruction(self):
        url = 'https://raw.githubusercontent.com/Chaek1403/VAWEIRR/refs/heads/main/module_instruction.txt'
        response = requests.get(url)
        return response.text

    def get_double_instruction(self):
        url = 'https://raw.githubusercontent.com/Chaek1403/VAWEIRR/refs/heads/main/double_instruction.txt'
        response = requests.get(url)
        return response.text

    def get_allmodule_instruction2(self):
        url = "https://raw.githubusercontent.com/Chaek1403/VAWEIRR/refs/heads/main/allmodule2.txt"
        response = requests.get(url)
        return response.text
    
    def get_allmodule_instruction(self):
        url = 'https://raw.githubusercontent.com/Chaek1403/VAWEIRR/refs/heads/main/allmodules.txt'
        response = requests.get(url)
        return response.text
        
    def get_module_instruction2(self):
        url = 'https://raw.githubusercontent.com/Chaek1403/VAWEIRR/refs/heads/main/module_instruction2.txt'
        response = requests.get(url)
        return response.text
        
    def get_module_instruction3(self):
        url = 'https://raw.githubusercontent.com/Chaek1403/VAWEIRR/refs/heads/main/module_instruction3.txt'
        response = requests.get(url)
        return response.text

    @loader.unrestricted
    async def aiinfocmd(self, message):
        """
        - Информация об обновлении✅
        """
        await message.edit('''<b>🧬Обновление 5.1:
Изменено:
- Теперь имеется 2 API провайдера: onlysq и devj. Изменить провайдера API для запросов можно с помощью команды .apiswitch.
- Добавлен data-set: 4. Команда aisup стала еще умнее.

Система поэтапного создания модуля: 
- Модель с дата-сетом(1) генерирует код
- затем модель с дата сетом(2) проверяет и корректирует код.
- затем модель с дата сетом(3) проверяет код на безопастность и корректирует код.
- после получается готовый модуль.

💫получается такая схема: Запрос>дт1>дт2>дт3>Модуль
🔗Тг канал модуля: https://t.me/hikkagpt</b>''')

    @loader.unrestricted
    async def aiprovcmd(self, message):
        """
        - Информация о провайдерах🔆
        """
        await message.edit('''<b>⚪️OnlySq: Стабильный, средняя скорость ответа.

🔸devj: Быстрая скорость ответа, Не стабилен из за разного возврата ответа от сервера что приводит к арбузам. P.s: Обезьянка может все съесть.</b>''')


    async def send_request_to_api(self, message, instructions, request_text, model="gpt-3.5-turbo"):
        """Отправляет запрос к API и возвращает ответ."""
        api_url = "http://api.onlysq.ru/ai/v2" if self.provider == "onlysq" else "https://api.vysssotsky.ru/"
        if self.provider == 'devj':
            payload = {
                    "model": "gpt-4",
                    "messages": [{"role": "user", "content": f"{instructions}\nЗапрос пользователя: {request_text}"}],
                    "max_tokens": 10048,
                    "temperature": 0.7,
                    "top_p": 1,
                }
        else:
            payload = {
                "model": 'gpt-3.5-turbo',
                "request": {
                    "messages": [
                        {
                            "role": "user",
                            "content": f"{instructions}\nНе используй HTML и форматирование текста. Так же помни что тебе нужно сохранить ответ предыдущей части модуля, если ты не знаешь ответа. И передать его дальше.\nЗапрос пользователя: {request_text}"
                        }
                    ]
                }
            }
        
        if self.provider == 'devj':
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(f"https://api.vysssotsky.ru/v1/chat/completions", headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}, data=json.dumps(payload)) as response:
                        if response.status == 200:
                            data = await response.json()
                            answer = data.get("choices", [{}])[0].get("message", {}).get("content", self.strings("no_server_respond"))
                            answer = f"<blockquote>{answer}</blockquote>"
                            return answer

                        else:
                            await message.edit("⚠️ Ошибка при запросе к API: Обезьяна съела арбуз🍉. Деталей ошибки нет.")
            except Exception as e:
                await message.edit(f"⚠️ Ошибка при запросе к API: {e}")
        else:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(api_url, json=payload) as response:
                        response.raise_for_status()
                        data = await response.json()
                        answer = data.get("answer", "🚫 Ответ не получен.").strip()
                        return answer
            except aiohttp.ClientError as e:
                await message.edit(f"⚠️ Ошибка при запросе к API: {e}\n\n💡 Попробуйте поменять модель или проверить код модуля.")
                return None


    async def allmodule(self, answer, message, request_text):
        rewrite2 = self.get_allmodule_instruction()
        await message.edit("<b>🎭Цепочка размышлений модели в процессе:\n🟢Первая модель приняла решение\n🟢Вторая модель приняла решение.\n💭Третья модель думает...</b>\n\nПочему так долго: каждая модель имеет свой дата сет. И сверяет ответ предыдущей модели с своими знаниями.")
        answer = await self.send_request_to_api(message, rewrite2, f"Запрос пользователя: {request_text}\nОтвет второй части модуля:{answer}")
        if answer:
            await self.allmodule2(answer, message, request_text)
    
    async def modulecreating(self, answer, message, request_text):
        rewrite = self.get_module_instruction2()
        await message.edit("<b>🎭Создается модуль:\n🟢Создание кода\n💭Тестирование...</b>\n\nЗаметка: чем лучше вы расспишите задачу для модели - тем лучше она создаст модуль. ")
        answer = await self.send_request_to_api(message, rewrite, f"User request: {request_text}\nAnswer to the first part of the module:{answer}")
        if answer:
            await self.modulecreating2(answer, message, request_text)

    async def allmodule2(self, answer, message, request_text):
        rewrite3 = self.get_allmodule_instruction2()  # Используем новый датасет
        await message.edit("<b>🎭Цепочка размышлений модели в процессе:\n🟢Первая модель приняла решение\n🟢Вторая модель приняла решение.\n🟢Третья модель приняла решение\n💭Четвертая модель думает...</b>\n\nПочему так долго: каждая модель имеет свой дата сет. И сверяет ответ предыдущей модели с своими знаниями.")
        answer = await self.send_request_to_api(message, rewrite3, f"Запрос пользователя: {request_text}\nОтвет третьей части модуля:{answer}")
        if answer:
            formatted_answer = f"❔ Запрос:\n`{request_text}`\n\n💡 <b>Ответ AI-помощника по Hikka</b>:\n{answer}"
            await message.edit(formatted_answer)
    
    async def modulecreating2(self, answer, message, request_text):
        rewrite = self.get_module_instruction3()
        await message.edit("<b>🎭Создается модуль:\n🟢Создание кода\n🟢Протестировано\n💭Проверка на безопастность и финальное тестирование...</b>\n\nЕще заметка: Лучше проверяйте что написала нейросеть, перед тем как использовать модуль.")
        answer = await self.send_request_to_api(message, rewrite, f"User request: {request_text}\nAnswer to the first part of the module:{answer}")
        if answer:
            try:
                if len(answer) > 4096:
                    await message.edit("⚠️ Код модуля слишком большой для отправки в сообщении. Был выслан просто файл.")
                    await self.save_and_send_code(answer, message)
                else:
                    await message.edit(f"<b>💡 Ответ AI-помощника по Hikka | Креатор модулей</b>:\n{answer}")
                    await self.save_and_send_code(answer, message)
            except Exception as e:
                if "Message was too long" in str(e):
                    await message.edit("⚠️ Код модуля слишком большой для отправки в сообщении. Отправляю файл...")
                    await self.save_and_send_code(answer, message)
                else:
                    await message.edit(f"⚠️ Ошибка: {e}")

    async def rewrite_process(self, answer, message, request_text):
        rewrite = self.get_double_instruction()
        await message.edit("<b>🎭Цепочка размышлений модели в процессе:\n🟢Первая модель приняла решение\n💭Вторая модель думает...</b>\n\nПочему так долго: каждая модель имеет свой дата сет. И сверяет ответ предыдущей модели с своими знаниями.")
        answer = await self.send_request_to_api(message, rewrite, f"Запрос пользователя: {request_text}\nОтвет первой части модуля:{answer}")
        if answer:
            await self.allmodule(answer, message, request_text)

    @loader.unrestricted
    async def apiswitchcmd(self, message):
        """
        Поменять API для запросов
        Использование: `.apiswitch <провайдер>
        доступные: onlysq и devj.
        
        """
        args = utils.get_args_raw(message)
        if args:
            provider = args.lower()  # Получаем аргумент и приводим к нижнему регистру
            if provider in ("onlysq", "devj"):
                self.provider = provider
                await message.edit(f"✅ Провайдер API изменен на {provider}")
            else:
                await message.edit("🚫 Недопустимый провайдер API. Доступные: onlysq, devj")
        else:
            await message.edit("🤔 Укажите провайдер API: onlysq или devj")

    @loader.unrestricted
    async def aicreatecmd(self, message):
        """
        Попросить AI помощника написать модуль.
        Использование: `.aicreate <запрос>` или ответить на сообщение с `.aicreate`
        
        🧠Скормлены знания:
        • Вся документация по написанию модулей Hikka (кроме Hikka only) | мелкие наводящие инструкции
        
        """
        r = "create"
        await self.process_request(message, self.module_instructions, r)

    @loader.unrestricted
    async def ultramodecmd(self, message):
        """
        Вкл/выкл качественного ответа
        Использование: `.ultramode <on/off>`
        
        """
        args = utils.get_args_raw(message)
        if args:
            metod = args.lower()
            if metod in ("on", "off"):
                self.metod = metod
                if metod == 'on':
                    await message.edit(f"📚 Качественный ответ включен. Скорость ответа меньше.")
                elif metod == 'off':
                    await message.edit(f"🏃‍♂️‍➡️ Качественный ответ выключен. Скорость ответа быстрее")
            else:
                await message.edit("🚫 Неправильные аргументы. Доступные: on, off")
        else:
            await message.edit("🤔 Укажите аргументы: on или off")

    async def save_and_send_code(self, answer, message):
        """Сохраняет код в файл, отправляет его и удаляет."""
        try:
            code_start = answer.find("`python") + len("`python")
            code_end = answer.find("```", code_start)
            code = answer[code_start:code_end].strip()
    
            with open("AI-module.py", "w") as f:
                f.write(code)
    
            await message.client.send_file(
                message.chat_id,
                "AI-module.py",
                caption="<b>💫Ваш готовый модуль</b>",
            )
    
            os.remove("AI-module.py")
    
        except (TypeError, IndexError) as e:
            await message.reply(f"Ошибка при извлечении кода: {e}")
        except Exception as e:  
            await message.reply(f"Ошибка при обработке кода: {e}")

    async def process_request(self, message, instructions, command):
        """
        Обрабатывает запрос к API модели ИИ.
        """
        reply = await message.get_reply_message()
        args = utils.get_args_raw(message)

        if reply:
            request_text = reply.raw_text
        elif args:
            request_text = args
        else:
            await message.edit("🤔 Введите запрос или ответьте на сообщение.")
            return

        try:
            await message.edit("<b>🤔 Думаю...</b>")
            answer = await self.send_request_to_api(message, instructions, request_text)
            if answer:
                if command == "error":
                    formatted_answer = f"💡<b> Ответ AI-помощника по Hikka | Спец. по ошибкам</b>:\n{answer}"
                    await message.edit(formatted_answer)
                elif command == "sup":
                    if self.metod == "on":
                        await message.edit("<b>💬Размышления моделей начались..</b>")
                        await self.rewrite_process(answer, message, request_text)
                    else:
                        formatted_answer = f"❔ Запрос:\n`{request_text}`\n\n💡 <b>Ответ AI-помощника по Hikka | Режим быстрого ответа</b>:\n{answer}\n\n❕В этом режиме модель ограничена знаниями встроенных модулей и базовой документации hikka"
                        await message.edit(formatted_answer)
                elif command == "create":
                    await self.modulecreating(answer, message, request_text)
                elif command == 'rewrite':
                    formatted_answer = f"❔ Запрос:\n`{request_text}`\n\n💡 <b>Ответ AI-помощника по Hikka</b>:\n{answer}"
                    await message.edit(formatted_answer)
                else:
                    formatted_answer = answer
                    await message.edit(formatted_answer)

        except Exception as e:
            await message.edit(f"⚠️ Ошибка: {e}")
