"""

    █▀▀ ▄▀█ █▄▀ █▀▀ █▀ ▀█▀ █░█░█ █ ▀▄▀
    █▄▄ █▀█ █░█ ██▄ ▄█ ░█░ ▀▄▀▄▀ █ █░█

    Copyleft 2022 t.me/CakesTwix
    This program is free software; you can redistribute it and/or modify

"""

__version__ = (1, 0, 0)

# requires: spotdl
# meta pic: https://cdn-icons-png.flaticon.com/512/2111/2111624.png
# meta developer: @cakestwix_mods
# scope: hikka_only

import os
import subprocess
import logging
import asyncio
import spotdl
from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class InlineSpotifyDownloaderMod(loader.Module):
    """Module for downloading music from Spotify"""

    strings = {
        "name": "InlineSpotifyDownloader",
        "cfg_spotdl_path": "Path to spotdl bin",
        "no_args": "🎞 <b>You need to specify link</b>",
        "no_track": "🎞 <b>You need to specify track link</b>",
        "downloading": "🎞 <b>Downloading...</b>",
        "no_spotdl": "🚫 <b>Spotdl not found... Check config or install spotdl (<code>.terminal pip install spotdl</code>)</b>",
        "not_found": "🎧 <b>Music not found...</b>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            "CONFIG_SPOTDL_PATH",
            "~/.local/bin/spotdl",
            lambda: self.strings("cfg_spotdl_path"),
        )

    async def spotdlcmd(self, message):
        """Download music from Spotify (Only tracks)"""
        if not (args := utils.get_args_raw(message)):
            return await utils.answer(message, self.strings["no_args"])
        if "https://open.spotify.com/track/" not in args:
            return await utils.answer(message, self.strings["no_track"])

        # Try write command
        await utils.answer(message, self.strings["downloading"])
        proc = await asyncio.create_subprocess_shell(
            self.config["CONFIG_SPOTDL_PATH"] + " " + args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        # Pass one line
        _ = await proc.stdout.readline()

        # Get console strings
        line = (await proc.stdout.readline()).decode().rstrip()

        await proc.wait()

        # Check "not found" error
        err = await proc.stderr.readline()
        if ": not found" in err.decode():
            return await utils.answer(message, self.strings["no_spotdl"]) 

        # Try get youtube video id
        if "https://www.youtube.com/watch?v=" in line and len(line.split("https://www.youtube.com/watch?v=")) == 2:
            photo_id = line.split("https://www.youtube.com/watch?v=")[1]
        elif "as it's already downloaded" in line:
            photo_id = None
        else:
            return await utils.answer(message, self.strings["not_found"])


        # Get track name and send message
        track_name = line.split('"')[1]
        await self.inline.form(
            text=line,
            photo=f"https://img.youtube.com/vi/{photo_id}/maxresdefault.jpg" if photo_id else None,
            message=message,
            reply_markup=[{"text": "Upload", "callback": self.inline__upload, "args": (track_name, message.chat.id)}]
        )
    
    async def inline__upload(self, call, track_name, chat_id):
        with open(track_name + ".mp3","rb",) as input_file:
            content = input_file.read()
            input_file.seek(0)
            await self._client.send_file(
                chat_id,
                track_name + ".mp3"
            )
            os.remove(track_name + ".mp3")
            await call.delete()