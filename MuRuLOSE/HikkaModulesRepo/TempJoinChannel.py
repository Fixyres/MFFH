from telethon.types import Message
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest

from .. import loader, utils

"""
    ███    ███ ██    ██ ██████  ██    ██ ██       ██████  ███████ ███████
    ████  ████ ██    ██ ██   ██ ██    ██ ██      ██    ██ ██      ██  
    ██ ████ ██ ██    ██ ██████  ██    ██ ██      ██    ██ ███████ █████
    ██  ██  ██ ██    ██ ██   ██ ██    ██ ██      ██    ██      ██ ██  
    ██      ██  ██████  ██   ██  ██████  ███████  ██████  ███████ ███████ 

                                   
    TempJoinChannel
"""

# 🔒      Licensed under the GNU AGPLv3

# meta banner: https://raw.githubusercontent.com/MuRuLOSE/HikkaModulesRepo/main/assets/modbanners/tempjoinchannel.png
# meta desc: Enter the channels temporarily!
# meta developer: @BruhHikkaModules


@loader.tds
class TempJoinChannel(loader.Module):
    """Enter the channels temporarily!"""

    strings = {
        "name": "TempJoinChannel",
        "added": "<emoji document_id=5206607081334906820>✔️</emoji> Channels added",
        "leaved": "<emoji document_id=5974506040828366250>🚪</emoji> <i>All the channels have disappeared...</i>"
    }   
    strings_ru = {
        "_cls_doc": "Входи в каналы временно!",
        "added": "<emoji document_id=5206607081334906820>✔️</emoji> Каналы добавлены",
        "leaved": "<emoji document_id=5974506040828366250>🚪</emoji> <i>Все каналы исчезли...</i>"
    }

    async def client_ready(self, client, db):
        self.db = db


    def __init__(self):
        self._lock = False # if cleaning channels, cmd locking
        self._channels = self.pointer("channels", [])

    @loader.command(
        ru_doc="Добавь каналы, напишите в аргументы слово inline если нужны каналы оттуда. Либо перечислите любые признаки канала (айди, ссылки, юзернеймы). Inline dont work"
    )
    async def addchannels(self, message: Message):
        """ - Add channels, put the word inline in the arguments if you need channels from there. Or list any channel attributes (ids, links, usernames). (Inline dont work)"""
        args = utils.get_args_raw(message)

        if "inline" in args:
            pass
        else:
            channels = args.split()
            for channel in channels:
                if channel not in self._channels:
                    self._channels.extend(str(channel))
                    await self.client(JoinChannelRequest(channel))
                else:
                    pass
            
        await utils.answer(message, self.srtings["added"])

    @loader.command(
        ru_doc="Покинуть все каналы которые были добавлены"
    )
    async def leavechannels(self, message: Message):
        """ - Leave all channels that have been added"""
        for channel in self._channels:
            self._channels.remove(str(channel))
            await self.client(LeaveChannelRequest(channel))

        await utils.answer(message, self.strings["leaved"])
        

        
