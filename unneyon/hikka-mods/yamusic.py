__version__ = (1, 0, 3)
#          █▄▀ ▄▀█ █▀▄▀█ █▀▀ █▄▀ █  █ █▀█ █▀█
#          █ █ █▀█ █ ▀ █ ██▄ █ █ ▀▄▄▀ █▀▄ █▄█ ▄
#                © Copyright 2025
#            ✈ https://t.me/kamekuro

# 🔒 Licensed under CC-BY-NC-ND 4.0 unless otherwise specified.
# 🌐 https://creativecommons.org/licenses/by-nc-nd/4.0
# + attribution
# + non-commercial
# + no-derivatives

# You CANNOT edit, distribute or redistribute this file without direct permission from the author.

# meta banner: https://raw.githubusercontent.com/kamekuro/hikka-mods/main/banners/yamusic.png
# meta pic: https://raw.githubusercontent.com/kamekuro/hikka-mods/main/icons/yamusic.png
# meta developer: @kamekuro_hmods
# scope: hikka_only
# scope: hikka_min 1.6.3
# requires: aiohttp asyncio requests pillow==11.2.1 git+https://github.com/MarshalX/yandex-music-api

import aiohttp
import asyncio
import io
import json
import logging
import random
import requests
import string
import yandex_music

import telethon
import textwrap
from PIL import (
    Image, ImageDraw, ImageEnhance,
    ImageFilter, ImageFont
)
import yandex_music.exceptions

from .. import loader, utils


logger = logging.getLogger(__name__)


