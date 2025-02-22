__version__ = (1, 2, 1)
# meta developer: @eremod
#
#
#	.----..----. .----..-.   .-. .----. .----.
#	| {_  | {}  }| {_  |  `.'  |/  {}  \| {}  \
#	| {__ | .-. \| {__ | |\ /| |\      /|     /
#	`----'`-' `-'`----'`-' ` `-' `----' `----'
#
#              	© Copyright 2024
#          	https://t.me/eremod
#
# 🔒      Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/gpl-3.0.html
# Original repository: https://github.com/eremeyko/ne_Hikka

import aiohttp
import os
import tempfile
from pydub import AudioSegment
from hikkatl.types import Message
from .. import loader, utils

UPDATE_URL = (
    'https://raw.githubusercontent.com/eremeyko/ne_Hikka/refs/heads/master/LazyTikTok.py'
)


@loader.tds
class LazyTikTok(loader.Module):
    """Скачивание видео из ТикТока"""

    strings = {
        'name': 'LazyTikTok',
        'downloading': (
            '<emoji document_id=5899757765743615694>⬇️</emoji> '
            'Downloading <a href="{url}">Video</a>'
        ),
        'downloading_music': (
            '<emoji document_id=5899757765743615694>⬇️</emoji> '
            'Downloading music from <a href="{url}">Video</a>'
        ),
        'video_success': (
            '<emoji document_id=5775981206319402773>🎞</emoji> '
            'Your <a href="{url}">Video</a>'
        ),
        'invalid_url': (
            '<emoji document_id=5778527486270770928>❌</emoji> Invalid link.\n\n'
            '<emoji document_id=5823396554345549784>✔️</emoji> Link format: '
            'https://vm.tiktok.com/XXXXXXX/'
        ),
        'no_music': (
            '<emoji document_id=5778527486270770928>❌</emoji> Could not get '
            'music from <a href="{url}">Video</a>'
        ),
        'music_success': (
            '<emoji document_id=6007938409857815902>🎧</emoji> Your Music from '
            '<a href="{url}">Video</a>'
        ),
        'update_available': (
            '<emoji document_id=5771695636411847302>📢</emoji> New version '
            'update available: {version}!\n<emoji '
            'document_id=5967816500415827773>💻</emoji> To update, use: '
            '<code>.dlm {url}</code>'
        ),
    }

    strings_ru = {
        'downloading': (
            '<emoji document_id=5899757765743615694>⬇️</emoji> Скачиваю '
            '<a href="{url}">Видео</a>'
        ),
        'downloading_music': (
            '<emoji document_id=5899757765743615694>⬇️</emoji> Скачиваю музыку '
            'из <a href="{url}">Видео</a>'
        ),
        'video_success': (
            '<emoji document_id=5775981206319402773>🎞</emoji> Ваше '
            '<a href="{url}">Видео</a>'
        ),
        'invalid_url': (
            '<emoji document_id=5778527486270770928>❌</emoji> Некорректная '
            'ссылка.\n\n<emoji document_id=5823396554345549784>✔️</emoji> '
            'Формат ссылки: https://vm.tiktok.com/XXXXXXX/'
        ),
        'no_music': (
            '<emoji document_id=5778527486270770928>❌</emoji> Не удалось '
            'получить музыку из <a href="{url}">Видео</a>'
        ),
        'music_success': (
            '<emoji document_id=6007938409857815902>🎧</emoji> Ваша Музыка из '
            '<a href="{url}">Видео</a>'
        ),
        'update_available': (
            '<emoji document_id=5771695636411847302>📢</emoji> Доступно '
            'обновление до версии: {version}!\n<emoji '
            'document_id=5967816500415827773>💻</emoji> Для обновления '
            'используйте: <code>.dlm {url}</code>'
        ),
    }

    def __init__(self):
        self.update_message = ''

    @loader.loop(interval=10800, autostart=True, wait_before=False)
    async def check_for_updates(self):
        try:
            print('[LazyTikTok | Update Checker] Проверка...')
            async with aiohttp.ClientSession() as session:
                async with session.get(UPDATE_URL) as response:
                    new_version_str = await response.text()
                    if new_version_str.startswith('__version__'):
                        version_line = new_version_str.split('=')[1]
                        version_line = version_line.strip().split('#')[0]
                        version_tuple = version_line.strip('() \n')
                        new_version = tuple(map(int, version_tuple.split(',')))
                        if new_version > __version__:
                            self.update_message = self.strings[
                                'update_available'
                            ].format(
                                version='.'.join(map(str, new_version)),
                                url=UPDATE_URL
                            )
                            print(f'[LazyTikTok] Новая версия обнаружена! '
                                  f'{new_version}')
                        else:
                            self.update_message = ''
        except Exception as e:
            await self._log(f'Ошибка проверки обновления: {e}')

    async def _fetch_data(self, url, session):
        api_url = 'https://downloader.bot/api/tiktok/info'
        headers = {
            'accept': 'application/json, text/plain, */*',
            'content-type': 'application/json'
        }
        data = f'{{"url":"{url}"}}'

        async with session.post(api_url, data=data, headers=headers) as response:
            if response.status == 400:
                return await response.json()
            if response.status != 200:
                return None
            return await response.json()

    async def _download_media(self, message, url, media_type):
        media_msg = self.strings[
            'downloading' if media_type == 'video' else 'downloading_music'
        ].format(url=url)
        media_msg += f'\n\n{self.update_message}'
        m = await utils.answer(message, media_msg)

        async with aiohttp.ClientSession() as session:
            data = await self._fetch_data(url, session)
            if not data or data.get('error'):
                await utils.answer(m, self.strings['invalid_url'] + f'\n\n{self.update_message}')
                return

            media_url = data['data'].get(
                'mp4' if media_type == 'video' else 'mp3'
            )
            if not media_url:
                await utils.answer(
                    m,
                    self.strings[
                        'no_music' if media_type == 'music' else 'invalid_url'
                    ].format(url=url) + f'\n\n{self.update_message}'
                )
                return

            try:
                suffix = '.mp4' if media_type == 'video' else '.mp3'
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
                    temp_path = temp_file.name

                async with session.get(media_url) as media_response:
                    media_data = await media_response.read()
                    with open(temp_path, 'wb') as f:
                        f.write(media_data)

                if media_type == 'music':
                    audio = AudioSegment.from_file(temp_path, format='mp3')
                    audio.export(
                        temp_path,
                        format='mp3',
                        tags={'artist': 'LazyTikTok by @eremod', 'title': url}
                    )

                await utils.answer_file(
                    m,
                    temp_path,
                    caption=self.strings[
                        'music_success' if media_type == 'music' else 'video_success'
                    ].format(url=url) + f'\n\n{self.update_message}',
                    force_document=False
                )

                os.remove(temp_path)

            except Exception as e:
                await self._client.send_message(
                    m.chat_id, 
                    (
                    f'<emoji document_id=5778527486270770928>❌</emoji> '
                    f'Ошибка: {str(e)}' + f'\n\n{self.update_message}'
                    )
                )

        await m.delete()

    @loader.command(ru_doc='Скачивает ТикТок Видео')
    async def ttcmd(self, message: Message):
        """Download TikTok video"""
        args = utils.get_args_raw(message)
        await self._download_media(message, args, 'video')

    @loader.command(ru_doc='Скачивает ТикТок Музыку')
    async def ttmcmd(self, message: Message):
        """Download TikTok music"""
        args = utils.get_args_raw(message)
        await self._download_media(message, args, 'music')
