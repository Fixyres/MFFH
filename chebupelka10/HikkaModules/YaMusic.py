# meta developer: @RemoveWoman

import logging
import asyncio
import logging
import aiohttp
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


class YaMusicMod(loader.Module):
    """
    Модуль для Яндекс.Музыки. Основан на YmNow от vsecoder. Теперь работает со всеми треками! Создатель: @RemoveWoman [BETA]
    """
    strings = {
        "name": "YaMusic",
        "no_token": "<b><emoji document_id=5843952899184398024>🚫</emoji> Укажи токен в конфиге! Если вы видите это сообщение но уже угазали токен то убедитесь в его правильности. Если ваш токен начинается с y0 то отпишите мне @RemoveWoman.</b>",
        "playing": "<b><emoji document_id=6030440409241488777>🎵</emoji> Сейчас играет: </b><code>{}</code><b> - </b><code>{}</code>\n<b><emoji document_id=6030802195811669198>🎵</emoji> Плейлист:</b> <code>{}</code>\n<b><emoji document_id=6030821505984630931>🕐</emoji> Длина трека: {}</b>\n\n<emoji document_id=5463424079568584767>🎧</emoji> <b>Слушаю на Яндекс.Музыке</b>\n\n<b><emoji document_id=6030333284167192486>🔗</emoji> <a href=\"{}\">Открыть в Яндекс.Музыке</a>\n<emoji document_id=6030333284167192486>🔗</emoji> <a href=\"{}\">Открыть на song.link</a></b>",
        "no_args": "<b><emoji document_id=5843952899184398024>🚫</emoji> Укажи аргументы!</b>",
        "state": "<emoji document_id=6030742019024883631>📄</emoji> <b>Виджеты теперь {}</b>\n{}",
        "tutorial": (
            "ℹ️ <b>Чтобы включить виджет, отправь сообщение в нужный чат с текстом"
            " </b><code>{YANDEXMUSIC}</code>"
        ),
        "no_results": "<b><emoji document_id=5285037058220372959>☹️</emoji> Ничего не найдено :(</b>",
        "autobioe": "<b>🔁 Autobio включен</b>",
        "autobiod": "<b>🔁 Autobio выключен</b>",
        "_cls_doc": "Модуль для Яндекс.Музыки. Основан на YmNow от vsecoder. Теперь работает со всеми треками! Создатель: @RemoveWoman [BETA]",
        "already_liked": "<b><emoji document_id=5843952899184398024>🚫</emoji> Текущий трек уже лайкнут!</b>",
        "liked": "<b><emoji document_id=5310109269113186974>❤️</emoji> Лайкнул текущий трек!</b>",
        "not_liked": "<b><emoji document_id=5843952899184398024>🚫</emoji> Текущий трек не лайкнут!</b>",
        "disliked": "<b><emoji document_id=5471954395719539651>💔</emoji> Дизлайкнул текущий трек!</b>",
        "my_wave": "<b><emoji document_id=5472377424228396503>🤭</emoji> Я до сих пор не могу найти трек. Попробуйте еще раз. Если ошибка повторяется то проверьте токен на правильность. Если ваш токен начинается на y0 то отпишите мне @RemoveWoman</b>",
        "_cfg_yandexmusictoken": "Токен аккаунта Яндекс.Музыка",
        "_cfg_autobiotemplate": "Шаблон для AutoBio",
        "_cfg_automesgtemplate": "Шаблон для AutoMessage",
        "_cfg_update_interval": "Интервал обновления виджета и био",
        "guide": (
            '<a href="https://github.com/MarshalX/yandex-music-api/discussions/513#discussioncomment-2729781">'
            "Инструкция по получению токена Яндекс.Музыка</a>"
        ),
        "configuring": "<emoji document_id=6030742019024883631>📄</emoji> <b>Виджет готов и скоро будет обновлен</b>",
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
            
    @loader.command()
    async def automsgcmd(self, message: Message):
        """Переключить виджеты Яндекс Музыки."""
        state = not self.get("state", False)
        self.set("state", state)
        await utils.answer(
            message,
            self.strings["state"].format(
                "on" if state else "off", self.strings("tutorial") if state else ""
            ),
        )

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue("YandexMusicToken", None, lambda: self.strings["_cfg_yandexmusictoken"], validator=loader.validators.Hidden()),
            loader.ConfigValue("AutoBioTemplate", "🎧 {}", lambda: self.strings["_cfg_autobiotemplate"], validator=loader.validators.String()),
            loader.ConfigValue("AutoMessageTemplate", "🎧 {}", lambda: self.strings["_cfg_automesgtemplate"], validator=loader.validators.String()),
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

    @loader.command()
    async def yanowcmd(self, message: Message):
        """Показывает что вы сейчас слушаете на яндекс музыке."""

        if not self.config["YandexMusicToken"]:
            await utils.answer(message, self.strings["no_token"])
            return

        collecting_msg = await utils.answer(
            message,
            "<emoji document_id=5463424079568584767>🎧</emoji> <b>Собираю данные о том, что вы слушаете на Яндекс.Музыке</b>"
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
        """❤ Поставить лайк на трек, который вы сейчас слушаете на Яндекс.Музыке"""
        if not self.config["YandexMusicToken"]:
            await utils.answer(message, self.strings["no_token"])
            return

        collecting_msg = await utils.answer(
            message, 
            "<emoji document_id=5463424079568584767>🎧</emoji> <b>Собираю информацию о том, что вы слушаете на Яндекс.Музыке</b>"
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
            
    @loader.command()
    async def yadislikecmd(self, message: Message):
        """💔 Поставить дизлайк на трек, который вы сейчас слушаете на Яндекс.Музыке"""
        if not self.config["YandexMusicToken"]:
            await utils.answer(message, self.strings["no_token"])
            return

        collecting_msg = await utils.answer(
            message,
            "<emoji document_id=5463424079568584767>🎧</emoji> <b>Собираю информацию о том, что вы слушаете на Яндекс.Музыке</b>"
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
                await client.users_likes_tracks_remove([track["id"]])
                await utils.answer(message, self.strings["disliked"])
            else:
                await utils.answer(message, self.strings["not_liked"])
        except Exception as e:
            await utils.answer(message, f"<b>Ошибка: {e}</b>")
            
    async def yafindcmd(self, message: Message):
        """Ищет трек по названию на яндекс музыке."""
        args = utils.get_args_raw(message)

        if not args:
            reply = await message.get_reply_message()
            if reply:
                args = reply.raw_text
            else:
                await utils.answer(message, "<emoji document_id=5843952899184398024>🚫</emoji> <b>Вы не указали название песни</b>")
                return

        await utils.answer(message, "<emoji document_id=5463424079568584767>🎧</emoji> <b>Ищу трек на Яндекс.Музыке</b>")

        try:
            results = await message.client.inline_query("@LyBot", args)
            await results[0].click(
                message.chat_id,
                hide_via=True,
                reply_to=message.reply_to_msg_id if message.reply_to_msg_id else None
            )
            await message.delete()
        except Exception as e:
            if "The bot did not answer to the callback query in time" in str(e):
                await utils.answer(message, "<emoji document_id=5843952899184398024>🚫</emoji> <b>Ошибка, трека не существует.</b>")
            else:
                await utils.answer(message, f"<emoji document_id=5843952899184398024>🚫</emoji> <b>Произошла ошибка: {e}</b>")
            
    @loader.command()
    async def yabio(self, message: Message):
        """Переключатель показа в био трека который вы слушаете."""

        if not self.config["YandexMusicToken"]:
            await utils.answer(message, self.strings["no_token"])
            return

        try:
            client = ClientAsync(self.config["YandexMusicToken"])
            await client.init()
        except:
            await utils.answer(message, self.strings["no_token"])
            return

        current = self.get("autobio", False)
        new = not current
        self.set("autobio", new)

        if new:
            await utils.answer(message, self.strings["autobioe"])
            self.autobio.start()
        else:
            await utils.answer(message, self.strings["autobiod"])
            self.autobio.stop()

    @loader.loop(interval=60)
    async def autobio(self):
        client = ClientAsync(self.config["YandexMusicToken"])

        await client.init()

        res = await get_current_track(client, self.config["YandexMusicToken"])

        track = res["track"]

        track = track[0]  # type: ignore

        title = track["title"]
        artists = [artist["name"] for artist in track["artists"]]
        duration_ms = int(track["duration_ms"])

        text = self.config["AutoBioTemplate"].format(
            f"{', '.join(artists)} - {title}"
        )

        try:
            await self.client(
                UpdateProfileRequest(about=text[: 140 if self._premium else 70])
            )
        except FloodWaitError as e:
            logger.info(f"Sleeping {e.seconds}")
            await sleep(e.seconds)
            return
    
    
    async def watcher(self, message: Message):
        try:
            if "{YANDEXMUSIC}" not in getattr(message, "text", "") or not message.out:
                return

            chat_id = utils.get_chat_id(message)
            message_id = message.id

            self.set(
                "widgets",
                self.get("widgets", []) + [(chat_id, message_id, message.text)],
            )

            await utils.answer(message, self.strings["configuring"])
            await self._parse(do_not_loop=True)
        except Exception as e:
            logger.exception("Can't send widget")
            await utils.respond(message, self.strings["error"].format(e))
