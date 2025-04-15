__version__ = (1, 0, 0)
# meta developer: @psyhomodules

from hikkatl.types import Message
from .. import loader, utils
import subprocess
import logging
import os
import sys
from typing import Optional

logger = logging.getLogger(__name__)

@loader.tds
class BotHostMod(loader.Module):
    """🤖 Управление запуском ботов через команды"""

    strings = {
        "name": "BotHost",
        "no_file": "🚫 <b>Ответьте на файл с ботом</b>",
        "invalid_file": "🚫 <b>Неверный формат файла. Нужен .py файл</b>",
        "bot_started": "✅ <b>Бот успешно запущен!</b>\n\n📝 Логи:\n<code>{}</code>",
        "bot_stopped": "🛑 <b>Бот остановлен</b>",
        "bot_error": "❌ <b>Ошибка при запуске бота:</b>\n<code>{}</code>",
        "already_running": "⚠️ <b>Бот уже запущен</b>",
        "not_running": "⚠️ <b>Бот не запущен</b>",
        "status": "📊 <b>Статус бота:</b> {}\n📌 PID: {}"
    }

    def __init__(self):
        self.bot_process: Optional[subprocess.Popen] = None
        self.bot_file: Optional[str] = None
        self.config = loader.ModuleConfig(
            "log_lines", 5,
            "Количество строк логов для отображения"
        )

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    @loader.command(ru_doc="Запускает бота (ответом на файл)")
    async def boton(self, message: Message):
        """Запускает бота. Использование: .boton (ответом на файл)"""
        if self.bot_process and self.bot_process.poll() is None:
            await utils.answer(message, self.strings["already_running"])
            return

        reply = await message.get_reply_message()
        if not reply or not reply.file:
            await utils.answer(message, self.strings["no_file"])
            return

        if not reply.file.name.endswith('.py'):
            await utils.answer(message, self.strings["invalid_file"])
            return

        try:
            file_path = await reply.download_media()
            self.bot_file = file_path

            self.bot_process = subprocess.Popen(
                [sys.executable, file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )

            logs = []
            for _ in range(self.config["log_lines"]):
                if self.bot_process.stdout.readable():
                    line = self.bot_process.stdout.readline()
                    if line:
                        logs.append(line.strip())

            if self.bot_process.poll() is None:
                await utils.answer(
                    message,
                    self.strings["bot_started"].format(
                        "\n".join(logs) if logs else "🕐 Ожидание логов..."
                    )
                )
            else:
                error = self.bot_process.stderr.read()
                await utils.answer(
                    message,
                    self.strings["bot_error"].format(error or "🚫 Неизвестная ошибка")
                )
                self.bot_process = None

        except Exception as e:
            logger.error(f"Ошибка запуска бота: {e}")
            await utils.answer(
                message, 
                self.strings["bot_error"].format(str(e))
            )
            if self.bot_process:
                self.bot_process.kill()
                self.bot_process = None

    @loader.command(ru_doc="Останавливает бота")
    async def botoff(self, message: Message):
        """Останавливает бота. Использование: .botoff"""
        if not self.bot_process or self.bot_process.poll() is not None:
            await utils.answer(message, self.strings["not_running"])
            return

        try:
            self.bot_process.kill()
            self.bot_process = None
            if self.bot_file and os.path.exists(self.bot_file):
                os.remove(self.bot_file)
                self.bot_file = None
            await utils.answer(message, self.strings["bot_stopped"])
        except Exception as e:
            logger.error(f"Ошибка остановки бота: {e}")
            await utils.answer(
                message, 
                self.strings["bot_error"].format(str(e))
            )

    @loader.command(ru_doc="Показывает статус бота")
    async def botstatus(self, message: Message):
        """Показывает статус бота. Использование: .botstatus"""
        if not self.bot_process:
            status = "🔴 Не запущен"
            pid = "N/A"
        elif self.bot_process.poll() is None:
            status = "🟢 Запущен"
            pid = self.bot_process.pid
        else:
            status = "🔴 Остановлен"
            pid = "N/A"

        await utils.answer(
            message,
            self.strings["status"].format(status, pid)
        )
