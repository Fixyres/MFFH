# `7MMM.     ,MMF'`7MMM.     ,MMF'   `7MMM.     ,MMF'              `7MM
# MMMb    dPMM    MMMb    dPMM       MMMb    dPMM                  MM
# M YM   ,M MM    M YM   ,M MM       M YM   ,M MM  ,pW"Wq.    ,M""bMM  ,pP"Ybd
# M  Mb  M' MM    M  Mb  M' MM       M  Mb  M' MM 6W'   `Wb ,AP    MM  8I   `"
# M  YM.P'  MM    M  YM.P'  MM mmmmm M  YM.P'  MM 8M     M8 8MI    MM  `YMMMa.
# M  `YM'   MM    M  `YM'   MM       M  `YM'   MM YA.   ,A9 `Mb    MM  L.   I8
# .JML. `'  .JMML..JML. `'  .JMML.   .JML. `'  .JMML.`Ybmd9'   `Wbmd"MML.M9mmmP'
#
# (c) 2023 — licensed under Apache 2.0 — https://www.apache.org/licenses/LICENSE-2.0

# meta pic: https://img.icons8.com/stickers/344/block.png
# meta developer: @mm_mods

__version__ = "1.2"

import asyncio
from hikka import loader, utils
import telethon as tt
from telethon.tl.types import Message
import logging

logger = logging.getLogger(__name__)


