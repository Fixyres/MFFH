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

@loader.tds
class fastfetch(loader.Module):
    """Модуль для отображения информации о системе с помощью fastfetch"""
    strings = {
        "name": "fastfetch",
        "installing": "📥 Устанавливаю fastfetch...",
        "installed": "✅ Fastfetch успешно установлен!",
        "install_error": "❌ Ошибка при установке fastfetch: {error}",
        "fetching": "🔍 Получаю информацию о системе...",
        "no_fastfetch": "❌ Fastfetch не установлен. Используйте .instfetch для установки.",
        "system_info": "💻 Информация о системе:",
    }
    strings_ru = {
        "installing": "📥 Устанавливаю fastfetch...",
        "installed": "✅ Fastfetch успешно установлен!",
        "install_error": "❌ Ошибка при установке fastfetch: {error}",
        "fetching": "🔍 Получаю информацию о системе...",
        "no_fastfetch": "❌ Fastfetch не установлен. Используйте .instfetch для установки.",
        "system_info": "💻 Информация о системе:",
    }

    def __init__(self):
        self._fastfetch_path = os.path.expanduser("~/.local/bin/fastfetch")
        self._fastfetch_config_path = os.path.expanduser("~/.config/fastfetch/config.jsonc")
        os.makedirs(os.path.expanduser("~/.local/bin"), exist_ok=True)

    async def _get_latest_fastfetch_url(self):
        """Получение URL последней версии fastfetch для Linux x64"""
        try:
            api_url = "https://api.github.com/repos/fastfetch-cli/fastfetch/releases/latest"
            with urllib.request.urlopen(api_url) as response:
                release_data = json.loads(response.read().decode())
            
            for asset in release_data.get("assets", []):
                if "linux-amd64" in asset["name"] and asset["name"].endswith(".tar.gz"):
                    return asset["browser_download_url"], asset["name"]
            
            return "https://github.com/fastfetch-cli/fastfetch/releases/latest/download/fastfetch-linux-amd64.tar.gz", "fastfetch-linux-amd64.tar.gz"
        except Exception:
            return "https://github.com/fastfetch-cli/fastfetch/releases/latest/download/fastfetch-linux-amd64.tar.gz", "fastfetch-linux-amd64.tar.gz"

    async def _write_fastfetch_config(self):
        """Создание конфигурации fastfetch с ASCII артом сверху"""
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
                "separator": " -> ",
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

    def _clean_ansi_codes(self, text):
        """Умная очистка ANSI escape последовательностей с сохранением структуры"""

        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        cleaned = ansi_escape.sub('', text)

        cleaned = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', cleaned)
        
        lines = cleaned.split('\n')
        result_lines = []
        
        for line in lines:

            if line.strip() or (result_lines and result_lines[-1].strip()):
                result_lines.append(line.rstrip())
        
        return '\n'.join(result_lines)

    @loader.command(ru_doc="Установить fastfetch")
    async def instfetch(self, message: Message):
        """Установка fastfetch в пользовательскую директорию"""
        await utils.answer(message, self.strings["installing"])
        
        try:
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
            
            shutil.rmtree(temp_dir, ignore_errors=True)
            await utils.answer(message, self.strings["installed"])
            
        except Exception as e:
            await utils.answer(message, self.strings["install_error"].format(error=str(e)))

    @loader.command(ru_doc="Показать информацию о системе")
    async def fastfetch(self, message: Message):
        """Отображение информации о системе с ASCII артом"""
        if not os.path.exists(self._fastfetch_path):
            await utils.answer(message, self.strings["no_fastfetch"])
            return
            
        await utils.answer(message, self.strings["fetching"])
        
        try:
            await self._write_fastfetch_config()
            
            result = subprocess.run(
                [self._fastfetch_path, "--config", self._fastfetch_config_path],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:

                clean_output = self._clean_ansi_codes(result.stdout)
                
                escaped_output = html.escape(clean_output)
                
                formatted_output = f"<blockquote expandable><pre>{escaped_output}</pre></blockquote>"
                
                await utils.answer(message, f"{self.strings['system_info']}\n\n{formatted_output}")
            else:
                error_msg = result.stderr or "Unknown error"
                await utils.answer(message, self.strings["install_error"].format(error=error_msg))
                
        except subprocess.TimeoutExpired:
            await utils.answer(message, self.strings["install_error"].format(error="Timeout"))
        except Exception as e:
            await utils.answer(message, self.strings["install_error"].format(error=str(e)))