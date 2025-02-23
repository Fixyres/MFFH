"""

    █▀▀ ▄▀█ █▄▀ █▀▀ █▀ ▀█▀ █░█░█ █ ▀▄▀
    █▄▄ █▀█ █░█ ██▄ ▄█ ░█░ ▀▄▀▄▀ █ █░█

    Copyleft 2022 t.me/CakesTwix
    This program is free software; you can redistribute it and/or modify

"""

__version__ = (1, 4, 5)

# requires: psutil py-cpuinfo
# meta pic: https://img.icons8.com/external-xnimrodx-lineal-color-xnimrodx/512/000000/external-pc-computer-xnimrodx-lineal-color-xnimrodx.png
# meta developer: @cakestwix_mods
# scope: inline
# scope: hikka_min 1.1.2

# For version info 
import telethon
import aiogram
import git

import datetime
import logging
from typing import Union
import platform
import cpuinfo
import psutil
from aiogram.utils.markdown import quote_html
from os.path import exists
from .. import loader, utils

logger = logging.getLogger(__name__)

# https://www.adamsmith.haus/python/answers/how-to-remove-empty-lines-from-a-string-in-python
def remove_empty_lines(string_with_empty_lines):
    lines = string_with_empty_lines.split("\n")
    non_empty_lines = [line for line in lines if line.strip() != ""]

    return "".join(line + "\n" for line in non_empty_lines)


backslash = "\n"


def get_os_release():
    if not exists("/etc/os-release"):
        return False

    list_ = []
    with open("/etc/os-release") as f:
        list_.extend(item.split("=") for item in f.readlines())
    return {item[0]: item[1].replace(backslash, "").replace('"', "") for item in list_}


# https://stackoverflow.com/questions/2756737/check-linux-distribution-name
def get_distro():
    """
    Name of your Linux distro
    """
    if not exists("/etc/issue"):
        return False

    with open("/etc/issue") as f:
        return f.read().split()[0]


