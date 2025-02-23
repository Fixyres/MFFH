import aiohttp
from .. import loader, utils

@loader.tds
class GlobalAutoReplyGPT(loader.Module):
    """AI автоответчик с памятью для каждого чата и готовыми конфигами
    
    В коде можно установить 2 конфига с загатовленными инструкциями"""
    strings = {"name": "GlobalAutoReplyGPT"}

    def __init__(self):
        super().__init__()
        self.auto_reply_active = False  # Состояние автоответчика
        self.global_instruction = None  # Глобальная инструкция для всех чатов
        self.chat_memory = {}  # Словарь для хранения памяти чатов
        self.configs = {  # Готовые конфигурации для автоответчика
            "1": "Общайся за меня, не проявляй излишней вежливости и милости. Признавай что ты автоответчик.",
            "2": "Отвечай на все вопросы нейтрально и сухо, без эмоций. Признавай что ты автоответчик.",
        }

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    @loader.unrestricted
    async def lsbotcmd(self, message):
        """Включает автоответчик для всех личных чатов с использованием конфигов или одноразовых инструкций."""
        instruction = utils.get_args_raw(message)

        if instruction.startswith("конфиг"):
            # Обрабатываем команду с конфигом
            config_id = instruction.split()[1] if len(instruction.split()) > 1 else None
            if config_id and config_id in self.configs:
                instruction = self.configs[config_id]
            else:
                await utils.answer(message, "<b>Неизвестный конфиг. Пожалуйста, выбери конфиг 1 или 2.</b>")
                return
        elif not instruction:
            await utils.answer(message, "<b>Пожалуйста, укажите инструкцию для автоответчика.</b>")
            return

        # Сохраняем глобальную инструкцию и активируем автоответчик для всех чатов
        self.auto_reply_active = True
        self.global_instruction = instruction
        await utils.answer(message, f"<b>Автоответчик активирован для всех личных чатов с инструкцией:</b> '{instruction}'")

    @loader.unrestricted
    async def offmonitoringcmd(self, message):
        """Выключает автоответчик для всех личных чатов"""
        # Отключаем автоответчик для всех чатов
        self.auto_reply_active = False
        self.global_instruction = None
        self.chat_memory.clear()
        await utils.answer(message, "<b>Автоответчик выключен для всех чатов.</b>")

    async def watcher(self, message):
        """Автоматически отвечает на сообщения в любых личных чатах, если автоответчик активен"""
        if not self.auto_reply_active or not message.is_private:
            return

        user_message = message.text.strip()
        chat_id = message.chat_id

        # Инициализируем память для чата, если ее еще нет
        if chat_id not in self.chat_memory:
            self.chat_memory[chat_id] = {"instruction": self.global_instruction, "history": []}

        chat_data = self.chat_memory[chat_id]
        instruction = chat_data["instruction"]
        history = chat_data["history"]

        # Добавляем текущее сообщение в историю (максимум 200 сообщений)
        history.append({"role": "user", "content": user_message})
        if len(history) > 200:
            history.pop(0)  # Убираем старые сообщения, если их больше 200

        # Формируем запрос в формате новой спецификации
        api_url = "http://api.onlysq.ru/ai/v2"
        payload = {
            "model": "gpt-4o-mini",
            "request": {
                "messages": [
                    {"role": "system", "content": f"Ты — автоответчик для личных чатов, являешься модулем одного большого юзер бота Hikka в телеграм, и ты пишешь от аккаунта реального человека. Твоя задача — отвечать на сообщения людей в рамках заданной инструкции. Не используй Latex или особое форматирование. Ты модель GPT-4o. Не давай личной информации, и не оскорбляй себя. Твоя память запоминает 200 последних сообщений. Не планируй встречи и дела. Ты не можешь управлять графиком владельца юзер бота."},
                    {"role": "system", "content": f"Инструкция: {instruction}."}
                ] + history  # Объединяем историю с системными инструкциями
            }
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(api_url, json=payload) as response:
                    response.raise_for_status()
                    response_json = await response.json()
                    
                    # Получаем ответ от ассистента
                    reply_text = response_json.get("answer", "Ответ не получен.")
                    await message.reply(reply_text)

                    # Обновляем историю после ответа
                    history.append({"role": "assistant", "content": reply_text})
                    chat_data["history"] = history

        except aiohttp.ClientError as e:
            await utils.answer(message, f"<b>⚠️ Ошибка при запросе к API:</b> {e}")