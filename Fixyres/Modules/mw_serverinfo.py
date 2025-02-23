# meta developer: @mwmodules
# meta desc: 📊 ServerInfo - Detailed server statistics including CPU, RAM, disk usage, and system performance metrics
# by @mwmodules
# 🔒 Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# meta link: .dlm http://mwmodules.ftp.sh/serverinfo.py



from .. import loader, utils
import platform
import psutil
import os
import sys
import distro
import socket
from datetime import datetime
from telethon.tl.types import Message

__version__ = (1, 1, 0)


"""
    █▀▄▀█ █░█░█ █▀█ █▀▀ █▀▀ █ █▀▀ █▀▀
    █░▀░█ ▀▄▀▄▀ █▄█ █▀░ █▀░ █ █▄▄ ██▄
    
    Developer: @mwoffice
    
    Copyright (C) 2024
    
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
"""


@loader.tds
class ServerInfoMod(loader.Module):
    """Мониторинг системных ресурсов сервера/устройства"""

    strings = {
        "name": "ServerInfo",
        "loading": "Загрузка...",
        "error": "Недоступно получить в вашем устройстве",
        "_cmd_doc_serverinfo": "Показывает информацию о системе с интерактивными кнопками",
        "_cls_doc": "Модуль для мониторинга системных ресурсов сервера/устройства"
    }

    async def client_ready(self, client, db):
        self._db = db
        self._client = client

    def get_markup(self):
        return [
            [
                {"text": "🔧 CPU", "callback": self.cpu_callback},
                {"text": "💾 RAM", "callback": self.ram_callback},
            ],
            [
                {"text": "💽 Диск", "callback": self.disk_callback},
                {"text": "🌐 Сеть", "callback": self.net_callback},
            ],
            [
                {"text": "📊 Процессы", "callback": self.proc_callback},
                {"text": "🔌 Sensors", "callback": self.sens_callback},
            ],
            [
                {"text": "🔄 Обновить", "callback": self.system_callback},
            ],
        ]

    def get_back_markup(self):
        return [
            [
                {"text": "⬅️ Назад", "callback": self.system_callback},
                {"text": "🔄 Обновить", "callback": self.current_callback},
            ],
        ]

    async def system_callback(self, call):
        self.current_callback = self.system_callback
        info = "<b>🖥 Системная информация</b>\n\n"
    
        try:
            info += f"<b>OS:</b> {platform.system() or self.strings['error']}\n"
        except:
            info += f"<b>OS:</b> {self.strings['error']}\n"
            
        try:    
            info += f"<b>Архитектура:</b> {platform.machine() or self.strings['error']}\n"
        except:
            info += f"<b>Архитектура:</b> {self.strings['error']}\n"
            
        try:
            info += f"<b>Python:</b> {sys.version.split()[0]}\n"
        except:
            info += f"<b>Python:</b> {self.strings['error']}\n"
            
        try:
            info += f"<b>Hostname:</b> {platform.node() or self.strings['error']}\n"
        except:
            info += f"<b>Hostname:</b> {self.strings['error']}\n"

        try:
            info += f"<b>Процессов активно:</b> {len(psutil.pids())}\n"
        except:
            info += f"<b>Процессов активно:</b> {self.strings['error']}\n"
            
        await call.edit(text=info, reply_markup=self.get_markup())

    async def cpu_callback(self, call):
        self.current_callback = self.cpu_callback
        info = "<b>🔧 Процессор</b>\n\n"
        
        try:
            info += f"<b>Модель:</b> {platform.processor() or self.strings['error']}\n"
        except:
            info += f"<b>Модель:</b> {self.strings['error']}\n"
            
        try:
            info += f"<b>Физические ядра:</b> {psutil.cpu_count(logical=False)}\n"
            info += f"<b>Логические ядра:</b> {psutil.cpu_count()}\n"
        except:
            info += f"<b>Ядра:</b> {self.strings['error']}\n"
            
        try:
            info += f"<b>Загрузка общая:</b> {psutil.cpu_percent()}%\n"
        except:
            info += f"<b>Загрузка:</b> {self.strings['error']}\n"

        await call.edit(text=info, reply_markup=self.get_back_markup())

    async def ram_callback(self, call):
        self.current_callback = self.ram_callback
        info = "<b>💾 Память</b>\n\n"
        
        try:
            mem = psutil.virtual_memory()
            info += f"<b>RAM всего:</b> {mem.total // (1024**2)}MB\n"
            info += f"<b>RAM доступно:</b> {mem.available // (1024**2)}MB\n"
            info += f"<b>RAM использовано:</b> {mem.used // (1024**2)}MB\n"
            info += f"<b>RAM загрузка:</b> {mem.percent}%\n"
        except:
            info += f"<b>RAM:</b> {self.strings['error']}\n"

        try:
            swap = psutil.swap_memory()
            info += f"\n<b>SWAP всего:</b> {swap.total // (1024**2)}MB\n"
            info += f"<b>SWAP использовано:</b> {swap.used // (1024**2)}MB\n"
            info += f"<b>SWAP загрузка:</b> {swap.percent}%\n"
        except:
            info += f"\n<b>SWAP:</b> {self.strings['error']}\n"
            
        await call.edit(text=info, reply_markup=self.get_back_markup())

    async def disk_callback(self, call):
        self.current_callback = self.disk_callback
        info = "<b>💽 Диски</b>\n\n"
        
        try:
            partitions = psutil.disk_partitions()
            if partitions:
                for partition in partitions:
                    try:
                        usage = psutil.disk_usage(partition.mountpoint)
                        info += (
                            f"<b>Раздел:</b> {partition.device}\n"
                            f"<b>Точка монтирования:</b> {partition.mountpoint}\n"
                            f"<b>Всего:</b> {usage.total // (1024**3)}GB\n"
                            f"<b>Использовано:</b> {usage.used // (1024**3)}GB\n"
                            f"<b>Загрузка:</b> {usage.percent}%\n\n"
                        )
                    except:
                        continue
            else:
                info += f"Разделы: {self.strings['error']}\n"
        except:
            info += f"Диски: {self.strings['error']}\n"
            
        await call.edit(text=info, reply_markup=self.get_back_markup())

    async def net_callback(self, call):
        self.current_callback = self.net_callback
        info = "<b>🌐 Сеть</b>\n\n"
        
        try:
            net_io = psutil.net_io_counters()
            info += (
                f"<b>Отправлено:</b> {net_io.bytes_sent // (1024**2)}MB\n"
                f"<b>Получено:</b> {net_io.bytes_recv // (1024**2)}MB\n\n"
            )
        except:
            info += f"<b>Статистика:</b> {self.strings['error']}\n\n"
            
        try:
            for interface, addrs in psutil.net_if_addrs().items():
                info += f"<b>{interface}:</b>\n"
                for addr in addrs:
                    if addr.family == socket.AF_INET:
                        info += f"IPv4: {addr.address}\n"
                info += "\n"
        except:
            info += f"<b>Интерфейсы:</b> {self.strings['error']}\n"
                    
        await call.edit(text=info, reply_markup=self.get_back_markup())

    async def proc_callback(self, call):
        self.current_callback = self.proc_callback
        info = "<b>📊 Топ процессов по CPU</b>\n\n"
        
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                try:
                    processes.append(proc.info)
                except:
                    continue
                    
            top_cpu = sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:5]
            
            for proc in top_cpu:
                info += (
                    f"<b>PID:</b> {proc['pid']}\n"
                    f"<b>Имя:</b> {proc['name']}\n"
                    f"<b>CPU:</b> {proc['cpu_percent']}%\n\n"
                )
        except:
            info += self.strings['error']
                
        await call.edit(text=info, reply_markup=self.get_back_markup())

    async def sens_callback(self, call):
        self.current_callback = self.sens_callback
        info = "<b>🔌 Сенсоры</b>\n\n"
        sensors_available = False
        
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                sensors_available = True
                info += "<b>Температура:</b>\n"
                for name, entries in temps.items():
                    for entry in entries:
                        info += f"<b>{name}:</b> {entry.current}°C\n"
                info += "\n"
        except:
            pass
                
        try:
            battery = psutil.sensors_battery()
            if battery:
                sensors_available = True
                info += (
                    "<b>Батарея:</b>\n"
                    f"<b>Заряд:</b> {battery.percent}%\n"
                    f"<b>Питание от сети:</b> {'Да' if battery.power_plugged else 'Нет'}\n"
                )
        except:
            pass
            
        if not sensors_available:
            info += self.strings['error']
            
        await call.edit(text=info, reply_markup=self.get_back_markup())

    @loader.command()
    async def serverinfo(self, message: Message):
        """Показывает информацию о системе с интерактивными кнопками"""
        info = "<b>🖥 Системная информация</b>\n\n"
    
        try:
            info += f"<b>OS:</b> {platform.system() or self.strings['error']}\n"
        except:
            info += f"<b>OS:</b> {self.strings['error']}\n"
            
        try:    
            info += f"<b>Архитектура:</b> {platform.machine() or self.strings['error']}\n"
        except:
            info += f"<b>Архитектура:</b> {self.strings['error']}\n"
            
        try:
            info += f"<b>Python:</b> {sys.version.split()[0]}\n"
        except:
            info += f"<b>Python:</b> {self.strings['error']}\n"
            
        try:
            info += f"<b>Hostname:</b> {platform.node() or self.strings['error']}\n"
        except:
            info += f"<b>Hostname:</b> {self.strings['error']}\n"

        try:
            info += f"<b>Процессов активно:</b> {len(psutil.pids())}\n"
        except:
            info += f"<b>Процессов активно:</b> {self.strings['error']}\n"
            
        await self.inline.form(
            text=info,
            message=message,
            reply_markup=self.get_markup(),
        )