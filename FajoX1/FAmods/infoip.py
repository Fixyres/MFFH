#   █▀▀ ▄▀█   █▀▄▀█ █▀█ █▀▄ █▀
#   █▀░ █▀█   █░▀░█ █▄█ █▄▀ ▄█

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: InfoIP
# Description: Информация об IP адресе
# meta developer: @FAmods
# meta banner: https://github.com/FajoX1/FAmods/blob/main/assets/banners/infoip.png?raw=true
# requires: ipinfo
# ---------------------------------------------------------------------------------

import ipinfo
import asyncio
import logging

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class InfoIP(loader.Module):
    """Информация об IP адресе"""

    strings = {
        "name": "InfoIP",

        "no_ip": "<emoji document_id=5854929766146118183>❌</emoji> <b>Должно быть .ipi [айпи]</b>",
        "no_token": "<emoji document_id=5854929766146118183>❌</emoji> <b>Нету токена! Поставь его в <code>{}cfg InfoIP</code></b>",
        "invalid_token": "<b>😕 Неверный токен</b>",
        "invalid_ip": "<b>😕 Неверный IP</b>",

        "searching_info": "<emoji document_id=5326015457155620929>🔄</emoji> <b>Получаю информацию...</b>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "api_token",
                None,
                lambda: "Токен для работы с API. Взять можно на сайте https://ipinfo.io/account/token",
                validator=loader.validators.Hidden(loader.validators.String()),
            ),
        )


    async def client_ready(self, client, db):
        self.db = db
        self._client = client

    @loader.command()
    async def ipi(self, message):
        """Информация об IP"""

        ip = utils.get_args_raw(message)
        if not ip:
            return await utils.answer(message, self.strings["no_ip"])

        if not self.config["api_token"]:
            return await utils.answer(message, self.strings["no_token"].format(self.get_prefix()))

        await utils.answer(message, self.strings['searching_info'])
            
        access_token = self.config["api_token"]
        handler = ipinfo.getHandler(access_token)

        try:
           info = handler.getDetails(ip)
        except ipinfo.error.APIError:
            return await utils.answer(message, self.strings['invalid_token'])
        except ValueError:
            return await utils.answer(message, self.strings['invalid_ip'])

        return await utils.answer(message, f"""<b>
🌐 Информация об IP

<emoji document_id=6334617384782923882>📟</emoji> IP: <code>{info.ip}</code>

⛰ Регион: <code>{info.region}</code>
🏙 Город: <code>{info.city}</code>
🗺 Страна: {info.country_flag['emoji']} <code>{info.country_name} ({info.country})</code>
🗺 Континент: <code>{info.continent['name']} ({info.continent['code']})</code>
🧾 Пост-код: <code>{info.postal}</code>
                                  
🏛 Организация: <code>{info.org}</code>

🪙 Валюта: <code>{info.country_currency['code']} ({info.country_currency['symbol']})</code>
                                  
🏕 Место: <code>{info.loc}</code>                       
<emoji document_id=6334427547228440889>🕒</emoji> Часовой пояс: <code>{info.timezone}</code>                         
</b>""")