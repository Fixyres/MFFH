# meta developer: @murpiz

import logging
import asyncio
import logging
import aiohttp
import eyed3
import random
import json
import string
from asyncio import sleep
from yandex_music import ClientAsync
from telethon import TelegramClient
from telethon.tl.types import Message
from telethon.errors.rpcerrorlist import FloodWaitError
from telethon.tl.functions.account import UpdateProfileRequest
from .. import loader, utils  # type: ignore
import os
import aiofiles

logger = logging.getLogger(__name__)
logging.getLogger("yandex_music").propagate = False


# https://github.com/FozerG/YandexMusicRPC/blob/main/main.py#L133
async def get_current_track(client, token):
    device_info = {
        "app_name": "Chrome",
        "type": 1,
    }

    ws_proto = {
        "Ynison-Device-Id": "".join(
            [random.choice(string.ascii_lowercase) for _ in range(16)]
        ),
        "Ynison-Device-Info": json.dumps(device_info),
    }

    timeout = aiohttp.ClientTimeout(total=15, connect=10)
    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.ws_connect(
                url="wss://ynison.music.yandex.ru/redirector.YnisonRedirectService/GetRedirectToYnison",
                headers={
                    "Sec-WebSocket-Protocol": f"Bearer, v2, {json.dumps(ws_proto)}",
                    "Origin": "http://music.yandex.ru",
                    "Authorization": f"OAuth {token}",
                },
                timeout=10,
            ) as ws:
                recv = await ws.receive()
                data = json.loads(recv.data)

            if "redirect_ticket" not in data or "host" not in data:
                print(f"Invalid response structure: {data}")
                return {"success": False}

            new_ws_proto = ws_proto.copy()
            new_ws_proto["Ynison-Redirect-Ticket"] = data["redirect_ticket"]

            to_send = {
                "update_full_state": {
                    "player_state": {
                        "player_queue": {
                            "current_playable_index": -1,
                            "entity_id": "",
                            "entity_type": "VARIOUS",
                            "playable_list": [],
                            "options": {"repeat_mode": "NONE"},
                            "entity_context": "BASED_ON_ENTITY_BY_DEFAULT",
                            "version": {
                                "device_id": ws_proto["Ynison-Device-Id"],
                                "version": 9021243204784341000,
                                "timestamp_ms": 0,
                            },
                            "from_optional": "",
                        },
                        "status": {
                            "duration_ms": 0,
                            "paused": True,
                            "playback_speed": 1,
                            "progress_ms": 0,
                            "version": {
                                "device_id": ws_proto["Ynison-Device-Id"],
                                "version": 8321822175199937000,
                                "timestamp_ms": 0,
                            },
                        },
                    },
                    "device": {
                        "capabilities": {
                            "can_be_player": True,
                            "can_be_remote_controller": False,
                            "volume_granularity": 16,
                        },
                        "info": {
                            "device_id": ws_proto["Ynison-Device-Id"],
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

            async with session.ws_connect(
                url=f"wss://{data['host']}/ynison_state.YnisonStateService/PutYnisonState",
                headers={
                    "Sec-WebSocket-Protocol": f"Bearer, v2, {json.dumps(new_ws_proto)}",
                    "Origin": "http://music.yandex.ru",
                    "Authorization": f"OAuth {token}",
                },
                timeout=10,
                method="GET",
            ) as ws:
                await ws.send_str(json.dumps(to_send))
                recv = await asyncio.wait_for(ws.receive(), timeout=10)
                ynison = json.loads(recv.data)
                track_index = ynison["player_state"]["player_queue"][
                    "current_playable_index"
                ]
                if track_index == -1:
                    print("No track is currently playing.")
                    return {"success": False}
                track = ynison["player_state"]["player_queue"]["playable_list"][
                    track_index
                ]

            await session.close()
            info = await client.tracks_download_info(track["playable_id"], True)
            track = await client.tracks(track["playable_id"])
            res = {
                "paused": ynison["player_state"]["status"]["paused"],
                "duration_ms": ynison["player_state"]["status"]["duration_ms"],
                "progress_ms": ynison["player_state"]["status"]["progress_ms"],
                "entity_id": ynison["player_state"]["player_queue"]["entity_id"],
                "repeat_mode": ynison["player_state"]["player_queue"]["options"][
                    "repeat_mode"
                ],
                "entity_type": ynison["player_state"]["player_queue"]["entity_type"],
                "track": track,
                "info": info,
                "success": True,
            }
            return res

    except Exception as e:
        print(f"Failed to get current track: {str(e)}")
        return {"success": False}


class YaMu(loader.Module):
    """
    Модуль для Яндекс.Музыки. Основан на YmNow от vsecoder (@vsecoder_m). Создатель: @murpiz [BETA]
    """
    strings = {
        "name": "YaMu",
        "no_token": "<b><emoji document_id=6030801830739448093>⚠️</emoji>  Укажи токен в конфиге! Если ты видишь это сообщение, но уже указал токен, то убедись в его правильности.</b>",
        "liked": "<b><emoji document_id=5208446645892562826>💘</emoji> Текущий трек был добавлен в плейлист 'Мне нравится' </b>",
        "already_liked": "<b><emoji document_id=6030801830739448093>⚠️</emoji> Текущий трек уже был добавлен</b>",
        "playing": """<b><emoji document_id=5334665104677941170>🎵</emoji> Сейчас играет: </b><code>{}</code><b> - </b><code>{}</code>
<b><emoji document_id=6030802195811669198>🎵</emoji> Альбом:</b> <code>{}</code>
<b><emoji document_id=4904882772637648609>⏰</emoji> Продолжительность: {}</b>

<emoji document_id=5426955812905959118>🗯</emoji><b>Слушаю на Яндекс.Музыке</b>

<emoji document_id=6030333284167192486>🔗</emoji><a href=\"{}\">Открыть в Яндекс.Музыке</a>
<emoji document_id=6030333284167192486>🔗</emoji><a href=\"{}\">Открыть на song.link</a></b>""",
      "_cls_doc": " Модуль для Яндекс.Музыки. Основан на YmNow от vsecoder. Создатель: @murpiz",
       "my_wave": "<b><emoji document_id=6030801830739448093>⚠️</emoji> Я до сих пор не могу найти что вы слушаете. Проверьте токен на правильность.</b>",
        "_cfg_yandexmusictoken": "Токен аккаунта Яндекс.Музыка",
        "guide": (
            '<a href="https://github.com/MarshalX/yandex-music-api/discussions/513#discussioncomment-2729781">'
            "Инструкция по получению токена Яндекс.Музыка</a>"
        ),
    }

    async def _parse(self, do_not_loop: bool = False):
        while True:
            for widget in self.get("widgets", []):
                if not self.config["YandexMusicToken"]:
                    logger.error("YandexMusicToken is missing")
                    return

                try:
                    client = ClientAsync(self.config["YandexMusicToken"])
                    await client.init()
                except Exception as e:
                    logger.error(f"Failed to initialize Yandex client: {e}")
                    return

                try:
                    res = await get_current_track(client, self.config["YandexMusicToken"])
                    track = res.get("track")

                    if not track:
                        track = await self.get_last_liked_track(client)

                    if not track:
                        logger.info("No current track found")
                        continue

                    artists = ", ".join(track.artists_name())
                    title = track.title + (f" ({track.version})" if track.version else "")

                    try:
                        await self._client.edit_message(
                            *widget[:2],
                            self.config["AutoMessageTemplate"].format(f"{artists} - {title}")
                        )
                    except FloodWaitError:
                        pass
                    except Exception:
                        logger.debug("YaNow widget update failed")
                        self.set("widgets", list(set(self.get("widgets", [])) - set([widget])))
                        continue

                except Exception as e:
                    logger.error(f"Error fetching or updating track info: {e}")
                    continue

            if do_not_loop:
                break

            await asyncio.sleep(int(self.config["update_interval"]))

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue("YandexMusicToken", None, lambda: self.strings["_cfg_yandexmusictoken"], validator=loader.validators.Hidden()),
            loader.ConfigValue("update_interval", 300, lambda: self.strings["_cfg_update_interval"], validator=loader.validators.Integer(minimum=100)),
        )

    async def on_dlmod(self):
        if not self.get("guide_send", False):
            await self.inline.bot.send_message(
                self._tg_id,
                self.strings["guide"],
            )
            self.set("guide_send", True)

    async def client_ready(self, client: TelegramClient, db):
        self.client = client
        self.db = db
        self._premium = getattr(await self.client.get_me(), "premium", False)
        if self.get("autobio", False):
            self.autobio.start()

    async def yafindcmd(self, message: Message):
        """Команда для поиска трека на Яндекс.Музыке."""
        args = utils.get_args_raw(message)

        if not args:
            reply = await message.get_reply_message()
            if reply:
                args = reply.raw_text.strip()
            else:
                await utils.answer(
                    message,
                    "<emoji document_id=5843952899184398024>🚫</emoji> <b>Вы не указали название трека.</b>"
                )
                return

        query = f"s:ynd {args}"

        await utils.answer(
            message,
            "<emoji document_id=5258396243666681152>🔎</emoji> <b>Ищу трек</b>"
        )

        try:
            results = await message.client.inline_query("@murglar_bot", query)

            if not results:
                await utils.answer(
                    message,
                    "<emoji document_id=5843952899184398024>🚫</emoji> <b>Трек не найден на Яндекс.Музыке.</b>"
                )
                return

            await results[0].click(
                entity=message.chat_id,
                hide_via=True,
                reply_to=message.reply_to_msg_id if message.reply_to_msg_id else None
            )
            await message.delete()

        except Exception as e:
            error_message = str(e)
            await utils.answer(
                message,
                f"<emoji document_id=5843952899184398024>🚫</emoji> <b>Произошла ошибка: {error_message}</b>"
            )

    @loader.command()
    async def yanowcmd(self, message: Message):
         """Показывает что вы сейчас слушаете."""

         if not self.config["YandexMusicToken"]:
            await utils.answer(message, self.strings["no_token"])
            return

         collecting_msg = await utils.answer(
            message,
            "<emoji document_id=5426955812905959118>🗯</emoji> <b>Обращаюсь к API Яндекс Музыки</b>"
        )

         try:
            client = ClientAsync(self.config["YandexMusicToken"])
            await client.init()
         except Exception:
            await utils.answer(message, self.strings["no_token"])
            return

         try:
            res = await get_current_track(client, self.config["YandexMusicToken"])
            track = res["track"]

            if not track:
                await utils.answer(message, self.strings["no_results"])
                return

            track = track[0]  # type: ignore
            link = res["info"][0]["direct_link"]  # type: ignore
            title = track["title"]
            artists = [artist["name"] for artist in track["artists"]]
            duration_ms = int(track["duration_ms"])
            
            if track['cover_uri']:
                cover = None
            else:
                async with aiohttp.ClientSession() as session:
                    async with session.get(image_url) as response:
                        if response.status == 200:
                            cover = await response.read()
                            
            album_id = track["albums"][0]["id"] if track["albums"] else None
            playlist_name = "Нет плейлиста"
            if album_id:
                albums = await client.albums(album_id)
                playlist_name = albums[0].title if albums else "Неизвестный альбом"

            lnk = track["id"]
            yandex_music_url = f"https://music.yandex.ru/album/{album_id}/track/{track['id']}" if album_id else "Нет ссылки"
            song_link_url = f"https://song.link/ya/{lnk}"

            caption = self.strings["playing"].format(
                utils.escape_html(", ".join(artists)),
                utils.escape_html(title),
                utils.escape_html(playlist_name),
                f"{duration_ms // 1000 // 60:02}:{duration_ms // 1000 % 60:02}",
                yandex_music_url,
                song_link_url
            )

            info = await client.tracks_download_info(track["id"], True)
            file_url = info[0].direct_link

            file_name = f"{', '.join(artists)} - {title}.mp3"
            async with aiofiles.open(file_name, 'wb') as f:
                async with aiohttp.ClientSession() as session:
                    async with session.get(file_url) as resp:
                        if resp.status == 200:
                            await f.write(await resp.read())
            audiofile = eyed3.load(file_name)
            if audiofile != None:
                audiofile.initTag()
                            
                song = audiofile.tag
                            
                song.title = title
                song.artist = ', '.join(artists)
                song.album = playlist_name
                if cover != None: song.images.set(eyed3.id3.frames.ImageFrame.FRONT_COVER, cover, "image/png")
                song.save()

            await self.client.send_file(
                message.chat_id,
                file_name,
                caption=caption,
                reply_to=message.reply_to_msg_id if message.reply_to_msg_id else None,
                voice=False,
                supports_streaming=True
            )
            await collecting_msg.delete()

            os.remove(file_name)

         except Exception as e:
            await utils.answer(message, f"<b>Ошибка получения трека: {e}</b>")
            
   

    @loader.command()
    async def yalikecmd(self, message: Message):
         """Добавить проигрываемый трек в плейлист 'Мне нравится"""
         if not self.config["YandexMusicToken"]:
            await utils.answer(message, self.strings["no_token"])
            return

         collecting_msg = await utils.answer(
            message, 
            "<emoji document_id=5426955812905959118>🗯</emoji> <b>Обращаюсь к API Яндекс Музыки</b>"
        )

         try:
            client = ClientAsync(self.config["YandexMusicToken"])
            await client.init()
         except Exception:
            await utils.answer(message, self.strings["no_token"])
            return

         try:
            res = await get_current_track(client, self.config["YandexMusicToken"])
            track = res.get("track")

            if not track:
                await utils.answer(message, self.strings["no_results"])
                return

            track = track[0]  # type: ignore

            liked_tracks = await client.users_likes_tracks()
            liked_tracks = await liked_tracks.fetch_tracks_async()

            if isinstance(liked_tracks, list) and any(liked.id == track["id"] for liked in liked_tracks):
                await utils.answer(message, self.strings["already_liked"])
            else:
                await client.users_likes_tracks_add([track["id"]])
                await utils.answer(message, self.strings["liked"])
         except Exception as e:
            await utils.answer(message, f"<b>Ошибка: {e}</b>")
            