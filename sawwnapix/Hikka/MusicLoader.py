# meta developer: @angellmodules

import os
import yt_dlp
import asyncio
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from youtube_search import YoutubeSearch
from telethon import events
from telethon.tl.types import DocumentAttributeAudio, MessageMediaDocument
from hikka import loader, utils

SPOTIFY_CLIENT_ID = "0406065a9b5e45f8b2f57a790db340a6"
SPOTIFY_CLIENT_SECRET = "c0ae405be2a84bfb83d3233af19c5f60"

@loader.tds
class MusicLoader(loader.Module):
    """Модуль для скачки песен с разных сервисов"""

    strings = {
        "name": "MusicLoader",
        "no_args": "❌ Укажите ссылку!",
        "not_spotify": "❌ Это не ссылка на трек Spotify!",
        "not_soundcloud": "❌ Это не ссылка на SoundCloud!",
        "track_not_found": "❌ Не удалось найти трек на YouTube!",
        "download_error": "❌ Ошибка загрузки!",
    }

    async def spotycmd(self, message):
        """Скачать песню со Spotify"""
        args = utils.get_args_raw(message)
        if not args:
            return await utils.answer(message, self.strings("no_args"))

        if "spotify.com/track" not in args:
            return await utils.answer(message, self.strings("not_spotify"))

        msg = await utils.answer(message, "🎶 Загружаю песню...")

        try:
            sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
                client_id=SPOTIFY_CLIENT_ID, 
                client_secret=SPOTIFY_CLIENT_SECRET
            ))

            track_id = args.split("/")[-1].split("?")[0]
            track_info = sp.track(track_id)
        except Exception as e:
            return await utils.answer(message, f"❌ Ошибка: {e}")

        title = track_info["name"]
        artist = track_info["artists"][0]["name"]
        search_query = f"{artist} - {title}"

        search = YoutubeSearch(search_query, max_results=1).to_dict()
        if not search:
            return await utils.answer(message, self.strings("track_not_found"))

        video_url = f"https://www.youtube.com{search[0]['url_suffix']}"

        opts = {
            "format": "bestaudio/best",
            "outtmpl": "song.%(ext)s",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
            "quiet": True,
        }

        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([video_url])

        if not os.path.exists("song.mp3"):
            return await utils.answer(message, self.strings("download_error"))

        await message.client.send_file(
            message.chat_id, 
            "song.mp3", 
            caption=f"🎵 {title} - {artist}",
            attributes=[DocumentAttributeAudio(duration=0, title=title, performer=artist)]
        )

        os.remove("song.mp3")
        await msg.delete()

    async def sclcmd(self, message):
        """Скачать песню с SoundCloud"""
        link = utils.get_args_raw(message)

        if not link:
            return await utils.answer(message, self.strings("no_args"))

        if "soundcloud.com" not in link:
            return await utils.answer(message, self.strings("not_soundcloud"))

        chat_id = message.chat_id
        await self._client.send_message("@scload_bot", link)
        await asyncio.sleep(1)
        await message.delete()

        @self._client.on(events.NewMessage(from_users="@scload_bot"))
        async def handler(event):
            if event.media and isinstance(event.media, MessageMediaDocument):
                await self._client.send_file(chat_id, event.media, caption="")
                self._client.remove_event_handler(handler, events.NewMessage(from_users="@scload_bot"))













#тока не воруйте и не вырезайте дева, я на разрабу модулч дохуя время потратил если будете как-то изменять то ставьте 

#made by @zerixgod
