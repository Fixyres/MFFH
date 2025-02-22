#   █▀▀ ▄▀█   █▀▄▀█ █▀█ █▀▄ █▀
#   █▀░ █▀█   █░▀░█ █▄█ █▄▀ ▄█

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: Telegrapher
# Description: Создание статей и другое связанное с telegra.ph
# meta developer: @FAmods
# meta banner: https://github.com/FajoX1/FAmods/blob/main/assets/banners/telegrapher.png?raw=true
# requires: aiohttp telegraph
# ---------------------------------------------------------------------------------

import logging
import aiohttp
import asyncio
from telegraph import Telegraph

from telethon import types
from telethon.tl.types import DocumentAttributeFilename
from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class Telegrapher(loader.Module):
    """Создание статей и другое связанное с telegra.ph"""

    strings = {
        "name": "Telegrapher",

        "waiting": "<b><emoji document_id=6334391057186293707>🕑</emoji> Создаю страницу на telegra.ph...</b>",
        "waiting_up": "<b><emoji document_id=6334391057186293707>🕑</emoji> Загружаю файл на telegra.ph...</b>",

        "article_ready": """<b>
<emoji document_id=6334758581832779720>✅</emoji> Твоя статья в Telegra.ph создана!

<emoji document_id=5271604874419647061>🔗</emoji> Ссылка: {}

<emoji document_id=6334638004920911460>ℹ️</emoji> </b><i>Редактировать заголовок/контент/автора на странице можно в <code>{}cfg telegrapher</code></i>
""",
        "upload_ready": """<b>
<emoji document_id=6334353510582191829>⬇️</emoji> Файл загружен!

<emoji document_id=5271604874419647061>🔗</emoji> Ссылка: {}
</b>""",
       "upload_error": "<emoji document_id=5019523782004441717>❌</emoji> <b>Ошибка при выгрузке файла на telegra.ph!</b>",

       "media_type_invalid": "<emoji document_id=5019523782004441717>❌</emoji> <b>Ответь на фото или видео/гиф</b>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "TITLE",
                "FAmods telegrapher",
                lambda: "Заголовок статьи",
            ),
            loader.ConfigValue(
                "CONTENT",
                "Редактировать заголовок/контент/автора на странице можно в .cfg telegrapher",
                lambda: "Контент статьи (можно использовать html-разметку)",
            ),
            loader.ConfigValue(
                "author_name",
                "famods",
                lambda: "Автор статьи",
            ),
            loader.ConfigValue(
                "author_short_name",
                "famods",
                lambda: "Короткое имя автора статьи (нужно для авторизации в telegraph api)",
            ),
        )


    async def client_ready(self, client, db):
        self.db = db
        self._client = client

    @loader.command()
    async def tghpost(self, message):
        """Выложить статью в telegra.ph"""

        await utils.answer(message, self.strings['waiting'])

        telegraph_api = Telegraph() 
        telegraph_api.create_account(short_name=self.config["author_short_name"], author_name=self.config["author_name"])
        response = telegraph_api.create_page(
            title=self.config["TITLE"], 
            html_content=self.config["CONTENT"],
            author_name=self.config["author_name"],
         )

        return await utils.answer(message, self.strings['article_ready'].format(f"https://telegra.ph/{response['path']}", self.get_prefix()))

    @loader.command()
    async def tghup(self, message):
        """Выложить медиа в telegra.ph"""
        reply_message = await message.get_reply_message()

        if not reply_message or not reply_message.media:
            await utils.answer(message, self.strings['media_type_invalid'])
            return
        
        await utils.answer(message, self.strings['waiting_up'])

        media_data = await self.check_media_type(reply_message.media)

        if not media_data:
            await utils.answer(message, self.strings['media_type_invalid'])
            return

        file_content = await message.client.download_media(media_data, bytes)
        telegraph_upload_url = "https://telegra.ph/upload"
        form = aiohttp.FormData()
        form.add_field('file', file_content, filename='file')

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(telegraph_upload_url, data=form) as response:
                    uploaded_data = await response.json()
                    telegraph_link = "https://telegra.ph" + uploaded_data[0]["src"]
        except Exception as e:
            logger.error(e)
            return await utils.answer(message, self.strings['upload_error'])

        await utils.answer(message, self.strings['upload_ready'].format(telegraph_link))

    async def check_media_type(self, media):
        if not media:
            return False

        if isinstance(media, types.MessageMediaPhoto):
            media_data = media.photo
        elif isinstance(media, types.MessageMediaDocument):
            document = media.document

            if any(
                isinstance(attribute, types.DocumentAttributeAudio)
                for attribute in document.attributes
            ):
                return False

            if DocumentAttributeFilename(file_name="AnimatedSticker.tgs") in document.attributes:
                return False

            media_data = document
        else:
            return False

        return media_data
