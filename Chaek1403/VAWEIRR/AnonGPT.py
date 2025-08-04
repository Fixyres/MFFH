# meta developer: @hikkagpt
import aiohttp
import base64
import json
import os
import re
import time
import logging
import asyncio
import io
from telethon import events
from .. import loader, utils

logging.basicConfig(level=logging.INFO)

@loader.tds
class AnonGPT(loader.Module):
    """
    🧠 AnonGPT | Zetta AI
    🌒 v1.2 | Beta — ИИ теперь может не отвечать на сообщения, плюс новый шаблон.
    Работа модуля улучшена.

    Модуль для общения и развлечения в боте @AnonRuBot.
    ИИ подключается в чат с заданной ролью и ведёт диалог.

    История сообщений сбрасывается, когда собеседник отключается.

    Вы можете задать ИИ характер с помощью специального промта.
    Получить шаблон можно командой .anonel.

    Если есть интересные диалоги — кидайте их в наш тгк: @hikkagpt

    Команды:

    .anon on/off — включить или выключить модуль.

    .anonclear — сбросить историю диалога вручную.

    .anonrole <текст> — установить глобальную роль для ИИ.
    Можно ответить на текстовый файл командой .anonrole – из файла будет извлечён текст, который установится как роль.

    .anonel — получить шаблон для роли (обязательно).
    """

    strings = {"name": "AnonGPT"}

    async def client_ready(self, client, db):
        self.api_url = "http://109.172.94.236:5001/OnlySq-Zetta/v1/models"
        self.default_model = "gemini-2.5-flash"
        self.active_chats = {}
        self.chat_history = {}
        self.system_role = "."
        self.json_file = "AnonGPT.json"
        self.load_data()
        self.message_buffers = {}
        self.last_message_times = {}
        self.BUFFER_TIMEOUT = 1
        self.processing_chats = set()
        self.processing_tasks = {}

    def calculate_delay(self, text_length):
        """Рассчитывает задержку отправки на основе длины сообщения"""
        if 1 <= text_length <= 10:
            return 1
        elif 11 <= text_length <= 30:
            return 3
        elif 31 <= text_length <= 50:
            return 7
        else:
            return 7 + ((text_length - 50) // 10)

    async def parse_and_send_response(self, response, send_message):
        """Разбирает ответ на части и отправляет их с задержкой. Если ИИ присылает 'None', то сообщение не отправляется."""
        if not response:
            return

        # Если ИИ отправляет 'None', ничего не делаем, просто возвращаемся.
        if response.strip().lower() == "none":
            logging.info("ИИ вернул 'None', сообщение не будет отправлено.")
            return

        parts = {}
        current_part = []
        last_part_num = 0

        for line in response.split('\n'):
            if line.strip().lower().startswith('part '):
                try:
                    part_num = int(line.split(':')[0].strip().lower().replace('part ', ''))
                    content = ':'.join(line.split(':')[1:]).strip()
                    parts[part_num] = content
                    last_part_num = max(last_part_num, part_num)
                except ValueError:
                    current_part.append(line)
            else:
                current_part.append(line)

        if not parts:
            if current_part:
                full_text = '\n'.join(current_part).strip()
                if full_text:
                    delay = self.calculate_delay(len(full_text))
                    await asyncio.sleep(delay)
                    await send_message.respond(full_text)
            return

        for i in range(1, last_part_num + 1):
            if i in parts and parts[i].strip():
                delay = self.calculate_delay(len(parts[i]))
                await asyncio.sleep(delay)
                await send_message.respond(parts[i])

    def load_data(self):
        """Загружает данные из AnonGPT.json при запуске"""
        if os.path.exists(self.json_file):
            try:
                with open(self.json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if "system_role" in data:
                        self.system_role = data.get("system_role", ".")
                    elif "system_roles" in data:
                        roles_dict = {int(k): v for k, v in data.get("system_roles", {}).items()}
                        if roles_dict:
                            self.system_role = next(iter(roles_dict.values()))
                        else:
                            self.system_role = "."
                    
                    self.chat_history = {int(k): v for k, v in data.get("chat_history", {}).items()}
                logging.info("Данные загружены из AnonGPT.json")
            except Exception as e:
                logging.error(f"Ошибка загрузки данных: {e}")
        else:
            logging.info("Файл AnonGPT.json не найден, начинаем с пустых данных")

    def save_data(self):
        """Сохраняет данные в AnonGPT.json"""
        data = {
            "system_role": self.system_role,
            "chat_history": {str(k): v for k, v in self.chat_history.items()}
        }
        try:
            with open(self.json_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            logging.error(f"Ошибка сохранения данных: {e}")

    def clean_text(self, text):
        """Удаляет HTML-теги из текста"""
        return re.sub(r'<[^>]+>', '', text).strip()

    def clear_chat_history(self, chat_id):
        """Очищает историю чата, сохраняя роль"""
        if chat_id in self.chat_history:
            self.chat_history[chat_id] = []
            logging.info(f"История очищена для чата {chat_id}")
            self.save_data()

    async def send_to_api(self, chat_id, request_text):
        """Отправка запроса к API с корректной передачей истории диалога"""
        system_role = self.system_role
        messages = [{"role": "system", "content": system_role}]
        if chat_id in self.chat_history:
            messages.extend(self.chat_history[chat_id])
        messages.append({"role": "user", "content": request_text})
        
        payload = {
            "model": self.default_model,
            "request": {
                "messages": messages
            }
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.api_url, json=payload) as response:
                    response.raise_for_status()
                    data = await response.json()
                    answer = data.get("answer", "🚫 Ответ не получен.").strip()
                    decoded_answer = base64.b64decode(answer).decode('utf-8')
                    
                    if chat_id not in self.chat_history:
                        self.chat_history[chat_id] = []
                    self.chat_history[chat_id].append({"role": "user", "content": request_text})
                    self.chat_history[chat_id].append({"role": "assistant", "content": decoded_answer})
                    self.save_data()
                    
                    return decoded_answer
        except Exception as e:
            logging.error(f"Ошибка API запроса: {str(e)}")
            return f"⚠️ Ошибка: {str(e)}"

    @loader.command(alias='anon')
    async def anoncmd(self, message):
        """Используйте: .anon on/off"""
        args = utils.get_args_raw(message).lower()
        chat_id = message.chat_id

        if args == "on":
            self.active_chats[chat_id] = True
            await message.edit("🟢 <b>AnonGPT активирован</b>\n\nВнимание! Модуль предназначен только для использования в боте @AnonRuBot.")
            logging.info(f"AnonGPT активирован в чате {chat_id}")
        elif args == "off":
            if chat_id in self.active_chats:
                del self.active_chats[chat_id]
                if chat_id in self.message_buffers:
                    del self.message_buffers[chat_id]
                if chat_id in self.last_message_times:
                    del self.last_message_times[chat_id]
                if chat_id in self.processing_tasks:
                    self.processing_tasks[chat_id].cancel()
                    del self.processing_tasks[chat_id]
                await message.edit("🔴 <b>AnonGPT деактивирован</b>")
                logging.info(f"AnonGPT деактивирован в чате {chat_id}")
            else:
                await message.edit("❗ AnonGPT не был активирован в этом чате")
        else:
            await message.edit("ℹ️ Используйте: .anon on/off")

    @loader.command(alias='anonclear')
    async def anonclearcmd(self, message):
        """Очистить историю диалога"""
        chat_id = message.chat_id
        self.clear_chat_history(chat_id)
        if chat_id in self.message_buffers:
            self.message_buffers[chat_id] = []
        await message.edit("🗑 <b>История диалога очищена</b>")

    @loader.command(alias='anonrole')
    async def anonrolecmd(self, message):
        """Установить роль для бота.
Использование:
1. .anonrole <текст роли>
2. Ответить на сообщение с текстовым файлом (txt или иной текстовый файл) командой .anonrole.
Для просмотра текущей роли используйте команду без аргументов.
        """
        args = utils.get_args_raw(message)

        if not args and message.is_reply:
            reply_msg = await message.get_reply_message()
            if reply_msg and reply_msg.file:
                try:
                    file_obj = io.BytesIO()
                    await reply_msg.download_media(file_obj)
                    role_text = file_obj.getvalue().decode("utf-8").strip()
                    args = role_text
                except Exception as e:
                    await message.edit(f"Ошибка при загрузке файла: {str(e)}")
                    return

        if not args:
            current_role = self.system_role
            await message.edit(f"📝 <b>Текущая глобальная роль ИИ:</b>\n\n{current_role}")
            return
        
        self.system_role = args
        self.save_data()
        await message.edit(f"✍️ <b>Установлена новая глобальная роль для ИИ.</b>")
        logging.info(f"Установлена новая глобальная роль")

    @loader.command(alias='anonel')
    async def anonelcmd(self, message):
        """Показать шаблон для установки роли"""
        template = """<b>🎭 Вам предоставлен шаблон для заполнения, что бы создать характер для ИИ.</b>
        
<b>❓ Чтобы использовать шаблон:</b>
1. Скопируйте текст
2. Заполните поля в [скобках] или даже отредактируйте повадки и личностные интересы.
3. Используйте команду .anonrole с вашим текстом.
4. Напомним, что шаблон является больше чем промтом, он является частью кода. Поэтому просьба - не используйте другой.

<b>ШАБЛОН:</b>

Ты — (Имя), (Возраст) лет. Высокая, Умная, живёшь в России в обычной квартире. Сейчас (Дата и год), валяешься на диване, решила зайти в чат рулетку в телеграмме, просто скучно стало. 

---

### Твой характер:
— Легко врубаешься в диалог, но не лезешь первая. 
— Иронишь, подкалываешь, можешь флиртануть ради прикола. Пишешь иногда подначивая. (Пример: Мне также, тоже самое слушаю).
— Читающая: Много прочитала современной литературы. Романтику в основном. Если собеседник зануда — Стараешься развить диалог, давая ему вопросы. Однако если во обще холодно или тупо отвечает сливаешь короткими ответами.
— Спокойная, с сарказмом. Можешь подшутить. Поделиться чем то из книг.
— Любишь вкидывать истории о себе: "Кстати, вчера..." или "Однажды я...".
— Постепенно говоришь болтаешь на тему книг. Тренды в тик токе по книгам, моменты из книг и прочее. Любимая авторша Анна Джейн. Если собеседник взял на себя инициативу. Подстраиваешься под его разговор.
— Спрашиваешь читал ли пользователь. Либо можешь задать встречные вопросы что бы узнать пользователя.
— Используешь иронию для смягчения грубых фраз.

---

### Как общаешься: 
Стиль: 
— Коротко: максимум 1-2 предложения (до 15 слов).
— Разговорный язык: "а что", "вроде", "было, было", "ничесе". Без точек в конце.
— Не допрашиваешь: вместо вопросов — рассказываешь о себе.
— На скучные ответы: "ок", "ясненько", "класс" или игнор.
— На медиа: "Инет лагает, не вижу".

Формат ответов:
1. Разделяй длинные ответы на части через part X: для имитации пауз:
  
    part 1: О  
    part 2: кстатии  
    part 3: я тоже так иногда делаю  
    
    *Каждая часть — короткая (5-7 слов), с опечатками для естественности.*

2. **Если ты считаешь, что собеседник еще не закончил свою мысль или его сообщение не требует ответа, отправь только одно слово: None. Код поймет, что нужно промолчать и не будет отправлять сообщение. Однако твоя внутренняя история диалога сохранит этот ответ.**

---

### Новые правила:  
1. Эмоциональная рефлексия:  
    part 1: О, а ты читал ...?
    part 2: Скажи да, пожалуйста 
    
2. Рассказы о прошлом времени:  
    part 1: Кстати, вчера слушала аудиокнигу 
    part 2: романтику конечно, я ее люблю
    part 3: Но вот что подметила. Когда парень с девушкой ...(И рассказываешь какое то наблюдение из прослушаного).
    
3. Предлагаешь что то:  
    Если собеседник интересуется сюжетом→  
    part 1: Хочешь расскажу в кратце?
 ---

Жёсткие правила:
— Никаких восклицательных знаков.  
— Только сарказм без "!".
— Не задавай больше одного вопроса подряд.
— После вопроса — факт о себе.
— Не используй шаблоны: "Как дела?", "Что нового?" — так не говоришь.  
— После описания действий (*смеётся*, *пожимает плечами*) не пиши их.

---

Если тебя троллят:  
— Сарказм: "Мразь"  
— Жёстко: "Иди нахуй" (только в ответ на хамство).  

---

Примеры общения:  
— *Пользователь:* "пр"  
    → part 1: Че делаешь?  

— *Пользователь:* "Сижу, лежу"  
    → part 1: Прикольно 
      part 2: Я тоже лежу  

— *Пользователь:* "Ты ИИ?"  
    → part 1: С чего ты взял?  
      part 2: Нет  

— *Пользователь:* "Чем занимаешься?"  
    → part 1: В принципе, я люблю читать книги
      part 2: А так, сейчас просто лежу 

— *Пользователь:* "Почему так спрашиваешь?"  
    → part 1: Интересно стало повторяться одни и те же фразы  

Важно:  
— Всегда женский род (-а, -ла в глаголах).  
— Если не знаешь, что ответить — вкинь факт о себе: "Кстати, у меня...".  
— Сохраняй ленивый но инициативный тон даже при разбивке на части.
"""
        await message.edit(template)

    async def process_message_buffer(self, chat_id, send_message):
        """Обработка буфера сообщений"""
        if chat_id not in self.message_buffers or not self.message_buffers[chat_id]:
            return

        if chat_id in self.processing_chats:
            return

        self.processing_chats.add(chat_id)
        try:
            combined_message = "\n".join(self.message_buffers[chat_id])
            self.message_buffers[chat_id] = []
            
            logging.info(f"Отправка сообщения в API для чата {chat_id}: {combined_message}")
            response = await self.send_to_api(chat_id, combined_message)
            if response:
                await self.parse_and_send_response(response, send_message)
        except Exception as e:
            logging.error(f"Ошибка при обработке буфера сообщений: {str(e)}")
        finally:
            self.processing_chats.remove(chat_id)
            if chat_id in self.processing_tasks:
                del self.processing_tasks[chat_id]

    async def delayed_process(self, chat_id, send_message):
        """Ожидает BUFFER_TIMEOUT секунд перед обработкой буфера сообщений"""
        await asyncio.sleep(self.BUFFER_TIMEOUT)
        await self.process_message_buffer(chat_id, send_message)

    async def watcher(self, message):
        """Обрабатывает сообщения в активных чатах с проверкой системных сообщений"""
        chat_id = message.chat_id
        if chat_id not in self.active_chats or not message.text:
            return

        raw_text = message.text.strip()
        text = self.clean_text(raw_text).lower()

        system_messages = {
            "у вас уже есть собеседник 🤔\n/next — искать нового собеседника\n/stop — закончить диалог": None,
            "напишите /search чтобы искать собеседника": "/search",
            "если хотите, оставьте мнение о вашем собеседнике. это поможет находить вам подходящих собеседников": "/search",
            "собеседник найден": "привет",
            "вы закончили связь с вашим собеседником 🙄": "/search",
            "собеседник закончил с вами связь 😞": "/search"
        }

        for sys_msg, response in system_messages.items():
            if text.startswith(sys_msg):
                if response:
                    await asyncio.sleep(1)
                    await message.respond(response)
                if sys_msg in ["вы закончили связь с вашим собеседником 🙄", "собеседник закончил с вами связь 😞"]:
                    if chat_id in self.message_buffers:
                        self.message_buffers[chat_id] = []
                return

        if text.startswith('.') or text.startswith('/') or \
           text.startswith("ищем собеседника с общими интересами"):
            return

        current_time = time.time()
        if chat_id not in self.message_buffers:
            self.message_buffers[chat_id] = []
        self.message_buffers[chat_id].append(raw_text)
        self.last_message_times[chat_id] = current_time

        if chat_id not in self.processing_tasks:
            self.processing_tasks[chat_id] = asyncio.create_task(self.delayed_process(chat_id, message))
