#  _____                          
# |_   _|____  ____ _ _ __   ___  
#   | |/ _ \ \/ / _` | '_ \ / _ \ 
#   | | (_) >  < (_| | | | | (_) |
#   |_|\___/_/\_\__,_|_| |_|\___/                      
# meta banner: https://envs.sh/oJf.jpg
# meta developer: @Toxano_Modules, @mqvon
from .. import loader, utils
import io
import requests
import json
__version__ = (1, 0, 1)

@loader.tds
class ImgBBUploaderMod(loader.Module):
    """Module for uploading images to imgbb.com"""

    strings = {
        "name": """ImgBBUploader""",
        "uploading": "⚡ <b>Uploading image to ImgBB...</b>",
        "reply_to_image": "❌ <b>Reply to an image!</b>",
        "uploaded": "❤️ <b>Image uploaded to ImgBB!</b>\n\n🔥 <b>Direct URL:</b> <code>{}</code>\n📝 <b>Delete URL:</b> <code>{}</code>\n🔗 <b>Page URL:</b> <code>{}</code>",
        "error": "❌ <b>Error while uploading: {}</b>",
        "not_image": "❌ <b>The file is not an image!</b>",
        "config_api_key": "ImgBB API key. Get it at https://api.imgbb.com/",
        "no_api_key": "❌ <b>No API key provided! Get your API key at https://api.imgbb.com/ and set it with .config ImgBBUploader api_key YOUR_API_KEY</b>"
    }

    strings_ru = {
        "name": """ImgBBUploader""",
        "uploading": "⚡ <b>Загружаю изображение на ImgBB...</b>",
        "reply_to_image": "❌ <b>Ответьте на изображение!</b>",
        "uploaded": "❤️ <b>Изображение загружено на ImgBB!</b>\n\n🔥 <b>Прямая ссылка:</b> <code>{}</code>\n📝 <b>Ссылка для удаления:</b> <code>{}</code>\n🔗 <b>Ссылка на страницу:</b> <code>{}</code>",
        "error": "❌ <b>Ошибка при загрузке: {}</b>",
        "not_image": "❌ <b>Файл не является изображением!</b>",
        "config_api_key": "API ключ ImgBB. Получите его на https://api.imgbb.com/",
        "no_api_key": "❌ <b>API ключ не указан! Получите API ключ на https://api.imgbb.com/ и установите его командой .config ImgBBUploader api_key ВАШ_API_КЛЮЧ</b>"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            "api_key", "f391de54c0741ea2667b5e58b7849d9b", lambda: self.strings["config_api_key"]
        )

    async def _get_image(self, message):
        """Helper to get image from message"""
        reply = await message.get_reply_message()
        if not reply:
            await utils.answer(message, self.strings["reply_to_image"])
            return None
            
        if not reply.media:
            await utils.answer(message, self.strings["reply_to_image"])
            return None
            
        # Check if media is an image
        if not hasattr(reply.media, "photo") and not (
            hasattr(reply.media, "document") and 
            reply.media.document.mime_type and 
            reply.media.document.mime_type.startswith("image/")
        ):
            await utils.answer(message, self.strings["not_image"])
            return None
            
        file = io.BytesIO(await self.client.download_media(reply.media, bytes))
        if hasattr(reply.media, "document"):
            file.name = reply.file.name or f"image_{reply.file.id}.jpg"
        else:
            file.name = f"image_{reply.id}.jpg"
            
        return file

    async def imgbbcmd(self, message):
        """Upload image to imgbb.com"""
        if not self.config["api_key"]:
            await utils.answer(message, self.strings["no_api_key"])
            return
            
        await utils.answer(message, self.strings["uploading"])
        file = await self._get_image(message)
        if not file:
            return
        
        try:
            # Upload to ImgBB
            response = requests.post(
                "https://api.imgbb.com/1/upload",
                params={"key": self.config["api_key"]},
                files={"image": file}
            )
            
            if response.ok:
                data = response.json()
                if data["success"]:
                    image_data = data["data"]
                    direct_url = image_data["url"]
                    delete_url = image_data["delete_url"]
                    page_url = image_data["url_viewer"]
                    
                    await utils.answer(
                        message, 
                        self.strings["uploaded"].format(direct_url, delete_url, page_url)
                    )
                else:
                    await utils.answer(message, self.strings["error"].format("API error"))
            else:
                await utils.answer(message, self.strings["error"].format(f"HTTP {response.status_code}: {response.text}"))
        except Exception as e:
            await utils.answer(message, self.strings["error"].format(str(e)))
