__version__ = (0, 1, 5)
# meta developer: @Kovalsky_modules


import aiohttp
import os
import tempfile
from pydub import AudioSegment
from hikkatl.types import Message
from .. import loader, utils


@loader.tds
class tiktokModule(loader.Module):
    """Скачивание видео из Tiktok"""

    strings = {
        'name': 'KoTik',
        'video_y': (
            '<emoji document_id=6028234806096041309>🔗</emoji> <a href="{url}">Видео</a> Скачано!'
        ),
        'error': (
            '<emoji document_id=5778527486270770928>❌</emoji> Некорректная ссылка!'
        ),
        'error_music': (
            '<emoji document_id=6028178340160999049>🔇</emoji> Не удалось '
            'получить музыку из Видео'
        ),
        'music_y': (
            '<a href="{url}">Музыка из Видео</a>'
        ),
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "audio_name", 'Музыка из Tiktok',
                "Установить название музыки",
                validator=loader.validators.String(),
            ),
            loader.ConfigValue(
                "audio_artist", '@Kovalsky_modules',
                "Установить автора музыки",
                validator=loader.validators.String(),
            ),
        )


    async def api(self, url, session):
        api = 'https://downloader.bot/api/tiktok/info'
        headers = {
            'accept': 'application/json, text/plain, */*',
            'content-type': 'application/json'
        }
        data = f'{{"url":"{url}"}}'

        async with session.post(api, data=data, headers=headers) as response:
            if response.status == 400:
                return await response.json()
            if response.status != 200:
                return None
            return await response.json()

    async def download(self, message, url, media_type):
        media_msg = '<emoji document_id=6030492936691519063>💬</emoji> Ожидайте...'.format(url=url)
        mv = await utils.answer(message, media_msg)

        async with aiohttp.ClientSession() as session:
            data = await self.api(url, session)
            if not data or data.get('error'):
                await utils.answer(mv, self.strings['error'])
                return

            media_url = data['data'].get(
                'mp4' if media_type == 'video' else 'mp3'
            )
            if not media_url:
                await utils.answer(mv, self.strings[
                        'error_music' if media_type == 'music' else 'error'].format(url=url))
                return

            try:
                suf = '.mp4' if media_type == 'video' else '.mp3'
                with tempfile.NamedTemporaryFile(delete=False, suffix=suf) as temp_file:
                    temp = temp_file.name

                async with session.get(media_url) as media_response:
                    media_data = await media_response.read()
                    with open(temp, 'wb') as f:
                        f.write(media_data)

                if media_type == 'music':
                    audio = AudioSegment.from_file(temp, format='mp3')
                    audio.export(
                        temp,
                        format='mp3',
                        tags={'artist': self.config["audio_artist"], 'title': self.config["audio_name"]}
                    )

                await utils.answer_file(
                    mv,
                    temp,
                    caption=self.strings[
                        'music_y' if media_type == 'music' else 'video_y'].format(url=url),
                    force_document=False
                )

                os.remove(temp)

            except Exception as e:
                pass

        await mv.delete()

    @loader.command(ru_doc='Скачать Музыку')
    async def tm(self, message: Message):
        args = utils.get_args_raw(message)
        await self.download(message, args, 'music')

    @loader.command(ru_doc='Скачать Видео')
    async def tt(self, message: Message):
        args = utils.get_args_raw(message)
        await self.download(message, args, 'video')
