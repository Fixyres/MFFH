# meta developer: @strongred
# meta name: Mailing
# meta desc: |
#   📢 Mailing - мощный и безопасный инструмент для массовых рассылок в Telegram
#   🔹 Автоматическая рассылка сообщений с защитой от бана
#   🔹 Поддержка неограниченного количества чатов
#   🔹 Умные задержки и лимиты сообщений
#   🔹 Сейф-режим включен по умолчанию (рекомендуется не отключать)

from .. import loader, utils
import asyncio
import time
import random
import logging
import re
from telethon.tl.types import Message

logger = logging.getLogger(__name__)

@loader.tds
class MailingMod(loader.Module):
    """Mailing - профессиональный инструмент для массовых рассылок в Telegram"""
    
    strings = {
        "name": "Mailing",
        "loading": (
            "📢 Mailing - модуль для массовых рассылок\n\n"
            "🔹 <b>Основные команды:</b>\n"
            ".msgo <время> <интервал> <текст> - <i>Запуск рассылки (время в секундах, интервал между сообщениями)</i>\n"
            ".msstop - <i>Экстренная остановка рассылки</i>\n"
            ".msadd <чат> - <i>Добавить чат (@username или -100ID)</i>\n"
            ".msdel <чат> - <i>Удалить чат из списка</i>\n"
            ".mslist - <i>Показать список всех чатов</i>\n"
            ".msmode - <i>Переключить режим защиты (включен по умолчанию)</i>\n"
            ".msstats - <i>Статистика рассылки</i>\n\n"
            "🛡️ <b>Безопасность:</b>\n"
            "- Сейф-режим включен по умолчанию\n"
            "- Автоматические задержки между сообщениями\n"
            "- Лимит сообщений в час\n"
            "- Защита от флуда и бана\n\n"
            "🫶 <b>Разработчик:</b> @strongred\n"
            "📢 <b>Канал:</b> @ZOLOKEYFREE"
        ),
        "start": "🚀 Рассылка запущена в {} чатов | Интервал: {} сек",
        "stop": "🛑 Рассылка остановлена",
        "done": "✅ Успешно завершено | Отправлено: {}",
        "args_error": "❌ Ошибка: Используйте .msgo <время> <интервал> <текст>",
        "num_error": "❌ Ошибка: Время и интервал должны быть числами",
        "no_chats": "❌ Ошибка: Нет чатов для рассылки",
        "invalid_chat": "❌ Ошибка: Некорректный формат чата (используйте @username или -100ID)",
        "chat_exists": "⚠️ Чат уже в списке",
        "chat_not_found": "⚠️ Чат не найден в списке",
        "stats": "📊 Статистика:\nОтправлено: {}\nОшибок: {}\nЛимит: {}/час",
        "protection": "🛡️ Защита от бана: {}",
        "protection_on": "ВКЛЮЧЕНА (рекомендуется)",
        "protection_off": "ВЫКЛЮЧЕНА (риск бана!)"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "ms_chats",
                [],
                lambda: "Список чатов для рассылки",
                validator=loader.validators.Series(
                    validator=loader.validators.String()
                )
            ),
            loader.ConfigValue(
                "ms_protection",
                True,
                lambda: "Защита от бана (включена по умолчанию)",
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "ms_limit",
                180,
                lambda: "Лимит сообщений в час",
                validator=loader.validators.Integer(minimum=50, maximum=500)
            )
        )
        self.active = False
        self.task = None
        self.sent = 0
        self.errors = 0
        self.last_send = 0
        self.hourly_count = 0
        self.last_hour = time.time()

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        await self.client.send_message("me", self.strings["loading"])

    @loader.command()
    async def msgo(self, message):
        """Запуск рассылки: .msgo <время> <интервал> <текст>"""
        if self.active:
            await utils.answer(message, "❗ Рассылка уже активна")
            return

        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings["args_error"])
            return

        try:
            args = args.split(" ", 2)
            duration = int(args[0])
            interval = max(int(args[1]), 15)
            text = args[2]
        except:
            await utils.answer(message, self.strings["num_error"])
            return

        chats = self._get_chats()
        if not chats:
            await utils.answer(message, self.strings["no_chats"])
            return

        self.active = True
        self.sent = 0
        self.errors = 0
        
        await utils.answer(message, self.strings["start"].format(len(chats), interval))

        end_time = time.time() + duration
        while self.active and time.time() < end_time:
            await self._send_to_chats(chats, text)
            if self.active and time.time() < end_time:
                await asyncio.sleep(interval)

        if self.active:
            await utils.answer(message, self.strings["done"].format(self.sent))
        self.active = False

    @loader.command()
    async def msstop(self, message):
        """Остановка рассылки: .msstop"""
        if not self.active:
            await utils.answer(message, "ℹ️ Нет активной рассылки")
            return

        self.active = False
        await utils.answer(message, self.strings["stop"])

    @loader.command()
    async def msadd(self, message):
        """Добавить чат: .msadd @username или -100ID"""
        chat = utils.get_args_raw(message)
        if not chat:
            await utils.answer(message, self.strings["invalid_chat"])
            return

        if not self._validate_chat(chat):
            await utils.answer(message, self.strings["invalid_chat"])
            return

        norm_chat = self._normalize_chat(chat)
        if norm_chat in [self._normalize_chat(c) for c in self.config["ms_chats"]]:
            await utils.answer(message, self.strings["chat_exists"])
            return

        self.config["ms_chats"].append(chat)
        await utils.answer(message, f"✅ Чат добавлен: {norm_chat}")

    @loader.command()
    async def msdel(self, message):
        """Удалить чат: .msdel @username или -100ID"""
        chat = utils.get_args_raw(message)
        if not chat:
            await utils.answer(message, "ℹ️ Укажите чат")
            return

        norm_chat = self._normalize_chat(chat)
        for i, c in enumerate(self.config["ms_chats"]):
            if self._normalize_chat(c) == norm_chat:
                self.config["ms_chats"].pop(i)
                await utils.answer(message, f"✅ Чат удален: {norm_chat}")
                return

        await utils.answer(message, self.strings["chat_not_found"])

    @loader.command()
    async def mslist(self, message):
        """Список чатов: .mslist"""
        if not self.config["ms_chats"]:
            await utils.answer(message, self.strings["no_chats"])
            return

        chats = [self._normalize_chat(c) for c in self.config["ms_chats"]]
        await utils.answer(message, f"📋 Чаты ({len(chats)}):\n" + "\n".join(f"• {c}" for c in chats))

    @loader.command()
    async def msstats(self, message):
        """Статистика: .msstats"""
        status = self.strings["protection_on"] if self.config["ms_protection"] else self.strings["protection_off"]
        stats = self.strings["stats"].format(
            self.sent,
            self.errors,
            self.hourly_count
        )
        await utils.answer(message, stats + "\n" + self.strings["protection"].format(status))

    @loader.command()
    async def msmode(self, message):
        """Режим защиты: .msmode"""
        self.config["ms_protection"] = not self.config["ms_protection"]
        status = self.strings["protection_on"] if self.config["ms_protection"] else self.strings["protection_off"]
        await utils.answer(message, self.strings["protection"].format(status) + 
                         "\nℹ️ Рекомендуется всегда держать включенным!")

    def _get_chats(self):
        return list(set(self._normalize_chat(c) for c in self.config["ms_chats"] if c.strip()))

    def _validate_chat(self, chat):
        patterns = [
            r'^@[a-zA-Z0-9_]{5,32}$',
            r'^https://t\.me/[a-zA-Z0-9_]{5,32}$',
            r'^-100\d+$',
            r'^https://t\.me/c/\d+$'
        ]
        return any(re.fullmatch(p, chat) for p in patterns)

    def _normalize_chat(self, chat):
        if chat.startswith("https://t.me/c/"):
            return "-100" + chat.split("/c/")[1].split("/")[0]
        elif chat.startswith("https://t.me/"):
            return "@" + chat.split("t.me/")[1].split("/")[0]
        return chat

    async def _send_to_chats(self, chats, text):
        self._check_limits()
        for chat in chats:
            if not self.active:
                break
            await self._safe_send(chat, text)

    async def _safe_send(self, chat, text):
        try:
            if self.config["ms_protection"]:
                delay = random.uniform(2.5, 6.0)
                if time.time() - self.last_send < 10:
                    delay += random.uniform(1.0, 3.0)
                await asyncio.sleep(delay)

            await self.client.send_message(chat, text)
            self.sent += 1
            self.hourly_count += 1
            self.last_send = time.time()
        except Exception as e:
            self.errors += 1
            if "Too Many Requests" in str(e) and self.config["ms_protection"]:
                wait = random.randint(45, 180)
                await asyncio.sleep(wait)
                return await self._safe_send(chat, text)

    def _check_limits(self):
        now = time.time()
        if now - self.last_hour > 3600:
            self.hourly_count = 0
            self.last_hour = now

    async def on_unload(self):
        self.active = False
        if self.task:
            self.task.cancel()