"""
Some description:
fake/custom fetch for rofls 🙂
"""
# ИИшка кормит, больные мозги тоже
#
# meta developer: @HikkaZPM
#
# The module is made as a joke, all coincidences are random :P
#
#       кот вахуи
#       /\_____/\
#      /  o   o  \
#     ( ==  ^  == )
#      )         (
#     (           )
#    ( (  )   (  ) )
#   (__(__)___(__)__)
#
#
from .. import loader, utils
import asyncio
import logging
import aiohttp
import re

logger = logging.getLogger(__name__)

@loader.tds
class FakeNeofetchMod(loader.Module):
    """Имитация neofetch/fastfetch, канал с пресетами: https://t.me/+FQHkk51Cb7U2MTUy"""

    strings = {
        "name": "FFetch",
        "loading": "<b>Loading system information...</b>",
        "custom_host_reset": "<b>Custom host reset to default</b>",
        "prefix_char": "™",  # Символ для добавления перед первой строкой логотипа
    }

    strings_ru = {
        "name": "FFetch",
        "loading": "<b>Загрузка системной информации...</b>",
        "custom_host_reset": "<b>Кастомный хост сброшен до стандартного</b>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "os",
                "Arch Linux",
                doc="Кастомная ОС для отображения",
                validator=loader.validators.String(min_len=1, max_len=60)
            ),
            loader.ConfigValue(
                "hostname",
                "archbtw",
                doc="Кастомный хостнейм для отображения",
                validator=loader.validators.String(min_len=1, max_len=20)
            ),
            loader.ConfigValue(
                "user",
                "root",
                doc="Кастомное имя пользователя",
                validator=loader.validators.String(min_len=1, max_len=20),
            ),
            loader.ConfigValue(
                "kernel",
                "Linux 6.2.0-arch1",
                doc="Кастомный ядро для отображения",
                validator=loader.validators.String(min_len=1, max_len=20),
            ),
            loader.ConfigValue(
                "uptime",
                "69 days, 4 hours, 20 minutes",
                doc="Кастомное время работы для отображения",
                validator=loader.validators.String(min_len=1, max_len=50),
            ),
            loader.ConfigValue(
                "packages",
                1337,
                doc="Кастомные пакеты для отображения",
                validator=loader.validators.Integer(minimum=0, maximum=999999999),
            ),
            loader.ConfigValue(
                "cpu",
                "AMD Ryzen 9 7950X",
                doc="Кастомный процессор для отображения",
                validator=loader.validators.String(min_len=1, max_len=50),
            ),
            loader.ConfigValue(
                "ram",
                "64GB / 128GB",
                doc="Кастомная память для отображения",
                validator=loader.validators.String(min_len=1, max_len=50),
            ),
            loader.ConfigValue(
                "enable_delay",
                True,
                doc="Включить задержку перед выводом",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "delay",
                1.5,
                doc="Задержка перед выводом в секундах",
                validator=loader.validators.Float(minimum=0.0, maximum=999999999.0),
            ),
            loader.ConfigValue(
                "enable_logo",
                True,
                doc="Включить логотип для отображения",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "logo_style",
                "arch_small",
                doc="Стиль логотипа",
                validator=loader.validators.Choice([
                     "arch", "arch_small", "ubuntu", "ubuntu_small",
                     "debian", "debian_small", "fedora", "fedora_small",
                     "windows", "windows_8", "android", "android_small", "macos", "macos_small"
                ]),
            ),
            loader.ConfigValue(
                "custom_logo_url",
                "",
                doc="Кастомный URL логотипа",
                validator=loader.validators.String(),
            ),
        )

    async def client_ready(self, client, db):
        self._client = client
        self._db = db
        self._me = await client.get_me()

    async def get_logo(self):
        # Определяем URL для загрузки логотипа
        url = self.config["custom_logo_url"] or f"https://raw.githubusercontent.com/fastfetch-cli/fastfetch/dev/src/logo/ascii/{self.config['logo_style']}.txt"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=5) as response:
                    if response.status == 200:
                        logo_text = await response.text()
                        
                        cleaned_logo = re.sub(r'\$\d+', '', logo_text)
                        cleaned_lines = [line for line in cleaned_logo.splitlines() if line.strip()]
                        
                        if cleaned_lines:
                            if cleaned_lines[0].startswith(" "):
                                cleaned_lines[0] = self.strings["prefix_char"] + cleaned_lines[0][1:]
                            else:
                                cleaned_lines[0] = self.strings["prefix_char"] + cleaned_lines[0]
                        
                        return "\n".join(cleaned_lines)
                    return f"Ошибка загрузки: {response.status}"
        except Exception as e:
            logger.error(f"Error loading logo: {str(e)}")
            return f"Ошибка: {str(e)}"

    @loader.command(ru_doc="Показать фейковый neofetch с кастомным хостом")
    async def fneo(self, message):
        """Показывает фейковый вывод neofetch/fastfetch"""
        msg = await utils.answer(message, self.strings["loading"])

        if self.config["enable_delay"]:
            await asyncio.sleep(float(self.config['delay']))

        logo = ""
        if self.config["enable_logo"]:
            try:
                logo = await self.get_logo()
                logo += "\n\n"
            except Exception as e:
                logger.error(f"Error loading logo: {str(e)}")

        system_info = f"""
{logo}{self.config['user']}@{self.config['hostname']}
-----------------
OS: {self.config['os']}
Kernel: {self.config['kernel']}
Uptime: {self.config['uptime']}
Packages: {self.config['packages']}
CPU: {self.config['cpu']}
Memory: {self.config['ram']}"""

        output = f"<pre>{system_info}</pre>\n<b>Выполнено за {self.config['delay']} секунд.</b>"

        await utils.answer(msg, output)

    @loader.command(ru_doc="Сбросить все настройки до стандартных")
    async def resetneofetch(self, message):
        """Сбрасывает все настройки neofetch до стандартных"""
        self.config["os"] = "Arch Linux"
        self.config["hostname"] = "archbtw"
        self.config["user"] = "root"
        self.config["kernel"] = "Linux 6.2.0-arch1"
        self.config["uptime"] = "69 days, 4 hours, 20 minutes"
        self.config["packages"] = 1337
        self.config["cpu"] = "AMD Ryzen 9 7950X"
        self.config["ram"] = "64GB / 128GB"
        self.config["delay"] = 1.5
        
        await utils.answer(message, self.strings["custom_host_reset"])
