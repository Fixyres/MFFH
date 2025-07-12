#  _____                          
# |_   _|____  ____ _ _ __   ___  
#   | |/ _ \ \/ / _` | '_ \ / _ \ 
#   | | (_) >  < (_| | | | | (_) |
#   |_|\___/_/\_\__,_|_| |_|\___/ 
#                             
# meta developer: @Toxano_Modules
# scope: @Toxano_Modules

from herokutl.types import Message
from .. import loader, utils
import subprocess
import os
import json
import shutil
import urllib.request
import urllib.error
import re
import html
import platform
import tempfile

@loader.tds
class fastfetch(loader.Module):
    """Модуль для отображения информации о системе с помощью fastfetch и neofetch"""
    strings = {
        "name": "fastfetch",
        "installing_fastfetch": "📥 Устанавливаю fastfetch...",
        "installing_neofetch": "📥 Устанавливаю neofetch...",
        "installed_fastfetch": "✅ Fastfetch успешно установлен!",
        "installed_neofetch": "✅ Neofetch успешно установлен!",
        "install_error": "❌ Ошибка при установке {tool}: {error}",
        "no_fastfetch": "❌ Fastfetch не установлен. Используйте .instfetch для установки.",
        "no_neofetch": "❌ Neofetch не установлен. Используйте .instneofetch для установки.",
        "detecting_distro": "🔍 Определяю дистрибутив...",
        "trying_package_manager": "📦 Пробую пакетный менеджер: {manager}",
        "compiling_from_source": "🔨 Компилирую из исходников...",
        "distro_detected": "🐧 Обнаружен: {distro}",
    }
    strings_ru = {
        "installing_fastfetch": "📥 Устанавливаю fastfetch...",
        "installing_neofetch": "📥 Устанавливаю neofetch...",
        "installed_fastfetch": "✅ Fastfetch успешно установлен!",
        "installed_neofetch": "✅ Neofetch успешно установлен!",
        "install_error": "❌ Ошибка при установке {tool}: {error}",
        "no_fastfetch": "❌ Fastfetch не установлен. Используйте .instfetch для установки.",
        "no_neofetch": "❌ Neofetch не установлен. Используйте .instneofetch для установки.",
        "detecting_distro": "🔍 Определяю дистрибутив...",
        "trying_package_manager": "📦 Пробую пакетный менеджер: {manager}",
        "compiling_from_source": "🔨 Компилирую из исходников...",
        "distro_detected": "🐧 Обнаружен: {distro}",
    }

    def __init__(self):
        self._fastfetch_path = os.path.expanduser("~/.local/bin/fastfetch")
        self._neofetch_path = os.path.expanduser("~/.local/bin/neofetch")
        self._fastfetch_config_path = os.path.expanduser("~/.config/fastfetch/config.jsonc")
        self._neofetch_config_path = os.path.expanduser("~/.config/neofetch/config.conf")
        os.makedirs(os.path.expanduser("~/.local/bin"), exist_ok=True)
        
        local_bin = os.path.expanduser("~/.local/bin")
        if local_bin not in os.environ.get("PATH", ""):
            os.environ["PATH"] = f"{local_bin}:{os.environ.get('PATH', '')}"

    def _detect_distro(self):
        """Определение дистрибутива Linux"""
        distro_info = {}

        try:
            with open("/etc/os-release", "r") as f:
                for line in f:
                    if "=" in line:
                        key, value = line.strip().split("=", 1)
                        distro_info[key] = value.strip('"')
        except FileNotFoundError:
            pass

        for file_path in ["/etc/lsb-release", "/etc/redhat-release", "/etc/debian_version"]:
            if os.path.exists(file_path):
                try:
                    with open(file_path, "r") as f:
                        content = f.read().strip()
                        if "debian" in content.lower():
                            distro_info["ID"] = "debian"
                        elif "ubuntu" in content.lower():
                            distro_info["ID"] = "ubuntu"
                        elif "red hat" in content.lower() or "rhel" in content.lower():
                            distro_info["ID"] = "rhel"
                        elif "centos" in content.lower():
                            distro_info["ID"] = "centos"
                except:
                    pass
        
        return distro_info

    def _get_architecture(self):
        """Определение архитектуры процессора"""
        arch = platform.machine().lower()
        if arch in ["x86_64", "amd64"]:
            return "amd64"
        elif arch in ["aarch64", "arm64"]:
            return "arm64"
        elif arch in ["armv7l", "armhf"]:
            return "armhf"
        else:
            return arch

    def _check_package_manager(self, manager):
        """Проверка доступности пакетного менеджера"""
        try:
            subprocess.run([manager, "--version"], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    async def _install_with_package_manager(self, package_name, tool_name, message):
        """Установка через пакетные менеджеры"""
        distro = self._detect_distro()
        distro_id = distro.get("ID", "").lower()
        
        await utils.answer(message, self.strings["distro_detected"].format(distro=distro.get("PRETTY_NAME", "Unknown")))

        package_managers = []
        
        if distro_id in ["ubuntu", "debian", "linuxmint", "kali", "pop"]:
            package_managers = [
                ("apt", ["apt", "update", "&&", "apt", "install", "-y", package_name]),
                ("apt-get", ["apt-get", "update", "&&", "apt-get", "install", "-y", package_name])
            ]
        elif distro_id in ["fedora", "rhel", "centos"]:
            package_managers = [
                ("dnf", ["dnf", "install", "-y", package_name]),
                ("yum", ["yum", "install", "-y", package_name])
            ]
        elif distro_id in ["arch", "manjaro", "endeavouros"]:
            package_managers = [
                ("pacman", ["pacman", "-S", "--noconfirm", package_name]),
                ("yay", ["yay", "-S", "--noconfirm", package_name])
            ]
        elif distro_id in ["opensuse", "sles"]:
            package_managers = [
                ("zypper", ["zypper", "install", "-y", package_name])
            ]
        elif distro_id in ["alpine"]:
            package_managers = [
                ("apk", ["apk", "add", package_name])
            ]

        package_managers.extend([
            ("snap", ["snap", "install", package_name]),
            ("flatpak", ["flatpak", "install", "-y", package_name])
        ])
        
        for manager, cmd in package_managers:
            if self._check_package_manager(manager):
                await utils.answer(message, self.strings["trying_package_manager"].format(manager=manager))
                try:

                    if "&&" in cmd:
                        cmd_str = " ".join(cmd)
                        result = subprocess.run(cmd_str, shell=True, capture_output=True, text=True, timeout=300)
                    else:
                        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                    
                    if result.returncode == 0:
                        return True
                except Exception as e:
                    continue
        
        return False

    async def _get_latest_fastfetch_url(self):
        """Получение URL последней версии fastfetch"""
        arch = self._get_architecture()
        
        try:
            api_url = "https://api.github.com/repos/fastfetch-cli/fastfetch/releases/latest"
            with urllib.request.urlopen(api_url) as response:
                release_data = json.loads(response.read().decode())

            arch_patterns = {
                "amd64": ["linux-amd64", "x86_64", "linux-x64"],
                "arm64": ["linux-aarch64", "linux-arm64"],
                "armhf": ["linux-armv7", "linux-armhf"]
            }
            
            for asset in release_data.get("assets", []):
                asset_name = asset["name"].lower()
                for pattern in arch_patterns.get(arch, []):
                    if pattern in asset_name and asset_name.endswith(".tar.gz"):
                        return asset["browser_download_url"], asset["name"]

            return "https://github.com/fastfetch-cli/fastfetch/releases/latest/download/fastfetch-linux-amd64.tar.gz", "fastfetch-linux-amd64.tar.gz"
        except Exception:
            return "https://github.com/fastfetch-cli/fastfetch/releases/latest/download/fastfetch-linux-amd64.tar.gz", "fastfetch-linux-amd64.tar.gz"

    async def _compile_fastfetch_from_source(self, message):
        """Компиляция fastfetch из исходников"""
        await utils.answer(message, self.strings["compiling_from_source"])
        
        try:
            with tempfile.TemporaryDirectory() as temp_dir:

                subprocess.run(["git", "clone", "https://github.com/fastfetch-cli/fastfetch.git", temp_dir], check=True, timeout=300)

                build_dir = os.path.join(temp_dir, "build")
                os.makedirs(build_dir, exist_ok=True)

                subprocess.run(["cmake", "..", "-DCMAKE_INSTALL_PREFIX=" + os.path.expanduser("~/.local")], 
                             cwd=build_dir, check=True, timeout=300)

                subprocess.run(["make", "-j4"], cwd=build_dir, check=True, timeout=600)

                subprocess.run(["make", "install"], cwd=build_dir, check=True, timeout=300)
                
                return True
        except Exception as e:
            return False

    async def _install_neofetch_from_source(self, message):
        """Загрузка neofetch из исходников"""
        try:
            download_url = "https://raw.githubusercontent.com/dylanaraps/neofetch/master/neofetch"
            urllib.request.urlretrieve(download_url, self._neofetch_path)
            os.chmod(self._neofetch_path, 0o755)
            return True
        except Exception:
            return False

    async def _write_fastfetch_config(self):
        """Создание конфигурации fastfetch"""
        config = {
            "$schema": "https://github.com/fastfetch-cli/fastfetch/raw/dev/doc/json_schema.json",
            "logo": {
                "type": "auto",
                "position": "top",
                "padding": {
                    "top": 1,
                    "bottom": 2
                }
            },
            "display": {
                "separator": ": ",
                "key": {
                    "width": 20
                }
            },
            "modules": [
                "title",
                "separator",
                "os",
                "host", 
                "kernel",
                "uptime",
                "packages",
                "shell",
                "terminal",
                "cpu",
                "gpu",
                "memory",
                {
                    "type": "disk",
                    "folders": {
                        "/": "Root"
                    }
                },
                "locale",
                "break",
                "colors"
            ]
        }
        
        os.makedirs(os.path.dirname(self._fastfetch_config_path), exist_ok=True)
        with open(self._fastfetch_config_path, "w") as f:
            json.dump(config, f, indent=2)

    async def _write_neofetch_config(self):
        """Создание конфигурации neofetch"""
        config_content = '''#!/usr/bin/env bash
# Neofetch config file

# Info
print_info() {
    info title
    info underline
    
    info "OS" distro
    info "Host" model
    info "Kernel" kernel
    info "Uptime" uptime
    info "Packages" packages
    info "Shell" shell
    info "Terminal" term
    info "CPU" cpu
    info "GPU" gpu
    info "Memory" memory
    
    info "Disk" disk
    info "Locale" locale
    
    info cols
}

# Separator
separator=":"

# Colors
ascii_colors=(distro)
colors=(distro)

# ASCII art
ascii_distro="auto"
ascii_bold="on"

# Image
image_backend="ascii"
image_source="auto"

# Disk
disk_show=('/')
disk_subtitle="mount"

# Text options
bold="on"
underline_enabled="on"
underline_char="-"
separator=":"

# Color blocks
block_range=(0 15)
color_blocks="on"
block_width=3
block_height=1
col_offset="auto"
'''
        
        os.makedirs(os.path.dirname(self._neofetch_config_path), exist_ok=True)
        with open(self._neofetch_config_path, "w") as f:
            f.write(config_content)

    def _clean_ansi_codes(self, text):
        """Умная очистка ANSI escape последовательностей"""
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        cleaned = ansi_escape.sub('', text)
        cleaned = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', cleaned)
        
        lines = cleaned.split('\n')
        result_lines = []
        
        for line in lines:
            if line.strip() or (result_lines and result_lines[-1].strip()):
                result_lines.append(line.rstrip())
        
        return '\n'.join(result_lines)

    def _fix_separator(self, text):
        """Заменяет стрелки на двоеточия"""
        text = re.sub(r'\s*->\s*', ': ', text)
        text = re.sub(r'\s*→\s*', ': ', text)
        text = re.sub(r'\s*-->\s*', ': ', text)
        return text

    @loader.command(ru_doc="Установить fastfetch")
    async def instfetch(self, message: Message):
        """Установка fastfetch в пользовательскую директорию"""
        await utils.answer(message, self.strings["installing_fastfetch"])
        
        try:
  
            if await self._install_with_package_manager("fastfetch", "fastfetch", message):
                await utils.answer(message, self.strings["installed_fastfetch"])
                return

            download_url, filename = await self._get_latest_fastfetch_url()
            
            temp_dir = "/tmp/fastfetch_install"
            os.makedirs(temp_dir, exist_ok=True)
            archive_path = os.path.join(temp_dir, filename)
            
            urllib.request.urlretrieve(download_url, archive_path)
            subprocess.run(["tar", "-xzf", archive_path, "-C", temp_dir], check=True)

            for root, dirs, files in os.walk(temp_dir):
                if "fastfetch" in files:
                    fastfetch_binary = os.path.join(root, "fastfetch")
                    shutil.copy2(fastfetch_binary, self._fastfetch_path)
                    os.chmod(self._fastfetch_path, 0o755)
                    break
            else:
 
                if await self._compile_fastfetch_from_source(message):
                    await utils.answer(message, self.strings["installed_fastfetch"])
                    return
                raise Exception("Не удалось найти исполняемый файл fastfetch")
            
            shutil.rmtree(temp_dir, ignore_errors=True)
            await utils.answer(message, self.strings["installed_fastfetch"])
            
        except Exception as e:
            await utils.answer(message, self.strings["install_error"].format(tool="fastfetch", error=str(e)))

    @loader.command(ru_doc="Установить neofetch")
    async def instneofetch(self, message: Message):
        """Установка neofetch в пользовательскую директорию"""
        await utils.answer(message, self.strings["installing_neofetch"])
        
        try:

            if await self._install_with_package_manager("neofetch", "neofetch", message):
                await utils.answer(message, self.strings["installed_neofetch"])
                return

            if await self._install_neofetch_from_source(message):
                await utils.answer(message, self.strings["installed_neofetch"])
                return
            
            raise Exception("Не удалось установить neofetch")
            
        except Exception as e:
            await utils.answer(message, self.strings["install_error"].format(tool="neofetch", error=str(e)))

    @loader.command(ru_doc="Показать информацию о системе через fastfetch")
    async def fastfetch(self, message: Message):
        """Отображение информации о системе с ASCII артом через fastfetch"""
 
        if not os.path.exists(self._fastfetch_path) and not shutil.which("fastfetch"):
            await utils.answer(message, self.strings["no_fastfetch"])
            return
        
        try:
            await self._write_fastfetch_config()

            fastfetch_cmd = "fastfetch" if shutil.which("fastfetch") else self._fastfetch_path
            
            result = subprocess.run(
                [fastfetch_cmd, "--config", self._fastfetch_config_path],
                capture_output=True,
                text=True,
                timeout=15   
            )
            
            if result.returncode == 0:
                clean_output = self._clean_ansi_codes(result.stdout)
                fixed_output = self._fix_separator(clean_output)
                escaped_output = html.escape(fixed_output)

                formatted_output = f"<blockquote>{escaped_output}</blockquote>"
                
                await utils.answer(message, formatted_output)
            else:
                error_msg = result.stderr or "Unknown error"
                await utils.answer(message, self.strings["install_error"].format(tool="fastfetch", error=error_msg))
                
        except subprocess.TimeoutExpired:
            await utils.answer(message, self.strings["install_error"].format(tool="fastfetch", error="Timeout"))
        except Exception as e:
            await utils.answer(message, self.strings["install_error"].format(tool="fastfetch", error=str(e)))

    @loader.command(ru_doc="Показать информацию о системе через neofetch")
    async def neofetch(self, message: Message):
        """Отображение информации о системе с ASCII артом через neofetch"""

        if not os.path.exists(self._neofetch_path) and not shutil.which("neofetch"):
            await utils.answer(message, self.strings["no_neofetch"])
            return
        
        try:
            await self._write_neofetch_config()
 
            neofetch_cmd = "neofetch" if shutil.which("neofetch") else self._neofetch_path
            
            result = subprocess.run(
                [neofetch_cmd, "--config", self._neofetch_config_path],
                capture_output=True,
                text=True,
                timeout=10   
            )
            
            if result.returncode == 0:
                clean_output = self._clean_ansi_codes(result.stdout)
                fixed_output = self._fix_separator(clean_output)
                escaped_output = html.escape(fixed_output)

                formatted_output = f"<blockquote>{escaped_output}</blockquote>"
                
                await utils.answer(message, formatted_output)
            else:
                error_msg = result.stderr or "Unknown error"
                await utils.answer(message, self.strings["install_error"].format(tool="neofetch", error=error_msg))
                
        except subprocess.TimeoutExpired:
            await utils.answer(message, self.strings["install_error"].format(tool="neofetch", error="Timeout"))
        except Exception as e:
            await utils.answer(message, self.strings["install_error"].format(tool="neofetch", error=str(e)))
