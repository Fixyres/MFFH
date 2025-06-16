# На модуль распространяется лицензия "GNU General Public License v3.0"
# https://github.com/all-licenses/GNU-General-Public-License-v3.0

# meta developer: @pymodule
# requires: psutil, py-cpuinfo

from .. import loader, utils
import platform, psutil, cpuinfo, socket, time, getpass
import telethon

try:
    import distro
except ImportError:
    distro = None

def bytes2human(n):
    symbols = ('B','K','M','G','T','P')
    prefix = {s:1<<(i*10) for i,s in enumerate(symbols[1:],1)}
    for s in reversed(symbols[1:]):
        if n>=prefix[s]:
            return f"{n/prefix[s]:.2f}{s}"
    return f"{n}B"

def format_uptime(sec):
    m,s=divmod(sec,60); h,m=divmod(m,60); d,h=divmod(h,24)
    return f"{int(d)}d {int(h)}h {int(m)}m"

def get_distro_info():
    if distro:
        name = distro.name(pretty=True)
        ver = distro.version(best=True)
    else:
        name = ver = "N/A"
        try:
            with open("/etc/os-release") as f:
                data = dict(line.strip().split("=",1) for line in f if "=" in line)
            name = data.get("PRETTY_NAME", data.get("NAME","Unknown"))
            ver = data.get("VERSION_ID","")
        except: pass
    return name, ver

@loader.tds
class SysInfoMod(loader.Module):
    """System information."""
    strings = {"name": "SysInfo"}

    @loader.command(
        doc="🔧 Find out information about the system.",
        ru_doc="🔧 Узнать информацию о системе",
    )
    async def sysinfo(self, message):
        me = await message.client.get_me()
        is_saved = message.chat_id == me.id

        uname = platform.uname()
        cpu = cpuinfo.get_cpu_info()
        boot = psutil.boot_time()
        uptime = time.time() - boot
        freq = psutil.cpu_freq()
        load = psutil.cpu_percent(interval=0.5)
        user = getpass.getuser()
        vm, sm = psutil.virtual_memory(), psutil.swap_memory()
        battery = psutil.sensors_battery()
        temps, fans = {}, {}
        try: temps = psutil.sensors_temperatures()
        except: pass
        try: fans = psutil.sensors_fans()
        except: pass
        net = psutil.net_io_counters()
        io = psutil.disk_io_counters()

        ip_addrs, mac_addrs = [], []
        if is_saved:
            for iface in psutil.net_if_addrs().values():
                for addr in iface:
                    if addr.family == socket.AF_INET:
                        ip_addrs.append(addr.address)
                    elif hasattr(socket, 'AF_PACKET') and addr.family == socket.AF_PACKET:
                        mac_addrs.append(addr.address)

        # Формируем текст с HTML
        text = (
f"<emoji document_id=5776118099812028333>📟</emoji> <b>System Info</b>\n\n"

f"<emoji document_id=5215186239853964761>🖥️</emoji> <u><b>ОС и система:</b></u>\n"
f"<b>OS:</b> <code>{uname.system} {uname.release}</code>\n"
f"<b>Distro:</b> <code>{get_distro_info()[0]} {get_distro_info()[1]}</code>\n"
f"<b>Kernel:</b> <code>{uname.version}</code>\n"
f"<b>Arch:</b> <code>{uname.machine}</code>\n"
f"<b>User:</b> <code>{user}</code>\n\n"

f"<emoji document_id=5341715473882955310>⚙️</emoji> <u><b>CPU:</b></u>\n"
f"<b>Model:</b> <code>{cpu.get('brand_raw','Unknown')}</code>\n"
f"<b>Cores:</b> <code>{psutil.cpu_count(logical=False)}/{psutil.cpu_count(logical=True)}</code>\n"
f"<b>Freq:</b> <code>{f'{freq.current:.0f} MHz' if freq else 'N/A'}</code>\n"
f"<b>Load:</b> <code>{load}%</code>\n\n"

f"<emoji document_id=5237799019329105246>🧠</emoji> <u><b>RAM:</b></u>\n"
f"<b>Used:</b> <code>{bytes2human(vm.used)}</code> / <code>{bytes2human(vm.total)}</code>\n"
f"<b>Swap:</b> <code>{bytes2human(sm.used)}</code> / <code>{bytes2human(sm.total)}</code>\n\n"

f"<emoji document_id=5370714135287832775>🔋</emoji> <u><b>Battery:</b></u>\n"
f"<b>Level:</b> <code>{battery.percent if battery else 'N/A'}%</code>"
f"{' (Charging)' if battery and battery.power_plugged else ''}\n\n"

f"<emoji document_id=5321141214735508486>📡</emoji> <u><b>Сеть:</b></u>\n"
f"<b>Recv:</b> <code>{bytes2human(net.bytes_recv)}</code>\n"
f"<b>Sent:</b> <code>{bytes2human(net.bytes_sent)}</code>\n\n"

f"<emoji document_id=5462956611033117422>💾</emoji> <u><b>Диск:</b></u>\n"
f"<b>Read:</b> <code>{bytes2human(io.read_bytes)}</code>\n"
f"<b>Write:</b> <code>{bytes2human(io.write_bytes)}</code>\n\n"

f"<emoji document_id=5470049770997292425>🌡️</emoji> <u><b>Температуры:</b></u>\n"
f"{'; '.join(f'{k}: ' + ', '.join(f'{t.current:.1f}°C' for t in v) for k,v in temps.items()) or 'N/A'}\n\n"

f"<emoji document_id=5888529492871221275>🌀</emoji> <u><b>Вентиляторы:</b></u>\n"
f"{'; '.join(f'{k}: ' + ', '.join(f'{f.current}rpm' for f in v) for k,v in fans.items()) or 'N/A'}\n\n"

f"<emoji document_id=5382194935057372936>⏱</emoji> <u><b>Аптайм:</b></u>\n"
f"<b>Since:</b> <code>{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(boot))}</code>\n"
f"<b>Uptime:</b> <code>{format_uptime(uptime)}</code>\n\n"

f"<emoji document_id=5854908544712707500>📦</emoji> <u><b>Версии:</b></u>\n"
f"<b>Python:</b> <code>{platform.python_version()}</code>\n"
f"<b>Telethon:</b> <code>{telethon.__version__}</code>\n"
        )

        if is_saved:
            text += f"\n<emoji document_id=5447410659077661506>🌐</emoji> <u><b>Сети:</b></u>\n"
            text += f"<b>IP:</b> <code>{', '.join(ip_addrs) or '—'}</code>\n"
            text += f"<b>MAC:</b> <code>{', '.join(mac_addrs) or '—'}</code>\n"

        await utils.answer(message, text)