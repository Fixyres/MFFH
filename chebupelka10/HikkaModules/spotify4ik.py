# This is fixed copy of module. Credits: https://raw.githubusercontent.com/hikariatama/ftg/master/spotify.py
# meta developer: @MiSidePlayer

import asyncio
import contextlib
import functools
import io
import logging
import re
import time
import traceback
from math import ceil
from types import FunctionType

import yt_dlp
import aiohttp
from telethon import types
import tempfile
import os

import requests
import spotipy
from hikkatl.errors.rpcerrorlist import FloodWaitError
from hikkatl.tl.functions.account import UpdateProfileRequest
from hikkatl.tl.types import Message
from PIL import Image, ImageDraw, ImageFont

from .. import loader, utils

logger = logging.getLogger(__name__)
logging.getLogger("spotipy").setLevel(logging.CRITICAL)


SIZE = (1200, 320)
INNER_MARGIN = (16, 16)

TRACK_FS = 48
ARTIST_FS = 32


@loader.tds
class Spotify4ikMod(loader.Module):
    """Display beautiful spotify now bar. Idea: t.me/fuccsoc. Implementation: t.me/hikariatama. Fixed by @MiSidePlayer."""

    strings = {
        "name": "Spotify4ik",
        "need_auth": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>Выполни"
            " </b><code>.sauth</code><b> перед выполнением этого действия.</b>"
        ),
        "on-repeat": (
            "<emoji document_id=5469741319330996757>💫</emoji> <b>Повторение трека"
            " включено.</b>"
        ),
        "off-repeat": (
            "<emoji document_id=5472354553527541051>✋</emoji> <b>Повторение трека"
            " выключено.</b>"
        ),
        "skipped": (
            "<emoji document_id=5471978009449731768>👉</emoji> <b>Трек переключен на следующий.</b>"
        ),
        "err": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>Произошла ошибка."
            " Убедитесь, что музыка играет!</b>\n<code>{}</code>"
        ),
        "already_authed": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>Уже авторизован</b>"
        ),
        "authed": (
            "<emoji document_id=5294137402430858861>🎵</emoji> <b>Успешная"
            " аутентификация</b>"
        ),
        "playing": "<emoji document_id=5294137402430858861>🎵</emoji> <b>Продолжил играть трек...</b>",
        "back": (
            "<emoji document_id=5469735272017043817>👈</emoji> <b>Переключил трек назад</b>"
        ),
        "paused": "<emoji document_id=5469904794376217131>🤚</emoji> <b>Поставил паузу на текущий трек</b>",
        "deauth": (
            "<emoji document_id=6037460928423791421>🚪</emoji> <b>Успешный выход из"
            " аккаунта</b>"
        ),
        "restarted": (
            "<emoji document_id=5469735272017043817>👈</emoji> <b>Начал трек"
            " сначала</b>"
        ),
        "auth": (
            '<emoji document_id=5472308992514464048>🔐</emoji> <a href="{}">Пройдите по этой'
            " ссылке</a>, разрешите вход, затем введите <code>.scode https://...</code> с"
            " ссылкой которую вы получили."
        ),
        "liked": (
            '<emoji document_id=5199727145022134809>❤️</emoji> <b>Поставил "Мне'
            ' нравится" текущему треку</b>'
        ),
        "autobio": (
            "<emoji document_id=5334673106202010226>✏️</emoji> <b>Обновление био"
            " {}</b>"
        ),
        "404": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>Нет результатов</b>"
        ),
        "playing_track": (
            "<emoji document_id=5294137402430858861>🎵</emoji> <b>Трек {} добавлен в"
            " очередь</b>"
        ),
        "no_music": (
            "<emoji document_id=5312526098750252863>🚫</emoji> <b>Музыка не играет!</b>"
        ),
        "searching": (
            "<emoji document_id=5188311512791393083>🔎</emoji> <b>Ищу трек на Spotify, почти готово!</b>"
        ),
        "currently_on": "Cлушаю на",
        "playlist": "Плейлист",
        "owner": "Владелец",
        "quality": "Качество",
    }

    def __init__(self):
        self._client_id = "e0708753ab60499c89ce263de9b4f57a"
        self._client_secret = "80c927166c664ee98a43a2c0e2981b4a"
        self.scope = (
            "user-read-playback-state playlist-read-private playlist-read-collaborative"
            " app-remote-control user-modify-playback-state user-library-modify"
            " user-library-read"
        )
        self.sp_auth = spotipy.oauth2.SpotifyOAuth(
            client_id=self._client_id,
            client_secret=self._client_secret,
            redirect_uri="https://thefsch.github.io/spotify/",
            scope=self.scope,
        )
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "AutoBioTemplate",
                "🎧 {track} - {author} ───○ 🔊 ᴴᴰ",
                lambda: "Шаблон для обновления био",
            )
        )

    def create_bar(self, current_playback: dict) -> str:
        try:
            percentage = ceil(
                current_playback["progress_ms"]
                / current_playback["item"]["duration_ms"]
                * 100
            )
            bar_filled = ceil(percentage / 10) - 1
            bar_empty = 10 - bar_filled - 1
            bar = "".join("─" for _ in range(bar_filled)) + "🞆"
            bar += "".join("─" for _ in range(bar_empty))

            bar += (
                f' {current_playback["progress_ms"] // 1000 // 60:02}:{current_playback["progress_ms"] // 1000 % 60:02} /'
            )
            bar += (
                f' {current_playback["item"]["duration_ms"] // 1000 // 60:02}:{current_playback["item"]["duration_ms"] // 1000 % 60:02}'
            )
        except Exception:
            bar = "──────🞆─── 0:00 / 0:00"

        return bar

    @staticmethod
    def create_vol(vol: int) -> str:
        volume = "─" * (vol * 4 // 100)
        volume += "○"
        volume += "─" * (4 - vol * 4 // 100)
        return volume

    async def create_badge(self, thumb_url: str, title: str, artist: str) -> bytes:
        thumb = Image.open(
            io.BytesIO((await utils.run_sync(requests.get, thumb_url)).content)
        )

        im = Image.new("RGB", SIZE, (30, 30, 30))
        draw = ImageDraw.Draw(im)

        thumb_size = SIZE[1] - INNER_MARGIN[1] * 2

        thumb = thumb.resize((thumb_size, thumb_size))

        im.paste(thumb, INNER_MARGIN)

        tpos = INNER_MARGIN
        tpos = (
            tpos[0] + thumb_size + INNER_MARGIN[0] + 8,
            thumb_size // 2 - (TRACK_FS + ARTIST_FS) // 2,
        )

        draw.text(tpos, title, (255, 255, 255), font=self.font)
        draw.text(
            (tpos[0], tpos[1] + TRACK_FS + 8),
            artist,
            (180, 180, 180),
            font=self.font_smaller,
        )

        img = io.BytesIO()
        im.save(img, format="PNG")
        return img.getvalue()

    @loader.loop(interval=90)
    async def autobio(self):
        try:
            current_playback = self.sp.current_playback()
            track = current_playback["item"]["name"]
            track = re.sub(r"([(].*?[)])", "", track).strip()

            artists = [
                artist["name"]
                for artist in current_playback.get("item", {}).get("artists", [])
                if "name" in artist
            ]
            artist_name = ", ".join(artists)

        except Exception:
            return

        bio_template = self.config.get("AutoBioTemplate", "🎧 {track} - {author}")

        if "{track}" in bio_template and "{author}" in bio_template:
            bio = bio_template.format(track=track, author=artist_name)
        elif "{track}" in bio_template:
            bio = bio_template.replace("{track}", track)
        elif "{author}" in bio_template:
            bio = bio_template.replace("{author}", artist_name)
        else:
            bio = bio_template

        try:
            await self._client(
                UpdateProfileRequest(about=bio[: 140 if self._premium else 70])
            )
        except FloodWaitError as e:
            logger.info(f"Sleeping {max(e.seconds, 60)} bc of floodwait")
            await asyncio.sleep(max(e.seconds, 60))
            return


    async def _dl_font(self):
        font = (
            await utils.run_sync(
                requests.get,
                "https://github.com/hikariatama/assets/raw/master/ARIALUNI.TTF",
            )
        ).content

        self.font_smaller = ImageFont.truetype(
            io.BytesIO(font), ARTIST_FS, encoding="UTF-8"
        )
        self.font = ImageFont.truetype(io.BytesIO(font), TRACK_FS, encoding="UTF-8")
        self.font_ready.set()

    async def client_ready(self, client, db):
        self.font_ready = asyncio.Event()
        asyncio.ensure_future(self._dl_font())

        self._premium = getattr(await client.get_me(), "premium", False)
        try:
            self.sp = spotipy.Spotify(auth=self.get("acs_tkn")["access_token"])
        except Exception:
            self.set("acs_tkn", None)
            self.sp = None

        if self.get("autobio", False):
            self.autobio.start()

        with contextlib.suppress(Exception):
            await utils.dnd(client, "@DirectLinkGenerator_Bot", archive=True)

        self.musicdl = await self.import_lib(
            "https://libs.hikariatama.ru/musicdl.py",
            suspend_on_error=True,
        )

    def tokenized(func) -> FunctionType:
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            if not args[0].get("acs_tkn", False) or not args[0].sp:
                await utils.answer(args[1], args[0].strings("need_auth"))
                return

            return await func(*args, **kwargs)

        wrapped.__doc__ = func.__doc__
        wrapped.__module__ = func.__module__

        return wrapped

    def error_handler(func) -> FunctionType:
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception:
                logger.exception(traceback.format_exc())
                with contextlib.suppress(Exception):
                    await utils.answer(
                        args[1],
                        args[0].strings("err").format(traceback.format_exc()),
                    )

        wrapped.__doc__ = func.__doc__
        wrapped.__module__ = func.__module__

        return wrapped

    def autodelete(func) -> FunctionType:
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            a = await func(*args, **kwargs)
            with contextlib.suppress(Exception):
                await asyncio.sleep(10)
                await args[1].delete()

            return a

        wrapped.__doc__ = func.__doc__
        wrapped.__module__ = func.__module__

        return wrapped

    @error_handler
    @tokenized
    async def srepeatcmd(self, message: Message):
        """💫 Повторять текущий трек"""
        self.sp.repeat("track")
        await utils.answer(message, self.strings("on-repeat"))

    @error_handler
    @tokenized
    async def sderepeatcmd(self, message: Message):
        """✋ Прекратить повторять текущий трек"""
        self.sp.repeat("context")
        await utils.answer(message, self.strings("off-repeat"))

    @error_handler
    @tokenized
    async def snextcmd(self, message: Message):
        """👉 Включить следующий трек"""
        self.sp.next_track()
        await utils.answer(message, self.strings("skipped"))

    @error_handler
    @tokenized
    async def spausecmd(self, message: Message):
        """🤚 Поставить текущий трек на паузу"""
        self.sp.pause_playback()
        await utils.answer(message, self.strings("paused"))

    @error_handler
    @tokenized
    async def splaycmd(self, message: Message, from_sq: bool = False):
        """▶️ Продолжить прослушивание текущего трека"""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()

        if not args:
            if not reply or "https://open.spotify.com/track/" not in reply.text:
                self.sp.start_playback()
                await utils.answer(message, self.strings("playing"))
                return
            else:
                args = re.search('https://open.spotify.com/track/(.+?)"', reply.text)[1]

        try:
            track = self.sp.track(args)
        except Exception:
            search = self.sp.search(q=args, type="track", limit=1)
            if not search:
                await utils.answer(message, self.strings("404"))
            try:
                track = search["tracks"]["items"][0]
            except Exception:
                await utils.answer(message, self.strings("404"))
                return

        self.sp.add_to_queue(track["id"])

        if not from_sq:
            self.sp.next_track()

        await message.delete()
        await self._client.send_file(
            message.peer_id,
            await self.create_badge(
                track["album"]["images"][0]["url"],
                track["name"],
                ", ".join([_["name"] for _ in track["artists"]]),
            ),
            caption=self.strings("playing_track").format(track["name"]),
        )

    @error_handler
    @tokenized
    async def sfindcmd(self, message: Message):
        """🔍 Найти трек и отправить его!"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings("404"))
            return

        progress_message = await utils.answer(message, self.strings("searching"))

        try:
            track = self.sp.track(args)
        except Exception:
            search = self.sp.search(q=args, type="track", limit=1)
            if not search or not search.get("tracks", {}).get("items"):
                await utils.answer(message, self.strings("404"))
                return
            track = search["tracks"]["items"][0]

        track_name = track["name"]
        artist_name = track["artists"][0]["name"]
        album_name = track["album"]["name"]
        track_duration = track["duration_ms"] // 1000
        track_url = track["external_urls"]["spotify"]

        current_playback = self.sp.current_playback()
        track_id = current_playback["item"]["id"] if current_playback else None
        universal_link = f"https://song.link/s/{track_id}" if track_id else None

        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                audio_path = os.path.join(temp_dir, f"{artist_name} - {track_name}.mp3")
                ydl_opts = {
                    "format": "bestaudio/best",
                    "outtmpl": audio_path,
                    "noplaylist": True,
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([f"ytsearch1:{track_name} - {artist_name}"])

                album_art_url = track["album"]["images"][0]["url"]
                async with aiohttp.ClientSession() as session:
                    async with session.get(album_art_url) as response:
                        art_path = os.path.join(temp_dir, "cover.jpg")
                        if response.status == 200:
                            with open(art_path, "wb") as f:
                                f.write(await response.read())

                caption = (
                    f"<emoji document_id=5870794890006237381>🎶</emoji> "
                    f"<code>{track_name}</code> - <code>{artist_name}</code>\n"
                    f"<emoji document_id=5870570722778156940>💿</emoji> <b>Альбом:</b> <code>{album_name}</code>\n"
                    f"<emoji document_id=5872756762347573066>🕒</emoji> <b>Длина трека: {track_duration // 60}:{track_duration % 60:02d}</b>"
                )
                if track_url:
                    caption += (
                        f"\n\n<emoji document_id=5294137402430858861>🎵</emoji> "
                        f"<b><a href=\"{track_url}\">Открыть на Spotify</a></b>"
                    )
                if universal_link:
                    caption += (
                        f"\n<emoji document_id=5902449142575141204>🔗</emoji> "
                        f"<b><a href=\"{universal_link}\">Открыть на song.link</a></b>"
                    )

                await self._client.send_file(
                    message.chat_id,
                    audio_path,
                    caption=caption,
                    attributes=[
                        types.DocumentAttributeAudio(
                            duration=track_duration,
                            title=track_name,
                            performer=artist_name
                        )
                    ],
                    thumb=art_path,
                    reply_to=message.reply_to_msg_id if message.is_reply else getattr(message, "top_id", None),
                )
                await progress_message.delete()
                return
            except Exception:
                pass

            try:
                search_query = f"ytsearch10:{track_name} - {artist_name}"
                ydl_opts_search = {
                    "format": "bestaudio/best",
                    "noplaylist": True,
                    "quiet": True,
                }
                with yt_dlp.YoutubeDL(ydl_opts_search) as ydl:
                    info = ydl.extract_info(search_query, download=False)
                entries = info.get("entries", [])
                success = False
                for entry in entries:
                    try:
                        video_url = entry.get("webpage_url")
                        if not video_url:
                            continue
                        audio_path = os.path.join(temp_dir, f"{artist_name} - {track_name}-{entry.get('id')}.mp3")
                        ydl_opts_download = {
                            "format": "bestaudio/best",
                            "outtmpl": audio_path,
                            "noplaylist": True,
                        }
                        with yt_dlp.YoutubeDL(ydl_opts_download) as ydl:
                            ydl.download([video_url])
                        success = True
                        break
                    except Exception:
                        continue
                if not success:
                    raise Exception("Не удалось скачать трек со второго способа")

                album_art_url = track["album"]["images"][0]["url"]
                async with aiohttp.ClientSession() as session:
                    async with session.get(album_art_url) as response:
                        art_path = os.path.join(temp_dir, "cover.jpg")
                        if response.status == 200:
                            with open(art_path, "wb") as f:
                                f.write(await response.read())

                caption = (
                    f"<emoji document_id=5870794890006237381>🎶</emoji> "
                    f"<code>{track_name}</code> - <code>{artist_name}</code>\n"
                    f"<emoji document_id=5870570722778156940>💿</emoji> <b>Альбом:</b> <code>{album_name}</code>\n"
                    f"<emoji document_id=5872756762347573066>🕒</emoji> <b>Длина трека: {track_duration // 60}:{track_duration % 60:02d}</b>"
                )
                if track_url:
                    caption += (
                        f"\n\n<emoji document_id=5294137402430858861>🎵</emoji> "
                        f"<b><a href=\"{track_url}\">Открыть на Spotify</a></b>"
                    )
                if universal_link:
                    caption += (
                        f"\n<emoji document_id=5902449142575141204>🔗</emoji> "
                        f"<b><a href=\"{universal_link}\">Открыть на song.link</a></b>"
                    )

                await self._client.send_file(
                    message.chat_id,
                    audio_path,
                    caption=caption,
                    attributes=[
                        types.DocumentAttributeAudio(
                            duration=track_duration,
                            title=track_name,
                            performer=artist_name
                        )
                    ],
                    thumb=art_path,
                    reply_to=message.reply_to_msg_id if message.is_reply else getattr(message, "top_id", None),
                )
                await progress_message.delete()
                return
            except Exception:
                pass

            try:
                name = track.get("name")
                artists = [artist["name"] for artist in track.get("artists", []) if "name" in artist]
                full_song_name = f"{name} - {', '.join(artists)}"
                music = await self.musicdl.dl(full_song_name, only_document=True)

                caption = (
                    f"<emoji document_id=5870794890006237381>🎶</emoji> "
                    f"<code>{track_name}</code> - <code>{artist_name}</code>\n"
                    f"<emoji document_id=5870570722778156940>💿</emoji> <b>Альбом:</b> <code>{album_name}</code>\n"
                    f"<emoji document_id=5872756762347573066>🕒</emoji> <b>Длина трека: {track_duration // 60}:{track_duration % 60:02d}</b>"
                )
                if track_url:
                    caption += (
                        f"\n\n<emoji document_id=5294137402430858861>🎵</emoji> "
                        f"<b><a href=\"{track_url}\">Открыть на Spotify</a></b>"
                    )
                if universal_link:
                    caption += (
                        f"\n<emoji document_id=5902449142575141204>🔗</emoji> "
                        f"<b><a href=\"{universal_link}\">Открыть на song.link</a></b>"
                    )

                await self._client.send_file(
                    message.peer_id,
                    music,
                    caption=caption,
                )
                await progress_message.delete()
            except Exception:
                await utils.answer(
                    message,
                    "<emoji document_id=5274099962655816924>❗️</emoji> <b>Скачать трек не удалось!</b>"
                )
            finally:
                await progress_message.delete()

    async def _open_track(
        self,
        track: dict,
        message: Message,
        override_text: str = None,
    ):
        name = track.get("name")
        artists = [
            artist["name"] for artist in track.get("artists", []) if "name" in artist
        ]

        full_song_name = f"{name} - {', '.join(artists)}"

        music = await self.musicdl.dl(full_song_name, only_document=True)

        await self._client.send_file(
            message.peer_id,
            music,
            caption=(
                override_text
                or (
                    (
                        f"🗽 <b>{utils.escape_html(full_song_name)}</b>{{is_flac}}"
                        if artists
                        else f"🗽 <b>{utils.escape_html(track)}</b>{{is_flac}}"
                    )
                    if track
                    else "{is_flac}"
                )
            ).format(
                is_flac=(
                    "\n<emoji document_id=5359582743992737342>😎</emoji> <b>FLAC"
                    f" {self.strings('quality')}</b>"
                    if getattr(music, "is_flac", False)
                    else ""
                )
            ),
        )

        if message.out:
            await message.delete()

    @error_handler
    @tokenized
    async def sqcmd(self, message: Message):
        """🔎 Добавить в очередь трек."""
        await self.splaycmd(message, True)

    @error_handler
    @tokenized
    async def sbackcmd(self, message: Message):
        """⏮ Включить предыдущий трек"""
        self.sp.previous_track()
        await utils.answer(message, self.strings("back"))

    @error_handler
    @tokenized
    async def sbegincmd(self, message: Message):
        """⏪ Включить текущий трек заного"""
        self.sp.seek_track(0)
        await utils.answer(message, self.strings("restarted"))

    @error_handler
    @tokenized
    async def slikecmd(self, message: Message):
        """❤️ Поставить лайк на текущий трек"""
        cupl = self.sp.current_playback()
        self.sp.current_user_saved_tracks_add([cupl["item"]["id"]])
        await utils.answer(message, self.strings("liked"))

    @error_handler
    async def sauthcmd(self, message: Message):
        """Получить ссылку для авторизации"""
        if self.get("acs_tkn", False) and not self.sp:
            await utils.answer(message, self.strings("already_authed"))
        else:
            self.sp_auth.get_authorize_url()
            await utils.answer(
                message,
                self.strings("auth").format(self.sp_auth.get_authorize_url()),
            )

    @error_handler
    async def scodecmd(self, message: Message):
        """Поставить код авторизации"""
        url = message.message.split(" ")[1]
        code = self.sp_auth.parse_auth_response_url(url)
        self.set("acs_tkn", self.sp_auth.get_access_token(code, True, False))
        self.sp = spotipy.Spotify(auth=self.get("acs_tkn")["access_token"])
        await utils.answer(message, self.strings("authed"))

    @error_handler
    async def unauthcmd(self, message: Message):
        """Выйти из аккаунта"""
        self.set("acs_tkn", None)
        del self.sp
        await utils.answer(message, self.strings("deauth"))

    @error_handler
    @tokenized
    async def sbiocmd(self, message: Message):
        """✏️ Включить/выключить показ трека в био"""
        current = self.get("autobio", False)
        new = not current
        self.set("autobio", new)
        await utils.answer(
            message,
            self.strings("autobio").format("включено" if new else "выключено"),
        )

        if new:
            self.autobio.start()
        else:
            self.autobio.stop()

    @error_handler
    @tokenized
    async def stokrefreshcmd(self, message: Message):
        """Сбросить токен авторизации"""
        self.set(
            "acs_tkn",
            self.sp_auth.refresh_access_token(self.get("acs_tkn")["refresh_token"]),
        )
        self.set("NextRefresh", time.time() + 45 * 60)
        self.sp = spotipy.Spotify(auth=self.get("acs_tkn")["access_token"])
        await utils.answer(message, self.strings("authed"))

    @error_handler
    @tokenized
    async def snowcmd(self, message: Message):
        """🎧 Просмотреть карточку текущего трека."""
        progress_message = await utils.answer(
            message,
            "<emoji document_id=5294137402430858861>🎵</emoji> <b>Погружаюсь в Spotify, чтобы найти, что играет прямо сейчас...</b>"
        )
        current_playback = self.sp.current_playback()
        try:
            device = (
                current_playback["device"]["name"]
                + " "
                + current_playback["device"]["type"].lower()
            )
        except Exception:
            device = None

        try:
            playlist_id = current_playback["context"]["uri"].split(":")[-1]
            playlist = self.sp.playlist(playlist_id)
            playlist_name = playlist.get("name", None)
            try:
                playlist_owner = (
                    f'<a href="https://open.spotify.com/user/{playlist["owner"]["id"]}">{playlist["owner"]["display_name"]}</a>'
                )
            except KeyError:
                playlist_owner = None
        except Exception:
            playlist_name = None
            playlist_owner = None

        try:
            track = current_playback["item"]["name"]
            track_id = current_playback["item"]["id"]
            album_name = current_playback["item"]["album"].get("name", "Unknown Album")
        except Exception:
            await utils.answer(message, self.strings("no_music"))
            return

        track_url = (
            current_playback.get("item", {})
            .get("external_urls", {})
            .get("spotify", None)
        )
        universal_link = f"https://song.link/s/{track_id}"

        artists = [
            artist["name"]
            for artist in current_playback.get("item", {}).get("artists", [])
            if "name" in artist
        ]

        try:
            result = (
                (
                    "<emoji document_id=5870794890006237381>🎶</emoji> <b>Сейчас играет:</b>"
                    f" <code>{utils.escape_html(track)}</code> -"
                    f" <code>{utils.escape_html(' '.join(artists))}</code>"
                    if artists
                    else (
                        "<emoji document_id=5870794890006237381>🎶</emoji> <b>Сейчас играет:</b>"
                        f" <code>{utils.escape_html(track)}</code>"
                    )
                )
                if track
                else ""
            )
            result += (
                f"\n<emoji document_id=5870570722778156940>💿</emoji> <b>Альбом:</b>"
                f" <code>{utils.escape_html(album_name)}</code>"
                if album_name
                else ""
            )
            if "duration_ms" in current_playback["item"]:
                duration = current_playback["item"]["duration_ms"] // 1000
                minutes = duration // 60
                seconds = duration % 60
                result += f"\n<emoji document_id=5872756762347573066>🕒</emoji> <b>Длина трека: {minutes}:{seconds:02}</b>"
            
            icon = (
                "<emoji document_id=5967816500415827773>💻</emoji>"
                if "computer" in str(device)
                else "<emoji document_id=5872980989705196227>📱</emoji>"
            )
            result += (
                "\n\n<emoji document_id=5877307202888273539>📁</emoji>"
                f" <b>{self.strings('playlist')}</b>: <a"
                f' href="https://open.spotify.com/playlist/{playlist_id}">{playlist_name}</a>'
                if playlist_name and playlist_id
                else ""
            )
            result += (
                "\n<emoji document_id=5879770735999717115>👤</emoji>"
                f" <b>{self.strings('owner')}</b>: {playlist_owner}"
                if playlist_owner
                else ""
            )
            result += (
                f"\n\n{icon} <b>{self.strings('currently_on')}</b>"
                f" <code>{device}</code>"
                if device
                else ""
            )
            result += (
                "\n\n<emoji document_id=5294137402430858861>🎵</emoji> <b><a"
                f' href="{track_url}">Открыть на Spotify</a></b>'
            )
            if universal_link:
                result += (
                    f'\n<emoji document_id=5877465816030515018>🔗</emoji> <b><a href="{universal_link}">Открыть на song.link</a></b>'
                )
        except Exception:
            result = self.strings("no_music")

        progress_message = await utils.answer(
            message,
            result.format(is_flac="") + "\n\n<emoji document_id=5451646226975955576>⌛️</emoji> <i>Скачиваю трек, почти готово!</i>",
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                audio_path = os.path.join(temp_dir, f"{artists[0]} - {track}.mp3")
                ydl_opts = {
                    "format": "bestaudio/best",
                    "outtmpl": audio_path,
                    "noplaylist": True,
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([f"ytsearch1:{track} - {artists[0]}"])

                album_art_url = current_playback["item"]["album"]["images"][0]["url"]
                async with aiohttp.ClientSession() as session:
                    async with session.get(album_art_url) as response:
                        art_path = os.path.join(temp_dir, "cover.jpg")
                        if response.status == 200:
                            with open(art_path, "wb") as f:
                                f.write(await response.read())

                await self._client.send_file(
                    message.chat_id,
                    audio_path,
                    caption=result,
                    attributes=[
                        types.DocumentAttributeAudio(
                            duration=current_playback["item"]["duration_ms"] // 1000,
                            title=track,
                            performer=artists[0]
                        )
                    ],
                    thumb=art_path,
                    reply_to=message.reply_to_msg_id if message.is_reply else getattr(message, "top_id", None)
                )
                await progress_message.delete()
                return
            except Exception:
                pass
            try:
                search_query = f"ytsearch10:{track} - {artists[0]}"
                ydl_opts_search = {
                    "format": "bestaudio/best",
                    "noplaylist": True,
                    "quiet": True,
                }
                with yt_dlp.YoutubeDL(ydl_opts_search) as ydl:
                    info = ydl.extract_info(search_query, download=False)
                entries = info.get("entries", [])
                success = False
                for entry in entries:
                    try:
                        video_url = entry.get("webpage_url")
                        if not video_url:
                            continue
                        audio_path = os.path.join(temp_dir, f"{artists[0]} - {track}-{entry.get('id')}.mp3")
                        ydl_opts_download = {
                            "format": "bestaudio/best",
                            "outtmpl": audio_path,
                            "noplaylist": True,
                        }
                        with yt_dlp.YoutubeDL(ydl_opts_download) as ydl:
                            ydl.download([video_url])
                        success = True
                        break
                    except Exception:
                        continue
                if not success:
                    raise Exception("Не удалось скачать трек со второго способа")
                album_art_url = current_playback["item"]["album"]["images"][0]["url"]
                async with aiohttp.ClientSession() as session:
                    async with session.get(album_art_url) as response:
                        art_path = os.path.join(temp_dir, "cover.jpg")
                        if response.status == 200:
                            with open(art_path, "wb") as f:
                                f.write(await response.read())

                await self._client.send_file(
                    message.chat_id,
                    audio_path,
                    caption=result,
                    attributes=[
                        types.DocumentAttributeAudio(
                            duration=current_playback["item"]["duration_ms"] // 1000,
                            title=track,
                            performer=artists[0]
                        )
                    ],
                    thumb=art_path,
                    reply_to=message.reply_to_msg_id if message.is_reply else getattr(message, "top_id", None)
                )
                await progress_message.delete()
                return
            except Exception:
                pass
            try:
                await self._open_track(current_playback["item"], message, result)
                await progress_message.delete()
            except Exception:
                await utils.answer(message, result + "\n\n<emoji document_id=5274099962655816924>❗️</emoji> <b>Скачать трек не удалось!</b>")
            finally:
                await progress_message.delete()

    async def watcher(self, message: Message):
        """Watcher is used to update token"""
        if not self.sp:
            return

        if self.get("NextRefresh", False):
            ttc = self.get("NextRefresh", 0)
            crnt = time.time()
            if ttc < crnt:
                self.set(
                    "acs_tkn",
                    self.sp_auth.refresh_access_token(
                        self.get("acs_tkn")["refresh_token"]
                    ),
                )
                self.set("NextRefresh", time.time() + 45 * 60)
                self.sp = spotipy.Spotify(auth=self.get("acs_tkn")["access_token"])
        else:
            self.set(
                "acs_tkn",
                self.sp_auth.refresh_access_token(self.get("acs_tkn")["refresh_token"]),
            )
            self.set("NextRefresh", time.time() + 45 * 60)
            self.sp = spotipy.Spotify(auth=self.get("acs_tkn")["access_token"])

    async def on_unload(self):
        with contextlib.suppress(Exception):
            self.autobio.stop()
