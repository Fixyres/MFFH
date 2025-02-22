# .------.------.------.------.------.------.------.------.------.------.
# |D.--. |4.--. |N.--. |1.--. |3.--. |L.--. |3.--. |K.--. |0.--. |0.--. |
# | :/\: | :/\: | :(): | :/\: | :(): | :/\: | :(): | :/\: | :/\: | :/\: |
# | (__) | :\/: | ()() | (__) | ()() | (__) | ()() | :\/: | :\/: | :\/: |
# | '--'D| '--'4| '--'N| '--'1| '--'3| '--'L| '--'3| '--'K| '--'0| '--'0|
# `------`------`------`------`------`------`------`------`------`------'
#
#                     Copyright 2022 t.me/D4n13l3k00
#           Licensed under the Creative Commons CC BY-NC-ND 4.0
#
#                    Full license text can be found at:
#       https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode
#
#                           Human-friendly one:
#            https://creativecommons.org/licenses/by-nc-nd/4.0

# meta developer: @D4n13l3k00


import datetime
import random
from asyncio import sleep

from telethon import events, functions
from telethon.errors.rpcerrorlist import YouBlockedUserError

from .. import loader, utils  # type: ignore


def register(cb):
    cb(RandomNSFWMod())


class RandomNSFWMod(loader.Module):
    """RndNsfw"""

    strings = {"name": "RndNsfw"}

    def __init__(self):
        self.name = self.strings["name"]
        self._me = None
        self._ratelimit = []

    async def client_ready(self, client, db):
        self._db = db
        self._client = client
        self.me = await client.get_me()

    async def crncmd(self, message):
        """
        Random pic from @wallhaven_nsfw
        """
        await message.edit("<b>_-*Wallhaven_NSFW*-_</b>")
        chat = "@wallhaven_nsfw"
        result = await message.client(
            functions.messages.GetHistoryRequest(
                peer=chat,
                offset_id=0,
                offset_date=datetime.datetime.now(),
                add_offset=random.choice(range(1, 101, 2)),
                limit=1,
                max_id=0,
                min_id=0,
                hash=0,
            )
        )
        await message.delete()
        await message.client.send_file(message.to_id, result.messages[0].media)

    async def crdcmd(self, message):
        """
        Random post from @dvach18
        """
        await message.edit("<b>_-*2ch_18+*-_</b>")
        chat = "@dvach18"
        result = await message.client(
            functions.messages.GetHistoryRequest(
                peer=chat,
                offset_id=0,
                offset_date=datetime.datetime.now(),
                add_offset=random.randint(0, 1000),
                limit=1,
                max_id=0,
                min_id=0,
                hash=0,
            )
        )
        await message.delete()
        await message.client.send_message(message.to_id, result.messages[0])

    async def crdbcmd(self, message):
        """
        Random post from @ru2ch_ban
        """
        await message.edit("<b>_-*2ch_Ban*-_</b>")
        chat = "@ru2ch_ban"
        result = await message.client(
            functions.messages.GetHistoryRequest(
                peer=chat,
                offset_id=0,
                offset_date=datetime.datetime.now(),
                add_offset=random.randint(0, 1000),
                limit=1,
                max_id=0,
                min_id=0,
                hash=0,
            )
        )
        await message.delete()
        await message.client.send_message(message.to_id, result.messages[0])

    async def crfncmd(self, message):
        """
        Random Furry from channel
        """
        links = ["https://t.me/joinchat/AAAAAEKWTxZPnvacazjM2Q"]
        await message.edit("<b>_-*Furry*-_</b>")
        chat = links[random.randint(0, len(links) - 1)]
        result = await message.client(
            functions.messages.GetHistoryRequest(
                peer=chat,
                offset_id=0,
                offset_date=datetime.datetime.now(),
                add_offset=random.randint(0, 1000),
                limit=1,
                max_id=0,
                min_id=0,
                hash=0,
            )
        )
        await message.delete()
        await message.client.send_message(message.to_id, result.messages[0])

    async def crhcmd(self, message):
        """
        Random Hentai from channels
        """
        #
        links = [
            "https://t.me/joinchat/AAAAAEWrsWbhMQppqTMNUw",
            "https://t.me/joinchat/AAAAAEkJjU8L9J6TDdkAIw",
            "@hentai",
        ]
        await message.edit("<b>_-*Hentai*-_</b>")
        chat = links[random.randint(0, len(links) - 1)]
        result = await message.client(
            functions.messages.GetHistoryRequest(
                peer=chat,
                offset_id=0,
                offset_date=datetime.datetime.now(),
                add_offset=random.randint(0, 1000),
                limit=1,
                max_id=0,
                min_id=0,
                hash=0,
            )
        )
        await message.delete()
        await message.client.send_message(message.to_id, result.messages[0])

    async def rh2dcmd(self, message):
        """
        Random Hentai2D pic/gif from @murglar_bot
        You can type category as argument(mustn't)
        """
        chat = "@murglar_bot"
        args = utils.get_args_raw(message)
        if args:
            arg = args
        else:
            arg = None
        await message.edit("<b>_-*Hentai_2D*-_</b>")
        async with message.client.conversation(chat) as conv:
            try:
                response = conv.wait_event(
                    events.NewMessage(incoming=True, from_users=507490514)
                )
                if arg:
                    m1 = await message.client.send_message(chat, f"/nudes2d {arg}")
                else:
                    m1 = await message.client.send_message(chat, f"/nudes2d")
                response = await response
            except YouBlockedUserError:
                await message.reply("<code>Unblock @murglar_bot</code>")
                return
            await message.delete()
            await m1.delete()
            await response.delete()
            await message.client.send_message(message.to_id, response.message)

    async def rn3dcmd(self, message):
        """
        Random Nudes3D from @murglar_bot
        """
        chat = "@murglar_bot"
        await message.edit("<b>_-*Nudes_3D*-_</b>")
        async with message.client.conversation(chat) as conv:
            try:
                response = conv.wait_event(
                    events.NewMessage(incoming=True, from_users=507490514)
                )
                m1 = await message.client.send_message(chat, "/nudes3d")
                response = await response
            except YouBlockedUserError:
                await message.reply("<code>Unblock @murglar_bot</code>")
                return
            await message.delete()
            await m1.delete()
            await response.delete()
            await message.client.send_message(message.to_id, response.message)