@loader.tds
class MiyaHostMod(loader.Module):
    """Module to manage your miyahost."""
    strings = {
        "name": "miyahost.manager",
        "error": "😵 <b>Error</b> ({}): {}",
        "success": "{} <b>Your container was successfully {}!</b> ({})",
        "err.NoAuthKeyProvided": "no auth key provided",
        "err.NoDBRecord": "you're not registered, not subscribed, or don't have a container",
        "err.Verlangsamt": "you're being rate limited. Try again at {}",
        "err.Banned": "you're banned from using this service",
        "err.InvalidAuthKey": "invalid auth key",
        "err.AuthNotEnabled": "API auth is not enabled",
        "err.APIServerDown": "API server isn't responding or down",
        "userinfo": "👤 <b>User</b> <code>{}</code>:\nSubscribed? {}\nBanned? {}",
        "err.NoUser": "no such user",
        "state.started": "started",
        "state.stopped": "stopped",
        "state.restarted": "restarted"
    }

    strings_ru = {
        "name": "miyahost.manager",
        "error": "😵 <b>Ошибка</b> ({}): {}",
        "success": "{} <b> Контейнер успешно {}!</b> ({})",
        "err.NoAuthKeyProvided": "не указан ключ авторизации",
        "err.NoDBRecord": "Вы не зарегистрированы, не подписаны или не имеете контейнера",
        "err.Verlangsamt": "Вы ограничены в использовании этого сервиса. Попробуйте снова в {}",
        "err.Banned": "Вы забанены",
        "err.InvalidAuthKey": "Неверный ключ авторизации",
        "err.AuthNotEnabled": "Авторизация по API не включена",
        "err.APIServerDown": "API сервер не отвечает или недоступен",
        "userinfo": "👤 <b>Пользователь</b> <code>{}</code>:\nПодписан? {}\nЗабанен? {}",
        "err.NoUser": "Нет такого пользователя",
        "_cls_doc": "Модуль для управлением вашим miyahost.",
        "_cmd_doc_mhinfo": "Отображает информацию о пользователе miyahost.",
        "_cmd_doc_mhstart": "Запускает ваш контейнер.",
        "_cmd_doc_mhstop": "Останавливает ваш контейнер.",
        "_cmd_doc_mhrestart": "Перезапускает ваш контейнер.",
        "state.started": "запущен",
        "state.stopped": "остановлен",
        "state.restarted": "перезапущен"
    }

    strings_de = {
        "name": "miyahost.manager",
        "error": "😵 <b>Fehler</b> ({}): {}",
        "success": "{} <b>Ihren Kontainer würde erfolgreich {}!</b> ({})",
        "err.NoAuthKeyProvided": "kein Authentifizierungsschlüssel angegeben",
        "err.NoDBRecord": "Sie sind nicht registriert, nicht abonniert oder haben keinen Container",
        "err.Verlangsamt": "Sie werden aufgrund von Rate-Limits eingeschränkt. Versuchen Sie es erneut um {}",
        "err.Banned": "Sie sind von der Nutzung dieses Dienstes ausgeschlossen",
        "err.InvalidAuthKey": "ungültiger Authentifizierungsschlüssel",
        "err.AuthNotEnabled": "API-Authentifizierung ist nicht aktiviert",
        "err.APIServerDown": "API-Server antwortet nicht oder ist nicht erreichbar",
        "userinfo": "👤 <b>Nutzer</b> <code>{}</code>:\nAbonniert? {}\nGebannt? {}",
        "err.NoUser": "kein solcher Nutzer",
        "_cls_doc": "Modul zum Ihren miyahost beheren.",
        "_cmd_doc_mhinfo": "Zeigt Informationen über den miyahost-Benutzer an.",
        "_cmd_doc_mhstart": "Startet Ihren Container.",
        "_cmd_doc_mhstop": "Stoppt Ihren Container.",
        "_cmd_doc_mhrestart": "Startet Ihren Container neu.",
        "state.started": "gestarted",
        "state.stopped": "gestoppt",
        "state.restarted": "neugestartet"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "auth_key",
                'NULL',
                lambda: "Basic auth key for miyahost API — get it via @miyahostbot using /hhttpauth",
                validator=loader.validators.Hidden(loader.validators.RegExp(r'[a-zA-Z0-9]+|NULL'))
            ),
            loader.ConfigValue(
                "mock_id",
                'NULL',
                lambda: "Enter another person's ID to rule it's container having it's auth key",
                validator=loader.validators.RegExp(r'[0-9]+|NULL')
            )
        )

    async def mhinfocmd(self, m: Message):
        """Get info about miyahost user."""
        if not utils.get_args_raw(m) and not m.is_reply:
            user = m.from_id
        elif utils.get_args_raw(m) and not m.is_reply:
            user = utils.get_args_raw(m)
        else:
            user = (await m.get_reply_message()).from_id

        try:
            import requests
            req = requests.get(f"http://129.151.220.181:41154/mhapi/{user}").json()
        except Exception as e:
            return await utils.answer(m, self.strings("error").format(500, self.strings('err.APIServerDown')))

        if list(req.keys())[0] == "error":
            req = req["error"]
            if req[0] == 404:
                return await utils.answer(m, self.strings("error").format(404, self.strings("err.NoUser")))

        else:
            req = req["OK"]
            useri = req[1]
            subscr = f"✅ ({useri['datumbis']})" if useri["activated"] else "❌"
            banned = "✅" if useri["banned"] else "❌"
            return await utils.answer(m, self.strings("userinfo").format(user, subscr, banned))

    async def mhstartcmd(self, m: Message):
        """Start miyahost container."""
        mock = False
        user = m.from_id
        if self.config["auth_key"] == 'NULL':
            return await utils.answer(m, self.strings("error").format(403, self.strings("err.NoAuthKeyProvided")))
        if self.config['mock_id'] != 'NULL':
            user = self.config['mock_id']
            mock = True

        try:
            import requests
            req = requests.get(
                f"http://129.151.220.181:41154/mhapi/controls/start/{user}",
                params={"basic_key": self.config["auth_key"]}
            ).json()
        except Exception as e:
            return await utils.answer(m, self.strings("error").format(500, self.strings('err.APIServerDown')))

        if list(req.keys())[0] == "error":
            req = req["error"]
            if req[0] == 404:
                logging.error(f'Failed with request to http://129.151.220.181:41154/mhapi/controls/start/{user}?basic_key={self.config["auth_key"]}, got {req[0]}')
                return await utils.answer(m, self.strings("error").format(404, self.strings("err.NoDBRecord")))
            elif req[0] == 401:
                logging.error(f'Failed with request to http://129.151.220.181:41154/mhapi/controls/start/{user}?basic_key={self.config["auth_key"]}, got {req[0]}')
                return await utils.answer(m, self.strings("error").format(401, self.strings("err.InvalidAuthKey")))
            elif req[0] == 429:
                logging.error(f'Failed with request to http://129.151.220.181:41154/mhapi/controls/start/{user}?basic_key={self.config["auth_key"]}, got {req[0]}')
                return await utils.answer(m, self.strings("error").format(429, self.strings("err.Verlangsamt").format(req[2])))
            elif req[0] == 403 and "banned" in req[1]:
                logging.error(f'Failed with request to http://129.151.220.181:41154/mhapi/controls/start/{user}?basic_key={self.config["auth_key"]}, got {req[0]}')
                return await utils.answer(m, self.strings("error").format(403, self.strings("err.Banned")))
            elif req[0] == 403:
                logging.error(f'Failed with request to http://129.151.220.181:41154/mhapi/controls/start/{user}?basic_key={self.config["auth_key"]}, got {req[0]}')
                return await utils.answer(m, self.strings("error").format(403, self.strings("err.AuthNotEnabled")))

        else:
            emoji = '(⚫) ▶' if mock else '▶'
            return await utils.answer(m, self.strings("success").format(emoji, self.strings("state.started"), user))

    async def mhstopcmd(self, m: Message):
        """Stop miyahost container."""
        user = m.from_id
        mock = False
        if self.config["auth_key"] == 'NULL':
            return await utils.answer(m, self.strings("error").format(403, self.strings("err.NoAuthKeyProvided")))
        if self.config['mock_id'] != 'NULL':
            user = self.config['mock_id']
            mock = True

        emoji = '(⚫) ⏸' if mock else '⏸'
        await utils.answer(m, self.strings("success").format(emoji, self.strings("state.stopped"), user))

        try:
            import requests
            req = requests.get(
                f"http://129.151.220.181:41154/mhapi/controls/stop/{user}",
                params={"basic_key": self.config["auth_key"]}
            ).json()
        except Exception as e:
            return await utils.answer(m, self.strings("error").format(500, self.strings('err.APIServerDown')))

        if list(req.keys())[0] == "error":
            req = req["error"]
            if req[0] == 404:
                logging.error(f'Failed with request to http://129.151.220.181:41154/mhapi/controls/start/{user}?basic_key={self.config["auth_key"]}, got {req[0]}')
                return await utils.answer(m, self.strings("error").format(404, self.strings("err.NoDBRecord")))
            elif req[0] == 401:
                logging.error(f'Failed with request to http://129.151.220.181:41154/mhapi/controls/start/{user}?basic_key={self.config["auth_key"]}, got {req[0]}')
                return await utils.answer(m, self.strings("error").format(401, self.strings("err.InvalidAuthKey")))
            elif req[0] == 429:
                logging.error(f'Failed with request to http://129.151.220.181:41154/mhapi/controls/start/{user}?basic_key={self.config["auth_key"]}, got {req[0]}')
                return await utils.answer(m, self.strings("error").format(429, self.strings("err.Verlangsamt").format(
                    req[2])))
            elif req[0] == 403 and "banned" in req[1]:
                logging.error(f'Failed with request to http://129.151.220.181:41154/mhapi/controls/start/{user}?basic_key={self.config["auth_key"]}, got {req[0]}')
                return await utils.answer(m, self.strings("error").format(403, self.strings("err.Banned")))
            elif req[0] == 403:
                logging.error(f'Failed with request to http://129.151.220.181:41154/mhapi/controls/start/{user}?basic_key={self.config["auth_key"]}, got {req[0]}')
                return await utils.answer(m, self.strings("error").format(403, self.strings("err.AuthNotEnabled")))

        else:
            return

    async def mhrestartcmd(self, m: Message):
        """Restart miyahost container."""
        user = m.from_id
        mock = False
        if self.config["auth_key"] == 'NULL':
            return await utils.answer(m, self.strings("error").format(403, self.strings("err.NoAuthKeyProvided")))
        if self.config['mock_id'] != 'NULL':
            user = self.config['mock_id']
            mock = True

        emoji = '(⚫) 🔁' if mock else '🔁'
        await utils.answer(m, self.strings("success").format(emoji, self.strings("state.restarted"), user))

        try:
            import requests
            req = requests.get(
                f"http://129.151.220.181:41154/mhapi/controls/restart/{user}",
                params={"basic_key": self.config["auth_key"]}
            ).json()
        except Exception as e:
            return await utils.answer(m, self.strings("error").format(500, self.strings('err.APIServerDown')))

        if list(req.keys())[0] == "error":
            req = req["error"]
            if req[0] == 404:
                logging.error(f'Failed with request to http://129.151.220.181:41154/mhapi/controls/start/{user}?basic_key={self.config["auth_key"]}, got {req[0]}')
                return await utils.answer(m, self.strings("error").format(404, self.strings("err.NoDBRecord")))
            elif req[0] == 401:
                logging.error(f'Failed with request to http://129.151.220.181:41154/mhapi/controls/start/{user}?basic_key={self.config["auth_key"]}, got {req[0]}')
                return await utils.answer(m, self.strings("error").format(401, self.strings("err.InvalidAuthKey")))
            elif req[0] == 429:
                logging.error(f'Failed with request to http://129.151.220.181:41154/mhapi/controls/start/{user}?basic_key={self.config["auth_key"]}, got {req[0]}')
                return await utils.answer(m, self.strings("error").format(429, self.strings("err.Verlangsamt").format(
                    req[2])))
            elif req[0] == 403 and "banned" in req[1]:
                logging.error(f'Failed with request to http://129.151.220.181:41154/mhapi/controls/start/{user}?basic_key={self.config["auth_key"]}, got {req[0]}')
                return await utils.answer(m, self.strings("error").format(403, self.strings("err.Banned")))
            elif req[0] == 403:
                logging.error(f'Failed with request to http://129.151.220.181:41154/mhapi/controls/start/{user}?basic_key={self.config["auth_key"]}, got {req[0]}')
                return await utils.answer(m, self.strings("error").format(403, self.strings("err.AuthNotEnabled")))

        else:
            return