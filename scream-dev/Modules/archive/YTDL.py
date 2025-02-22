#           __..--''``---....___   _..._    __
# /// //_.-'    .-/";  `        ``<._  ``.''_ `. / // /
#///_.-' _..--.'_    \                    `( ) ) // //
#/ (_..-' // (< _     ;_..__               ; `' / ///
# / // // //  `-._,_)' // / ``--...____..-' /// / //
# 🐈 Module writed @ScreamDev 
# 👌 Channel @ScreamModules
# 🧨 Blog: @ScreamDevBlog

import io
import os
from asyncio import sleep

from requests import get
from telethon import events, functions
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.types import MessageEntityTextUrl, MessageEntityUrl

from .. import loader, utils

@loader.tds
class DownloaderMod(loader.Module):
    """Downloader YT module"""

    strings = {"name": "YTDL"}

    async def dlytcmd(self, message):
        """YouTubeDownload"""
        chat = "@SaveFromVkBot"
        reply = await message.get_reply_message()
        async with message.client.conversation(chat) as conv:
            text = utils.get_args_raw(message)
            if reply:
                text = await message.get_reply_message()
            await message.edit("<b>Downloading...</b>")
            try:
                response = conv.wait_event(
                    events.NewMessage(incoming=True, from_users=6049010225)
                )
                response2 = conv.wait_event(
                    events.NewMessage(incoming=True, from_users=6049010225)
                )
                response3 = conv.wait_event(
                    events.NewMessage(incoming=True, from_users=6049010225)
                )
                mm = await message.client.send_message(chat, text)
                response = await response
                response2 = await response2
                response3 = await response3
                await mm.delete()
            except YouBlockedUserError:
                await message.edit("<code>Разблокируй @SaveFromVkBot</code>")
                return
            await message.client.send_file(
                message.to_id, response3.media, reply_to=reply
            )
            await message.delete()
            await message.client(
                functions.messages.DeleteHistoryRequest(
                    peer="ttsavebot", max_id=0, just_clear=False, revoke=True
                )
            )