def progressbar(iteration: int, length: int) -> str:
    percent = ("{0:." + str(1) + "f}").format(100 * (iteration / float(100)))
    filledLength = int(length * iteration // 100)
    return "█" * filledLength + "▒" * (length - filledLength)


# From Hikka https://github.com/hikariatama/Hikka/blob/master/hikka/utils.py#L459-L461
def chunks(_list: Union[list, tuple, set], n: int, /) -> list:
    """Split provided `_list` into chunks of `n`"""
    return [_list[i : i + n] for i in range(0, len(_list), n)]


def bytes2human(n):
    # http://code.activestate.com/recipes/578019
    # >>> bytes2human(10000)
    # '9.8K'
    # >>> bytes2human(100001221)
    # '95.4M'
    symbols = ("K", "M", "G", "T", "P", "E", "Z", "Y")
    prefix = {s: 1 << (i + 1) * 10 for i, s in enumerate(symbols)}
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return "%.1f%s" % (value, s)
    return "%sB" % n


@loader.tds
class InlineSystemInfoMod(loader.Module):
    """🖥 Get detailed information about your server"""

    strings = {
        "name": "🖥 InlineSystemInfo",
    }

    AddressFamily = {
        2: "IPv4",
        10: "IPv6",
        28: "IPv6",
        17: "Link",
        18: "Link",
    }

    def menu_keyboard(self) -> list:
        keyboard = [
            [
                {
                    "text": "😼 General",
                    "callback": self.change_stuff,
                    "args": ("General",),
                }
            ],
        ]

        keyboard.extend(
            iter(
                chunks(
                    [
                        {
                            "text": "🧠 CPU",
                            "callback": self.change_stuff,
                            "args": ("CPU",),
                        },
                        {
                            "text": "🐧 Linux",
                            "callback": self.change_stuff,
                            "args": ("Linux",),
                        },
                        {
                            "text": "🗄 Memory",
                            "callback": self.change_stuff,
                            "args": ("Memory",),
                        },
                        {
                            "text": "🌐 Network Address",
                            "callback": self.change_stuff,
                            "args": ("Network Address",),
                        },
                        {
                            "text": "🌐 Network Stats",
                            "callback": self.change_stuff,
                            "args": ("Network Stats",),
                        },
                        {
                            "text": "💽 Disk",
                            "callback": self.change_stuff,
                            "args": ("Disk",),
                        },
                        {
                            "text": "🌡 Sensors",
                            "callback": self.change_stuff,
                            "args": ("Sensors",),
                        },
                        {
                            "text": "🐍 Python",
                            "callback": self.change_stuff,
                            "args": ("Python",),
                        }
                    ],
                    3,
                )
            )
        )

        keyboard.append([{"text": "🚫 Close", "callback": self.inline__close}])
        try:
            return keyboard[3].remove([])
        except ValueError:
            return keyboard

    def general_info(self):
        string = "😼 <b>System Info</b>\n"
        string += f"  ├──<b>CPU Name</b>: <code>{self.cpu_info.get('brand_raw', 'Undetermined.')}</code> {self.cpu_count_logic}/{self.cpu_count} ({self.cpu_info['arch_string_raw']})\n"
        string += f"  ├──<b>RAM</b>: {progressbar(self.virtual_memory.percent, 10)} <code>({bytes2human(self.virtual_memory.used)}/{bytes2human(self.virtual_memory.total)})</code>\n"
        string += f"  └──<b>Swap</b>: {progressbar(self.swap_memory.percent, 10)} <code>({bytes2human(self.swap_memory.used)}/{bytes2human(self.swap_memory.total)})</code>\n\n"

        string += "🐧 <b>Linux Info</b>\n"
        string += f"  ├──<b>Name</b>: <code>{get_distro()}</code>\n"
        string += f"  └──<b>Kernel</b>: <code>{platform.release()}</code>\n\n"

        if hasattr(self, "disk_partitions"):
            for disk_root in psutil.disk_partitions("/"):
                if disk_root.mountpoint == '/':
                    disk_usage = psutil.disk_usage(disk_root.mountpoint)

                    string += "💽 <b>Disk Info</b> <code>(/)</code>\n"
                    string += f"  └──<b>{disk_root.device}</b>\n"
                    string += f"        ├── <b>Mount</b> {disk_root.mountpoint}\n"
                    string += f"        ├── <b>FS</b> {disk_root.fstype}\n"
                    string += f"        ├── <b>Disk Usage</b> {disk_usage.percent}% ({bytes2human(disk_usage.used)}/{bytes2human(disk_usage.total)})\n"
                    string += f"        │       └──{progressbar(disk_usage.percent, 10)}\n"
                    string += f"        └── <b>Options</b> {disk_root.opts}\n\n"

        return string

    def cpu_string(self):
        string = "🧠  <b>CPU Info</b>\n"
        string += f"⦁ <b>Name</b>: {self.cpu_info.get('brand_raw', 'Undetermined.')} ({self.cpu_info['arch_string_raw']})\n"
        string += f"⦁ <b>Count</b>: {self.cpu_count_logic} ({self.cpu_count})\n"
        string += (
            f"⦁ <b>Freq</b>: {self.cpu_freq[0]} (max: {self.cpu_freq[2]} / min: {self.cpu_freq[1]})\n"
            if hasattr(self, "cpu_freq") and self.cpu_freq
            else ""
        )
        string += f"⦁ <b>Flags</b>: {' '.join(self.cpu_info.get('flags', 'No flags'))}\n"
        string += (
            f"⦁ <b>Load avg</b>: {self.loadavg[0]} {self.loadavg[1]} {self.loadavg[2]}\n"
            if hasattr(self, "loadavg")
            else ""
        )

        return string

    def disks_string(self):
        if not hasattr(self, "disk_partitions"):
            return None

        string = "💽  <b>Disk Info</b>\n"
        for disk in self.disk_partitions:
            disk_usage = psutil.disk_usage(disk.mountpoint)

            string += f"<b>{disk.device}</b>\n"
            string += f"├── <b>Mount</b> {disk.mountpoint}\n"
            string += f"├── <b>FS</b> {disk.fstype}\n"
            string += f"├── <b>Disk Usage</b> {disk_usage.percent}% ({bytes2human(disk_usage.used)}/{bytes2human(disk_usage.total)})\n"
            string += f"│       └──{progressbar(disk_usage.percent, 10)}\n"
            string += f"└── <b>Options</b> {disk.opts}\n\n"

        return string

    def network_addr_string(self):
        if not hasattr(self, "net_if_addrs"):
            return None

        string = "🌐  <b>Network Info</b>\n"
        string += "<b>Address</b>:\n"
        for interf in self.net_if_addrs:
            interface = self.net_if_addrs[interf]
            string += f"<b>{interf}</b>\n"
            for addr in interface:
                attr = [
                    a
                    for a in dir(psutil.net_if_addrs()[interf][0])
                    if not a.startswith("__")
                    and not a.startswith("_")
                    and not callable(getattr(psutil.net_if_addrs()[interf][0], a))
                ]
                string += f"{self.AddressFamily[getattr(addr, 'family')]}\n"
                for item in attr[:-1]:
                    string += f"├── {item}: {getattr(addr, item)}\n"
                string += f"└── {attr[-1]}: {getattr(addr, attr[-1])}\n"
            string += "\n"

        return string

    def memory_string(self):
        string = "🗄  <b>Memory Info</b>\n"
        string += f"<b>RAM</b>: {progressbar(self.virtual_memory.percent, 10)} <code>({bytes2human(self.virtual_memory.used)}/{bytes2human(self.virtual_memory.total)})</code>\n"
        string += f"<b>Swap</b>: {progressbar(self.swap_memory.percent, 10)} <code>({bytes2human(self.swap_memory.used)}/{bytes2human(self.swap_memory.total)})</code>\n"

        return string

    def sensors_string(self):
        string = None
        if hasattr(self, "sensors_temperatures"):
            string = "🌡  <b>Sensors Info</b>\n" + "<b>Temperature</b>:\n"
            for sensor_name in self.sensors_temperatures:
                sensor = self.sensors_temperatures[sensor_name]
                string += f"<b>{sensor_name}</b>\n"
                for sensor_info in sensor:
                    attr = [
                        a
                        for a in dir(sensor_info)
                        if not a.startswith("__")
                        and not a.startswith("_")
                        and not callable(getattr(sensor_info, a))
                    ]
                    for item in attr[:-1]:
                        string += f"├── {item}: {getattr(sensor_info, item)}\n"
                    string += f"└── {attr[-1]}: {getattr(sensor_info, attr[-1])}\n"
                string += "\n"

        if hasattr(self, "sensors_fans"):
            string += "<b>Fans</b>:"
            for sensor_name in self.sensors_fans:
                sensor = self.sensors_fans[sensor_name]
                string += f"<b>{sensor_name}</b>\n"
                for sensor_info in sensor:
                    attr = [
                        a
                        for a in dir(sensor_info)
                        if not a.startswith("__")
                        and not a.startswith("_")
                        and not callable(getattr(sensor_info, a))
                    ]
                    for item in attr[:-1]:
                        string += f"├── {item}: {getattr(sensor_info, item)}\n"
                    string += f"└── {attr[-1]}: {getattr(sensor_info, attr[-1])}\n"

        return string

    def network_stats_string(self):
        if not hasattr(self, "net_if_stats"):
            return None

        string = "🌐  <b>Network Info</b>\n" + "<b>Stats</b>:\n"
        for interf in self.net_if_stats:
            interface = self.net_if_stats[interf]
            string += f"<b>{interf}</b>\n"
            string += f"└── {quote_html(interface)}\n\n"

        return string

    def linux_string(self):
        os_release = get_os_release()

        string = f"""🐧  <b>Linux Info</b>
        Name: {get_distro()}
        Kernel: {platform.release()}
        Hostname: {platform.node()}
        {f'glibc ver: {platform.glibc()[1]}' if hasattr(platform, 'glibc') else ''}
        Boot time: {self.boot_time if hasattr(self, "boot_time") else "Termux moment"}

        """
        if os_release:
            string += f"""<b>\n        /etc/os-releases Info:</b>
        Pretty Name: {os_release["PRETTY_NAME"]}
        Name: {os_release["NAME"]}
        Version: {os_release.get("VERSION", "Not available")}
        Documentation: {os_release.get("DOCUMENTATION_URL", "Not available")}
        Support: {os_release.get("SUPPORT_URL", "Not available")}
        Bug Report: {os_release["BUG_REPORT_URL"]}
            """

        return remove_empty_lines(string)
    
    def python_string(self):
        string = "🐍 <b>Python Info</b>\n"
        string += f"  ├──<b>Version</b>: <code>{platform.python_version()}</code>\n"
        string += f"  ├──<b>Version (More details)</b>: <code>{cpuinfo.get_cpu_info()['python_version']}</code>\n"
        string += f"  └──<b>Python Packages version</b>\n"
        string += f"         ├──<b>Telethon</b>: <code>{telethon.__version__}</code>\n"
        string += f"         ├──<b>AIOgram</b>: <code>{aiogram.__version__}</code>\n"
        string += f"         ├──<b>Cpuinfo</b>: <code>{cpuinfo.get_cpu_info()['cpuinfo_version_string']}</code>\n"
        string += f"         ├──<b>psutil</b>: <code>{psutil.__version__}</code>\n"
        string += f"         └──<b>git</b>: <code>{git.__version__}</code>\n"

        return string

    def __init__(self):
        # CPU stuff
        self.cpu_count_logic = psutil.cpu_count()
        self.cpu_count = psutil.cpu_count(logical=False)

        try:
            self.cpu_freq = psutil.cpu_freq()
        except FileNotFoundError:
            pass

        self.cpu_info = cpuinfo.get_cpu_info()

        # Network
        try:
            self.net_if_addrs = psutil.net_if_addrs()
            self.net_if_stats = psutil.net_if_stats()
        except PermissionError:
            pass

    def update_data(self):
        # Memory
        self.virtual_memory = psutil.virtual_memory()
        self.swap_memory = psutil.swap_memory()

        # Sensors
        if hasattr(psutil, "sensors_temperatures"):
            self.sensors_temperatures = psutil.sensors_temperatures()
        if hasattr(psutil, "sensors_fans"):
            self.sensors_fans = psutil.sensors_fans()
        
        # self.sensors_battery = psutil.sensors_battery()

        # CPU stuff
        self.cpu_percent = psutil.cpu_percent(interval=None)

        # Linux stuff
        self.loadavg = psutil.getloadavg()

        # Disks
        try:
            self.disk_partitions = psutil.disk_partitions()
        except PermissionError:
            pass

        # Other
        self.boot_time = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # Generate string
        self.info_string = {
            "General": self.general_info(),
            "CPU": self.cpu_string(),
            "Disk": self.disks_string(),
            "Network Address": self.network_addr_string(),
            "Network Stats": self.network_stats_string(),
            "Memory": self.memory_string(),
            "Sensors": self.sensors_string(),
            "Linux": self.linux_string(),
            "Python": self.python_string(),
        }

    async def client_ready(self, client, db) -> None:
        if utils.get_platform_name() == '🕶 Termux':
            raise loader.LoadError("No Termux support. Change your host")

    async def systeminfocmd(self, message):
        """Get information about your server"""
        await utils.run_sync(self.update_data)

        await self.inline.form(
            text=self.general_info(),
            message=message,
            reply_markup=self.menu_keyboard(),
        )

    # Inline callback

    async def change_stuff(self, call, stuff):
        if self.info_string[stuff] != None:
            await call.edit(text=self.info_string[stuff], reply_markup=self.menu_keyboard())
        else:
            await call.answer("No data :(")

    async def inline__close(self, call) -> None:
        await call.delete()
