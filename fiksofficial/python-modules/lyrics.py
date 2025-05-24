# На модуль распространяется лицензия "GNU General Public License v3.0"
# https://github.com/all-licenses/GNU-General-Public-License-v3.0

# meta developer: @PyModule
from lyricsgenius import Genius
from .. import loader, utils

@loader.tds
class LyricsMod(loader.Module):
    """Модуль для поиска текста песни через Genius API"""

    strings = {"name": "Lyrics"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            "GENIUS_TOKEN", 
            None, 
            lambda: "Токен для доступа к Genius API. Получите его на https://genius.com/api-clients",
        )

    def get_genius(self):
        token = self.config["GENIUS_TOKEN"]
        if not token:
            return None
        return Genius(token, timeout=10)

    @loader.command()
    async def lyrics(self, message):
        """[запрос] - Найти текст песни по запросу"""
        genius = self.get_genius()
        if not genius:
            return await message.edit(
                "<emoji document_id=5774077015388852135>❌</emoji> <b>Токен Genius API не установлен. Используйте <code>.cfg Lyrics</code>, чтобы добавить токен.</b>"
            )

        args = utils.get_args_raw(message)
        if not args:
            return await message.edit("<emoji document_id=5253959125838090076>👁</emoji> <b>Использование:</b> .lyrics [запрос]")

        await message.edit(f"<emoji document_id=5253959125838090076>👁</emoji> <b>Ищу текст песни по запросу:</b> {args}...")

        try:
            search_results = genius.search_songs(args)
            if not search_results or not search_results["hits"]:
                return await message.edit("<emoji document_id=5774077015388852135>❌</emoji> <b>Ничего не найдено.</b>")

            song_info = search_results["hits"][0]["result"]
            song = genius.search_song(song_info["title"], song_info["primary_artist"]["name"])

            if not song:
                return await message.edit("<emoji document_id=5774077015388852135>❌</emoji> <b>Не удалось загрузить текст песни.</b>")

            lyrics = song.lyrics
            if len(lyrics) > 4096: 
                lyrics = lyrics[:4000] + "\n\n<b>Текст обрезан из-за ограничения Telegram.</b>"

            await message.edit(
                f"<b><emoji document_id=5938473438468378529>🎶</emoji> {song.title} — {song.artist}</b>\n\n"
                f"<blockquote><b>{lyrics}</b></blockquote>"
            )
        except Exception as e:
            await message.edit(f"<b>Ошибка:</b> {str(e)}")
