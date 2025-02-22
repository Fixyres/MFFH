from hikkatl.types import Message
from .. import loader, utils
import urllib.request
import re
import aiohttp

"""
    ███    ███ ██    ██ ██████  ██    ██ ██       ██████  ███████ ███████
    ████  ████ ██    ██ ██   ██ ██    ██ ██      ██    ██ ██      ██  
    ██ ████ ██ ██    ██ ██████  ██    ██ ██      ██    ██ ███████ █████
    ██  ██  ██ ██    ██ ██   ██ ██    ██ ██      ██    ██      ██ ██  
    ██      ██  ██████  ██   ██  ██████  ███████  ██████  ███████ ███████ 


    YoutubeSearcher
    📜 Licensed under the GNU AGPLv3	
"""


# meta desc: desc
# meta developer: @BruhHikkaModules
# requires: aiohttp


@loader.tds
class YoutubeSearcher(loader.Module):
    """Ищет видео в ютуб"""

    strings = {"name": "YoutubeSearcher", "change_api_key": "Change api key"}

    strings_ru = {"change_api_key": "Поменяйте ключ API на свой."}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "api_key",
                "Change it",
                lambda: self.strings("change_api_key"),
                validator=loader.validators.Hidden(),
            )
        )

    @loader.command()
    async def ytsearch(self, message: Message):
        """- [Запрос поиска] [Максимальное количество видео] Ищет видео в ютуб"""
        query = utils.get_args_split_by(message, " ")
        api_key = self.config["api_key"]
        if api_key == "Change it":
            await utils.answer(message, self.strings("change_api_key"))

        base_url = "https://www.googleapis.com/youtube/v3/search"

        params = {
            "key": api_key,
            "part": "snippet",
            "q": query[0],
            "maxResults": query[1],  # Количество результатов поиска
            "type": "video",
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(base_url, params=params) as response:
                data = await response.json()
                video_text = ""

                for item in data["items"]:
                    video_id = item["id"]["videoId"]
                    video_title = item["snippet"]["title"]
                    video_url = f"https://www.youtube.com/watch?v={video_id}"
                    video_text += f"Ссылка на видео: {video_url}\nНазвание: <b>{video_title}</b>\n\n"
                await utils.answer(message, video_text)
