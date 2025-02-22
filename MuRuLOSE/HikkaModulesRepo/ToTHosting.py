from telethon.types import Message
from telethon.tl.types import DocumentAttributeFilename
from .. import loader, utils

import logging
import aiohttp

"""
    ███    ███ ██    ██ ██████  ██    ██ ██       ██████  ███████ ███████
    ████  ████ ██    ██ ██   ██ ██    ██ ██      ██    ██ ██      ██  
    ██ ████ ██ ██    ██ ██████  ██    ██ ██      ██    ██ ███████ █████
    ██  ██  ██ ██    ██ ██   ██ ██    ██ ██      ██    ██      ██ ██  
    ██      ██  ██████  ██   ██  ██████  ███████  ██████  ███████ ███████ 

                                   
    Module Name
"""

# scopes:

# 🔒      Licensed under the GNU AGPLv3

# meta banner: link
# meta desc: desc
# meta developer: @BruhHikkaModules

logger = logging.getLogger(__name__)


class UserInfo:
    def __init__(self, userbots, regdate, balance):
        self.userbots = userbots
        self.regdate = regdate
        self.balance = balance


    def __repr__(self):
        return f"UserInfo(userbots={self.userbots}, regdate={self.regdate}, balance={self.balance})"

class UserbotInfo:
    def __init__(self, name, emojistatus, status, serveremoji, server, time):
        self.name = name
        self.emojistatus = emojistatus
        self.status = status
        self.serveremoji = serveremoji
        self.server = server
        self.time = time


    def __repr__(self):
        return f"UserbotInfo(name={self.name}, emojistatus={self.emojistatus}, status={self.status}, serveremoji={self.serveremoji}, server={self.server}, time={self.time})"


class TothostAPI:
    def __init__(self, token):
        self._token = token


    async def logs(self, ub_id):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.tothost.live/api/v1/userbot/get_logs?userbotID={ub_id}&token={self._token}") as response:
                return bytes(await response.text(), encoding='utf-8')

    async def userbotstatus(self, ub_id):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.tothost.live/api/v1/userbot/status?userbotID={ub_id}&token={self._token}") as response:
                if dict(await response.json())['status'] == "active":
                    return True
                else:
                    return False

    async def userbotinfo(self, ub_id):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.tothost.live/api/v1/userbot/userbot_info?userbotID={ub_id}&token={self._token}") as response:
                data = await response.json()
                ubstatus = await self.userbotstatus(ub_id)
                enddate = data['endDate']
                

                name = data['name']
                emojistatus = "🟢" if ubstatus else "🔴"
                status ="Включен" if ubstatus else "Выключен"
                serveremoji = data['server']['emoji']
                server = data['server']['text']
                time = f"{enddate['year']}-{enddate['month']}-{enddate['day']} {enddate['hour']}:{enddate['minute']}:{enddate['second']}"

                return UserbotInfo(name, emojistatus, status, serveremoji, server, time)

    async def restart(self, ub_id):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.tothost.live/api/v1/userbot/restart?userbotID={ub_id}&token={self._token}"):
                return True


    async def userinfo(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.tothost.live/api/v1/user/user_info?token={self._token}") as response:
                data = await response.json()
                userbots = [str(userbot['userbotID']) for userbot in data['userbots']]

                regdate = data['registeredDate'][:10]

                balance = data['balance']

                return UserInfo(userbots, regdate, balance)


@loader.tds
class ToTHosting(loader.Module):
    """Module for interaction with ToTHosting API (obviously) """

    strings = {
        "name": "ToTHosting",
        "userbot_info": (
            "<blockquote><b>🌟Информация о юзерботе🌟</b></blockquote>"
            "\n"
            "<blockquote><b>🤖 Юзербот: {}</b></blockquote>"
            "\n"
            "<blockquote><b>{} Статус: {}</b></blockquote>"
            "\n"
            "<blockquote><b>{} Сервер: {}</b></blockquote>"
            "\n"
            "<blockquote><b>⏰ Подписка истекает: <code>{}</code></b></blockquote>"
        ),
        "wait": "<emoji document_id=6334358870701376795>⌛️</emoji> Подождите пожалуйста",
        "userinfo": (
            "<blockquote><b>🌟 Информация о юзере 🌟</b></blockquote>"
            "\n"
            "<blockquote><b>🤖 Юзерботы: {}</b></blockquote>"
            "\n"
            "<blockquote><b>💸 Баланс: <code>{}</code></b></blockquote>"
            "\n"
            "<blockquote><b>🎂 Дата регистрации: {}</b></blockquote>"
        )
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "token",
                "None",
                lambda: "Получите ваш токен в: https://t.me/ToThosTing_bot (/get_token)",
                validator=loader.validators.Hidden()
            ),
            loader.ConfigValue(
                "defaultid",
                123,
                lambda: "Айди по-умолчанию",
                validator=loader.validators.Hidden(loader.validators.Integer())
            )
        )

    @loader.loop(interval=5, autostart=True)
    async def autoupdatetoken(self):
        self.api = TothostAPI(token=self.config['token'])
    
    # async def client_ready(self, client, db):
        # self.get("token_ready", False) soon
        
        
    @loader.command()
    async def tinfocmd(self, message: Message):
        """ [id/None] - Get info about your userbot"""
        args = utils.get_args_raw(message)

        if not args:
            args = self.config['defaultid']
        
        await utils.answer(message, self.strings["wait"])

        data = await self.api.userbotinfo(ub_id=args)

        

        await utils.answer(
            message,
            self.strings['userbot_info'].format(
                data.name,
                data.emojistatus,
                data.status,
                data.serveremoji,
                data.server,
                data.time
            )
        )

    @loader.command()
    async def tlogscmd(self, message: Message):
        ''' [id/None] - Get logs of your userbot'''
        args = utils.get_args_raw(message)

        if not args:
            args = self.config['defaultid']

        await utils.answer(message, self.strings["wait"])

        logs = await self.api.logs(ub_id=args)

        attributes = [
            DocumentAttributeFilename("logs.html")
        ]

        await utils.answer_file(message, logs,"<emoji document_id=5226512880362332956>📖</emoji> Here you go!", attributes=attributes)
        
    
    @loader.command()
    async def trestartcmd(self, message: Message):
        ''' [id/None] - Restart the userbot'''

        args = utils.get_args_raw(message)

        if not args:
            args = self.config['defaultid']

        await utils.answer(message, self.strings["wait"])

        await self.api.restart(args)


        
    @loader.command()
    async def tuserinfo(self, message: Message):
        ''' - Info about user'''
        
        await utils.answer(message, self.strings["wait"])

        userinfo = await self.api.userinfo()

        await utils.answer(
            message,
            self.strings["userinfo"].format(
                ' '.join(userinfo.userbots),
                userinfo.balance,
                userinfo.regdate
            )
        )