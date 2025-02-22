# ---------------------------------------------------------------------------------
# Author: @shiro_hikka
# Name: Tracker
# Description: Tracks the change history of usernames and nicknames of users
# Commands: track, addtrack, deltrack, trackstat
# ---------------------------------------------------------------------------------
#              © Copyright 2025
#
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# ---------------------------------------------------------------------------------
# scope: hikka_only
# meta developer: @shiro_hikka
# meta banner: https://0x0.st/s/FIR0RnhUN5pZV5CZ6sNFEw/8KBz.jpg
# ---------------------------------------------------------------------------------

__version__ = (1, 1, 0)

from .. import loader, utils
from telethon.tl.types import Message
from ..inline.types import InlineCall
import datetime
import time as t
import re

@loader.tds
class Tracker(loader.Module):
    """Tracks the change history of usernames and nicknames of users"""

    strings = {
        "name": "Tracker",
        "enabled": "The tracker successfully enabled",
        "disabled": "The tracker successfully disabled",
        "no_user": "It seems this user doesn't exist, try another ID/Username",
        "change_status": "You just changed a status of tracking the user",
        "new_user": "You've successfully added a new user to track",
        "no_stat": "You're currently tracking no user",
        "only_one": "You're currently tracking only one user",
        "removed": "You've removed this user from the track list and each ID was descendingly replaced",
        "not_removed": "This user isn't added to the list so there's nobody to remove",
        "exists": "This user's already included in the track list, he's ID is {}",
        "cfg": "Specify a period of the cooldown between checks"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "Cooldown",
                120,
                lambda: self.strings["cfg"],
                validator = loader.validators.Integer()
            )
        )

    async def client_ready(self):
        if not self.db.get(__name__, "status"):
            self.db.set(__name__, "status", False)

        if not self.db.get(__name__, "users"):
            self.db.set(__name__, "users", {})

        if not self.db.get(__name__, "time"):
            self.db.set(__name__, "time", t.time())


    async def trackcmd(self, message: Message):
        """ Enable / Disable the tracking"""
        status = not(self.db.get(__name__, "status"))
        self.db.set(__name__, "status", status)

        if status is True:
            await utils.answer(message, self.strings["enabled"])

        else:
            await utils.answer(message, self.strings["disabled"])

    async def addtrackcmd(self, message: Message):
        """ <ID / Username> - add a new user to track"""
        args = utils.get_args_raw(message)
        users = self.db.get(__name__, "users")
        ID = len(users) + 1
        ID = str(ID)

        try:
            user = await self.client.get_entity(int(args) if args.isdigit() else args)

        except Exception:
            return await utils.answer(message, self.strings["no_user"])

        for _user in users:
            if users[_user]["user_id"] == user.id:
                return await utils.answer(message, self.strings["exists"].format(_user))

        UID = user.id
        nick = f"{user.first_name} {user.last_name}" if user.last_name else user.first_name
        username = f"@{user.username}" if user.username else "<i>Empty</i>"

        time = datetime.datetime.now()
        date = str(time.date()).split('-')
        hms = str(time.time()).split(':')

        users[ID] = {
            "nicks": [
                "[{}.{}.{} - {}:{}:{}] {}".format(
                    date[2], date[1], date[0], hms[0], hms[1], hms[2].split('.')[0], nick
                )
            ],
            "unames": [
                "[{}.{}.{} - {}:{}:{}] {}".format(
                    date[2], date[1], date[0], hms[0], hms[1], hms[2].split('.')[0], username
                )
            ],
            "active": True,
            "user_id": UID
        }

        self.db.set(__name__, "users", users)
        await utils.answer(message, self.strings["new_user"])

    async def deltrackcmd(self, message: Message):
        """ Remove user from the track list"""
        args = utils.get_args_raw(message)
        users = self.db.get(__name__, "users")
        if not users:
            return await utils.answer(message, self.strings["no_stat"]+"\nWho do you suppose to remove")

        try:
            user = await self.client.get_entity(int(args) if args.isdigit() else args)

        except Exception:
            return await utils.answer(message, self.strings["no_user"])


        for _user in users:
            if users[_user]["user_id"] == user.id:
                ID = int(_user)
                del users[_user]

                for i in range(ID, len(users)+1):
                    if i == ID:
                        continue

                    users[str(i-1)] = users.pop(str(i))

                self.db.set(__name__, "users", users)
                return await utils.answer(message, self.strings["removed"])

        await utils.answer(message, self.strings["not_removed"])

    async def trackstatcmd(self, message: Message):
        """ View the statistic about users you're tracking"""
        users = self.db.get(__name__, "users")
        if not users:
            return await utils.answer(message, self.strings["no_stat"])

        ID = "1"
        user = await self.client.get_entity(users[ID]["user_id"])
        status = "In progress" if users[ID]["active"] else "Inactive"

        text = (
            f"<b>ID:</b> <a href='tg://user?id={user.id}'>{user.id}</a>"+
            "\n\n     <b>Nicknames</b>\n"+
            "\n".join(users[ID]["nicks"])+
            "\n\n     <b>Usernames</b>\n"+
            "\n".join(users[ID]["unames"])
        )

        await self.inline.form(
            text=text,
            message=message,
            reply_markup=[
                [
                    {
                        "text": f"Tracking status: {status}",
                        "callback": lambda call: self.showStat(call, int(ID), "change_status")
                    }
                ],
                [
                    {
                        "text": "Previous user",
                        "callback": lambda call: self.showStat(call, int(ID), "previous")
                    },
                    {
                        "text": "Next user",
                        "callback": lambda call: self.showStat(call, int(ID), "next")
                    }
                ]
            ]
        )


    async def showStat(self, call: InlineCall, ID, action) -> None:
        users = self.db.get(__name__, "users")
        if not users:
            return await call.answer(self.strings["no_stat"])

        user = await self.client.get_entity(users[str(ID)]["user_id"])
        ID = ID + 1 if action == "next" else ID - 1 if action == "previous" else ID

        if ID == 0:
            ID = len(users)
        elif ID > len(users):
            ID = 1

        ID = str(ID)
        if action == "change_status":
            users[ID]["active"] = not(users[ID]["active"])
            await call.answer(self.strings["change_status"])

        else:
            if len(users) == 1:
                return await call.answer(self.strings["only_one"])

        status = "In progress" if users[ID]["active"] else "Inactive"
        self.db.set(__name__, "users", users)

        text = (
            f"<b>ID:</b> <a href='tg://user?id={user.id}'>{user.id}</a>"+
            "\n\n     <b>Nicknames</b>\n"+
            "\n".join(users[ID]["nicks"])+
            "\n\n     <b>Usernames</b>\n"+
            "\n".join(users[ID]["unames"])
        )

        await call.edit(
            text=text,
            reply_markup=[
                [
                    {
                        "text": f"Tracking status: {status}",
                        "callback": lambda call: self.showStat(call, int(ID), "change_status")
                    }
                ],
                [
                    {
                        "text": "Previous user",
                        "callback": lambda call: self.showStat(call, int(ID), "previous")
                    },
                    {
                        "text": "Next user",
                        "callback": lambda call: self.showStat(call, int(ID), "next")
                    }
                ]
            ]
        )


    async def watcher(self, message: Message):
        diff = t.time() - self.db.get(__name__, "time")
        if diff < self.config["Cooldown"]:
            return

        users = self.db.get(__name__, "users")
        if not users:
            return

        for user in users:
            if users[user]["active"] is False:
                continue

            entity = await self.client.get_entity(users[user]["user_id"])
            nick = f"{entity.first_name} {entity.last_name}" if entity.last_name else entity.first_name
            username = f"@{entity.username}" if entity.username else "<i>Empty</i>"

            time = datetime.datetime.now()
            date = str(time.date()).split('-')
            hms = str(time.time()).split(':')

            if nick != re.sub(r"\[.*\]", "", users[user]["nicks"][-1]).strip():
                users[user]["nicks"].append(
                    "[{}.{}.{} - {}:{}:{}] {}".format(
                        date[2], date[1], date[0], hms[0], hms[1], hms[2].split('.')[0], nick
                    )
                )

            if username != re.sub(r"\[.*\]", "", users[user]["unames"][-1]).strip():
                users[user]["unames"].append(
                    "[{}.{}.{} - {}:{}:{}] {}".format(
                        date[2], date[1], date[0], hms[0], hms[1], hms[2].split(',')[0], username
                    )
                )

            self.db.set(__name__, "users", users)
            self.db.set(__name__, "time", t.time())
