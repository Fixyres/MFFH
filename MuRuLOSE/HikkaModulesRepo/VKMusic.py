from typing import Union, Dict
import aiohttp
from aiohttp.client_exceptions import ServerTimeoutError
import logging
import tempfile
import ffmpeg

from telethon.types import Message
from .. import loader, utils


"""
    ███    ███ ██    ██ ██████  ██    ██ ██       ██████  ███████ ███████
    ████  ████ ██    ██ ██   ██ ██    ██ ██      ██    ██ ██      ██  
    ██ ████ ██ ██    ██ ██████  ██    ██ ██      ██    ██ ███████ █████
    ██  ██  ██ ██    ██ ██   ██ ██    ██ ██      ██    ██      ██ ██  
    ██      ██  ██████  ██   ██  ██████  ███████  ██████  ███████ ███████ 

                                   
    VKMusic
    📜 Licensed under the GNU AGPLv3	
"""

# meta banner: https://0x0.st/HYVT.jpg
# meta desc: desc
# meta developer: @BruhHikkaModules
# requires: aiohttp ffmpeg-python

logger = logging.getLogger(__name__)


class VKMusicAPI:
    def __init__(self, user_id: str, token: str) -> Union[Dict, int]:
        """VKMusicAPI - class for vk music API

        Arguments:
            user_id {str} -- User ID of user
            token {str} -- Access token

        Returns:
            Dict, int -- Data of music or status code
        """
        self.token = token
        self.user_id = user_id

    async def get_music(
        self,
    ):  # errors:  10 token not set or no right 'доступ в любое время', 20 music are not playing, 30 API not asnwering, 40, status mode, 50 sucsessfull,
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"https://api.vk.com/method/status.get?user_id={self.user_id}&access_token={self.token}&v=5.199",
                    # params={
                    #     "user_id": self.user_id,
                    #     "access_token": self.token,
                    #     "v": "5.199",  # it's last version when module is released
                    # },
                ) as response:
                    data: dict = await response.json()
                    if data['response'].get('audio') is not None:
                        audio = 50, data['response']
                        return audio
                    else:
                        return 40, data['response']['text'] # VKontakte does not return audio in 
                                                            # all cases (see https://dev.vk.com/ru/method/status.get).
                                                            # But it displays it in the status, so we return the status, 
                                                            # but if music is not playing, the user's status will be returned.
                                                            # Also this is VK fault, not my fault
        except ServerTimeoutError:
             return 30


@loader.tds
class VKMusic(loader.Module):
    """Module for VK Music (Remember, if your server is outside of Russia, errors can happen because VK does not want to give out track information due to restrictions)"""

    strings = {
        "name": "VKMusic",
        "no_music": "Music is not playing (not all music is displayed in the status).",
        "server_error": "Server of VK does not answering",
        "music_form": (
            "<emoji document_id=5222175680652917218>🎵</emoji> <b>Listening now:</b> <code>{title}</code>"
            "\n<emoji document_id=5269537556336222550>🐱</emoji> <b>Artist:</b> <code>{artist}</code>"
        ),
        "instructions": (
            "<b>Go to <a href='https://vkhost.github.io/'>vkhost</a>, open settings, leave anytime access and status,"
            "and click get, copy the token and id, and then paste it in properly (in config)."
        ),
        "not_russia": (
            "\n<emoji document_id=5303281542422865331>🇷🇺</emoji> VK gave not all information about" 
            "the track because your userbot server is outside the Russian Federation."
        )
    }

    strings_ru = {
        "_doc_cls": "Модуль для ВК Музыки",
        "no_music": "Музыка не играет (не вся музыка отображается в статусе).",
        "server_error": "Сервер VK не отвечает",
        "music_form": (
            "<emoji document_id=5222175680652917218>🎵</emoji> <b>Сейчас слушает:</b> <code>{title}</code>"
            "\n<emoji document_id=5269537556336222550>🐱</emoji> <b>Исполнитель:</b> <code>{artist}</code>"
        ),
        "instructions": (
            "<b>Зайдите на <a href='https://vkhost.github.io/'>vkhost</a>, откройте настройки, оставьте доступ в любое время и статус,"
            "и нажмите получить, скопируйте токен и айди, а дальше вставьте как положено (в конфиге).</b>"
        ),
        "not_russia": (
            "\n<emoji document_id=5303281542422865331>🇷🇺</emoji> ВК передал не всю информацию" 
            "о треке т.к ваш сервер юзербота за пределами РФ."
        )
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "token",
                "token",
                lambda: "How get token: .vkmtoken",
                validator=loader.validators.Hidden(loader.validators.String()),
            ),
            loader.ConfigValue(
                "user_id",
                "1278631",
                lambda: "Here your userid, (about this in .vkmtoken)",
                validator=loader.validators.Hidden(loader.validators.String()),
            ),
        )

        self._vkmusic = VKMusicAPI(self.config["user_id"], self.config["token"])

    @loader.command(ru_doc=" - Текущая песня")
    async def vkmpnow(self, message: Message):
        """ - Current song"""

        self._vkmusic = VKMusicAPI(
            str(self.config["user_id"]), str(self.config["token"])
        )

        music = await self._vkmusic.get_music()

        if music == 20:
            return await utils.answer(message, self.strings["no_music"])
        elif music == 30:
            return await utils.answer(message, self.strings["server_error"])
        elif music[0] == 50:
            title = music[1]['audio']["title"]
            artist = music[1]['audio']["artist"]
            url = music[1]['audio']["url"] # hikka dont want to work with this url, idk

            with tempfile.TemporaryDirectory() as path:
                (
                    ffmpeg
                    .input(url)
                    .output(path + '/index.mp3', format='mp3')
                    .run()
                )

                # todo: add tags
                await utils.answer_file(
                    message,
                    file=path + '/index.mp3',
                    caption=self.strings["music_form"].format(title=title, artist=artist) +
                    self.strings['not_russia'],
                )

        elif music[0] == 40:
            data = music[1].split('—')
            title = data[1]
            artist = data[0]

            await utils.answer(
                message,
                self.strings["music_form"].format(title=title, artist=artist) +
                self.strings['not_russia'] + '\n\nMusic file is unavailable (sorry)'
            )

    @loader.command(ru_doc=" - Инструкции для токена и пользовательского индетефикатора")
    async def vkmtoken(self, message: Message):
        """- Instructions for token and user ID"""
        await utils.answer(message, self.strings["instructions"])
