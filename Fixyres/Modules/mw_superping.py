# meta developer: @mwmodules
# meta desc: SuperPing - Красиво показывает пинг бота. Да и не только.
# by @mwmodules
# 🔒 Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# meta link: .dlm http://mwmodules.ftp.sh/superping.py

from .. import loader, utils
from telethon.tl.types import Message
import time, psutil, platform
from datetime import datetime
import io
import matplotlib.pyplot as plt
import asyncio

@loader.tds
class SuperPingMod(loader.Module):
    strings = {
        "name": "SuperPing",
        "stats": "📊 Статистика",
        "sys_stats": "💻 Система",
        "visual": "📈 Графики",
    }

    async def get_ping(self):
        start = time.perf_counter()
        await self.client.get_me()
        return round((time.perf_counter() - start) * 1000, 2)

    async def get_main_buttons(self):
        ping = await self.get_ping()
        return [
            [{
                "text": f"🚀 Пинг: {ping} мс",
                "callback": self.ping_callback
            }],
            [{
                "text": self.strings["sys_stats"],
                "callback": self.sys_stats_callback
            }],
            [{
                "text": self.strings["visual"],
                "callback": self.visual_callback
            }],
            [{
                "text": "🔄 Обновить",
                "callback": self.refresh_callback
            }]
        ]

    async def ping_callback(self, call):
        ping = await self.get_ping()
        await call.answer(f"Задержка: {ping}мс")

    async def create_stats_graph(self):
        plt.clf()
        cpu_history = []
        for _ in range(10):
            cpu_history.append(psutil.cpu_percent())
            await asyncio.sleep(0.5)
            
        plt.figure(figsize=(10, 5))
        plt.plot(cpu_history, 'b-', label='CPU %')
        plt.title('CPU Usage History')
        plt.xlabel('Time')
        plt.ylabel('Percentage')
        plt.grid(True)
        plt.legend()
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        return buf

    async def sys_stats_callback(self, call):
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        text = (
            "💻 Система:\n\n"
            f"🔧 CPU: {cpu}%\n"
            f"📊 RAM: {ram.percent}%\n"
            f"💾 Диск: {disk.percent}%\n"
            f"🐍 Python: {platform.python_version()}\n"
            f"🖥 OS: {platform.system()} {platform.release()}\n\n"
            f"📈 Загрузка CPU по ядрам:\n"
            f"{' '.join([str(x) + '%' for x in psutil.cpu_percent(percpu=True)])}"
        )
        await call.edit(
            text=text,
            reply_markup=[[{
                "text": "◀️ Назад",
                "callback": self.back_callback
            }]]
        )

    async def visual_callback(self, call):
        await call.edit("⏳ Генерация графика...")
        graph = await self.create_stats_graph()
        
        message = await self.client.send_file(
            call.from_user.id,  # Отправляем в личку пользователю
            graph,
            caption="📊 График загрузки CPU за последние 5 секунд"
        )
        
        await call.edit(
            text="📊 Главное меню",
            reply_markup=await self.get_main_buttons()
        )

    async def back_callback(self, call):
        await call.edit(
            text="📊 Главное меню",
            reply_markup=await self.get_main_buttons()
        )

    async def refresh_callback(self, call):
        await call.edit(
            text="📊 Главное меню",
            reply_markup=await self.get_main_buttons()
        )

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    @loader.command()
    async def sping(self, message: Message):
        """Запустить интерактивный пинг"""
        await self.inline.form(
            text="📊 Главное меню",
            message=message,
            reply_markup=await self.get_main_buttons(),
        )