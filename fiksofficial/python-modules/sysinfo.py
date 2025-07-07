#         ______     ___  ___          _       _      
#    ____ | ___ \    |  \/  |         | |     | |     
#   / __ \| |_/ /   _| .  . | ___   __| |_   _| | ___ 
#  / / _` |  __/ | | | |\/| |/ _ \ / _` | | | | |/ _ \
# | | (_| | |  | |_| | |  | | (_) | (_| | |_| | |  __/
#  \ \__,_\_|   \__, \_|  |_/\___/ \__,_|\__,_|_|\___|
#   \____/       __/ |                                
#               |___/                                 

# На модуль распространяется лицензия "GNU General Public License v3.0"
# https://github.com/all-licenses/GNU-General-Public-License-v3.0

# meta developer: @pymodule
# requires: psutil

from .. import loader, utils
import platform, psutil, socket, time, getpass, telethon
import os

def bytes2human(n):
    symbols = ('B','K','M','G','T','P')
    prefix = {s:1<<(i*10) for i,s in enumerate(symbols[1:],1)}
    for s in reversed(symbols[1:]):
        if n >= prefix[s]:
            return f"{n/prefix[s]:.2f}{s}"
    return f"{n}B"

def format_uptime(sec):
    m, s = divmod(sec, 60); h, m = divmod(m, 60); d, h = divmod(h, 24)
    return f"{int(d)}d {int(h)}h {int(m)}m"

def get_distro_info():
    name = ver = "N/A"
    try:
        with open("/etc/os-release") as f:
            data = dict(line.strip().split("=", 1) for line in f if "=" in line)
        name = data.get("PRETTY_NAME", data.get("NAME", "Unknown")).strip('"')
        ver = data.get("VERSION_ID", "").strip('"')
    except: pass
    return name, ver

def get_cpu_model():
    try:
        with open("/proc/cpuinfo") as f:
            for line in f:
                if "model name" in line:
                    return line.split(":",1)[1].strip()
    except: pass
    return platform.processor() or "Unknown"

@loader.tds
class SysInfoMod(loader.Module):
    """System information."""
    strings = {"name": "SysInfo"}

    @loader.command(
        doc="🔧 Shows information about the system.",
        ru_doc="🔧 Показывает информацию о системе.",
    )
    async def sysinfo(self, message):
        me = await message.client.get_me()
        is_saved = message.chat_id == me.id

        uname = platform.uname()
        boot = psutil.boot_time()
        uptime = time.time() - boot
        freq = psutil.cpu_freq()
        load = psutil.cpu_percent(interval=0.5)
        user = getpass.getuser()
        vm, sm = psutil.virtual_memory(), psutil.swap_memory()
        net = psutil.net_io_counters()
        io = psutil.disk_io_counters()

        distro_name, distro_ver = get_distro_info()
        cpu_model = get_cpu_model()

        ip_addrs = []
        mac_addrs = []
        net_info = []

        for iface, addrs in psutil.net_if_addrs().items():
            ip = mac = "—"
            for addr in addrs:
                if addr.family == socket.AF_INET:
                    ip = addr.address
                    ip_addrs.append(ip)
                elif hasattr(socket, 'AF_PACKET') and addr.family == socket.AF_PACKET:
                    mac = addr.address
                    mac_addrs.append(mac)
            net_info.append(f"<b>{iface}</b>: IP <code>{ip}</code>, MAC <code>{mac}</code>")

        freq_str = f"{freq.current:.0f} MHz" if freq else "N/A"

        text = (
f"<emoji document_id=5776118099812028333>📟</emoji> <b>System Info</b>\n\n"

f"<emoji document_id=5215186239853964761>🖥️</emoji> <u><b>ОС и система:</b></u>\n"
f"<b>OS:</b> <code>{uname.system} {uname.release}</code>\n"
f"<b>Distro:</b> <code>{distro_name} {distro_ver}</code>\n"
f"<b>Kernel:</b> <code>{uname.version}</code>\n"
f"<b>Arch:</b> <code>{uname.machine}</code>\n"
f"<b>User:</b> <code>{user}</code>\n\n"

f"<emoji document_id=5341715473882955310>⚙️</emoji> <u><b>CPU:</b></u>\n"
f"<b>Model:</b> <code>{cpu_model}</code>\n"
f"<b>Cores:</b> <code>{psutil.cpu_count(logical=False)}/{psutil.cpu_count(logical=True)}</code>\n"
f"<b>Freq:</b> <code>{freq_str}</code>\n"
f"<b>Load:</b> <code>{load}%</code>\n\n"

f"<emoji document_id=5237799019329105246>🧠</emoji> <u><b>RAM:</b></u>\n"
f"<b>Used:</b> <code>{bytes2human(vm.used)}</code> / <code>{bytes2human(vm.total)}</code>\n"
f"<b>Swap:</b> <code>{bytes2human(sm.used)}</code> / <code>{bytes2human(sm.total)}</code>\n\n"

f"<emoji document_id=5462956611033117422>💾</emoji> <u><b>Диск:</b></u>\n"
f"<b>Read:</b> <code>{bytes2human(io.read_bytes)}</code>\n"
f"<b>Write:</b> <code>{bytes2human(io.write_bytes)}</code>\n\n"

f"<emoji document_id=5321141214735508486>📡</emoji> <u><b>Сеть:</b></u>\n"
f"<b>Recv:</b> <code>{bytes2human(net.bytes_recv)}</code>\n"
f"<b>Sent:</b> <code>{bytes2human(net.bytes_sent)}</code>\n"
f"{chr(10).join(net_info)}\n\n"

f"<emoji document_id=5382194935057372936>⏱</emoji> <u><b>Аптайм:</b></u>\n"
f"<b>Since:</b> <code>{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(boot))}</code>\n"
f"<b>Uptime:</b> <code>{format_uptime(uptime)}</code>\n\n"

f"<emoji document_id=5854908544712707500>📦</emoji> <u><b>Версии:</b></u>\n"
f"<b>Python:</b> <code>{platform.python_version()}</code>\n"
f"<b>Telethon:</b> <code>{telethon.__version__}</code>\n"
        )

        await utils.answer(message, text)
