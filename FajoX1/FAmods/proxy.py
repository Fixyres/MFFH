#   █▀▀ ▄▀█   █▀▄▀█ █▀█ █▀▄ █▀
#   █▀░ █▀█   █░▀░█ █▄█ █▄▀ ▄█

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: Proxy
# Description: Работа с прокси
# meta developer: @FAmods
# meta banner: https://github.com/FajoX1/FAmods/blob/main/assets/banners/proxy.png?raw=true
# requires: aiohttp
# ---------------------------------------------------------------------------------

import random
import aiohttp
import asyncio
import logging

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class Proxy(loader.Module):
    """Работа с прокси"""

    strings = {
        "name": "Proxy",

        "not_work_proxy": "<emoji document_id=5854929766146118183>❌</emoji> <b>Прокси не работает</b>",
        "no_args": "<emoji document_id=5854929766146118183>❌</emoji> <b>Нужно быть </b><code>{}{} {}</code>",
        "no_link": "<emoji document_id=5854929766146118183>❌</emoji> <b>Нету ссылки на прокси! Вставь её в </b><code>{}cfg proxy</code>",
        "incorrect_protocol": "<b>😕 Неверный протокол или его нету в нашей базе!</b>",
        "update_link": "<b>😕 Истек срок работы ссылки! Обнови её в </b><code>{}cfg proxy</code>",

        "searching_proxy": "<emoji document_id=5332518162195816960>🔄</emoji> <b>Ищю прокси...</b>",
        "checking_proxy": "<emoji document_id=5332518162195816960>🔄</emoji> <b>Проверяю прокси...</b>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "link",
                None,
                lambda: "Ссылка для получение прокси. Взять можно в https://advanced.name/ru/freeproxy",
            ),
            loader.ConfigValue(
                "check_work",
                True,
                lambda: "Проверять работу прокси?",
                validator=loader.validators.Boolean(),
            ),
        )


    async def client_ready(self, client, db):
        self.db = db
        self._client = client

    @loader.command()
    async def gproxy(self, message):
        """Получить рандомное прокси"""
        protocol = utils.get_args_raw(message)
        if not protocol:
            return await utils.answer(message, self.strings["no_args"].format(self.get_prefix(), "gproxy", "[протокол]"))

        if not self.config["link"]:
            return await utils.answer(message, self.strings["no_link"].format(self.get_prefix()))

        await utils.answer(message, self.strings['searching_proxy'])
        
        proxys_link = self.config["link"]

        params = {"type": protocol}

        async with aiohttp.ClientSession() as session:
            async with session.get(proxys_link) as res:
                proxys_default = await res.text()
                if not proxys_default:
                    return await utils.answer(message, self.strings['update_link'].format(self.get_prefix()))

        async with aiohttp.ClientSession() as session:
            async with session.get(proxys_link, params=params) as res:
                proxys = await res.text()

        if proxys_default == proxys:
            return await utils.answer(message, self.strings['incorrect_protocol'])
        
        proxys = proxys.split("\n")

        while True:
            proxy = random.choice(proxys)        
            proxy_ip = proxy.split(":")[0]
            proxy_port = proxy.split(":")[1]

            if not self.config['check_work']:
                break

            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get('http://example.com', proxy=f"{protocol}://{proxy_ip}:{proxy_port}", timeout=5) as res:
                        if res.status == 200:
                            break
            except:
                continue

        return await utils.answer(message, f"""<b>🌐 Рандомное прокси
                              
💾 Протокол: <code>{protocol}</code>
🖥 IP: <code>{proxy_ip}</code>
📟 Порт: <code>{proxy_port}</code>

{'<emoji document_id=5215191209131123104>💎</emoji> Модуль проверяет работоспособность прокси!' if self.config['check_work'] else ''}</b>""")
    
    @loader.command()
    async def wproxy(self, message):
        """Проверить работу прокси"""
        try:
            protocol, ip_port = utils.get_args_raw(message).split(" ")
            ip_port = ip_port.split(":")
            ip = ip_port[0]
            port = ip_port[1]
        except:
            return await utils.answer(message, self.strings["no_args"].format(self.get_prefix(), "wproxy", "[протокол] [айпи:порт]"))

        await utils.answer(message, self.strings['checking_proxy'])

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('http://example.com', proxy=f"{protocol}://{ip}:{port}", timeout=5) as res:
                    if res.status == 200:
                        return await utils.answer(message, f"""<emoji document_id=6334758581832779720>✅</emoji> <b>Прокси работает!</b>""")
                    else:
                        return await utils.answer(message, self.strings['not_work_proxy'])
        except:
            return await utils.answer(message, self.strings['not_work_proxy'])