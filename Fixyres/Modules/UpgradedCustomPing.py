from hikkatl.types import Message
from .. import loader, utils
import time
import psutil
import os
import platform
import subprocess

"""
    Licensed under the GNU AGPLv3	
"""

# meta banner: https://i.ibb.co/wNDp6Sb/b3be3f0c-cb6a-4443-afaf-b569bb369401.jpg
# meta developer: Ksenon

@loader.tds
class UCustomPing(loader.Module):
    """Just upgraded custom ping."""

    strings = {
        "name": "UpgradedCustomPing",
        "configping": "Кастом текст, лол.\n"
        "Вы можете использовать плейсхолдеры:\n"
        "{prefix} - префикс команд\n"
        "{ping} - пинг\n"
        "{uptime} - аптайм\n"
        "{ram_used} - использованная RAM\n"
        "{ram_total} - общая RAM\n"
        "{disk_used} - использованная память\n"
        "{disk_total} - общая память\n"
        "{hikka_version} - версия Hikka\n"
        "{branch} - текущая ветка\n"
        "{cpu_info} - информация о процессоре\n"
        "{cpu_usage} - использование CPU\n"
        "{os_info} - информация об ОС",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "text",
                "<b><emoji document_id=5456140674028019486>⚡️</emoji> Пинг:</b> <code>{ping}</code> мс\n"
                "<b><emoji document_id=5244837092042750681>📈</emoji> Аптайм:</b> <code>{uptime}</code>\n"
                "<b><emoji document_id=5416117059207572332>➡️</emoji> Префикс:</b> <code>{prefix}</code>\n"
                "<b><emoji document_id=5217822164362739968>👑</emoji> RAM:</b> <code>{ram_used:.2f}GB | {ram_total:.2f}GB</code>\n"
                "<b><emoji document_id=5282843764451195532>🖥</emoji> Память:</b> <code>{disk_used:.2f}GB | {disk_total:.2f}GB</code>\n"
                "<b><emoji document_id=5438496463044752972>⭐️</emoji> Версия Hikka:</b> <code>{hikka_version}</code>\n"
                "<b><emoji document_id=5305265301917549162>📎</emoji> Ветка:</b> <code>{branch}</code>\n"
                "<b><emoji document_id=5341715473882955310>⚙️</emoji> Процессор:</b> <code>{cpu_info}</code>\n"
                "<b><emoji document_id=5424972470023104089>🔥</emoji> Использование CPU:</b> <code>{cpu_usage}%</code>\n"
                "<b><emoji document_id=5206607081334906820>✔️</emoji> ОС:</b> <code>{os_info}</code>",
                lambda: self.strings["configping"],
                validator=loader.validators.String(),
            ),
            loader.ConfigValue(
                "banner_url",
                "https://i.ibb.co/wNDp6Sb/b3be3f0c-cb6a-4443-afaf-b569bb369401.jpg",
                lambda: "URL баннера для команды ping",
                validator=loader.validators.Link(),
            ),
            loader.ConfigValue(
                "ceping_message",
                "<emoji document_id=5431449001532594346>⚡️</emoji> <b>Ping:</b>",
                lambda: "Тут вы можете изменить ответное сообщения команды",
            ),
            loader.ConfigValue(
                "custom_message",
                "<emoji document_id=5445284980978621387>🚀</emoji> <b>Uptime: {uptime}</b>",
                doc=lambda: "Модуль поддерживает значения {time} и {uptime}",
            ),
            loader.ConfigValue(
                "download",
                "<emoji document_id=5188377234380954537>🌘</emoji>",
                doc=lambda: "Модуль поддерживает значения {time} и {uptime}",
            ),
            loader.ConfigValue(
                "timezone",
                "3",
                lambda: "используйте 1, -1, -3 и т. д. для корректировки времени сервера на {time}.",
            ),
        )

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    def get_cpu_info(self):
        try:
            with open('/proc/cpuinfo', 'r') as f:
                for line in f:
                    if 'model name' in line:
                        return line.split(':')[1].strip()
        except:
            pass
        try:
            result = subprocess.check_output(['cat', '/proc/cpuinfo']).decode('utf-8')
            for line in result.split('\n'):
                if 'model name' in line:
                    return line.split(':')[1].strip()
        except:
            pass
        return platform.processor() or "Неизвестно"

    def _render_ping(self):
        import datetime
        offset = datetime.timedelta(hours=self.config["timezone"])
        tz = datetime.timezone(offset)
        time2 = datetime.datetime.now(tz)
        time = time2.strftime("%H:%M:%S")
        uptime = utils.formatted_uptime()
        return (
            self.config["custom_message"].format(
                time=time,
                uptime=uptime,
            )
            if self.config["custom_message"] != "no"
            else (f'🕷️ <b>Аптайм</b>: <b>{uptime}</b>')
        )

    @loader.command(
        ru_doc=" - Узнать пинг вашего юзербота",
    )
    async def cping(self, message: Message):
        """- Узнать пинг вашего юзербота"""
        ceping = self.config["ceping_message"]
        start = time.perf_counter_ns()
        download_config = self.config["download"]

        if isinstance(download_config, set):
            download_config = list(download_config)  # Преобразовать set в list
            message = await utils.answer(message, download_config)
        else:
            message = await utils.answer(message, download_config)

        try:
            ping_ms = round((time.perf_counter_ns() - start) / 10**6, 3)
            
            ram = psutil.virtual_memory()
            ram_used = ram.used / (1024 ** 3)
            ram_total = ram.total / (1024 ** 3)
            disk = psutil.disk_usage('/')
            disk_used = disk.used / (1024 ** 3)
            disk_total = disk.total / (1024 ** 3)
            hikka_version, branch = self.get_hikka_version()
            cpu_info = self.get_cpu_info()
            cpu_usage = psutil.cpu_percent(interval=1)
            os_info = f"{platform.system()} {platform.release()}"
            prefix = self.get_prefix()

            text = self.config["text"].format(
                prefix=prefix,
                ping=ping_ms,
                uptime=utils.formatted_uptime(),
                ram_used=ram_used,
                ram_total=ram_total,
                disk_used=disk_used,
                disk_total=disk_total,
                hikka_version=hikka_version,
                branch=branch,
                cpu_info=cpu_info,
                cpu_usage=cpu_usage,
                os_info=os_info,
            )

            banner = self.config["banner_url"]

            try:
                await self.client.send_file(message.chat_id, banner, caption=text)
                if message.out:
                    await message.delete()
            except Exception:
                await utils.answer(message, text)
        except TypeError:
            await utils.answer(
                message,
                "Неверное число в .config -> cenping -> timezone, пожалуйста, обновите его",
            )

    def get_prefix(self):
        """гет префикс."""
        return self.db.get("hikka.main", "command_prefix", ".")

    def get_hikka_version(self):
        """гет зе хикка бранч."""
        try:
            version_file = os.path.join(utils.get_base_dir(), "version.py")
            with open(version_file, "r") as f:
                content = f.read()
                version_tuple = eval(content.split("__version__ = ")[1].split("\n")[0])
                version = ".".join(map(str, version_tuple))

                try:
                    branch = content.split('branch = "')[1].split('"')[0]
                except Exception:
                    branch = "master"

                return version, branch
        except:
            return "Неизвестно", "Неизвестно"