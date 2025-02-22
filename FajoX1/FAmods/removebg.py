#   █▀▀ ▄▀█   █▀▄▀█ █▀█ █▀▄ █▀
#   █▀░ █▀█   █░▀░█ █▄█ █▄▀ ▄█

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: RemoveBG
# Description: Убрать фон из изображения
# meta developer: @FAmods
# meta banner: https://github.com/FajoX1/FAmods/blob/main/assets/banners/removebg.png?raw=true
# requires: aiohttp
# ---------------------------------------------------------------------------------

import os
import asyncio
import tempfile
import logging
import aiohttp

from aiohttp import FormData

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class RemoveBG(loader.Module):
    """Убрать фон из изображения"""

    strings = {
        "name": "RemoveBG",

        "must_be_forced": "<emoji document_id=5854929766146118183>❌</emoji> <b>Фото не должно быть сжатым!</b>",
        "no_photo": "<emoji document_id=5854929766146118183>❌</emoji> <b>Нужно ответить на фото!</b>",
        "no_token": "<emoji document_id=5854929766146118183>❌</emoji> <b>Нету токена! Поставь его в <code>{}cfg RemoveBG</code></b>",
        "invalid_token": "<b>😕 Неверный токен</b>",
        "only_photo": "<b>😕 Удалять фон можно только с фото (.png, .jpg, .jpeg)</b>",

        "removing_bg": "<emoji document_id=5326015457155620929>🔄</emoji> <b>Удаление фона...</b>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "api_token",
                None,
                lambda: "Токен для работы с API. Взять можно на сайте https://www.remove.bg/dashboard#api-key",
                validator=loader.validators.Hidden(loader.validators.String()),
            ),
        )


    async def client_ready(self, client, db):
        self.db = db
        self._client = client

    @loader.command()
    async def removebg(self, message):
        """Убрать фон из изображения"""
        
        reply = await message.get_reply_message()
        if not reply:
            return await utils.answer(message, self.strings("no_photo"))
        
        try:
            if not any(ext in reply.file.name for ext in [".png", ".jpg", ".jpeg"]):
              return await utils.answer(message, self.strings['only_photo'])
        except TypeError:
            return await utils.answer(message, self.strings['must_be_forced'])

        if not self.config["api_token"]:
            return await utils.answer(message, self.strings["no_token"].format(self.get_prefix()))

        await utils.answer(message, self.strings['removing_bg'])

        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                file_path = os.path.join(temp_dir, reply.file.name)
                await reply.download_media(file_path)
            except TypeError:
                return await utils.answer(message, self.strings['must_be_forced'])

            access_token = self.config["api_token"]
            async with aiohttp.ClientSession() as session:
                form_data = FormData()
                form_data.add_field('image_file', open(file_path, 'rb'))
                form_data.add_field('size', 'auto')

                async with session.post(
                    'https://api.remove.bg/v1.0/removebg',
                    headers={'X-Api-Key': access_token},
                    data=form_data
                ) as res:
                    try:
                        response_json = await res.json()
                        if 'errors' in response_json and response_json['errors'][0]['title'] == "API Key invalid":
                            return await utils.answer(message, self.strings['invalid_token'])
                    except Exception as e:
                        print(f"Error processing response: {e}")

                    file_name = f"famods-no-bg-{os.path.splitext(reply.file.name)[0]}.png"
                    with open(os.path.join(temp_dir, file_name), 'wb') as out:
                        out.write(await res.read())

            await message.client.send_file(message.chat_id, os.path.join(temp_dir, file_name), force_document=True)
            await message.delete()