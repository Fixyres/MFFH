import os
import git
import enum
import aiohttp
import requests
import subprocess
from datetime import datetime, timezone
from typing import Union, Optional, Dict, List, Tuple
from hikkatl.tl.types import Message
from hikkatl.utils import get_display_name
from .. import loader, utils

__version__ = (2, 0, 0)

FLAGS = {
    # Добавьте все необходимые флаги стран...
}

class Error(enum.Enum):
    critical = 500
    not_found = 404
    unauthorized = 403
    unknown = 0

class Host:
    def __init__(self, id: int, name: str, server_id: int, port: int, start_date: str, end_date: str, rate: float):
        self.id = id
        self.name = name
        self.server_id = server_id
        self.port = port
        self.start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S.%f%z")
        self.end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S.%f%z")
        self.rate = rate

class API:
    async def _request(self, url: str, method: str = "GET", params: Optional[Dict] = None, data: Optional[Dict] = None, headers: Optional[Dict] = None) -> Union[Dict, List[Union[Dict, int]]]:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.request(method, url, params=params, data=data, headers=headers) as response:
                    if response.status == 200:
                        answer = await response.json()
                        if "status_code" in answer:
                            return [{"detail": answer["detail"]}, answer["status_code"]}
                        return answer if isinstance(answer, dict) else {"data": answer}
                    return [{"detail": await response.text()}, response.status]
            except aiohttp.ClientConnectorError:
                return [{"detail": "Connection error"}, 500]
            except Exception as e:
                return [{"detail": f"Unknown error: {e}"}, 500]

class HostAPI(API):
    def __init__(self, url: str, token: str):
        self.auth_header = {"token": token}
        self._url = f"{url}/api/host"

    async def check_answer(self, res: Union[Dict, List]) -> Tuple[bool, Union[Error, Dict]]:
        if isinstance(res, list):
            for error in Error:
                if error.value == res[1]:
                    return False, error
            return False, Error.unknown
        return True, res

    async def get_host(self, user_id: Union[str, int]) -> Union[Host, Error]:
        route = f"{self._url}/{user_id}"
        res = await self._request(route, method="GET", headers=self.auth_header)

        answer = await self.check_answer(res)
        if not answer[0]:
            return answer[1]

        host = res["host"]
        return Host(**host)

    async def get_stats(self, user_id) -> Dict:
        return await self._request(f"{self._url}/{user_id}/stats", headers=self.auth_header)

    async def get_status(self, user_id) -> Dict:
        return await self._request(f"{self._url}/{user_id}/status", headers=self.auth_header)

@loader.tds
class HInfoMod(loader.Module):
    """Show userbot and host information"""

    strings = {
        "name": "HInfo",
        "loading_info": "⌛️ Loading...",
        "no_apikey": "🚫 No API Key set. Get token:\n\n1. Go to @hikkahost_bot\n2. Send /token\n3. Paste token to .config HH",
        "warn_sub_left": "🚫 Less than 5 days until subscription ends.\n",
        "statuses": {
            "running": "🟢",
            "stopped": "🔴",
        },
        "info": (
            "👤 Info for <code>{id}</code>\n"
            "📶 Status: {status}\n"
            "⚙️ Server: {server}\n"
            "❤️ The subscription expires after <code>{days_end} days</code>\n"
            "{stats}\n"
            "{warns}"
        ),
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue("custom_message", doc=lambda: self.strings("custom_msg"),),
            loader.ConfigValue("banner_url", "https://imgur.com/a/7LBPJiq.png"),
            loader.ConfigValue("show_heroku", True, validator=loader.validators.Boolean()),
            loader.ConfigValue("token", None, validator=loader.validators.Hidden()),
        )

    async def hinfo(self, message: Message):
        """Command to display info about userbot and host."""

        # Получение информации о юзерботе
        repo_info = ""
        try:
            repo = git.Repo(search_parent_directories=True)
            diff = repo.git.log([f"HEAD..origin/{version.branch}", "--oneline"])
            upd = "Update required" if diff else "Up to date"
        except Exception as e:
            upd = f"Error fetching repo info: {str(e)}"

        me = '<b><a href="tg://user?id={}">{}</a></b>'.format(
            self._client.hikka_me.id,
            utils.escape_html(get_display_name(self._client.hikka_me)),
        )
        build = utils.get_commit_url()
        _version = f'<i>{".".join(map(str, list(version.__version__)))}</i>'
        prefix = f"«<code>{utils.escape_html(self.get_prefix())}</code>»"
        platform = utils.get_named_platform()

        if self.config["token"] is None:
            await utils.answer(message, self.strings("no_apikey"))
            return

        token = self.config["token"]
        user_id = token.split(":")[0]
        api = HostAPI("https://api.hikka.host", token)

        host = await api.get_host(user_id)
        if isinstance(host, Error):
            await utils.answer(message, str(host))
            return

        status = await api.get_status(user_id)
        stats = (await api.get_stats(user_id))["stats"]
        working = status["status"] == "running"

        stats_info = ""
        if working:
            ram_usage = round(stats["memory_stats"]["usage"] / (1024 * 1024), 2)
            cpu_stats = stats["cpu_stats"]
            cpu_total_usage = cpu_stats['cpu_usage']['total_usage']
            system_cpu_usage = cpu_stats['system_cpu_usage']
            cpu_percent = round((cpu_total_usage / system_cpu_usage) * 100.0, 2)

            stats_info = f"<b>💾 Used now:</b> <code>{cpu_percent}%</code> CPU, <code>{ram_usage}MB</code> RAM\n"

        end_date = host.end_date.replace(tzinfo=timezone.utc)
        warns = ""
        days_end = (end_date - datetime.now(timezone.utc)).days
        if days_end < 5:
            warns += self.strings["warn_sub_left"]

        # Извлечение информации о сервере
        servers = await api.get_servers()
        server_info = servers["data"][host.server_id - 1]
        server = f"{FLAGS[server_info['country_code']]} {server_info['name']}"

        # Формирование окончательного сообщения
        full_info = (
            f"<b>🪐 Userbot Info</b>\n"
            f"{self.config['custom_message'].format(me=me, version=_version, build=build, prefix=prefix, platform=platform, upd=upd)}\n\n"
            f"{self.strings['info'].format(id=user_id, warns=warns, stats=stats_info, server=server, days_end=days_end, status=self.strings["statuses"][status["status"]])}"
        )

        await utils.answer(message, full_info)