@loader.tds
class YaMusicMod(loader.Module):
    """The module for Yandex.Music streaming service"""

    strings = {
        "name": "YaMusic",
        "queue_types": {
            "VARIOUS": "Your queue",
            "RADIO": "«My Wave»",
            "PLAYLIST": "Playlist «{}»",
            "ALBUM": "Album «{}»"
        },
        "guide": (
            "<emoji document_id=5956561916573782596>📜</emoji> <b><a "
            "href=\"https://github.com/MarshalX/yandex-music-api/discussions/513"
            "#discussioncomment-2729781\">Guide for obtaining a Yandex.Music token</a></b>"
        ),
        "no_token": (
            "<emoji document_id=5778527486270770928>❌</emoji> <b>You didn't specify "
            "the access token in the config!</b>"
        ),
        "autobio_e": "<emoji document_id=5429189857324841688>🎧</emoji> <b>Autobio is on now</b>",
        "autobio_d": "<emoji document_id=5429189857324841688>🎧</emoji> <b>Autobio is off now</b>",
        "there_is_no_playing": (
            "<emoji document_id=5474140048741901455>❌</emoji> <b>You don't "
            "listening to anything right now.</b>"
        ),
        "now": (
            "<emoji document_id=5474304919651491706>🎧</emoji> <b>{performer} — {title}</b>\n\n"
            "<emoji document_id={device_eid}>⌨️</emoji> <b>Now is listening on</b> <code>{device}</code> "
            "<b>(<emoji document_id=6039454987250044861>🔊</emoji> {volume}%)</b>\n"
            "<emoji document_id=5257969839313526622>🗂</emoji> <b>Playing from:</b> {playing_from}\n\n"
            "<emoji document_id=5429189857324841688>🎵</emoji> <b><a href=\"https://music.yandex.ru/"
            "album/{album_id}/track/{track_id}\">Yandex.Music</a> | "
            "<a href=\"https://song.link/ya/{track_id}\">song.link</a></b>"
        ),
        "downloading": "\n\n<emoji document_id=5841359499146825803>🕔</emoji> <i>Downloading audio…</i>",
        "downloading_banner": "\n\n<emoji document_id=5841359499146825803>🕔</emoji> <i>Downloading banner…</i>",
        "likes": {
            "liked": (
                "<emoji document_id=6037533152593842454>❤️</emoji> <b>Track "
                "<a href=\"https://music.yandex.ru/album/{album_id}/track/{track_id}\">{track}</a> "
                "was successfully liked</b>"
            ),
            "unliked": (
                "<emoji document_id=5992453811510186287>❤️</emoji> <b>Track "
                "<a href=\"https://music.yandex.ru/album/{album_id}/track/{track_id}\">{track}</a> "
                "was successfully unliked</b>"
            ),
            "disliked": (
                "<emoji document_id=5222400230133081714>💔</emoji> <b>Track "
                "<a href=\"https://music.yandex.ru/album/{album_id}/track/{track_id}\">{track}</a> "
                "was successfully disliked</b>"
            )
        },
        "lyrics": (
            "<emoji document_id=5956561916573782596>📜</emoji> <b>Lyrics of the <a href=\""
            "https://music.yandex.ru/album/{album_id}/track/{track_id}\">{track}</a> track:</b>\n"
            "<blockquote expandable>{text}</blockquote>\n\n"
            "<emoji document_id=5247213725080890199>©️</emoji> <b>Writers:</b> {writers}"
        ),
        "no_lyrics": (
            "<emoji document_id=5886285363869126932>❌</emoji> <b>Track "
            "<a href=\"https://music.yandex.ru/album/{album_id}/track/{track_id}\">{track}</a> "
            "has no lyrics!</b>"
        ),
        "search": (
            "<emoji document_id=5474304919651491706>🎧</emoji> <b>{performer} — {title}</b>\n"
            "<emoji document_id=5429189857324841688>🎵</emoji> <b><a href=\"https://music.yandex.ru/"
            "album/{album_id}/track/{track_id}\">Yandex.Music</a> | "
            "<a href=\"https://song.link/ya/{track_id}\">song.link</a></b>"
        ),
        "args": "<emoji document_id=5778527486270770928>❌</emoji> <b>Specify search query</b>",
        "404": "<emoji document_id=5778527486270770928>❌</emoji> <b>No results found</b>",
        "searching": "<emoji document_id=5258274739041883702>🔍</emoji> <b>Searching…</b>",
        "_cfg_token": "Your access token of Yandex.Music",
        "_cfg_autobio": "Automatic bio template (may contain {artist} and {title})",
        "_cfg_no_playing_bio": "Bio that is set when nothing is playing"
    }

    strings_ru = {
        "_cls_doc": "Модуль для стримингового сервиса Яндекс.Музыка",
        "queue_types": {
            "VARIOUS": "Ваша очередь",
            "RADIO": "«Моя Волна»",
            "PLAYLIST": "Плейлист «{}»",
            "ALBUM": "Альбом «{}»"
        },
        "guide": (
            "<emoji document_id=5956561916573782596>📜</emoji> <b><a "
            "href=\"https://github.com/MarshalX/yandex-music-api/discussions/513"
            "#discussioncomment-2729781\">Гайд по получению токена Яндекс.Музыки</a></b>"
        ),
        "no_token": (
            "<emoji document_id=5312526098750252863>❌</emoji> <b>Ты не "
            "указал токен Яндекс.Музыки в конфиге!</b>"
        ),
        "autobio_e": "<emoji document_id=5429189857324841688>🎧</emoji> <b>Автобио включено</b>",
        "autobio_d": "<emoji document_id=5429189857324841688>🎧</emoji> <b>Автобио выключено</b>",
        "there_is_no_playing": (
            "<emoji document_id=5474140048741901455>❌</emoji> <b>Ты ничего " 
            "не слушаешь сейчас.</b>"
        ),
        "now": (
            "<emoji document_id=5474304919651491706>🎧</emoji> <b>{performer} — {title}</b>\n\n"
            "<emoji document_id={device_eid}>⌨️</emoji> <b>Сейчас слушаю на</b> <code>{device}</code> "
            " <b>(<emoji document_id=6039454987250044861>🔊</emoji> {volume}%)</b>\n"
            "<emoji document_id=5257969839313526622>🗂</emoji> <b>Откуда играет:</b> {playing_from}\n\n"
            "<emoji document_id=5429189857324841688>🎵</emoji> <b><a href=\"https://music.yandex.ru/"
            "album/{album_id}/track/{track_id}\">Яндекс.Музыка</a> | "
            "<a href=\"https://song.link/ya/{track_id}\">song.link</a></b>"
        ),
        "downloading": "\n\n<emoji document_id=5841359499146825803>🕔</emoji> <i>Загрузка трека…</i>",
        "downloading_banner": "\n\n<emoji document_id=5841359499146825803>🕔</emoji> <i>Загрузка баннера…</i>",
        "likes": {
            "liked": (
                "<emoji document_id=6037533152593842454>❤️</emoji> <b>Лайкнул трек "
                "<a href=\"https://music.yandex.ru/album/{album_id}/track/{track_id}\">{track}</a></b>"
            ),
            "unliked": (
                "<emoji document_id=5992453811510186287>❤️</emoji> <b>Убрал лайк с трека "
                "<a href=\"https://music.yandex.ru/album/{album_id}/track/{track_id}\">{track}</a></b>"
            ),
            "disliked": (
                "<emoji document_id=5222400230133081714>💔</emoji> <b>Дизлайкнул трек "
                "<a href=\"https://music.yandex.ru/album/{album_id}/track/{track_id}\">{track}</a></b>"
            )
        },
        "lyrics": (
            "<emoji document_id=5956561916573782596>📜</emoji> <b>Текст трека "
            "<a href=\"https://music.yandex.ru/album/{album_id}/track/{track_id}\">{track}</a>:</b>\n"
            "<blockquote expandable>{text}</blockquote>\n\n"
            "<emoji document_id=5247213725080890199>©️</emoji> <b>Авторы:</b> {writers}"
        ),
        "no_lyrics": (
            "<emoji document_id=5886285363869126932>❌</emoji> <b>У трека "
            "<a href=\"https://music.yandex.ru/album/{album_id}/track/{track_id}\">{track}</a> "
            "нет текста!</b>"
        ),
        "search": (
            "<emoji document_id=5474304919651491706>🎧</emoji> <b>{performer} — {title}</b>\n"
            "<emoji document_id=5429189857324841688>🎵</emoji> <b><a href=\"https://music.yandex.ru/"
            "album/{album_id}/track/{track_id}\">Яндекс.Музыка</a> | "
            "<a href=\"https://song.link/ya/{track_id}\">song.link</a></b>"
        ),
        "args": "<emoji document_id=5312526098750252863>❌</emoji> <b>Укажите поисковый запрос</b>",
        "404": "<emoji document_id=5312526098750252863>❌</emoji> <b>Ничего не найдено</b>",
        "searching": "<emoji document_id=5258274739041883702>🔍</emoji> <b>Ищем…</b>",
        "_cfg_token": "Твой токен от Яндекс.Музыки",
        "_cfg_autobio": "Шаблон автоматического био (может содержать {artist} и {title})",
        "_cfg_no_playing_bio": "Био, которое ставится, когда ничего не играет"
    }


    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "token",
                None,
                lambda: self.strings["_cfg_token"],
                validator=loader.validators.Hidden()
            ),
            loader.ConfigValue(
                "autobio",
                "🎧 {artist} - {title}",
                lambda: self.strings["_cfg_autobio"],
                validator=loader.validators.String()
            ),
            loader.ConfigValue(
                "no_playing_bio",
                "Hello!",
                lambda: self.strings["_cfg_no_playing_bio"],
                validator=loader.validators.String()
            )
        )

    async def on_dlmod(self):
        if not self.get("guide_send", False):
            await self.inline.bot.send_message(
                self._tg_id,
                self.strings("guide").replace("<emoji document_id=6334657396698253102>📜</emoji>", "📜"),
            )
            self.set("guide_send", True)

    async def client_ready(self, client, db):
        self._client = client
        self._db = db

        me = await self._client.get_me()
        self._premium = me.premium if hasattr(me, "premium") else False
        self.premium_check.start()

        if self.get("autobio", False):
            self.autobio.start()


    @loader.loop(1800)
    async def premium_check(self):
        me = await self._client.get_me()
        self._premium = me.premium if hasattr(me, "premium") else False


    @loader.loop(30)
    async def autobio(self):
        if not self.config['token']:
            self.autobio.stop(); self.set("autobio", False)
            return
        client = yandex_music.Client(self.config['token']).init()
        now = await self.__get_now_playing(self.config['token'], client)
        out = self.config['no_playing_bio'][:(140 if self._premium else 70)]
        if now and (not now['paused']):
            out = self.config['autobio'].format(
                title=now['track']['title'],
                artist=", ".join(now['track']['artist'])
            )[:(140 if self._premium else 70)]
        try:
            await self._client(
                telethon.functions.account.UpdateProfileRequest(about=out)
            )
        except telethon.errors.rpcerrorlist.FloodWaitError as e:
            logger.info(f"Sleeping {max(e.seconds, 60)} because of floodwait")
            await asyncio.sleep(max(e.seconds, 60))


    @loader.command(
        ru_doc="👉 Гайд по получению токена Яндекс.Музыки",
        alias="yg"
    )
    async def yguidecmd(self, message: telethon.types.Message):
        """👉 Guide for obtaining a Yandex.Music token"""
        await utils.answer(message, self.strings("guide"))


    @loader.command(
        ru_doc="👉 Включить/выключить автобио",
        alias="yb"
    )
    async def ybiocmd(self, message: telethon.types.Message):
        """👉 Enable/disable autobio"""

        if not self.config['token']:
            return await utils.answer(message, self.strings("no_token"))

        bio_now = self.get("autobio", False)
        self.set("autobio", not bio_now)
        if (not bio_now):
            self.autobio.start()
        else:
            self.autobio.stop()
            try:
                await self._client(
                    telethon.functions.account.UpdateProfileRequest(
                        about=self.config['no_playing_bio'][:(140 if self._premium else 70)]
                    )
                )
            except: pass

        await utils.answer(
            message,
            self.strings(f"autobio_{'e' if (not bio_now) else 'd'}")
        )


    @loader.command(
        ru_doc="👉 Получить трек, который играет сейчас",
        alias="yn"
    )
    async def ynowcmd(self, message: telethon.types.Message):
        """👉 Get now playing track"""

        if not self.config['token']:
            return await utils.answer(message, self.strings("no_token"))
        client = yandex_music.Client(self.config['token']).init()
        now = await self.__get_now_playing(self.config['token'], client)
        if not now:
            return await utils.answer(message, self.strings("there_is_no_playing"))

        playlist_name = ""
        if now['entity_type'] in ["PLAYLIST", "ALBUM"]:
            func = getattr(
                client,
                "playlists_list" if now['entity_type'] == "PLAYLIST" else "albums"
            )
            if func:
                entity = func(now['entity_id'])[0]
                playlist_name = f"<b><a href=\"https://music.yandex.ru/users/" \
                                f"{client.me.account.login}/playlists/" \
                                f"{now['entity_id'].split(':')[1]}\">{entity.title}</a></b>"
            else:
                now['entity_type'] = "RADIO"

        device_eid, device, volume = "6039404727542747508", "Unknown Device", "❓"
        if now['device']:
            device=now['device']['info']['title']
            volume=round(now['device']['volume']*100, 2)
            if now['device']['info']['type'] == "ANDROID": device_eid = "5373266788970670174"
            if now['device']['info']['type'] == "IOS": device_eid = "5372908412604525258"

        out = self.strings("now").format(
            title=now['track']['title'],
            performer=", ".join(now['track']['artist']),
            device=device, volume=volume, device_eid=device_eid,
            playing_from=self.strings("queue_types").get(now['entity_type'], "VARIOUS").format(playlist_name),
            track_id=now['track']['track_id'],
            album_id=now['track']['album_id']
        )

        await utils.answer(
            message, out+self.strings("downloading")
        )

        audio = io.BytesIO((await utils.run_sync(requests.get, now['track']['download_link'])).content)
        audio.name = "audio.mp3"

        await utils.answer(
            message=message, response=out,
            file=audio,
            attributes=([
                telethon.types.DocumentAttributeAudio(
                    duration=now['track']['duration'],
                    title=now['track']['title'],
                    performer=", ".join(now['track']['artist'])
                )
            ])
        )


    @loader.command(
        ru_doc="👉 Получить баннер трека, который играет сейчас",
        alias="ynb"
    )
    async def ynowbcmd(self, message: telethon.types.Message):
        """👉 Get now playing track's banner"""

        if not self.config['token']:
            return await utils.answer(message, self.strings("no_token"))
        client = yandex_music.Client(self.config['token']).init()
        now = await self.__get_now_playing(self.config['token'], client)
        if not now:
            return await utils.answer(message, self.strings("there_is_no_playing"))

        playlist_name = ""
        if now['entity_type'] in ["PLAYLIST", "ALBUM"]:
            func = getattr(
                client,
                "playlists_list" if now['entity_type'] == "PLAYLIST" else "albums"
            )
            if func:
                entity = func(now['entity_id'])[0]
                playlist_name = f"<b><a href=\"https://music.yandex.ru/users/" \
                                f"{client.me.account.login}/playlists/" \
                                f"{now['entity_id'].split(':')[1]}\">{entity.title}</a></b>"
            else:
                now['entity_type'] = "RADIO"

        device_eid, device, volume = "6039404727542747508", "Unknown Device", "❓"
        if now['device']:
            device=now['device']['info']['title']
            volume=round(now['device']['volume']*100, 2)
            if now['device']['info']['type'] == "ANDROID": device_eid = "5373266788970670174"
            if now['device']['info']['type'] == "IOS": device_eid = "5372908412604525258"

        out = self.strings("now").format(
            title=now['track']['title'],
            performer=", ".join(now['track']['artist']),
            device=device, volume=volume, device_eid=device_eid,
            playing_from=self.strings("queue_types").get(now['entity_type'], "VARIOUS").format(playlist_name),
            track_id=now['track']['track_id'],
            album_id=now['track']['album_id']
        )

        await utils.answer(
            message, out+self.strings("downloading_banner")
        )

        file = self.__create_banner(
            now['track']['title'], now['track']['artist'],
            now['duration_ms'], now['progress_ms'],
            requests.get(now['track']['img']).content
        )
        await utils.answer(
            message=message, response=out, file=file
        )


    @loader.command(
        ru_doc="👉 Лайкнуть играющий сейчас трек"
    )
    async def ylikecmd(self, message: telethon.types.Message):
        """👉 Like now playing track's banner"""

        if not self.config['token']:
            return await utils.answer(message, self.strings("no_token"))
        client = yandex_music.Client(self.config['token']).init()
        now = await self.__get_now_playing(self.config['token'], client)
        if not now:
            return await utils.answer(message, self.strings("there_is_no_playing"))

        client.users_likes_tracks_add(now['track']['track_id'])
        await utils.answer(
            message, self.strings("likes")['liked'].format(
                track_id=now['track']['track_id'], album_id=now['track']['album_id'],
                track=f"{', '.join(now['track']['artist'])} — {now['track']['title']}"
            )
        )

    @loader.command(
        ru_doc="👉 Убрать лайк с играющего сейчас трека"
    )
    async def yunlikecmd(self, message: telethon.types.Message):
        """👉 Unlike now playing track"""

        if not self.config['token']:
            return await utils.answer(message, self.strings("no_token"))
        client = yandex_music.Client(self.config['token']).init()
        now = await self.__get_now_playing(self.config['token'], client)
        if not now:
            return await utils.answer(message, self.strings("there_is_no_playing"))

        client.users_likes_tracks_remove(now['track']['track_id'])
        await utils.answer(
            message, self.strings("likes")['unliked'].format(
                track_id=now['track']['track_id'], album_id=now['track']['album_id'],
                track=f"{', '.join(now['track']['artist'])} — {now['track']['title']}"
            )
        )

    @loader.command(
        ru_doc="👉 Дизлайкнуть играющий сейчас трек",
        alias="ydis"
    )
    async def ydislikecmd(self, message: telethon.types.Message):
        """👉 Dislike now playing track"""

        if not self.config['token']:
            return await utils.answer(message, self.strings("no_token"))
        client = yandex_music.Client(self.config['token']).init()
        now = await self.__get_now_playing(self.config['token'], client)
        if not now:
            return await utils.answer(message, self.strings("there_is_no_playing"))

        client.users_dislikes_tracks_add(now['track']['track_id'])
        await utils.answer(
            message, self.strings("likes")['disliked'].format(
                track_id=now['track']['track_id'], album_id=now['track']['album_id'],
                track=f"{', '.join(now['track']['artist'])} — {now['track']['title']}"
            )
        )


    @loader.command(
        ru_doc="👉 Получить текст играющего сейчас трека"
    )
    async def ylyricscmd(self, message: telethon.types.Message):
        """👉 Get lyrics of the now playing track"""

        if not self.config['token']:
            return await utils.answer(message, self.strings("no_token"))
        client = yandex_music.Client(self.config['token']).init()
        now = await self.__get_now_playing(self.config['token'], client)
        if not now:
            return await utils.answer(message, self.strings("there_is_no_playing"))

        try:
            lyrics = client.tracks_lyrics(now['track']['track_id'])
            await utils.answer(
                message, self.strings("lyrics").format(
                    track_id=now['track']['track_id'], album_id=now['track']['album_id'],
                    track=f"{', '.join(now['track']['artist'])} — {now['track']['title']}",
                    text=requests.get(lyrics.download_url).text,
                    writers=", ".join(lyrics.writers)
                )
            )
        except yandex_music.exceptions.NotFoundError:
            await utils.answer(
                message, self.strings("no_lyrics").format(
                    track_id=now['track']['track_id'], album_id=now['track']['album_id'],
                    track=f"{', '.join(now['track']['artist'])} — {now['track']['title']}"
                )
            )


    @loader.command(
        ru_doc="<запрос> 👉 Поиск трека в Яндекс.Музыке",
        alias="yq"
    )
    async def ysearchcmd(self, message: telethon.types.Message):
        """<query> 👉 Search track in Yandex.Music"""

        if not self.config['token']:
            return await utils.answer(message, self.strings("no_token"))
        client = yandex_music.Client(self.config['token']).init()

        query = utils.get_args_raw(message)
        if not query:
            await utils.answer(message, self.strings("args"))
            return

        message = await utils.answer(message, self.strings("searching"))

        search = client.search(query, type_="track")
        if (not search.tracks) or (len(search.tracks.results) == 0):
            return await utils.answer(message, self.strings("404"))

        out = self.strings("search").format(
            title=search.tracks.results[0].title + (
                f" ({search.tracks.results[0].version})" if search.tracks.results[0].version else ""
            ),
            performer=", ".join([x.name for x in search.tracks.results[0].artists]),
            album_id=search.tracks.results[0].albums[0].id, track_id=search.tracks.results[0].id
        )
        message = await utils.answer(message, out+self.strings("downloading"))

        info = client.tracks_download_info(search.tracks.results[0].id, True)
        link = info[0].direct_link
        audio = None
        audio = io.BytesIO((await utils.run_sync(requests.get, link)).content)
        audio.name = "audio.mp3"

        await utils.answer(
            message=message, response=out,
            file=audio,
            attributes=([
                telethon.types.DocumentAttributeAudio(
                    duration=int(search.tracks.results[0].duration_ms / 1000),
                    title=search.tracks.results[0].title,
                    performer=", ".join([x.name for x in search.tracks.results[0].artists])
                )
            ])
        )



    # Original code: https://raw.githubusercontent.com/MIPOHBOPOHIH/YMMBFA/main/main.py
    async def __create_ynison_ws(self, yamusic_token: str, ws_proto: dict) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(
                "wss://ynison.music.yandex.ru/redirector.YnisonRedirectService/GetRedirectToYnison",
                headers={
                    "Sec-WebSocket-Protocol": f"Bearer, v2, {json.dumps(ws_proto)}",
                    "Origin": "http://music.yandex.ru",
                    "Authorization": f"OAuth {yamusic_token}",
                },
            ) as ws:
                response = await ws.receive()
                return json.loads(response.data)

    # Original code: https://raw.githubusercontent.com/MIPOHBOPOHIH/YMMBFA/main/main.py
    async def  __get_now_playing(self, yamusic_token: str, client: yandex_music.Client):
        device_id = ''.join(random.choices(string.ascii_lowercase, k=16))
        ws_proto = {
            "Ynison-Device-Id": device_id,
            "Ynison-Device-Info": json.dumps({"app_name": "Chrome", "type": 1}),
        }
        data = await self.__create_ynison_ws(yamusic_token, ws_proto)

        ws_proto["Ynison-Redirect-Ticket"] = data["redirect_ticket"]

        payload = {
            "update_full_state": {
                "player_state": {
                    "player_queue": {
                        "current_playable_index": -1,
                        "entity_id": "",
                        "entity_type": "VARIOUS",
                        "playable_list": [],
                        "options": {"repeat_mode": "NONE"},
                        "entity_context": "BASED_ON_ENTITY_BY_DEFAULT",
                        "version": {"device_id": device_id, "version": 9021243204784341000, "timestamp_ms": 0},
                        "from_optional": "",
                    },
                    "status": {
                        "duration_ms": 0,
                        "paused": True,
                        "playback_speed": 1,
                        "progress_ms": 0,
                        "version": {"device_id": device_id, "version": 8321822175199937000, "timestamp_ms": 0},
                    },
                },
                "device": {
                    "capabilities": {"can_be_player": True, "can_be_remote_controller": False, "volume_granularity": 16},
                    "info": {
                        "device_id": device_id,
                        "type": "WEB",
                        "title": "Chrome Browser",
                        "app_name": "Chrome",
                    },
                    "volume_info": {"volume": 0},
                    "is_shadow": True,
                },
                "is_currently_active": False,
            },
            "rid": "ac281c26-a047-4419-ad00-e4fbfda1cba3",
            "player_action_timestamp_ms": 0,
            "activity_interception_type": "DO_NOT_INTERCEPT_BY_DEFAULT",
        }

        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(
                f"wss://{data['host']}/ynison_state.YnisonStateService/PutYnisonState",
                headers={
                    "Sec-WebSocket-Protocol": f"Bearer, v2, {json.dumps(ws_proto)}",
                    "Origin": "http://music.yandex.ru",
                    "Authorization": f"OAuth {yamusic_token}",
                }
            ) as ws:
                await ws.send_str(json.dumps(payload))
                response = await ws.receive()
                ynison: dict = json.loads(response.data)

        if len(ynison.get("player_state", {}).get("player_queue", {}).get("playable_list", [])) == 0:
            return {}
        raw_track = ynison["player_state"]["player_queue"]["playable_list"][
            ynison["player_state"]["player_queue"]["current_playable_index"]
        ]
        track = client.tracks(raw_track["playable_id"])[0]
        device = [
            x for x in ynison['devices'] if x['info']['device_id'] == ynison.get('active_device_id_optional', "")
        ]

        return {
            "paused": ynison["player_state"]["status"]["paused"],
            "duration_ms": int(ynison["player_state"]["status"]["duration_ms"]),
            "progress_ms": int(ynison["player_state"]["status"]["progress_ms"]),
            "entity_id": ynison["player_state"]["player_queue"]["entity_id"],
            "entity_type": ynison["player_state"]["player_queue"]["entity_type"],
            "device": device[0] if len(device) > 0 else None,
            "track": {
                "track_id": int(track.track_id.split(":")[0]) if track.track_id.split(":")[0].isdigit() else track.track_id,
                "album_id": track.albums[0].id,
                "title": track.title,
                "artist": track.artists_name(),
                "img": f"https://{track.cover_uri[:-2]}1000x1000",
                "duration": track.duration_ms // 1000,
                "minutes": round(track.duration_ms / 1000) // 60,
                "seconds": round(track.duration_ms / 1000) % 60,
                "download_link": track.get_download_info(get_direct_links=True)[0].direct_link
            }
        } if raw_track['playable_type'] != "LOCAL_TRACK" else {}


    def __create_banner(
        self,
        title: str, artists: list,
        duration: int, progress: int,
        track_cover: bytes
    ):
        w, h = 1920, 768
        title_font = ImageFont.truetype(io.BytesIO(requests.get(
            "https://raw.githubusercontent.com/kamekuro/assets/master/fonts/Onest-Bold.ttf"
        ).content), 80)
        art_font = ImageFont.truetype(io.BytesIO(requests.get(
            "https://raw.githubusercontent.com/kamekuro/assets/master/fonts/Onest-Regular.ttf"
        ).content), 55)
        time_font = ImageFont.truetype(io.BytesIO(requests.get(
            "https://raw.githubusercontent.com/kamekuro/assets/master/fonts/Onest-Bold.ttf"
        ).content), 36)

        # Gen banner (bg)
        track_cov = Image.open(io.BytesIO(track_cover)).convert("RGBA")
        banner = track_cov.resize((w, w)).crop(
            (0, (w-h)//2, w, ((w-h)//2)+h)
        ).filter(ImageFilter.GaussianBlur(radius=14))
        banner = ImageEnhance.Brightness(banner).enhance(0.3)

        # Gen track cover and put to bg
        track_cov = track_cov.resize((banner.size[1]-150, banner.size[1]-150))
        mask = Image.new("L", track_cov.size, 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, track_cov.size[0], track_cov.size[1]), radius=35, fill=255)
        track_cov.putalpha(mask)
        track_cov = track_cov.crop(track_cov.getbbox())
        banner.paste(track_cov, (75, 75), mask)

        # Editing text
        title_lines = textwrap.wrap(title, 23)
        if len(title_lines) > 1:
            title_lines[1] = title_lines[1] + "..." if len(title_lines) > 2 else title_lines[1]
        title_lines = title_lines[:2]
        artists_lines = textwrap.wrap(" • ".join(artists), width=40)
        if len(artists_lines) > 1:
            for index, art in enumerate(artists_lines):
                if "•" in art[-2:]:
                    artists_lines[index] = art[:art.rfind("•") - 1]

        # Put title and artists to banner
        draw = ImageDraw.Draw(banner)
        x, y = 150+track_cov.size[0], 110
        for index, line in enumerate(title_lines):
            draw.text((x, y), line, font=title_font, fill="#FFFFFF")
            if index != len(title_lines)-1:
                y += 70
        x, y = 150+track_cov.size[0], 110*2
        if len(title_lines) > 1: y += 70
        for index, line in enumerate(artists_lines):
            draw.text((x, y), line, font=art_font, fill="#A0A0A0")
            if index != len(artists_lines)-1:
                y += 50

        # Drawing status bar
        draw.rounded_rectangle([768, 650, 768+1072, 650+15], radius=15//2, fill="#A0A0A0")
        draw.rounded_rectangle([768, 650, 768+int(1072*(progress/duration)), 650+15], radius=15//2, fill="#FFFFFF")
        draw.text((768, 600), f"{(progress//1000//60):02}:{(progress//1000%60):02}", font=time_font, fill="#FFFFFF")
        draw.text((1745, 600), f"{(duration//1000//60):02}:{(duration//1000%60):02}", font=time_font, fill="#FFFFFF")

        by = io.BytesIO()
        banner.save(by, format="PNG"); by.seek(0)
        by.name = "banner.png"
        return by