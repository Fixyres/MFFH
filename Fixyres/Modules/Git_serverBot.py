#      ███████╗  █████╗   ██████╗  ███╗   ███╗
#      ██╔════╝ ██╔══██╗ ██╔═══██╗ ████╗ ████║
#      ███████╗ ███████║ ██║   ██║ ██╔████╔██║
#      ╚════██║ ██╔══██║ ██║▄▄ ██║ ██║╚██╔╝██║
#      ███████║ ██║  ██║  ██████╔╝ ██║ ╚═╝ ██║

# meta developer: @Yaukais,@Shadow_red1

import requests
import asyncio
import aiohttp
import os
import subprocess
from .. import loader, utils
from hikkatl.types import Message
import time
import shutil  # Импортируем shutil для удаления директорий

@loader.tds
class GitServerBot(loader.Module):
    """Модуль для запуска ботов через GitHub!"""
    strings = {
        "name": "GitServerBot",
        "loader_Repo": "URL репозитория GitHub."
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "repo",
                "None",
                lambda: self.strings["loader_Repo"],
                validator=loader.validators.String(),
            ),
        )
        self.processes = {}

    async def pythoncmd(self, message: Message):
        """Запускает файл бота"""
        bot_file = message.text.strip().split(" ", 1)[1]
        repo_url = self.config.get("repo")

        if repo_url == "None":
            await message.reply("Репозиторий не указан в конфигурации.")
            return

        # Клонировать репозиторий (если еще не клонирован)
        if not os.path.exists("bot_repo"):
            subprocess.run(["git", "clone", repo_url, "bot_repo"])

        # Путь к файлу бота
        bot_path = os.path.join("bot_repo", bot_file)

        if os.path.exists(bot_path):
            self.processes[bot_file] = subprocess.Popen(["python3", bot_path])
            await message.reply(f"Бот {bot_file} запущен.")
        else:
            await message.reply("Файл бота не найден.")

    async def of_bcmd(self, message: Message):
        """Отключает файл бота"""
        bot_file = message.text.strip().split(" ", 1)[1]

        if bot_file in self.processes:
            self.processes[bot_file].terminate()
            del self.processes[bot_file]
            await message.reply(f"Бот {bot_file} остановлен.")
        else:
            await message.reply("Бот не запущен.")

    async def restart_bcmd(self, message: Message):
        """Перезапускает файл бота"""
        bot_file = message.text.strip().split(" ", 1)[1]

        if bot_file in self.processes:
            self.processes[bot_file].terminate()
            del self.processes[bot_file]

        await self.pythoncmd(message)

    async def bot_pingcmd(self, message: Message):
        """Показывает задержку бота"""
        start_time = time.time()
        await asyncio.sleep(0)  # Задержка для имитации работы бота
        ping = (time.time() - start_time) * 1000  # В миллисекундах
        await message.reply(f"Задержка бота: {ping:.2f} мс.")

    async def clear_datacmd(self, message: Message):
        """Удаляет все данные с сервера"""
        if os.path.exists("bot_repo"):
            shutil.rmtree("bot_repo")  # Удаляем директорию с репозиторием
            await message.reply("Все данные успешно удалены.")
        else:
            await message.reply("Данные не найдены.")