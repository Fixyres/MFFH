# meta developer: @mwmodules
# meta desc: 🚀 Speed Test - Internet speed measurement module with multilanguage support (use .config SpeedTest language en/ru/uk to change language)
# by @mwmodules
# 🔒 Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# meta link: .dlm http://mwmodules.ftp.sh/speedtest.py

import asyncio
import aiohttp
import time
from datetime import datetime
from .. import loader, utils

@loader.tds
class SpeedTestMod(loader.Module):
    """🚀 Accurate internet speed measurement
    🚀 Точное измерение скорости интернета (для смены языка используйте .config SpeedTest language en/ru/uk)
    🚀 Точне вимірювання швидкості інтернету (для зміни мови використовуйте .config SpeedTest language en/ru/uk)"""

    strings = {
        "name": "SpeedTest",
        "_cls_doc": "Speed Test - Test your internet speed",
        
        "testing_en": "🔄 <b>Testing speed...</b>",
        "testing_ru": "🔄 <b>Тестирование скорости...</b>",
        "testing_uk": "🔄 <b>Тестування швидкості...</b>",

        "result_en": """<b>📊 Internet Speed Test:</b>

<b>📥 Download:</b> <code>{}</code>
<b>📤 Upload:</b> <code>{}</code>
<b>🕒 Ping:</b> <code>{}</code>

<b>🌐 Server:</b> <code>{}</code>
<b>📡 Provider:</b> <code>{}</code>

<b>⏳ Estimated download time:</b>
<b>📄 Photo (5 MB):</b> <code>{}</code>
<b>📱 App (100 MB):</b> <code>{}</code>
<b>🎥 HD Movie (2 GB):</b> <code>{}</code>
<b>🎮 Game (50 GB):</b> <code>{}</code>

<b>⌚️ Test took:</b> <code>{}</code>
<b>📅 Time:</b> <code>{}</code>""",

        "result_ru": """<b>📊 Тест скорости интернета:</b>

<b>📥 Загрузка:</b> <code>{}</code>
<b>📤 Отдача:</b> <code>{}</code>
<b>🕒 Пинг:</b> <code>{}</code>

<b>🌐 Сервер:</b> <code>{}</code>
<b>📡 Провайдер:</b> <code>{}</code>

<b>⏳ Расчетное время загрузки:</b>
<b>📄 Фото (5 МБ):</b> <code>{}</code>
<b>📱 Приложение (100 МБ):</b> <code>{}</code>
<b>🎥 Фильм HD (2 ГБ):</b> <code>{}</code>
<b>🎮 Игра (50 ГБ):</b> <code>{}</code>

<b>⌚️ Тест занял:</b> <code>{}</code>
<b>📅 Время:</b> <code>{}</code>""",

        "result_uk": """<b>📊 Тест швидкості інтернету:</b>

<b>📥 Завантаження:</b> <code>{}</code>
<b>📤 Віддача:</b> <code>{}</code>
<b>🕒 Пінг:</b> <code>{}</code>

<b>🌐 Сервер:</b> <code>{}</code>
<b>📡 Провайдер:</b> <code>{}</code>

<b>⏳ Розрахунковий час завантаження:</b>
<b>📄 Фото (5 МБ):</b> <code>{}</code>
<b>📱 Додаток (100 МБ):</b> <code>{}</code>
<b>🎥 Фільм HD (2 ГБ):</b> <code>{}</code>
<b>🎮 Гра (50 ГБ):</b> <code>{}</code>

<b>⌚️ Тест тривав:</b> <code>{}</code>
<b>📅 Час:</b> <code>{}</code>""",

        "error_en": "❌ <b>Test error:</b>\n<code>{}</code>",
        "error_ru": "❌ <b>Ошибка при тестировании:</b>\n<code>{}</code>",
        "error_uk": "❌ <b>Помилка тестування:</b>\n<code>{}</code>"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            "language", "en", "Module language (en, ru, uk)"
        )

    def format_speed(self, bytes_per_sec):
        if bytes_per_sec <= 0:
            return "0 Mbps"
            
        mbits = (bytes_per_sec * 8) / (1024 * 1024)
        
        if mbits < 1:
            return f"{mbits * 1000:.1f} Kbps"
        return f"{mbits:.1f} Mbps"

    def format_time(self, size_bytes, speed_bytes_per_sec):
        if speed_bytes_per_sec <= 0:
            return "∞"
        
        seconds = size_bytes / speed_bytes_per_sec
        
        if seconds < 1:
            return "< 1 sec"
            
        if seconds < 60:
            return f"{seconds:.0f} sec"
            
        minutes = seconds / 60
        if minutes < 60:
            return f"{minutes:.0f} min"
            
        hours = minutes / 60
        if hours < 24:
            return f"{hours:.1f} h"
            
        days = hours / 24
        return f"{days:.1f} d"

    async def download_test(self, session):
        urls = [
            "https://speed.cloudflare.com/__down?bytes=25000000",
            "https://speed.hetzner.de/100MB.bin",
            "https://cdn.speedcheck.org/tests/files/10mb.dat"
        ]
        speeds = []
        
        for url in urls:
            try:
                start = time.time()
                total = 0
                async with session.get(url) as response:
                    while True:
                        chunk = await response.content.read(8192)
                        if not chunk:
                            break
                        total += len(chunk)
                duration = time.time() - start
                if duration > 0:
                    speeds.append(total / duration)
            except:
                continue
                
        return max(speeds) if speeds else 0

    async def upload_test(self, session):
        url = "https://speed.cloudflare.com/__up"
        try:
            data = b"0" * (1024 * 1024 * 10)
            start = time.time()
            async with session.post(url, data=data) as response:
                await response.read()
            duration = time.time() - start
            return len(data) / duration if duration > 0 else 0
        except:
            return 0

    async def measure_ping(self, session):
        try:
            start = time.time()
            async with session.get("https://www.google.com") as response:
                await response.read()
            return int((time.time() - start) * 1000)
        except:
            return 0

    async def get_network_info(self, session):
        try:
            async with session.get("https://ipinfo.io/json") as response:
                data = await response.json()
                return {
                    "location": f"{data.get('city', 'N/A')}, {data.get('country', 'N/A')}",
                    "org": data.get('org', 'N/A').replace('AS', '')
                }
        except:
            return {"location": "N/A", "org": "N/A"}

    @loader.command(
        ru_doc="Запустить тест скорости интернета",
        uk_doc="Запустити тест швидкості інтернету",
        en_doc="Start internet speed test"
    )
    async def speedtest(self, message):
        """🚀 Start internet speed test"""
        
        lang = self.config["language"]
        await message.edit(self.strings[f"testing_{lang}"])
        start_time = time.time()

        timeout = aiohttp.ClientTimeout(total=30)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            try:
                network_info = await self.get_network_info(session)
                ping = await self.measure_ping(session)
                download_speed = await self.download_test(session)
                upload_speed = await self.upload_test(session)

                duration = time.time() - start_time

                size_photo = 5 * 1024 * 1024
                size_app = 100 * 1024 * 1024
                size_movie = 2 * 1024 * 1024 * 1024
                size_game = 50 * 1024 * 1024 * 1024

                result = self.strings[f"result_{lang}"].format(
                    self.format_speed(download_speed),
                    self.format_speed(upload_speed),
                    f"{ping}ms",
                    network_info["location"],
                    network_info["org"],
                    self.format_time(size_photo, download_speed),
                    self.format_time(size_app, download_speed),
                    self.format_time(size_movie, download_speed),
                    self.format_time(size_game, download_speed),
                    f"{duration:.1f} sec",
                    datetime.now().strftime("%d.%m.%Y %H:%M:%S")
                )

                await message.edit(result)

            except Exception as e:
                await message.edit(self.strings[f"error_{lang}"].format(str(e)))