# .------.------.------.------.------.------.------.------.------.------.
# |D.--. |4.--. |N.--. |1.--. |3.--. |L.--. |3.--. |K.--. |0.--. |0.--. |
# | :/\: | :/\: | :(): | :/\: | :(): | :/\: | :(): | :/\: | :/\: | :/\: |
# | (__) | :\/: | ()() | (__) | ()() | (__) | ()() | :\/: | :\/: | :\/: |
# | '--'D| '--'4| '--'N| '--'1| '--'3| '--'L| '--'3| '--'K| '--'0| '--'0|
# `------`------`------`------`------`------`------`------`------`------'
#
#                     Copyright 2023 t.me/D4n13l3k00
#           Licensed under the Creative Commons CC BY-NC-ND 4.0
#
#                    Full license text can be found at:
#       https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode
#
#                           Human-friendly one:
#            https://creativecommons.org/licenses/by-nc-nd/4.0

# meta developer: @D4n13l3k00

# requires: yt-dlp

import os

from telethon.tl.types import DocumentAttributeAudio
from yt_dlp import YoutubeDL
from yt_dlp.utils import (
    ContentTooShortError,
    DownloadError,
    ExtractorError,
    GeoRestrictedError,
    MaxDownloadsReached,
    PostProcessingError,
    UnavailableVideoError,
    XAttrMetadataError,
)

from .. import loader, utils  # type: ignore


@loader.tds
class YtDlMod(loader.Module):
    """Youtube-Dl Module"""

    strings = {
        "name": "Youtube-Dl",
        "preparing": "<b>[YouTube-Dl]</b> Preparing...",
        "downloading": "<b>[YouTube-Dl]</b> Downloading...",
        "working": "<b>[YouTube-Dl]</b> Working...",
        "exporting": "<b>[YouTube-Dl]</b> Exporting...",
        "reply": "<b>[YouTube-Dl]</b> No link!",
        "noargs": "<b>[YouTube-Dl]</b> No args!",
        "content_too_short": "<b>[YouTube-Dl]</b> Downloading content too short!",
        "geoban": "<b>[YouTube-Dl]</b> The video is not available "
        "for your geographical location due to geographical "
        "restrictions set by the website!",
        "maxdlserr": '<b>[YouTube-Dl]</b> The download limit is as follows: " oh ahah"',
        "pperr": "<b>[YouTube-Dl]</b> Error in post-processing!",
        "noformat": "<b>[YouTube-Dl]</b> Media is not available in "
        "the requested format",
        "xameerr": "<b>[YouTube-Dl]</b> {0.code}: {0.msg}\n{0.reason}",
        "exporterr": "<b>[YouTube-Dl]</b> Error when exporting video",
        "err": "<b>[YouTube-Dl]</b> {}",
        "err2": "<b>[YouTube-Dl]</b> {}: {}",
    }

    async def ripvcmd(self, m):
        """.ripv <link / reply_to_link> - download video"""
        await self.riper(m, "video")

    async def ripacmd(self, m):
        """.ripa <link / reply_to_link> - download audio"""
        await self.riper(m, "audio")

    async def riper(self, m, type):
        reply = await m.get_reply_message()
        args = utils.get_args_raw(m)
        url = args or reply.raw_text
        if not url:
            return await utils.answer(m, self.strings("noargs", m))
        m = await utils.answer(m, self.strings("preparing", m))
        if type == "audio":
            opts = {
                "format": "bestaudio",
                "addmetadata": True,
                "key": "FFmpegMetadata",
                "writethumbnail": True,
                "prefer_ffmpeg": True,
                "geo_bypass": True,
                "nocheckcertificate": True,
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "320",
                    }
                ],
                "outtmpl": "%(id)s.mp3",
                "quiet": True,
                "logtostderr": False,
            }
            video = False
            song = True
        elif type == "video":
            opts = {
                "format": "best",
                "addmetadata": True,
                "key": "FFmpegMetadata",
                "prefer_ffmpeg": True,
                "geo_bypass": True,
                "nocheckcertificate": True,
                "postprocessors": [
                    {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}
                ],
                "outtmpl": "%(id)s.mp4",
                "logtostderr": False,
                "quiet": True,
            }
            song = False
            video = True
        try:
            await utils.answer(m, self.strings("downloading", m))
            with YoutubeDL(opts) as rip:
                rip_data = rip.extract_info(url)
        except DownloadError as DE:
            return await utils.answer(m, self.strings("err", m).format(str(DE)))
        except ContentTooShortError:
            return await utils.answer(m, self.strings("content_too_short", m))
        except GeoRestrictedError:
            return await utils.answer(m, self.strings("geoban", m))
        except MaxDownloadsReached:
            return await utils.answer(m, self.strings("maxdlserr", m))
        except PostProcessingError:
            return await utils.answer(m, self.strings("pperr", m))
        except UnavailableVideoError:
            return await utils.answer(m, self.strings("noformat", m))
        except XAttrMetadataError as XAME:
            return await utils.answer(m, self.strings("xameerr", m).format(XAME))
        except ExtractorError:
            return await utils.answer(m, self.strings("exporterr", m))
        except Exception as e:
            return await utils.answer(
                m, self.strings("err2", m).format(str(type(e)), str(e))
            )
        if song:
            u = rip_data["uploader"] if "uploader" in rip_data else "Northing"
            await utils.answer(
                m,
                open(f"{rip_data['id']}.mp3.mp3", "rb"),
                supports_streaming=True,
                reply_to=reply.id if reply else None,
                attributes=[
                    DocumentAttributeAudio(
                        duration=int(rip_data["duration"]),
                        title=str(rip_data["title"]),
                        performer=u,
                    )
                ],
            )
            os.remove(f"{rip_data['id']}.mp3")
        elif video:
            await utils.answer(
                m,
                open(f"{rip_data['id']}.mp4", "rb"),
                reply_to=reply.id if reply else None,
                supports_streaming=True,
                caption=rip_data["title"],
            )
            os.remove(f"{rip_data['id']}.mp4")
