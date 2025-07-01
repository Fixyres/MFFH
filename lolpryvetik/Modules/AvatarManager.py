# ©️ LoLpryvet, 2025
# 🌐 https://github.com/lolpryvetik/AvatarManager
# Licensed under GNU AGPL v3.0
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
# meta developer: @LoLpryvet

import io
import aiohttp
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import InputPhoto
from .. import loader, utils


@loader.tds
class AvatarManagerMod(loader.Module):
    """Module for managing profile avatar"""
    
    strings = {
        "name": "AvatarManager",
        "downloading": "🔄 <b>Downloading image...</b>",
        "uploading": "⬆️ <b>Uploading new avatar...</b>",
        "success_set": "✅ <b>Avatar successfully updated!</b>",
        "success_delete": "✅ <b>Current avatar deleted!</b>",
        "no_reply": "❌ <b>Reply to a photo/video to set as avatar</b>",
        "no_media": "❌ <b>Message doesn't contain media</b>",
        "invalid_url": "❌ <b>Invalid URL or unable to download image</b>",
        "no_avatar": "❌ <b>No current avatar to delete</b>",
        "error": "❌ <b>Error occurred: {}</b>",
        "invalid_format": "❌ <b>Invalid file format. Use photo or video</b>"
    }

    strings_ru = {
        "downloading": "🔄 <b>Скачивание изображения...</b>",
        "uploading": "⬆️ <b>Загрузка нового аватара...</b>",
        "success_set": "✅ <b>Аватар успешно обновлен!</b>",
        "success_delete": "✅ <b>Текущий аватар удален!</b>",
        "no_reply": "❌ <b>Ответьте на фото/видео для установки аватара</b>",
        "no_media": "❌ <b>Сообщение не содержит медиа</b>",
        "invalid_url": "❌ <b>Неверная ссылка или не удалось скачать изображение</b>",
        "no_avatar": "❌ <b>Нет текущего аватара для удаления</b>",
        "error": "❌ <b>Произошла ошибка: {}</b>",
        "invalid_format": "❌ <b>Неверный формат файла. Используйте фото или видео</b>"
    }

    async def _download_from_url(self, url: str) -> bytes:
        """Download image from URL"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        return await response.read()
                    else:
                        return None
        except Exception:
            return None

    async def _upload_avatar(self, file_data: bytes) -> bool:
        """Upload avatar from bytes data"""
        try:
            
            file = await self._client.upload_file(
                io.BytesIO(file_data),
                file_name="avatar.jpg"
            )
            
            await self._client(UploadProfilePhotoRequest(file=file))
            return True
        except Exception:
            return False

    async def setavacmd(self, message):
        """Set avatar from reply or URL
        Usage: 
        .setava (reply to photo/video)
        .setava <url>"""
        
        args = utils.get_args_raw(message)
        
        try:
            if args:
                
                await utils.answer(message, self.strings("downloading"))
                
                file_data = await self._download_from_url(args)
                if not file_data:
                    await utils.answer(message, self.strings("invalid_url"))
                    return
                
                await utils.answer(message, self.strings("uploading"))
                success = await self._upload_avatar(file_data)
                
                if success:
                    await utils.answer(message, self.strings("success_set"))
                else:
                    await utils.answer(message, self.strings("error").format("Failed to upload"))
                    
            else:
                
                reply = await message.get_reply_message()
                if not reply:
                    await utils.answer(message, self.strings("no_reply"))
                    return
                
                if not reply.media:
                    await utils.answer(message, self.strings("no_media"))
                    return
                
                
                if not (reply.photo or reply.video):
                    await utils.answer(message, self.strings("invalid_format"))
                    return
                
                await utils.answer(message, self.strings("downloading"))
                
            
                file_data = await reply.download_media(bytes)
                if not file_data:
                    await utils.answer(message, self.strings("error").format("Failed to download"))
                    return
                
                await utils.answer(message, self.strings("uploading"))
                success = await self._upload_avatar(file_data)
                
                if success:
                    await utils.answer(message, self.strings("success_set"))
                else:
                    await utils.answer(message, self.strings("error").format("Failed to upload"))
                    
        except Exception as e:
            await utils.answer(message, self.strings("error").format(str(e)))

    async def delavacmd(self, message):
        """Delete current profile avatar
        Usage: .delava"""
        
        try:
            
            me = await self._client.get_me()
            full_user = await self._client(GetFullUserRequest(me.id))
            
            
            if not full_user.full_user.profile_photo:
                await utils.answer(message, self.strings("no_avatar"))
                return
            
            
            current_photo = full_user.full_user.profile_photo
            
            
            await self._client(DeletePhotosRequest([
                InputPhoto(
                    id=current_photo.id,
                    access_hash=current_photo.access_hash,
                    file_reference=current_photo.file_reference
                )
            ]))
            
            await utils.answer(message, self.strings("success_delete"))
            
        except Exception as e:
            await utils.answer(message, self.strings("error").format(str(e)))

    async def client_ready(self, client, db):
        """Called when client is ready"""
        self._client = client
        self._db = db