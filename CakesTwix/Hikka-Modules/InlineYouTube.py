"""

    █▀▀ ▄▀█ █▄▀ █▀▀ █▀ ▀█▀ █░█░█ █ ▀▄▀
    █▄▄ █▀█ █░█ ██▄ ▄█ ░█░ ▀▄▀▄▀ █ █░█

    Copyleft 2022 t.me/CakesTwix
    This program is free software; you can redistribute it and/or modify

"""

__version__ = (1, 2, 3)

# meta pic: https://img.icons8.com/bubbles/512/000000/youtube-play.png
# meta developer: @cakestwix_mods
# requires: yt_dlp aiohttp
# scope: hikka_min 1.1.11
# scope: hikka_only

import asyncio
import logging
import aiohttp
import os
from yt_dlp.utils import DownloadError
import yt_dlp
from telethon.tl.types import Message
from telethon import functions, types

from .. import loader, utils
from ..inline.types import InlineCall

logger = logging.getLogger(__name__)


def bytes2human(num, suffix="B"):
    if not num:
        return 0
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


def progressbar(iteration: int, length: int) -> str:
    percent = ("{0:." + str(1) + "f}").format(100 * (iteration / float(100)))
    filledLength = int(length * iteration // 100)
    return "█" * filledLength + "▒" * (length - filledLength)


@loader.tds
class YouTubeMod(loader.Module):
    """Download YouTube videos with video and audio quality selection"""

    strings = {
        "name": "InlineYouTube",
        "args": "🎞 <b>You need to specify link</b>",
        "downloading": "🎞 <b>Downloading...</b>",
        "not_found": "🎞 <b>Video not found...</b>",
        "no_qualt":"No quality",
        "format": "<b>Format</b>:",
        "ext": "<b>Ext</b>:",
        "video_codec": "<b>Video codec</b>:",
        "audio": "Audio",
        "file_size": "<b>File size</b>:",
        "uploading": "🎞 <b>Uploading File...</b>",
        "getting_info": "ℹ️ <b>Getting information about the video...</b>",
    }

    strings_ru = {
        "name": "InlineYouTube",
        "args": "🎞 <b>Вам необходимо указать ссылку</b>",
        "downloading": "🎞 <b>Скачиваю...</b>",
        "not_found": "🎞 <b>Видео не найдено...</b>",
        "no_qualt":"Нету такого качества",
        "format": "<b>Формат</b>:",
        "ext": "<b>Расширение</b>:",
        "video_codec": "<b>Видео кодек</b>:",
        "audio": "Аудио",
        "file_size": "<b>Размер</b>:",
        "uploading": "🎞 <b>Загружаю...</b>",
        "getting_info": "ℹ️ <bПолучаю информацию про видео...</b>",
    }

    async def client_ready(self, client, db):
        self._db = db
        self._client = client

    @loader.unrestricted
    async def ytcmd(self, message: Message):
        """[quality(144p/720p/etc)] <link> - Download video from youtube"""
        args = utils.get_args(message)
        await utils.answer(message, self.strings("getting_info"))

        if not args:
            return await utils.answer(message, self.strings("args"))

        with yt_dlp.YoutubeDL() as ydl:
            try:
                info_dict = ydl.extract_info(
                    args[1] if len(args) >= 2 else args[0], download=False
                )
            except DownloadError as e:
                return await utils.answer(message, e.msg)

            formats_list = [{"text": f"{item['format_note']} ({item['video_ext']})", "callback": self.format_change, "args": (item, info_dict, message.chat.id, item["format_id"],),} for item in info_dict["formats"] if item["ext"] in ["mp4", "webm"] and item["vcodec"] != "none" and (len(args) >= 2 and args[0] == item["format_note"] or len(args) < 2)]

            caption = f"<b>{info_dict['title']}</b>\n\n"
            # caption += info_dict["description"]

            await self.inline.form(text=caption if formats_list else self.strings["no_qualt"], photo=f"https://img.youtube.com/vi/{info_dict['id']}/0.jpg", message=message, reply_markup=utils.chunks(formats_list, 2))
            

    async def format_change(
        self,
        call: InlineCall,
        quality: dict,
        info_dict: dict,
        chat_id: int,
        format_id: int):
        string = f"{self.strings['format']} {quality['format']}\n"
        string += f"{self.strings['ext']} {quality['ext']}\n"
        string += f"{self.strings['video_codec']} {quality['vcodec']}\n"
        string += f"{self.strings['file_size']} {bytes2human(quality['filesize'])}\n"

        audio_keyboard = [{"text": f"{self.strings['audio']} ({audio['format_note']})", "callback": self.download, "args": (info_dict["id"], quality["ext"], quality["format_id"], audio["format_id"], chat_id,),} for audio in info_dict["formats"] if audio["ext"] == "m4a"]

        audio_keyboard.append(
            {
                "text": "Back",
                "callback": self.back,
                "args": (
                    info_dict,
                    chat_id,
                ),
            },
        )

        await call.edit(
            text=string,
            reply_markup=audio_keyboard,
        )

    async def back(self, call: InlineCall, info_dict: dict, chat_id: int):
        formats_list = [{"text": f"{item['format_note']} ({item['video_ext']})", "callback": self.format_change, "args": (item, info_dict, chat_id, item["format_id"]),} for item in info_dict["formats"] if item["ext"] in ["mp4", "webm"] and item["vcodec"] != "none"]

        caption = f"<b>{info_dict['title']}</b>\n\n"
        # caption += info_dict["description"]

        await call.edit(text=caption, reply_markup=utils.chunks(formats_list, 2))

    async def download(
        self,
        call: InlineCall,
        video_id: str,
        ext: str,
        video_format: int,
        audio_format: int,
        chat_id: int,
    ):
        meta = {}

        def download():
            nonlocal meta
            with yt_dlp.YoutubeDL(
                {
                    "format": "{}+{}".format(str(video_format), str(audio_format)),
                    "outtmpl": "%(resolution)s.%(id)s.%(ext)s",
                }
            ) as yd:
                meta = yd.extract_info(
                    "https://www.youtube.com/watch?v=" + video_id, download=False
                )
                yd.download("https://www.youtube.com/watch?v=" + video_id)

        await call.edit(
            text=f"{self.strings['downloading']}",
        )
        await utils.run_sync(download)

        await call.edit(
            text=f"{self.strings['uploading']}",
        )

        # Download thumb for video
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://img.youtube.com/vi/{meta['id']}/0.jpg") as resp:
                with open(meta['id'] + ".jpg", 'wb') as fd:
                    async for chunk in resp.content.iter_chunked(512):
                        fd.write(chunk)

        await self._client.send_file(
            chat_id,
            "{0}x{1}.{2}.{3}".format(
            (meta["width"]),
            (meta["height"]),
            (meta["id"]),
            (meta["ext"].replace("webm", "mkv")),
        ),
            supports_streaming=True,
            thumb=meta["id"] + ".jpg"
        )
        os.remove(
            "{0}x{1}.{2}.{3}".format(
                (meta["width"]),
                (meta["height"]),
                (meta["id"]),
                (meta["ext"].replace("webm", "mkv")),
            )
        )
        os.remove(meta["id"] + ".jpg")
        await call.delete()
