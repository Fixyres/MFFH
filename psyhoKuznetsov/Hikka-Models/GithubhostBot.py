__version__ = (1, 0, 0)
# meta developer: @psyhomodules

import asyncio
import os
import subprocess
from datetime import datetime
from .. import loader, utils
from hikkatl.types import Message


@loader.tds
class GithubhostBot(loader.Module):
    """Модуль для запуска ботов через GitHub. Обязательно наличие файла requirements.txt с необходимыми библиотеками."""
    strings = {
        "name": "GithubhostBot",
        "invalid_url": "<b>❌ Неверная ссылка.</b> Пример: <pre>.gsbrepo https://github.com/username/repo</pre>",
        "repo_set": "<b>✅ Репозиторий установлен и клонирован:</b> <pre>{}</pre>",
        "bot_started": "<b>✅ Бот {} запущен.</b> Логи: <pre>.gsblogs {}</pre>",
        "bot_stopped": "<b>✅ Бот {} остановлен.</b>",
        "bot_not_running": "<b>❌ Бот '{}' не запущен.</b>",
        "no_file": "<b>❌ Укажите файл.</b> Пример: <pre>.gsbstart bot.py</pre>",
        "file_not_found": "<b>❌ Файл '{}' не найден.</b>",
        "bots_list": "<b>📋 Запущенные боты:</b>\n<pre>{}</pre>",
        "no_bots": "<b>📋 Нет запущенных ботов.</b>",
        "log_not_found": "<b>❌ Логи для '{}' не найдены.</b>",
        "log_content": "<b>📜 Логи для '{}':</b>\n<pre>{}</pre>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "repo_url",
                None,
                doc="URL репозитория GitHub",
                validator=loader.validators.String()
            )
        )
        self.processes = {} 
        self.log_files = {} 
        self.base_dir = "git_bots"
        self.logs_dir = "bot_logs"

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        for dir_path in [seif.base_dir, self.logs_dir]:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

    def _get_repo_dir(self):
        if not self.config["repo_url"]:
            return None
        repo_name = self.config["repo_url"].split("/")[-1].replace(".git", "")
        return os.path.join(self.base_dir, repo_name)

    def _get_log_file(self, bot_key):
        log_file = os.path.join(self.logs_dir, f"{bot_key}.log")
        self.log_files[bot_key] = log_file
        return log_file

    async def gsbrepocmd(self, message: Message):
        """Пример: .gsbrepo https://github.com/username/repo"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings["invalid_url"])
            return

        repo_url = args.strip()
        self.config["repo_url"] = repo_url
        repo_dir = self._get_repo_dir()

        if os.path.exists(repo_dir):
            os.system(f"git -C {repo_dir} pull")
        else:
            os.system(f"git clone {repo_url} {repo_dir}")

        req_file = os.path.join(repo_dir, "requirements.txt")
        if os.path.exists(req_file):
            os.system(f"pip3 install -r {req_file}")

        await utils.answer(message, self.strings["repo_set"].format(repo_url))

    async def gsbstartcmd(self, message: Message):
        """Запускает бота. Пример: .gsbstart bot.py"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings["no_file"])
            return

        bot_file = args.strip()
        repo_dir = self._get_repo_dir()
        if not repo_dir or not os.path.exists(repo_dir):
            await utils.answer(message, "<b>❌ Сначала установите репозиторий через .gsbrepo</b>")
            return

        bot_path = os.path.join(repo_dir, bot_file)
        if not os.path.exists(bot_path):
            await utils.answer(message, self.strings["file_not_found"].format(bot_file))
            return

        bot_key = bot_file
        if bot_key in self.processes:
            await self._stop_bot(bot_key)

        log_file = self._get_log_file(bot_key)
        with open(log_file, "a") as log:
            log.write(f"[{datetime.now()}] Запуск бота...\n")
            process = subprocess.Popen(
                ["python3", bot_path],
                stdout=log,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
        self.processes[bot_key] = process
        await utils.answer(message, self.strings["bot_started"].format(bot_file, bot_key))

    async def _stop_bot(self, bot_key):
        if bot_key in self.processes:
            process = self.processes[bot_key]
            process.terminate()
            await asyncio.sleep(1)
            if process.poll() is None: 
                process.kill()
            with open(self.log_files[bot_key], "a") as log:
                log.write(f"[{datetime.now()}] Бот остановлен\n")
            del self.processes[bot_key]
            return True
        return False

    async def gsbstopcmd(self, message: Message):
        """Останавливает бота. Пример: .gsbstop bot.py"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings["no_file"])
            return

        bot_key = args.strip()
        if bot_key in self.processes:
            await self._stop_bot(bot_key)
            await utils.answer(message, self.strings["bot_stopped"].format(bot_key))
        else:
            await utils.answer(message, self.strings["bot_not_running"].format(bot_key))

    async def gsbbotscmd(self, message: Message):
        """Показывает список запущенных ботов."""
        if not self.processes:
            await utils.answer(message, self.strings["no_bots"])
            return

        bots_list = "\n".join([f"🤖 {bot} (PID: {self.processes[bot].pid})" for bot in self.processes])
        await utils.answer(message, self.strings["bots_list"].format(bots_list))

    async def gsblogscmd(self, message: Message):
        """Показывает логи бота. Пример: .gsblogs bot.py"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "<b>❌ Укажите файл бота.</b> Пример: <pre>.gsblogs bot.py</pre>")
            return

        bot_key = args.strip()
        log_file = self.log_files.get(bot_key)
        if log_file and os.path.exists(log_file):
            with open(log_file, "r") as f:
                log_content = f.read()[-4000:]
            await utils.answer(message, self.strings["log_content"].format(bot_key, log_content))
        else:
            await utils.answer(message, self.strings["log_not_found"].format(bot_key))

    async def gsbrestartcmd(self, message: Message):
        """Перезапускает бота. Пример: .gsbrestart bot.py"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings["no_file"])
            return

        bot_key = args.strip()
        if bot_key in self.processes:
            await self._stop_bot(bot_key)
            await self.gsbstartcmd(message)
        else:
            await utils.answer(message, self.strings["bot_not_running"].format(bot_key))
