# meta developer: @hikkagpt
import json

import aiohttp
from .. import loader, utils
from telethon import events
import requests
from telethon import events
from .. import loader, utils
import re
from time import sleep
from bs4 import BeautifulSoup
import base64
from telethon.tl.custom import Message 

available_models = {
    "1": "o3-mini",
    "2": "o1-preview",
    "3": "o1-Mini",
    "4": "gpt-4o",
    "5": "gpt-4o-mini",
    "6": "gpt4-turbo",
    "7": "gpt-3.5-turbo",
    "8": "gpt-4",
    "9": "deepseek-v3",
    "10": "deepseek-r1",
    "11": "gemini",
    "12": "gemini-1.5 Pro",
    "13": "gemini-flash",
    "14": "llama-3.1",
    "15": "llama-2",
    "16": "claude-3-haiku",
    "17": "claude-3.5-sonnet",  # Claude 3.5 Sonnet рядом с Claude 3 Haiku
    "18": "bard",
    "19": "qwen",
    "20": "t-pro",
    "21": "t-lite"
}



# Путь к файлу для хранения личностей
PERSONAS_FILE = "personas.json"


# Функция для загрузки личностей из файла
def load_personas():
    try:
        with open(PERSONAS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


# Функция для сохранения личностей в файл
def save_personas(personas):
    with open(PERSONAS_FILE, "w", encoding="utf-8") as f:
        json.dump(personas, f, indent=4)




# Загружаем личности при запуске модуля
personas = load_personas()


@loader.tds
class AIModule(loader.Module):
    """
🧠 Модуль Zetta - AI Models
>> Часть экосистемы Zetta - AI models << 
🌒 Version: 8.3 | MoDeLs

**Описание:**
Модуль объединяет несколько мощных инструментов для работы с ИИ, делая общение и взаимодействие максимально удобным. Подходит как для быстрых запросов, так и для создания глубоких диалогов с контекстом.  

**Режимы работы:**
  - **Одиночный запрос:**
    .ai **запрос** - мгновенный ответ без сохранения истории диалога.  

  - **Чат:**
    **.chat** - ведите диалог с ИИ, который запоминает контекст беседы.  

  - **Создание личностей:**
    Создавайте роли для ИИ, чтобы он мог выполнять уникальные задачи. Сохранение ролей и их переключение через **.switchpersona.**

  - **Переписывание текстов:**
    Используйте .rewrite для перевода, стилизации или упрощения сложных формулировок.  

  - **Работа с Hikka Userbot:**
    Команды aisup, aicreate, aierror помогут в создании, улучшении и отладке модулей.  

**Особенности:**
- Поддержка до 21 моделей ИИ.  
- Полная интеграция с Telegram.  
- Универсальность и практичность для любых задач.
    """
    strings = {"name": "Zetta - AI models"}

    def __init__(self):
        super().__init__()
        self.default_model = "gpt-4o-mini"
        self.active_chats = {}
        self.chat_history = {}
        self.chat_archive = {}
        self.role = {}
        self.response_mode = {}
        self.edit_promt = "off"
        self.instructions = self.get_instructions()
        self.error_instructions = self.get_error_instructions()
        self.module_instructions = self.get_module_instruction()
        self.double_instructions = self.get_double_instruction()
        self.allmodule_instruction = self.get_allmodule_instruction()
        self.module_instruction2 = self.get_module_instruction2()
        self.module_instruction3 = self.get_module_instruction3()
        self.allmodule_instruction2 = self.get_allmodule_instruction2()
        self.metod = "on"
        self.provider = 'zetta'
        self.api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
        self.handle_voice_message = self.handle_voice_message()
        self.humanmode = 'off'

    @loader.unrestricted
    async def aisupcmd(self, message):
        """
        Спросить у AI помощника для Hikka.
        Использование: `.aisup <запрос>` или ответить на сообщение с `.aisup`
        """
        r = "sup"
        await self.process_request(message, self.instructions, r)

    @loader.unrestricted
    async def aierrorcmd(self, message):
        """
        Спросить у AI помощника  для Hikka об ошибке модуля.
        Использование: `.aierror <запрос>` или ответить на сообщение с `.aierror`
        """
        r = "error"
        await self.process_request(message, self.error_instructions, r)

    def get_instructions(self):
        url = 'https://raw.githubusercontent.com/Chaek1403/VAWEIRR/refs/heads/main/data-set1.txt'
        response = requests.get(url)
        return response.text

    def get_error_instructions(self):
        url = 'https://raw.githubusercontent.com/Chaek1403/VAWEIRR/refs/heads/main/error_set.txt'
        response = requests.get(url)
        return response.text

    def get_module_instruction(self):
        url = 'https://raw.githubusercontent.com/Chaek1403/VAWEIRR/refs/heads/main/module_set.txt'
        response = requests.get(url)
        return response.text

    def get_double_instruction(self):
        url = 'https://raw.githubusercontent.com/Chaek1403/VAWEIRR/refs/heads/main/data-set2.txt'
        response = requests.get(url)
        return response.text

    def get_allmodule_instruction2(self):
        url = "https://raw.githubusercontent.com/Chaek1403/VAWEIRR/refs/heads/main/data-set4.txt"
        response = requests.get(url)
        return response.text
    
    def get_allmodule_instruction(self):
        url = 'https://raw.githubusercontent.com/Chaek1403/VAWEIRR/refs/heads/main/data-set3.txt'
        response = requests.get(url)
        return response.text
        
    def get_module_instruction2(self):
        url = 'https://raw.githubusercontent.com/Chaek1403/VAWEIRR/refs/heads/main/module_set2.txt'
        response = requests.get(url)
        return response.text
        
    def get_module_instruction3(self):
        url = 'https://raw.githubusercontent.com/Chaek1403/VAWEIRR/refs/heads/main/module_set3.txt'
        response = requests.get(url)
        return response.text
    
    
    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.active_chats = self.db.get("AIModule", "active_chats", {})
        self.chat_history = self.db.get("AIModule", "chat_history", {})
        self.chat_archive = self.db.get("AIModule", "chat_archive", {})
        self.role = self.db.get("AIModule", "role", {})
        self.response_mode = self.db.get("AIModule", "response_mode", {})


    async def handle_voice_message(message: Message):
        try:
            # Получаем ссылку на файл
            file_path = await client.download_media(message.voice)

            # Конвертируем аудио в формат WAV
            audio = AudioSegment.from_ogg(file_path)
            audio_path = "temp_audio.wav"
            audio.export(audio_path, format="wav")

            # Распознаем аудио
            voice = await message.edit("Слушаю...🎙")
            recognized_text = recognize_audio(audio_path)

            if recognized_text:
                request_text = recognized_text
                return request_text
            else:
                await message.edit("Не удалось распознать голосовое сообщение.")

            # Удаляем временный файл
            os.remove(audio_path)
        except Exception as e:
            await message.reply(f"Произошла ошибка: {e}")

    @loader.unrestricted
    async def modelcmd(self, message):
        """
        Устанавливает модель ИИ по умолчанию.
        Использование: `.model <номер>` или `.model list` для списка.
        """
        args = utils.get_args_raw(message)
        if not args:
            await message.edit("🤔 <b>Укажите номер модели или list для просмотра списка.</b>")
            return

        if args == "list":
            model_list = "\n".join([f"<b>{k}.</b> {v}" for k, v in available_models.items()])
            await message.edit(f"📝 <b>Доступные модели:</b>\n{model_list}")
            return

        if args not in available_models:
            await message.edit("🚫 <b>Неверный номер модели.</b>")
            return

        self.default_model = available_models[args]
        await message.edit(f"✅ <b>Модель изменена на:</b> {self.default_model}")

    @loader.unrestricted
    async def chatcmd(self, message):
        """
        Включает/выключает режим чата.
        Использование: `.chat`
        """
        chat_id = str(message.chat_id)
        if self.active_chats.get(chat_id):
            self.active_chats.pop(chat_id, None)
            self.db.set("AIModule", "active_chats", self.active_chats)

            if chat_id in self.chat_history:
                self.chat_archive[chat_id] = self.chat_history[chat_id]
                self.chat_history.pop(chat_id, None)
                self.db.set("AIModule", "chat_history", self.chat_history)
                self.db.set("AIModule", "chat_archive", self.chat_archive)
                await message.edit("📴 <b>Режим чата выключен. История архивирована.</b>")
            else:
                await message.edit("📴 <b>Режим чата выключен.</b>")
        else:
            self.active_chats[chat_id] = True
            self.db.set("AIModule", "active_chats", self.active_chats)

            if chat_id in self.chat_archive:
                self.chat_history[chat_id] = self.chat_archive[chat_id]
                self.chat_archive.pop(chat_id, None)
                self.db.set("AIModule", "chat_history", self.chat_history)
                self.db.set("AIModule", "chat_archive", self.chat_archive)
                await message.edit("💬 <b>Режим чата включен. История загружена.</b>")
            else:
                await message.edit("💬 <b>Режим чата включен.</b>")

    async def send_request_to_api(self, message, instructions, request_text, model="gpt-4o-mini"):
        """Отправляет запрос к API и возвращает ответ."""
        api_url = "http://109.172.94.236:5001/Zetta/v1/models" if self.provider == "zetta" else "https://api.vysssotsky.ru/"
        if self.provider == 'devj':
            # Формируем payload для запроса к devj API
            payload = {
                "model": "gpt-4",
                "messages": [{"role": "user", "content": f"{instructions}\nЗапрос пользователя: {request_text}"}],
                "max_tokens": 10048,
                "temperature": 0.7,
                "top_p": 1,
            }

            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(f"https://api.vysssotsky.ru/v1/chat/completions", 
                                           headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                                           data=json.dumps(payload)) as response:
                        if response.status == 200:
                            data = await response.json()
                            answer = data.get("choices", [{}])[0].get("message", {}).get("content", "Ответ не получен.")
                            answer = f"<blockquote>{answer}</blockquote>"
                            return answer
                        else:
                            await message.edit("⚠️ Ошибка при запросе к API: Обезьяна съела арбуз🍉. Деталей ошибки нет.")
            except Exception as e:
                await message.edit(f"⚠️ Ошибка при запросе к API: {e}")

        else:
            api_url = "http://109.172.94.236:5001/Zetta/v1/models"
            payload = {
                "model": self.default_model,
                "request": {
                    "messages": [
                        {
                            "role": "user",
                            "content": f"{instructions}\nНе используй HTML и форматирование текста. Также помни, что тебе нужно сохранить ответ предыдущей части модуля, если ты не знаешь ответа. И передать его дальше.\nЗапрос пользователя: {request_text}"
                        }
                    ]
                }
            }

            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(api_url, json=payload) as response:
                        # Проверка на успешный статус
                        response.raise_for_status()
                        data = await response.json()

                        # Получаем ответ
                        answer = data.get("answer", "🚫 Ответ не получен.").strip()
                        decoded_answer = base64.b64decode(answer).decode('utf-8')
                        answer = decoded_answer
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
        доступные: zetta и devj.
        
        """
        args = utils.get_args_raw(message)
        if args:
            provider = args.lower()  # Получаем аргумент и приводим к нижнему регистру
            if provider in ("zetta", "devj"):
                self.provider = provider
                await message.edit(f"✅ Провайдер API изменен на {provider}")
            else:
                await message.edit("🚫 Недопустимый провайдер API. Доступные: zetta, devj")
        else:
            await message.edit("🤔 Укажите провайдер API: zetta или devj")

    @loader.unrestricted
    async def aicreatecmd(self, message):
        """
        Попросить AI помощника  для  Hikka написать модуль.
        Использование: `.aicreate <запрос>` или ответить на сообщение с `.aicreate` """
        r = "create"
        await self.process_request(message, self.module_instructions, r)

    @loader.unrestricted
    async def ultramodecmd(self, message):
        """
        Вкл/выкл качественного ответа для aisup
        Использование: `.ultramode <on/off>`
        
        """
        args = utils.get_args_raw(message)
        if args:
            metod = args.lower()
            if metod in ("on", "off"):
                self.metod = metod
                if metod == 'on':
                    await message.edit(f"📚 Качественный ответ включен. Скорость ответа aisup меньше.")
                elif metod == 'off':
                    await message.edit(f"🏃‍♂️‍➡️ Качественный ответ выключен. Скорость ответа aisup быстрее")
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
        if message.voice:
            request_text = await self.handle_voice_message(message)
        else:

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
    
    @loader.unrestricted
    async def clearcmd(self, message):
        """
        Сбрасывает историю диалога.
        Использование: `.clear`
        """
        chat_id = str(message.chat_id)
        if chat_id in self.chat_history or chat_id in self.chat_archive:
            self.chat_history.pop(chat_id, None)
            self.chat_archive.pop(chat_id, None)
            self.db.set("AIModule", "chat_history", self.chat_history)
            self.db.set("AIModule", "chat_archive", self.chat_archive)
            await message.edit("🗑️ <b>История диалога очищена.</b>")
        else:
            await message.edit("📭️ <b>История диалога пуста.</b>")
    
    @loader.unrestricted
    async def rolecmd(self, message):
        """
        Устанавливает роль для ИИ в режиме чата.
        Использование: `.role <роль>`
        """
        chat_id = str(message.chat_id)
        args = utils.get_args_raw(message)
        if not args:
            await message.edit("🎭 <b>Укажите роль для ИИ.</b>")
            return

        self.role[chat_id] = args
        self.db.set("AIModule", "role", self.role)
        await message.edit(f"🎭 <b>Роль ИИ установлена:</b> {args}")

    @loader.unrestricted
    async def modecmd(self, message):
        """
        Устанавливает режим ответа ИИ.
        Использование: `.mode <reply/all>`
        """
        chat_id = str(message.chat_id)
        args = utils.get_args_raw(message)
        if not args or args not in ("reply", "all"):
            await message.edit("🤔 <b>Укажите режим ответа: reply или all.</b>")
            return

        self.response_mode[chat_id] = args
        self.db.set("AIModule", "response_mode", self.response_mode)
        await message.edit(f"✅ <b>Режим ответа установлен на:</b> {args}")

    @loader.unrestricted
    async def createpersonacmd(self, message):
        """
        Создает новую личность.
        Использование: `.createpersona <имя> <роль>`
        """
        args = utils.get_args_raw(message)
        if not args:
            await message.edit("🤔 <b>Укажите имя и роль для личности.</b>")
            return

        try:
            name, role = args.split(" ", 1)
        except ValueError:
            await message.edit("🤔 <b>Неверный формат. Используйте: .createpersona <имя> <роль></b>")
            return

        # Изменено: chat_id заменен на 'global'
        if 'global' not in personas:
            personas['global'] = {}
        personas['global'][name] = role
        save_personas(personas)  # Сохраняем изменения в файл
        await message.edit(f"✅ <b>Личность {name} создана.</b>")

    @loader.unrestricted
    async def personascmd(self, message):
        """
        Показывает список личностей.
        Использование: `.personas`
        """
        # Изменено: chat_id заменен на 'global'
        if 'global' not in personas or not personas['global']:
            await message.edit("🤔 <b>Список личностей пуст.</b>")
            return

        persona_list = "\n".join([f"<b>{name}:</b> {role}" for name, role in personas['global'].items()])
        await message.edit(f"📝 <b>Доступные личности:</b>\n{persona_list}\n\nА в нашем боте, есть модель o1-preview с стримингом рассуждений. на заметку)")

    @loader.unrestricted
    async def switchpersonacmd(self, message):
        """
        Переключается на указанную личность.
        Использование: `.switchpersona <имя>`
        """
        args = utils.get_args_raw(message)
        if not args:
            await message.edit("🤔 <b>Укажите имя личности.</b>")
            return

        # Изменено: chat_id заменен на 'global'
        if 'global' not in personas or args not in personas['global']:
            await message.edit("🚫 <b>Личность не найдена.</b>")
            return

        chat_id = str(message.chat_id)
        self.role[chat_id] = personas['global'][args]
        await message.edit(f"✅ <b>Переключено на личность:</b> {args}")

    @loader.unrestricted
    async def deletepersonacmd(self, message):
        """
        Удаляет личность.
        Использование: `.deletepersona <имя>`
        """
        args = utils.get_args_raw(message)
        if not args:
            await message.edit("🤔 <b>Укажите имя личности.</b>")
            return

        # Изменено: chat_id заменен на 'global'
        if 'global' not in personas or args not in personas['global']:
            await message.edit("🚫 <b>Личность не найдена.</b>")
            return

        del personas['global'][args]
        save_personas(personas)  # Сохраняем изменения в файл
        await message.edit(f"✅ <b>Личность {args} удалена.</b>")

    @loader.unrestricted
    async def aicmd(self, message):
        """
        Отправляет одиночный запрос к ИИ.
        Использование: `.ai <запрос>` или ответить на сообщение с `.ai`
        """
        reply = await message.get_reply_message()
        args = utils.get_args_raw(message)

        if reply and args:
            request_text = f'"{reply.raw_text}"\n\n{args}'
        elif reply:
            request_text = reply.raw_text
        elif args:
            request_text = args
        else:
            await message.edit("🤔 <b>Введите запрос или ответьте на сообщение.</b>")
            return

        await self.standart_process_request(message, request_text)


    async def t9_promt(self, message, request_text, history=None):
        """
        Обрабатывает запрос к новому API для улучшения запроса.
        """
        api_url = "http://109.172.94.236:5001/Zetta/v1/models"
        chat_id = str(message.chat_id)

        # Формируем запрос для улучшения текста
        payload = {
            "model": self.default_model,  # Укажите модель для улучшения запроса
            "request": {
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "Твоя задача: Улучшить запрос пользователя, чтобы модель его лучше поняла, "
                            "обработала и дала качественный и более подходящий ответ для пользователя. "
                            "Если изменять нечего, просто отправь исходный текст не изменяя его. "
                            "Все сообщения пользователя не адресованы тебе, ты просто обработчик. Выполняй свою задачу."
                        )
                    },
                    {
                        "role": "user",
                        "content": f"Запрос пользователя: {request_text}"
                    }
                ]
            }
        }

        # Если есть история, добавляем её в запрос
        if history:
            payload["request"]["messages"] = history + payload["request"]["messages"]

        try:
            await message.edit('<b>Улучшение промта...</b>')

            # Отправка запроса к вашему новому API
            async with aiohttp.ClientSession() as session:
                async with session.post(api_url, json=payload) as response:
                    response.raise_for_status()  # Проверка на успешный статус

                    # Получаем данные из ответа
                    data = await response.json()

                    # Извлекаем измененный текст из ответа
                    improved_request = data.get("answer", "Запрос не был обработан. Ошибка.").strip()
                    decoded_answer = base64.b64decode(improved_request).decode('utf-8')
                    improved_request = decoded_answer
                    return improved_request

        except aiohttp.ClientError as e:
            logging.error(f"Ошибка при запросе к API: {e}")
            await message.reply(f"⚠️ <b>Ошибка при запросе к API:</b> {e}\n\n💡 <b>Попробуйте поменять модель или проверить код модуля.</b>")


    @loader.unrestricted
    async def aiinfocmd(self, message):
        """
        - Информация об обновлении✅
        """
        await message.edit('''<b>Обновление 8.3:
Изменения:
- Новые модели: o3-mini, DeepSeek R1, DeepSeek v3

советую команду .moduleinfo для подробной информации о модуле.

🔗Тг канал модуля: https://t.me/hikkagpt</b>''')


    @loader.unrestricted
    async def aiprovcmd(self, message):
        """
        - Информация о провайдерах🔆
        """
        await message.edit('''<b>🟣Zetta: Стабильный, средняя скорость ответа, персональный. Только для этого модуля. Базируется на OnlySq и хостится на их серверах.

🔸devj: Быстрая скорость ответа, Не стабилен из за разного возврата ответа от сервера.</b>''')
    
    
    async def standart_process_request(self, message, request_text):
        """
        Обрабатывает запрос к API модели ИИ.
        """
        api_url = "http://109.172.94.236:5001/Zetta/v1/models"
        chat_id = str(message.chat_id)

        # Если включено улучшение запроса
        if self.edit_promt == "on":
            request_text = await self.t9_promt(message, request_text)

        # Формируем payload для запроса в другой API
        payload = {
            "model": self.default_model,
            "request": {
                "messages": [
                    {
                        "role": "user",
                        "content": request_text
                    }
                ]
            }
        }

        try:
            # Редактируем сообщение, чтобы информировать пользователя о процессе
            await message.edit("🤔 <b>Думаю...</b>")

            # Отправляем запрос в ваше новое API, которое передаст его дальше
            async with aiohttp.ClientSession() as session:
                async with session.post(api_url, json=payload) as response:
                    response.raise_for_status()  # Проверка на успешный статус

                    # Получаем данные из ответа
                    data = await response.json()
                    answer = data.get("answer", "🚫 <b>Ответ не получен.</b>").strip()
                    decoded_answer = base64.b64decode(answer).decode('utf-8')
                    answer = decoded_answer

                    # Форматируем ответ в зависимости от состояния запроса
                    if self.edit_promt == "on":
                        formatted_answer = f"❔ <b>Улучшенный запрос с помощью ИИ:</b>\n`{request_text}`\n\n💡 <b>Ответ модели {self.default_model}:</b>\n{answer}"
                    else:
                        formatted_answer = f"❔ <b>Запрос:</b>\n`{request_text}`\n\n💡 <b>Ответ модели {self.default_model}:</b>\n{answer}"

                    # Отправляем отформатированный ответ пользователю
                    await message.edit(formatted_answer)

        except aiohttp.ClientError as e:
            # Обработка ошибок в случае проблем с запросом
            await message.edit(f"⚠️ <b>Ошибка при запросе к API:</b> {e}\n\n💡 <b>Попробуйте поменять модель или проверить код модуля.</b>")

    @loader.unrestricted
    async def humanmodecmd(self, message):
        """
        Вкл/выкл улучшения вашего промта
        Использование: `.humanmode <on/off>`
        
        """
        args = utils.get_args_raw(message)
        if args:
            humanmode = args.lower()
            if humanmode in ("on", "off"):
                self.humanmode = humanmode
                if humanmode == 'on':
                    await message.edit(f"💫 <b>Отображение 'Ответ модели ...' отключено в режиме чата.\n\nОтветы ИИ будут отправляться без лишнего текста, буд то это написали вы.</b>")
                elif humanmode == 'off':
                    await message.edit(f"💬 <b>Пометка 'Ответ модели ...' включена. \n\nОтветы ИИ будут отправляться с указанием что это написала модель ИИ.</b>")
            else:
                await message.edit("🚫 Неправильные аргументы. Доступные: on, off")
        else:
            await message.edit("🤔 Укажите аргументы: on или off")

    @loader.unrestricted
    async def superpromtcmd(self, message):
        """
        Вкл/выкл улучшения вашего промта
        Использование: `.superpromt <on/off>`
        
        """
        args = utils.get_args_raw(message)
        if args:
            edit_promt = args.lower()
            if edit_promt in ("on", "off"):
                self.edit_promt = edit_promt
                if edit_promt == 'on':
                    await message.edit(f"💫 <b>Улучшение вашего промта включено.\n\nПолезно для тех, кто не умеет правильно задавать промт или нету на это времени.</b>")
                elif edit_promt == 'off':
                    await message.edit(f"💬 <b>Улучшение вашего промта выключено</b>")
            else:
                await message.edit("🚫 Неправильные аргументы. Доступные: on, off")
        else:
            await message.edit("🤔 Укажите аргументы: on или off")

    @loader.unrestricted
    async def watcher(self, message):
        """
        Следит за сообщениями и отвечает, если активен режим чата.
        """
        chat_id = str(message.chat_id)
        if self.active_chats.get(chat_id):
            if self.response_mode.get(chat_id, "all") == "reply" and \
               not (message.is_reply and await self.is_reply_to_bot(message)):
                return

            if message.voice:
                request_text = await self.handle_voice_message(message)
                user_name = await self.get_user_name(message)
                await self.respond_to_message(message, user_name, request_text) 
            elif message.text:
                request_text = message.text.strip()
                user_name = await self.get_user_name(message)
                await self.respond_to_message(message, user_name, request_text)
                    
    
    async def is_reply_to_bot(self, message):
        """
        Проверяет, является ли сообщение ответом на сообщение бота.
        """
        if message.is_reply:
            reply_to_message = await message.get_reply_message()
            if reply_to_message and reply_to_message.sender_id == (await self.client.get_me()).id:
                return True
        return False





    async def get_user_name(self, message):
        """
        Возвращает имя пользователя из сообщения.
        """
        if message.sender:
            user = await self.client.get_entity(message.sender_id)
            return user.first_name or user.username
        else:
            return "Аноним"  # Или другой вариант по умолчанию

    async def respond_to_message(self, message, user_name, question):  # Изменено: добавлен аргумент user_name
        """
        Обрабатывает вопрос и отправляет ответ с учетом истории.
        """
        chat_id = str(message.chat_id)

        if chat_id not in self.chat_history:
            self.chat_history[chat_id] = []

        # Сохраняем имя пользователя и сообщение в историю
        self.chat_history[chat_id].append({
            "role": "user",
            "content": f"{user_name} написал: {question}"
        })

        if len(self.chat_history[chat_id]) > 1000:
            self.chat_history[chat_id] = self.chat_history[chat_id][-1000:]

        # --- Добавлено: ---
        if self.edit_promt == "on":
            # Вызов функции t9_promt для улучшения запроса
            request_text = await self.t9_promt(message, question, self.chat_history[chat_id])
            question = request_text
        # --- Конец добавления ---
            
        self.chat_history[chat_id][-1]["content"] = f"{user_name} написал: {question}"

        api_url = "http://109.172.94.236:5001/Zetta/v1/models"
        payload = {
            "model": self.default_model,
            "request": {
                "messages": [
                    {"role": "system", "content": self.role.get(chat_id, "")}
                ] + self.chat_history[chat_id]
            }
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(api_url, json=payload) as response:
                    response.raise_for_status()  # Проверка на успешный статус

                    # Получаем данные из ответа
                    data = await response.json()
                    answer = data.get("answer", "🚫 <b>Ответ не получен.</b>").strip()
                    decoded_answer = base64.b64decode(answer).decode('utf-8')
                    answer = decoded_answer

                    # Добавляем ответ в историю чата
                    self.chat_history[chat_id].append({
                        "role": "assistant",
                        "content": answer
                    })
                    # Сохраняем обновленную историю
                    self.db.set("AIModule", "chat_history", self.chat_history)

                    # Отправка ответа пользователю
                    if self.humanmode == 'off':
                        await message.reply(f"<b>Ответ модели {self.default_model}:</b>\n{answer}")

                    else:
                        await message.reply(answer)

        except aiohttp.ClientError as e:
            await message.reply(f"⚠️ <b>Ошибка при запросе к API:</b> {e}\n\n💡 <b>Попробуйте поменять модель или проверить код модуля.</b>")

    @loader.unrestricted
    async def rewritecmd(self, message):
        """Переписывает текст по инструкции. Использование: .rewrite <инструкция>"""
        # Получаем инструкцию пользователя после команды
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "<b>Пожалуйста, укажите инструкцию для переписывания.</b>")
            return

        # Проверяем, есть ли сообщение, на которое пользователь ответил
        if not message.is_reply:
            await utils.answer(message, "<b>Пожалуйста, ответьте на сообщение, которое нужно переписать.</b>")
            return

        # Получаем текст из сообщения, на которое пользователь ответил
        reply_message = await message.get_reply_message()
        original_text = reply_message.text

        if not original_text:
            await utils.answer(message, "<b>Не найден текст для переписывания.</b>")
            return

        instruction = args
        api_url = "http://109.172.94.236:5001/Zetta/v1/models"
        payload = {
            "model": self.default_model,
            "request": {
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "Ты — помощник для переписывания текста. "
                            "Твоя задача — переписывать текст по указанной пользователем инструкции, "
                            "отвечать четко и по делу, не выходя за рамки своей задачи. "
                            "Не используй Latex или особое форматирование, сохраняй текст простым и доступным."
                        )
                    },
                    {
                        "role": "user",
                        "content": f"{instruction}: {original_text}"
                    }
                ]
            }
        }

        try:
            # Редактируем сообщение, чтобы информировать пользователя о процессе
            await message.edit('<b>💭Переписываю..</b>')

            # Отправляем запрос в ваше новое API
            async with aiohttp.ClientSession() as session:
                async with session.post(api_url, json=payload) as response:
                    response.raise_for_status()  # Проверка на успешный статус

                    # Получаем данные из ответа
                    data = await response.json()

                    # Проверяем наличие ответа
                    rewritten_text = data.get("answer", "🚫 <b>Ответ не получен.</b>").strip()
                    decoded_answer = base64.b64decode(rewritten_text).decode('utf-8')
                    rewritten_text = decoded_answer

                    # Форматируем ответ в зависимости от состояния запроса
                    formatted_answer = f"✏️ <b>Переписанный текст моделью {self.default_model}:</b>\n{rewritten_text}"

                    # Отправляем отформатированный ответ пользователю
                    await message.edit(formatted_answer)

        except aiohttp.ClientError as e:
            # В случае ошибки отправляем соответствующее сообщение
            logging.error(f"Ошибка при запросе к API: {e}")
            await message.edit(f"⚠️ <b>Ошибка при запросе к API:</b> {e}")
        except Exception as e:
            # Обработка других ошибок
            logging.error(f"Неожиданная ошибка: {e}")
            await message.edit(f"⚠️ <b>Произошла ошибка:</b> {e}")

    
    @loader.unrestricted
    async def moduleinfocmd(self, message):  # Changed command name
        """
        Дополнительная информация о модуле и других проектах.
        """
        info_text = """
        <b>💡 Дополнительная информация</b>

<b>📌 Автор:</b>@procot1  
🌐 <b>Модуль является частью экосистемы Zetta - AI models.</b>  
📖 Весь его потенциал можно раскрыть с помощью бота: <a href="https://t.me/gpt4o_freetouse_bot">@gpt4o_freetouse_bot</a>.  

---

<b>🔥 Особенности модуля:</b>  
💼 <i>Объединён функционал 3 разных модулей!</i>  
Это делает его <b>универсальным</b>, <b>практичным</b> и <b>удобным</b>.  
<b>Все лучшие разработки собраны в одном месте.</b>

---

<b>🎯 Возможности модуля:</b>  
1️⃣ <b>Поиск как в Google.</b>  
Используйте модуль для <i>быстрого и точного</i> поиска информации.  

2️⃣ <b>Чат с моделью ИИ.</b>  
- Запускайте диалог в любом чате.  
- ИИ различает участников беседы благодаря передаче <i>ников</i>.  
- Модель может стать полноценным <i>участником ваших обсуждений.</i>  

3️⃣ <b>Создание личностей.</b>  
- Задайте временную роль для модели в чате.  
- Создайте <i>постоянную личность</i> с функцией сохранения ролей.  
- Используйте команду <code>.switchpersona</code> для <i>мгновенного переключения</i> ролей.  

4️⃣ <b>Выбор до 21 моделей ИИ.</b>  
Настраивайте работу с различными моделями под ваши задачи.  

5️⃣ <b>Запросы для Hikka Userbot.</b>  
- Команды <code>aisup</code>/<code>aicreate</code>/<code>aierror</code> помогут:  
    🔹 Узнать любую информацию про Hikka Userbot.  
    🔹 Решить проблему Hikka Userbot
    🔹 Создать или улучшить модуль для Hikka Userbot  

6️⃣ <b>Переписывание текстов (<code>.rewrite</code>):</b>  
- Эффективный перевод.  
- Стилизация текста.  
- Упрощение сложных формулировок.  

---

<b>💡 Почему этот модуль уникален?</b>  
Функционал модуля <i>огромен.</i>  
Освоив его, вы сможете использовать возможности ИИ на <b>максимум.</b>

---

📢 <b>Не упустите важное!</b>  
🔗 Подписывайтесь на канал: <a href="https://t.me/hikkagpt">@hikkagpt</a>  

✨ <b>Раскройте весь потенциал Zetta - AI models уже сегодня!</b>


        """
        await message.edit(info_text)
