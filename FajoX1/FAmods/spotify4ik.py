#   █▀▀ ▄▀█   █▀▄▀█ █▀█ █▀▄ █▀
#   █▀░ █▀█   █░▀░█ █▄█ █▄▀ ▄█

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: Spotify4ik
# Description: Слушай музыку в Spotify
# meta developer: @FAmods
# meta banner: https://github.com/FajoX1/FAmods/blob/main/assets/banners/spotify4ik.png?raw=true
# requires: spotipy yt-dlp aiohttp
# ---------------------------------------------------------------------------------

import os
import asyncio
import logging
import tempfile
import aiohttp

import yt_dlp
import spotipy

from telethon import types
from telethon.tl.types import ChatAdminRights
from telethon.tl.functions.channels import EditTitleRequest, EditAdminRequest
from telethon.tl.functions.account import UpdateProfileRequest

from aiogram.types import InputFile
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class Spotify4ik(loader.Module):
    """Слушай музыку в Spotify"""

    strings = {
        "name": "Spotify4ik",

        "go_auth_link": """<b><emoji document_id=5271604874419647061>🔗</emoji> Ссылка для авторизации создана!
        
🔐 Перейди по <a href='{}'>этой ссылке</a>.
        
✏️ Потом введи: <code>{}spcode свой_auth_token</code></b>""",

        "need_client_tokens": """<emoji document_id=5472308992514464048>🔐</emoji> <b>Создай приложение по <a href="https://developer.spotify.com/dashboard">этой ссылке</a></b>

<emoji document_id=5467890025217661107>‼️</emoji> <b>Важно:</b> redirect_url приложения должен быть <code>https://sp.fajox.one</code>
        
<b><emoji document_id=5330115548900501467>🔑</emoji> Заполни <code>client_id</code> и <code>client_secret</code> в <code>{}cfg Spotify4ik</code></b>

<b><emoji document_id=5431376038628171216>💻</emoji> И снова напиши <code>{}spauth</code></b>""",

        "no_auth_token": "<emoji document_id=5854929766146118183>❌</emoji> <b>Авторизуйся в свой аккаунт через <code>{}spauth</code></b>",
        "no_song_playing": "<emoji document_id=5854929766146118183>❌</emoji> <b>Сейчас ничего не играет.</b>",
        "no_code": "<emoji document_id=5854929766146118183>❌</emoji> <b>Должно быть <code>{}spcode код_авторизации</code></b>",
        "code_installed": """<b><emoji document_id=5330115548900501467>🔑</emoji> Код авторизации установлен!</b>
        
<emoji document_id=5870794890006237381>🎶</emoji> <b>Наслаждайся музыкой!</b>""",

        "auth_error": "<emoji document_id=5854929766146118183>❌</emoji> <b>Ошибка авторизации:</b> <code>{}</code>",
        "unexpected_error": "<emoji document_id=5854929766146118183>❌</emoji> <b>Произошла ошибка:</b> <code>{}</code>",

        "track_pause": "<b><emoji document_id=6334755820168808080>⏸️</emoji> Трек поставлен на паузу.</b>",
        "track_play": "<b><emoji document_id=5938473438468378529>🎶</emoji> Играю...</b>",

        "track_loading": "<emoji document_id=5334768819548200731>💻</emoji> <b>Загружаю трек...</b>",

        "music_bio_disabled": "<b><emoji document_id=5188621441926438751>🎵</emoji> Стрим музыки в био выключен</b>",
        "music_bio_enabled": "<b><emoji document_id=5188621441926438751>🎵</emoji> Стрим музыки в био включен</b>",

        "track_skipped": "<b><emoji document_id=5188621441926438751>🎵</emoji> Следующий трек...</b>",

        "track_repeat": "<b><emoji document_id=6334550748365325938>🔁</emoji> Трек будет повторяться.</b>",
        "track_norepeat": "<b><emoji document_id=6334550748365325938>🔁</emoji> Трек не будет повторяться.</b>",

        "track_liked": f"<b><emoji document_id=5287454910059654880>❤️</emoji> Трек добавлен в избранное!</b>",

        "channel_music_bio_disabled": "<b><emoji document_id=5188621441926438751>🎵</emoji> Стрим музыки в био канале выключен!</b>",

        "channel_music_bio_enabled": """<b><emoji document_id=5188621441926438751>🎵</emoji> Стрим музыки в био канале включен!</b>
        
<b><emoji document_id=5787544344906959608>ℹ️</emoji> Инструкция:</b>
1. Создай публичный канал (название любое)
2. Добавь канал в профиль
3. Добавь <code>@username</code> канала в config (<code>.cfg Spotify4ik</code> → <code>channel</code>)
4. Готово"""        
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "client_id",
                None,
                lambda: "Айди приложения, Получить: https://developer.spotify.com/dashboard",
                validator=loader.validators.Hidden(loader.validators.String()),
            ),
            loader.ConfigValue(
                "client_secret",
                None,
                lambda: "Секретный ключ приложения, Получить: https://developer.spotify.com/dashboard",
                validator=loader.validators.Hidden(loader.validators.String()),
            ),
            loader.ConfigValue(
                "auth_token",
                None,
                lambda: "Токен для авторизации",
                validator=loader.validators.Hidden(loader.validators.String()),
            ),
            loader.ConfigValue(
                "refresh_token",
                None,
                lambda: "Токен для обновления",
                validator=loader.validators.Hidden(loader.validators.String()),
            ),
            loader.ConfigValue(
                "bio_text",
                "🎵 {track_name} - {artist_name}",
                lambda: "Текст био с текущим треком",
            ),
            loader.ConfigValue(
                "scopes",
                (
                    "user-read-playback-state playlist-read-private playlist-read-collaborative"
                    " app-remote-control user-modify-playback-state user-library-modify"
                    " user-library-read"
                ),
                lambda: "Список разрешений",
            ),
            loader.ConfigValue(
                "use_ytdl",
                False,
                lambda: "Для загрузки файла песни использовать yt-dl",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "channel",
                None,
                lambda: "Канал для показа текущей музыки в био"
            ),
            loader.ConfigValue(
                "stream_upload_track",
                False,
                lambda: "Загрузка трека в био канал для стриминга",
                validator=loader.validators.Boolean(),
            )
        )

    async def client_ready(self, client, db):
        self.db = db
        self._client = client
        self.current_track = ""

        self.musicdl = await self.import_lib(
            "https://famods.fajox.one/assets/musicdl.py",
            suspend_on_error=True,
        )

    async def _create_stream_messages(self, channel):
        await self.client(
            EditAdminRequest(
                channel=channel,
                user_id=self.inline.bot_username,
                admin_rights=ChatAdminRights(
                    change_info=True,
                    post_messages=True,
                    edit_messages=True,
                    delete_messages=True
                ),
                rank="spot"
            )
        )
        
        audio_path = await self.musicdl.dl("The Lost Soul Down - NBSPLV", only_document=True)

        if self.config['stream_upload_track']:
            first_message = await self.client.send_file(
                channel,
                audio_path,
                caption="first_message",
                attributes=[
                    types.DocumentAttributeAudio(
                        duration=0,
                        title="famods",
                        performer=""
                    )
                ],
                thumb="https://github.com/fajox1/famods/raw/main/assets/photo_2025-03-26_17-03-56.jpg"
            )
        else:
            first_message = await self.client.send_message(
                channel,
                "first_message",
            )
        display_message = await self.inline.bot.send_message(int("-100"+str(channel.id)), "display_message")

        self.db.set(self.name, 'stream_upload_message', self.config['stream_upload_track'])

        me = await self.client.get_me()
        me_mention = f"@{me.username}" if me.username else (f"@{me.usernames[0].username}" if me.usernames else me.first_name)
        
        try:
            await self.inline.bot.set_chat_description(
                chat_id=int("-100"+str(channel.id)),
                description=f"Current track playing for the {me_mention}"
            )
        except:
            pass

        self.db.set(self.name, 'stream_channel_data', {
            "first_message": first_message.id,
            "display_message": display_message.message_id,
            "channel": self.config['channel']
        })

    @loader.command()
    async def spauth(self, message):
        """Войти в свой аккаунт"""
        if not self.config['client_id'] or not self.config['client_secret']:
            return await utils.answer(message, self.strings['need_client_tokens'].format(self.get_prefix(), self.get_prefix()))

        sp_oauth = spotipy.oauth2.SpotifyOAuth(
            client_id=self.config['client_id'],
            client_secret=self.config['client_secret'],
            redirect_uri="https://sp.fajox.one",
            scope=self.config['scopes']
        )

        auth_url = sp_oauth.get_authorize_url()

        await utils.answer(message, self.strings['go_auth_link'].format(auth_url, self.get_prefix()))

    @loader.command()
    async def spcode(self, message):
        """Ввести код авторизации"""
        if not self.config['client_id'] or not self.config['client_secret']:
            return await utils.answer(message, self.strings['need_client_tokens'].format(self.get_prefix()))
        code = utils.get_args_raw(message)
        if not code:
            return await utils.answer(message, self.strings['no_code'].format(self.get_prefix()))

        sp_oauth = spotipy.oauth2.SpotifyOAuth(
            client_id=self.config['client_id'],
            client_secret=self.config['client_secret'],
            redirect_uri="https://sp.fajox.one",
            scope=self.config['scopes']
        )
        token_info = sp_oauth.get_access_token(code)
        self.config['auth_token'] = token_info['access_token']
        self.config['refresh_token'] = token_info['refresh_token']

        try:
            sp = spotipy.Spotify(auth=token_info['access_token'])
            current_playback = sp.current_playback()
        except spotipy.oauth2.SpotifyOauthError as e:
            return await utils.answer(message, self.strings['auth_error'].format(str(e)))
        except Exception as e:
            return await utils.answer(message, self.strings['unexpected_error'].format(str(e)))

        await utils.answer(message, self.strings['code_installed'])

    @loader.command()
    async def sppause(self, message):
        """Поставить на паузу текущий трек"""
        if not self.config['auth_token']:
            return await utils.answer(message, self.strings['no_auth_token'].format(self.get_prefix()))

        sp = spotipy.Spotify(auth=self.config['auth_token'])

        try:
            sp.pause_playback()
        except spotipy.oauth2.SpotifyOauthError as e:
            return await utils.answer(message, self.strings['auth_error'].format(str(e)))
        except spotipy.exceptions.SpotifyException as e:
            if "Restriction violated" in str(e):
                return await utils.answer(message, self.strings['track_pause'])
            if "The access token expired" in str(e):
                return await utils.answer(message, self.strings['no_auth_token'].format(self.get_prefix()))
            if "NO_ACTIVE_DEVICE" in str(e):
                return await utils.answer(message, self.strings['no_song_playing'])
            return await utils.answer(message, self.strings['unexpected_error'].format(str(e)))
        await utils.answer(message, self.strings['track_pause'])

    @loader.command()
    async def spplay(self, message):
        """Воспроизвести текущий трек"""
        if not self.config['auth_token']:
            return await utils.answer(message, self.strings['no_auth_token'].format(self.get_prefix()))

        sp = spotipy.Spotify(auth=self.config['auth_token'])

        try:
            sp.start_playback()
        except spotipy.oauth2.SpotifyOauthError as e:
            return await utils.answer(message, self.strings['auth_error'].format(str(e)))
        except spotipy.exceptions.SpotifyException as e:
            if "Restriction violated" in str(e):
                return await utils.answer(message, self.strings['track_play'])
            if "The access token expired" in str(e):
                return await utils.answer(message, self.strings['no_auth_token'].format(self.get_prefix()))
            if "NO_ACTIVE_DEVICE" in str(e):
                return await utils.answer(message, self.strings['no_song_playing'])
            return await utils.answer(message, self.strings['unexpected_error'].format(str(e)))
        await utils.answer(message, self.strings['track_play'])

    @loader.command()
    async def spbegin(self, message):
        """Включить текущий трек с начала"""
        if not self.config['auth_token']:
            return await utils.answer(message, self.strings['no_auth_token'].format(self.get_prefix()))

        sp = spotipy.Spotify(auth=self.config['auth_token'])

        try:
            current_playback = sp.current_playback()
            if not current_playback or not current_playback.get('item'):
                return await utils.answer(message, self.strings['no_song_playing'])

            track_uri = current_playback['item']['uri']
            sp.start_playback(uris=[track_uri])
            sp.seek_track(0)
            await utils.answer(message, self.strings['track_play'])
        except spotipy.oauth2.SpotifyOauthError as e:
            return await utils.answer(message, self.strings['auth_error'].format(str(e)))
        except spotipy.exceptions.SpotifyException as e:
            if "The access token expired" in str(e):
                return await utils.answer(message, self.strings['no_auth_token'].format(self.get_prefix()))
            if "NO_ACTIVE_DEVICE" in str(e):
                return await utils.answer(message, self.strings['no_song_playing'])
                return await utils.answer(message, self.strings['unexpected_error'].format(str(e)))

    @loader.command()
    async def spback(self, message):
        """Включить предыдущий трек"""
        if not self.config['auth_token']:
            return await utils.answer(message, self.strings['no_auth_token'].format(self.get_prefix()))

        sp = spotipy.Spotify(auth=self.config['auth_token'])

        try:
            sp.previous_track()
        except spotipy.oauth2.SpotifyOauthError as e:
            return await utils.answer(message, self.strings['auth_error'].format(str(e)))
        except spotipy.exceptions.SpotifyException as e:
            if "The access token expired" in str(e):
                return await utils.answer(message, self.strings['no_auth_token'].format(self.get_prefix()))
            if "NO_ACTIVE_DEVICE" in str(e):
                return await utils.answer(message, self.strings['no_song_playing'])
                return await utils.answer(message, self.strings['unexpected_error'].format(str(e)))

        await utils.answer(message, self.strings['track_play'])

    @loader.command()
    async def spnext(self, message):
        """Включить следующий трек"""
        if not self.config['auth_token']:
            return await utils.answer(message, self.strings['no_auth_token'].format(self.get_prefix()))

        sp = spotipy.Spotify(auth=self.config['auth_token'])

        try:
            sp.next_track()
        except spotipy.oauth2.SpotifyOauthError as e:
            return await utils.answer(message, self.strings['auth_error'].format(str(e)))
        except spotipy.exceptions.SpotifyException as e:
            if "Restriction violated" in str(e):
                return await utils.answer(message, self.strings['track_play'])
            if "The access token expired" in str(e):
                return await utils.answer(message, self.strings['no_auth_token'].format(self.get_prefix()))
            if "NO_ACTIVE_DEVICE" in str(e):
                return await utils.answer(message, self.strings['no_song_playing'])
                return await utils.answer(message, self.strings['unexpected_error'].format(str(e)))
        await utils.answer(message, self.strings['track_skipped'])

    @loader.command()
    async def spbio(self, message):
        """Включить/выключить стрим текущего трека в био"""
        if not self.config['auth_token']:
            return await utils.answer(message, self.strings['no_auth_token'].format(self.get_prefix()))

        if self.db.get(self.name, "bio_change", False):
            self.db.set(self.name, 'bio_change', False)
            return await utils.answer(message, self.strings['music_bio_disabled'])

        self.db.set(self.name, 'bio_change', True)
        await utils.answer(message, self.strings['music_bio_enabled'])

    @loader.command()
    async def spbiochannel(self, message):
        """Включить/выключить стрим текущего трека в канале в био"""
        if not self.config['auth_token']:
            return await utils.answer(message, self.strings['no_auth_token'].format(self.get_prefix()))

        if self.db.get(self.name, "channel_bio_change", False):
            self.db.set(self.name, 'channel_bio_change', False)
            return await utils.answer(message, self.strings['channel_music_bio_disabled'])

        self.db.set(self.name, 'channel_bio_change', True)
        await utils.answer(message, self.strings['channel_music_bio_enabled'])

    @loader.command()
    async def splike(self, message):
        """Лайкнуть текущий трек"""
        if not self.config['auth_token']:
            return await utils.answer(message, self.strings['no_auth_token'].format(self.get_prefix()))

        sp = spotipy.Spotify(auth=self.config['auth_token'])

        try:
            current_playback = sp.current_playback()
            if not current_playback or not current_playback.get('item'):
                return await utils.answer(message, self.strings['no_song_playing'])

            track_id = current_playback['item']['id']
            sp.current_user_saved_tracks_add([track_id])
            await utils.answer(message, self.strings['track_liked'])
        except spotipy.oauth2.SpotifyOauthError as e:
            return await utils.answer(message, self.strings['auth_error'].format(str(e)))
        except spotipy.exceptions.SpotifyException as e:
            if "The access token expired" in str(e):
                return await utils.answer(message, self.strings['no_auth_token'].format(self.get_prefix()))
            if "NO_ACTIVE_DEVICE" in str(e):
                return await utils.answer(message, self.strings['no_song_playing'])
            return await utils.answer(message, self.strings['unexpected_error'].format(str(e)))

    @loader.command()
    async def sprepeat(self, message):
        """Повторить текущий трек"""
        if not self.config['auth_token']:
            return await utils.answer(message, self.strings['no_auth_token'].format(self.get_prefix()))

        sp = spotipy.Spotify(auth=self.config['auth_token'])

        try:
            current_playback = sp.current_playback()
            if not current_playback or not current_playback.get('item'):
                return await utils.answer(message, self.strings['no_song_playing'])

            sp.repeat("track")
            await utils.answer(message, self.strings['track_repeat'])
        except spotipy.oauth2.SpotifyOauthError as e:
            return await utils.answer(message, self.strings['auth_error'].format(str(e)))
        except spotipy.exceptions.SpotifyException as e:
            if "The access token expired" in str(e):
                return await utils.answer(message, self.strings['no_auth_token'].format(self.get_prefix()))
            if "NO_ACTIVE_DEVICE" in str(e):
                return await utils.answer(message, self.strings['no_song_playing'])
            return await utils.answer(message, self.strings['unexpected_error'].format(str(e)))
        
    @loader.command()
    async def spnorepeat(self, message):
        """Перестать повторять текущий трек"""
        if not self.config['auth_token']:
            return await utils.answer(message, self.strings['no_auth_token'].format(self.get_prefix()))

        sp = spotipy.Spotify(auth=self.config['auth_token'])

        try:
            current_playback = sp.current_playback()
            if not current_playback or not current_playback.get('item'):
                return await utils.answer(message, self.strings['no_song_playing'])

            sp.repeat("no")
            await utils.answer(message, self.strings['track_norepeat'])
        except spotipy.oauth2.SpotifyOauthError as e:
            return await utils.answer(message, self.strings['auth_error'].format(str(e)))
        except spotipy.exceptions.SpotifyException as e:
            if "The access token expired" in str(e):
                return await utils.answer(message, self.strings['no_auth_token'].format(self.get_prefix()))
            if "NO_ACTIVE_DEVICE" in str(e):
                return await utils.answer(message, self.strings['no_song_playing'])
            return await utils.answer(message, self.strings['unexpected_error'].format(str(e)))

    @loader.command()
    async def spnow(self, message):
        """Текущий трек"""
        if not self.config['auth_token']:
            return await utils.answer(message, self.strings['no_auth_token'].format(self.get_prefix()))

        try:
            sp = spotipy.Spotify(auth=self.config['auth_token'])
            current_playback = sp.current_playback()

            if not current_playback or not current_playback.get('item'):
                return await utils.answer(message, self.strings['no_song_playing'])

            await utils.answer(message, self.strings['track_loading'])

            track = current_playback['item']
            track_name = track.get('name', 'Unknown Track')
            artist_name = track['artists'][0].get('name', 'Unknown Artist')
            album_name = track['album'].get('name', 'Unknown Album')
            duration_ms = track.get('duration_ms', 0)
            progress_ms = current_playback.get('progress_ms', 0)
            is_playing = current_playback.get('is_playing', False)

            duration_min, duration_sec = divmod(duration_ms // 1000, 60)
            progress_min, progress_sec = divmod(progress_ms // 1000, 60)

            playlist = current_playback.get('context', {}).get('uri', '').split(':')[-1] if current_playback.get('context') else None
            device_name = current_playback.get('device', {}).get('name', 'Unknown Device')+" "+current_playback.get('device', {}).get('type', '')
            device_type = current_playback.get('device', {}).get('type', 'unknown')

            user_profile = sp.current_user()
            user_name = user_profile['display_name']
            user_id = user_profile['id']

            track_url = track['external_urls']['spotify']
            user_url = f"https://open.spotify.com/user/{user_id}"
            playlist_url = f"https://open.spotify.com/playlist/{playlist}" if playlist else None

            track_info = (
                f"<b>🎧 Now Playing</b>\n\n"
                f"<b><emoji document_id=5188705588925702510>🎶</emoji> {track_name} - <code>{artist_name}</code>\n"
                f"<b><emoji document_id=5870794890006237381>💿</emoji> Album:</b> <code>{album_name}</code>\n\n"
                f"<b><emoji document_id=6007938409857815902>🎧</emoji> Device:</b> <code>{device_name}</code>\n"
                + (("<b><emoji document_id=5872863028428410654>❤️</emoji> From favorite tracks</b>\n" if "playlist/collection" in playlist_url else
                    f"<b><emoji document_id=5944809881029578897>📑</emoji> From Playlist:</b> <a href='{playlist_url}'>View</a>\n") if playlist else "")
                + f"\n<b><emoji document_id=5902449142575141204>🔗</emoji> Track URL:</b> <a href='{track_url}'>Open in Spotify</a>"
            )

            with tempfile.TemporaryDirectory() as temp_dir:
                if self.config['use_ytdl']:
                    audio_path = os.path.join(temp_dir, f"{artist_name} - {track_name}.mp3")

                    ydl_opts = {
                        "format": "bestaudio/best[ext=mp3]",
                        "outtmpl": audio_path,
                        "noplaylist": True,
                    }

                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([f"ytsearch1:{track_name} - {artist_name}"])

                else:
                    audio_path = await self.musicdl.dl(f"{artist_name} - {track_name}", only_document=True)

                album_art_url = track['album']['images'][0]['url']
                async with aiohttp.ClientSession() as session:
                    async with session.get(album_art_url) as response:
                        art_path = os.path.join(temp_dir, "cover.jpg")
                        with open(art_path, "wb") as f:
                            f.write(await response.read())

            await self._client.send_file(
                message.chat_id,
                audio_path,
                caption=track_info,
                attributes=[
                    types.DocumentAttributeAudio(
                        duration=duration_ms//1000,
                        title=track_name,
                        performer=artist_name
                    )
                ],
                thumb=art_path,
                reply_to=message.reply_to_msg_id if message.is_reply else getattr(message, "top_id", None)
            )

            await message.delete()

        except spotipy.oauth2.SpotifyOauthError as e:
            return await utils.answer(message, self.strings['auth_error'].format(str(e)))
        except spotipy.exceptions.SpotifyException as e:
            if "The access token expired" in str(e):
                return await utils.answer(message, self.strings['no_auth_token'].format(self.get_prefix()))
            if "NO_ACTIVE_DEVICE" in str(e):
                return await utils.answer(message, self.strings['no_song_playing'])
            return await utils.answer(message, self.strings['unexpected_error'].format(str(e)))

    @loader.loop(interval=60*40, autostart=True)
    async def loop_token(self):
        if not self.config['auth_token']:
            return

        try:
            sp_oauth = spotipy.oauth2.SpotifyOAuth(
                client_id=self.config['client_id'],
                client_secret=self.config['client_secret'],
                redirect_uri="https://sp.fajox.one",
                scope=self.config['scopes']
            )

            token_info = sp_oauth.refresh_access_token(self.config['refresh_token'])
            self.config['auth_token'] = token_info['access_token']
            self.config['refresh_token'] = token_info['refresh_token']
        except Exception as e:
            pass
        #    logger.error(f"Failed to refresh Spotify token: {str(e)}", exc_info=True)

    @loader.loop(interval=70, autostart=True)
    async def loop(self):
        if not self.config['auth_token']:
            return
        
        if not self.db.get(self.name, "channel_bio_change", False):
            return
        if not self.config['channel']:
            return
                    
        sp = spotipy.Spotify(auth=self.config['auth_token'])
        current_playback = sp.current_playback()

        if not current_playback or not current_playback.get('item'):
            return
        
        track = current_playback['item']
        track_name = track.get('name', 'Unknown Track')
        artist_name = track['artists'][0].get('name', 'Unknown Artist')

        current_track = f"{track_name} - {artist_name}"
        last_track = self.db.get(self.name, "last_track", False)
        if last_track == current_track:
            return

        self.db.set(self.name, 'last_track', f"{track_name} - {artist_name}")

        channel = await self.client.get_entity(self.config['channel'])

        stream_channel_data = self.db.get(self.name, "stream_channel_data", False)
        stream_upload_message = self.db.get(self.name, "stream_upload_message", True)

        if not stream_channel_data or self.config['channel'] != stream_channel_data['channel'] or self.config['stream_upload_track'] != stream_upload_message:
            await self._create_stream_messages(channel)
            await asyncio.sleep(3)

        stream_channel_data = self.db.get(self.name, "stream_channel_data", False)

        artist_link = track['artists'][0]['external_urls']['spotify']
        album_name = track['album'].get('name', 'Unknown Album')
        track_url = track['external_urls']['spotify']
        duration_ms = track.get('duration_ms', 0)
        playlist = current_playback.get('context', {}).get('uri', '').split(':')[-1] if current_playback.get('context') else None
        device_name = current_playback.get('device', {}).get('name', 'Unknown Device')+" "+current_playback.get('device', {}).get('type', '')
        playlist_url = f"https://open.spotify.com/playlist/{playlist}" if playlist else None

        keyboard = InlineKeyboardMarkup()
        keyboard.add(
            InlineKeyboardButton(
                text="Open in Spotify", 
                url=track_url
            )
        )

        now_play_text = f"""
<b><emoji document_id=5188705588925702510>🎶</emoji> {track_name} - <code>{artist_name}</code>
<b><emoji document_id=5870794890006237381>💿</emoji> Album:</b> <code>{album_name}</code>

<b><emoji document_id=6007938409857815902>🎧</emoji> Device:</b> <code>{device_name}</code>
"""+ (("<b><emoji document_id=5872863028428410654>❤️</emoji> From favorite tracks</b>\n" if "playlist/collection" in playlist_url else
                    f"<b><emoji document_id=5944809881029578897>📑</emoji> From Playlist:</b> <a href='{playlist_url}'>View</a>\n") if playlist else "")

        if self.config['stream_upload_track']:
            with tempfile.TemporaryDirectory() as temp_dir:
                if self.config['use_ytdl']:
                    audio_path = os.path.join(temp_dir, f"{artist_name} - {track_name}.mp3")

                    ydl_opts = {
                        "format": "bestaudio/best[ext=mp3]",
                        "outtmpl": audio_path,
                        "noplaylist": True,
                    }

                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([f"ytsearch1:{track_name} - {artist_name}"])

                else:
                    audio_path = await self.musicdl.dl(f"{artist_name} - {track_name}", only_document=True)

                album_art_url = track['album']['images'][0]['url']
                async with aiohttp.ClientSession() as session:
                    async with session.get(album_art_url) as response:
                        art_path = os.path.join(temp_dir, "cover.jpg")
                        with open(art_path, "wb") as f:
                            f.write(await response.read())

                await self.inline.bot.set_chat_photo(
                    chat_id=int("-100"+str(channel.id)),
                    photo=InputFile(art_path)
                )
        
                await self.client.edit_message(
                    entity=channel.username,
                    message=stream_channel_data['first_message'],
                    file=audio_path,
                    attributes=[
                        types.DocumentAttributeAudio(
                            duration=duration_ms//1000,
                            title=track_name,
                            performer=artist_name
                        )
                    ],
                    thumb=art_path,
                    text=now_play_text
                )

        else:
            with tempfile.TemporaryDirectory() as temp_dir:
                album_art_url = track['album']['images'][0]['url']
                async with aiohttp.ClientSession() as session:
                    async with session.get(album_art_url) as response:
                        art_path = os.path.join(temp_dir, "cover.jpg")
                        with open(art_path, "wb") as f:
                            f.write(await response.read())

                await self.inline.bot.set_chat_photo(
                    chat_id=int("-100"+str(channel.id)),
                    photo=InputFile(art_path)
                )
            await self.client.edit_message(
                entity=channel.username,
                message=stream_channel_data['first_message'],
                text="<b>🎧 Now Playing</b>\n"+now_play_text
            )

        try:
            await self.inline.bot.edit_message_reply_markup(
                chat_id=int("-100"+str(channel.id)),
                message_id=stream_channel_data['first_message'],
                reply_markup=keyboard
            )
        except:
            await self._create_stream_messages(channel)
        await asyncio.sleep(2.3342)
        try:
            await self.client.edit_message(
                entity=channel,
                message=stream_channel_data['display_message'],
                text=f"<emoji document_id=5346074681004801565>📱</emoji> <a href='{artist_link}'>{artist_name}</a>",
                link_preview=False
            )
        except:
            pass
            
        await asyncio.sleep(1.3342)

        try:
            await self.inline.bot.set_chat_title(
                chat_id=int("-100"+str(channel.id)),
                title=f"🎧 {track_name}"
            )

            messages = await self.client.get_messages(
                entity=channel,
                limit=2
            )
            for message in messages:
                await message.delete()
        except:
            return
        
    @loader.loop(interval=90, autostart=True)
    async def loop_bio(self):
        if self.db.get(self.name, "bio_change", False):
            return
        sp = spotipy.Spotify(auth=self.config['auth_token'])
        try:
            current_playback = sp.current_playback()
            if current_playback and current_playback.get('item'):
                track = current_playback['item']
                track_name = track.get('name', 'Unknown Track')
                artist_name = track['artists'][0].get('name', 'Unknown Artist')
                bio = self.config['bio_text'].format(track_name=track_name, artist_name=artist_name)
                await self._client(UpdateProfileRequest(about=bio[:70]))
        except Exception as e:
            logger.error(f"Error updating bio: {e}")
