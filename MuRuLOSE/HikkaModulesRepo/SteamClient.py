import steam_web_api.steam_types
from telethon.types import Message
from telethon import TelegramClient
from .. import loader, utils
from steam_web_api import Steam
import steam_web_api
from datetime import datetime
import logging
from typing import Union
import asyncio

"""
    ███    ███ ██    ██ ██████  ██    ██ ██       ██████  ███████ ███████
    ████  ████ ██    ██ ██   ██ ██    ██ ██      ██    ██ ██      ██  
    ██ ████ ██ ██    ██ ██████  ██    ██ ██      ██    ██ ███████ █████
    ██  ██  ██ ██    ██ ██   ██ ██    ██ ██      ██    ██      ██ ██  
    ██      ██  ██████  ██   ██  ██████  ███████  ██████  ███████ ███████ 


    Module name
    📜 Licensed under the GNU AGPLv3	
"""

# meta banner: link
# meta desc: desc
# meta developer: @BruhHikkaModules
# requires: python-steam-api beautifulsoup4

logger = logging.getLogger(__name__)


@loader.tds
class SteamClient(loader.Module):
    """Module for manage steam"""

    strings = {
        "name": "SteamClient",
        "profile_data": "<emoji document_id=5936017305585586269>🪪</emoji> <b>Steam ID:</b> <code>{id}</code>"
        "\n<emoji document_id=5870994129244131212>👤</emoji> <b>Username:</b> <code>{username}</code>"
        "\n<emoji document_id=5933613451044720529>🙂</emoji> <b>Steam level:</b> <code>{level}</code>"
        "\n<emoji document_id=5879770735999717115>👤</emoji> <b>Profile URL:</b> <code>{profileurl}</code>"
        "\n<emoji document_id=5872829476143894491>🚫</emoji> <b>VAC-BAN INFO:</b> {vacinfo}"
        "\n<emoji document_id=5967412305338568701>📅</emoji> <b>Registration date:</b> <code>{registration_date}</code>",
        "api_key_updated": "<emoji document_id=5292226786229236118>🔄</emoji> <b>API key has been updated</b>",
        "vac_ban": (
            "\n    <b>VACBanned</b>: <code>{vacbanned}</code>"
            "\n    <b>Number of VAC-BANs</b>: <code>{numberofvacbans}</code>"
            "\n    <b>Days since last VAC-BAN</b>: <code>{dayslastvac}</code>"
            "\n    <b>Number of game bans</b>: <code>{numberofgamebans}</code>"
        ),
        "vac_ban_title": "<b>Information about bans of</b> <code>{}</code>:",
        "game_info_title": "<b>Information about games of</b> <code>{}</code>",
        "game_info_template": (
            "\n    <b>Name:</b> <code>{name}</code>"
            "\n    <b>Total playtime:</b> <code>{playtime_forever}</code>minutes"
            "\n    <b>Played in the last two weeks:</b> <code>{playtime_2weeks}</code>minutes"
            "\n    <b>Last launch:</b> <code>{lastplay}</code>"
        ),
        "widget": "<b>{nickname}</b> currently playing in <b>{gamename}</b>",
    }

    strings_ru = {
        "profile_data": "<emoji document_id=5936017305585586269>🪪</emoji> <b>Steam ID:</b> <code>{id}</code>"
        "\n<emoji document_id=5870994129244131212>👤</emoji> <b>Юзернейм:</b> <code>{username}</code>"
        "\n<emoji document_id=5933613451044720529>🙂</emoji> <b>Уроверь Steam:</b> <code>{level}</code>"
        "\n<emoji document_id=5879770735999717115>👤</emoji> <b>Профиль:</b> <code>{profileurl}</code>"
        "\n<emoji document_id=5872829476143894491>🚫</emoji> <b>VAC-BAN INFO:</b> {vacinfo}"
        "\n<emoji document_id=5967412305338568701>📅</emoji> <b>Дата регистрации:</b> <code>{registration_date}</code>",
        "api_key_updated": "<emoji document_id=5292226786229236118>🔄</emoji> <b>API ключ был обновлён</b>",
        "vac_ban": (
            "\n    <b>VACBanned</b>: <code>{vacbanned}</code>"
            "\n    <b>Число VAC-BANов</b>: <code>{numberofvacbans}</code>"
            "\n    <b>Дни с последнего VAC-BANа</b>: <code>{dayslastvac}</code>"
            "\n    <b>Число игровых банов</b>: <code>{numberofgamebans}</code>"
        ),
        "vac_ban_title": "<b>Информация о банах</b> <code>{}</code>:",
        "game_info_title": "<b>Информация о играх</b> <code>{}</code>",
        "game_info_template": (
            "\n    <b>Название:</b> <code>{name}</code>"
            "\n    <b>Наиграно всего:</b> <code>{playtime_forever}</code>мин"
            "\n    <b>Наиграно за последние 2 недели:</b> <code>{playtime_2weeks}</code>мин"
            "\n    <b>Последний запуск:</b> <code>{lastplay}</code>"
        ),
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "apikey",
                "aabbccddeeff1252345234",
                lambda: (
                    "Here's your api key"
                    "About API key: https://steamcommunity.com/dev/apikey"
                ),
                validator=loader.validators.Hidden(),
            ),
            loader.ConfigValue(
                "steamid",
                0,
                lambda: "Your steamid for widgets and other things",
                validator=loader.validators.Integer(),
            ),
        )
        self._widget_info = {"msgid": 0, "groupid": 0}
        self.debug = False

    async def client_ready(self, db, client):
        self.steam = Steam(self.config["apikey"])
        self.msgid = self.get("msgid", 0)
        self.groupid = self.get("groupid", 0)

    def resolve_id(self, username):
        data = self.steam.users.search_user(username)
        return data["player"]["steamid"]

    def get_user_data(
        self,
        username=Union[bool, str],
        uid: Union[int, bool] = 0,
        by_id: Union[bool, str] = None,
    ):
        if by_id:
            return self.steam.users.get_user_details(uid)["player"]
        else:
            return self.steam.users.search_user(username)["player"]

    @loader.command(ru_doc=" [Юзернейм] Найти пользователя (--id поиск по id)")
    async def searchuser(self, message: Message):
        """[Username] (--raw  raw json answer) (--id search by id) - Search user"""
        args = utils.get_args_raw(message).split()

        user = args[0]

        if not args:
            return await utils.answer(message, "noargs")

        userdata = None
        try:
            if "--id" in args:
                userdata = self.get_user_data(by_id=True, uid=int(user))["player"]
                level = self.steam.users.get_user_steam_level(int(user))["player_level"]
                vacdata = self.steam.users.get_player_bans(int(user))["players"][0]

            else:
                userdata = self.get_user_data(user)
                uid = self.resolve_id(user)
                level = self.steam.users.get_user_steam_level(uid)["player_level"]
                vacdata = self.steam.users.get_player_bans(uid)["players"][0]
        except ValueError:
            return await utils.answer(
                message, "this user not exist / no search results"
            )

        vacinfo = self.strings["vac_ban"].format(
            vacbanned=vacdata["VACBanned"],
            numberofvacbans=vacdata["NumberOfVACBans"],
            dayslastvac=vacdata["DaysSinceLastBan"],
            numberofgamebans=vacdata["NumberOfGameBans"],
        )

        account_created_date = datetime.fromtimestamp(userdata["timecreated"])
        account_created_formatted = account_created_date.strftime("%d.%m.%Y")
        await utils.answer_file(
            message,
            userdata["avatarfull"],
            caption=self.strings["profile_data"].format(
                id=userdata["steamid"],
                username=userdata["personaname"],
                level=level,
                profileurl=userdata["profileurl"],
                vacinfo=vacinfo,
                avatar=userdata["avatar"],
                registration_date=account_created_formatted,
            ),
        )

    @loader.command(
        ru_doc=" [Юзернейм] Информация о VAC-BANах пользователя (--id поиск по id)"
    )
    async def vacbaninfo(self, message: Message):
        """[Username] Informbation about user VAC-BANs (--id search by id)"""

        args = utils.get_args_raw(message).split()

        user = args[0]

        if not args:
            return await utils.answer(message, "noargs")
        try:
            if "--id" in args:
                userdata = self.get_user_data(by_id=True, uid=int(user))["player"]
                vacdata = self.steam.users.get_player_bans(int(user))["players"][0]

            else:
                userdata = self.get_user_data(user)
                uid = self.resolve_id(user)
                vacdata = self.steam.users.get_player_bans(uid)["players"][0]
        except ValueError:
            return await utils.answer(
                message, "this user not exist / no search results"
            )

        vacinfo = self.strings["vac_ban"].format(
            vacbanned=vacdata["VACBanned"],
            numberofvacbans=vacdata["NumberOfVACBans"],
            dayslastvac=vacdata["DaysSinceLastBan"],
            numberofgamebans=vacdata["NumberOfGameBans"],
        )

        vactitle = self.strings["vac_ban_title"]
        await utils.answer(
            message, response=vactitle.format(userdata["personaname"]) + vacinfo
        )

    @loader.command(
        ru_doc=" - [Юзернейм] Информация о играх пользователя (--id поиск по id)"
    )
    async def gameownedlist(self, message: Message):
        """- [Username] Informbation about user games (--id search by id)"""

        args = utils.get_args_raw(message).split()

        user = args[0]

        if not args:
            return await utils.answer(message, "noargs")

        try:
            if "--id" in args:
                userdata = self.get_user_data(by_id=True, uid=int(user))["player"]
                gamedata = self.steam.users.get_owned_games(user)["games"]

            else:
                userdata = self.get_user_data(user)
                uid = self.resolve_id(user)
                gamedata = self.steam.users.get_owned_games(uid)["games"]
        except ValueError:
            return await utils.answer(
                message, "this user not exist / no search results"
            )

        gameinfo_templates = []
        for info in gamedata:
            gameinfo = self.strings["game_info_template"].format(
                name=info["name"],
                playtime_forever=info["playtime_forever"],
                playtime_2weeks=info.get("playtime_2weeks") or 0,
                lastplay=info["rtime_last_played"],
            )

            gameinfo_templates.append(gameinfo)

        await utils.answer(
            message,
            response=self.strings["game_info_title"].format(userdata["personaname"])
            + "\n\n".join(gameinfo_templates),
        )

    @loader.loop(autostart=True, interval=10)
    async def updatewidget(self):
        if 0 not in [self.groupid, self.msgid]:
            gameid = self.get_user_data(by_id=True, uid=self.config["steamid"]).get(
                "gameid"
            )
            gamename = self.get_user_data(by_id=True, uid=self.config["steamid"]).get(
                "gameextrainfo"
            )
            await self.client.edit_message(
                self._widget_info["groupid"],
                self._widget_info["msgid"],
                self.strings["widget"].format(
                    nickname=self.get_user_data(by_id=True, uid=self.config["steamid"])[
                        "personaname"
                    ],
                    gamename=(
                        f"<a href='store.steampowered.com/app/{gameid}'>{gamename}</a>"
                        if gameid
                        else "nothing."
                    ),
                ),
            )

    @loader.command()
    async def setwidgetsteam(self, message: Message):
        """- Reply to message what need to be widget (--reset to remove widget)"""

        args = utils.get_args_raw(message)

        await utils.answer(
            message, "wait pls..."
        )  # into self.strings (translate description) and wait in all modules

        if self.config["steamid"] == 0:
            return await utils.answer(message, "no steamid in cfg")

        if not args:

            reply = await message.get_reply_message()
            msgid = reply.id
            chid = reply.chat_id

            self.set("msgid", msgid)
            self.set("groupid", chid)

            await utils.answer(
                message,
                "Info collected, message delete in 5 seconds, soon this message edit in widget",
            )

            await asyncio.sleep(5)

            await message.delete()

            gameid = self.get_user_data(by_id=True, uid=self.config["steamid"]).get(
                "gameid"
            )

            gamename = self.get_user_data(by_id=True, uid=self.config["steamid"]).get(
                "gameextrainfo"
            )

            await self.client.edit_message(
                self.groupid,
                self.msgid,
                self.strings["widget"].format(
                    nickname=self.get_user_data(by_id=True, uid=self.config["steamid"])[
                        "personaname"
                    ],
                    gamename=(
                        f"<a href='store.steampowered.com/app/{gameid}'>{gamename}</a>"
                        if gameid
                        else "nothing."
                    ),
                ),
            )
        else:
            self.set("msgid", 0)
            self.set("groupid", 0)

    @loader.command()
    async def execsteamcode(self, message: Message):
        """DO NOT USE THIS COMMAND! IT ONLY WORKS WHEN DEBUGGING IS ENABLED! THIS COMMAND IS FOR DEVELOPER"""
        if not self.debug:
            await utils.answer(
                message,
                "this command does nothing if debug-mode is not enabled."
                "don't try to use it."
                "even if you get into the code and enable debug-mode, all responsibility for actions with this command is yours.",
            )
        else:
            environment = {
                "client": self.steam,
                "widget_info": self._widget_info
                }
            args = utils.get_args_raw(message)

            await utils.answer(message, str(eval(args, environment)))

    @loader.command(ru_doc=" - Обновить API ключ")
    async def updateapikey(self, message: Message):
        """- Update API key"""
        self.steam = Steam(self.config["apikey"])
        await utils.answer(message, self.strings["api_key_updated"])
