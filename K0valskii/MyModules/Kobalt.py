__version__ = (0, 1, 3)
# meta developer: @Kovalsky_modules
# requires: kobalt

import os
from hikkatl.types import Message
from .. import loader, utils
from pydub import AudioSegment
from Kobalt import CobaltAPI
import mimetypes

@loader.tds
class Kobalt(loader.Module):
    """
    Скачивание видео по ссылке из разных источников.
    Если не указывать качество, будет выбрано Возможные варианты качества:
    
    max, 4320, 2160, 1440, 1080, 720, 480, 360, 240, 144
    """

    strings = {
        'name': 'Kobalt',
        'audio_load': '<emoji document_id=5873204392429096339>📥</emoji> Загрузка <a href="{}">Аудио</a>',
        'audio_send': '<emoji document_id=5361697044723419988>✅</emoji> Ваше <a href="{}">Аудио</a>',
        'audio_error': '<emoji document_id=5361780367088958862>⚠</emoji> Не получилось скачать аудио. Проверьте правильность ссылки',
        'media_load': '<emoji document_id=5873204392429096339>📥</emoji> Загрузка <a href="{}">Медиа</a>',
        'video_send': '<emoji document_id=5361697044723419988>✅</emoji> Ваше <a href="{}">Видео</a>',
        'media_error': '<emoji document_id=5361780367088958862>⚠</emoji> Не получилось скачать медиа. Проверьте правильность ссылки',
        'video_muted': ' без звука',
        'photo_send': '<emoji document_id=5361697044723419988>✅</emoji> Ваше <a href="{}">Фото</a>',
        'services': '<blockquote><b>Поддерживаемые сервисы:</b></blockquote>\n<blockquote>{}</blockquote>',
        'quality_error': '<blockquote><emoji document_id=5361780367088958862>⚠</emoji> Неверное качество видео! Доступные варианты:</blockquote>\n<blockquote>{}</blockquote>'
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "caption", True,
                "Подписывать файлы?",
                validator=loader.validators.Boolean(),
            ),
        )
        
    @loader.command(ru_doc='Поддерживаемые сервисы')
    async def kservicescmd(self, message: Message):
        cobalt = CobaltAPI()
        services = cobalt.services()
        await utils.answer(message, self.strings["services"].format('\n'.join(services)))
        
    @loader.command(ru_doc='Скачать Аудио')
    async def kacmd(self, message: Message):
        cobalt = CobaltAPI()
        cobalt.mode("audio")
        args = utils.get_args_raw(message).split()
        await utils.answer(message, self.strings["audio_load"].format(args[0]))
        try:
            filename = cobalt.download(args[0])
        except:
            await utils.answer(message, self.strings["audio_error"])
            return
            
        me = await self._client.get_me()
        artist = "@" + me.username if me.username else me.first_name
        
        with open(filename, "rb") as f:
            audio = AudioSegment.from_file(filename, format='mp3')
            audio.export(
                        filename,
                        format='mp3',
                        tags={'artist': artist, 'title': f'{filename.split("_")[0]}_audio'}
                    )
            await utils.answer_file(
            message, f,
            caption=self.strings["audio_send"].format(
                args[0]) if self.config["caption"] else None,
            force_document=False
            )
        os.remove(filename)
        

    @loader.command(ru_doc='{url} {quality} - Скачать Медиа')
    async def kmcmd(self, message: Message):
        cobalt = CobaltAPI()
        args = utils.get_args_raw(message).split()
        quality_list = ["max", "4320", "2160", "1440", "1080", "720", "480", "360", "240", "144"]
        
        if len(args) > 1:
            quality = args[1]
            if quality not in quality_list:
                await utils.answer(message, self.strings["quality_error"].format(' '.join(quality_list)))
                return
            cobalt.quality(quality)
        else:
            cobalt.quality("max")
        await utils.answer(message, self.strings["media_load"].format(args[0]))
        try:
            filename = cobalt.download(args[0])
        except:
            await utils.answer(message, self.strings["media_error"])
            return
        mime_type, _ = mimetypes.guess_type(filename)
        if (mime_type and mime_type.startswith('video/')):
            caption = self.strings["video_send"].format(args[0]) if self.config["caption"] else None  
        else:
            caption = self.strings["photo_send"].format(args[0]) if self.config["caption"] else None
        with open(filename, "rb") as f:
            await utils.answer_file(
                message, f,
                caption=caption,
                force_document=False
                )
        os.remove(filename)
        
    @loader.command(ru_doc='{url} {quality} - Скачать Видео без звука')
    async def kmvcmd(self, message: Message):
        args = utils.get_args_raw(message).split()
        cobalt = CobaltAPI()
        cobalt.mode("mute")
        quality_list = ["max", "4320", "2160", "1440", "1080", "720", "480", "360", "240", "144"]
        
            
        if len(args) > 1:
            quality = args[1]
            if quality not in quality_list:
                await utils.answer(message, self.strings["quality_error"].format(' '.join(quality_list)))
                return
            cobalt.quality(quality)
        else:
            cobalt.quality("max")
        args = utils.get_args_raw(message).split()
        await utils.answer(message, self.strings["media_load"].format(args[0])+self.strings["video_muted"])
        try:
            filename = cobalt.download(args[0])
        except:
            await utils.answer(message, self.strings["media_error"])
            return
            
        with open(filename, "rb") as f:
            await utils.answer_file(
            message, f,
            caption=self.strings["video_send"].format(
                args[0])+self.strings["video_muted"] if self.config["caption"] else None,
            force_document=False
            )
        os.remove(filename)
