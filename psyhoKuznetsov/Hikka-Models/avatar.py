__version__ = (1, 0, 0)
# meta developer: @psyhomodules

from .. import loader, utils
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest
from telethon.tl.types import InputPhoto
import io
import requests

@loader.tds
class Avatar(loader.Module):
    """Аватар инструмент"""
    strings = {
        "name": "Avatar",
        "added": "<b>✅ Добавлено {} аватарок</b>",
        "removed": "<b>✅ Удалено {} аватарок</b>",
        "all_removed": "<b>✅ Все аватарки удалены</b>",
        "no_link": "<b>❌ Укажи ссылку или ответь на фото</b>",
        "invalid_count": "<b>❌ Укажи число аватарок</b>",
        "download_error": "<b>❌ Ошибка загрузки: {}</b>",
        "upload_error": "<b>❌ Ошибка: {}</b>",
        "no_photo": "<b>❌ Нет фото в ответе</b>",
        "empty_file": "<b>❌ Файл пустой</b>"
    }

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    @loader.command()
    async def avataradd(self, message):
        """Добавить аватарки - .AvatarADD <количество> <ответ на фото>"""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()

        if not args:
            await utils.answer(message, self.strings["invalid_count"], parse_mode="HTML")
            return

        try:
            count = int(args.split()[0])
            url = args.split(maxsplit=1)[1] if len(args.split()) > 1 else None
        except (ValueError, IndexError):
            await utils.answer(message, self.strings["invalid_count"], parse_mode="HTML")
            return

        if count <= 0:
            await utils.answer(message, self.strings["invalid_count"], parse_mode="HTML")
            return

        image_bytes = None
        if url:
            try:
                response = requests.get(url, timeout=5)
                image_bytes = response.content
                if not image_bytes:
                    await utils.answer(message, self.strings["empty_file"], parse_mode="HTML")
                    return
            except Exception as e:
                await utils.answer(message, self.strings["download_error"].format(str(e)), parse_mode="HTML")
                return
        elif reply and reply.photo:
            try:
                image_bytes = await reply.download_media(bytes)
                if not image_bytes:
                    await utils.answer(message, self.strings["empty_file"], parse_mode="HTML")
                    return
            except Exception as e:
                await utils.answer(message, self.strings["download_error"].format(str(e)), parse_mode="HTML")
                return
        else:
            await utils.answer(message, self.strings["no_link"], parse_mode="HTML")
            return

        try:
            image_data = io.BytesIO(image_bytes)
            uploaded_file = await self.client.upload_file(image_data, file_name="avatar.jpg")
        except Exception as e:
            await utils.answer(message, self.strings["upload_error"].format(str(e)), parse_mode="HTML")
            return

        success_count = 0
        for _ in range(count):
            try:
                await self.client(UploadProfilePhotoRequest(file=uploaded_file))
                success_count += 1
            except Exception as e:
                await utils.answer(message, self.strings["upload_error"].format(str(e)), parse_mode="HTML")
                break

        if success_count > 0:
            await utils.answer(message, self.strings["added"].format(success_count), parse_mode="HTML")

    @loader.command()
    async def avatarrem(self, message):
        """Удалить аватарки - .AvatarREM <количество>"""
        args = utils.get_args_raw(message)

        if not args:
            await utils.answer(message, self.strings["invalid_count"], parse_mode="HTML")
            return

        try:
            count = int(args)
        except ValueError:
            await utils.answer(message, self.strings["invalid_count"], parse_mode="HTML")
            return

        if count <= 0:
            await utils.answer(message, self.strings["invalid_count"], parse_mode="HTML")
            return

        photos = await self.client.get_profile_photos('me')
        photos_to_delete = photos[:count]

        if not photos_to_delete:
            await utils.answer(message, self.strings["removed"].format(0), parse_mode="HTML")
            return

        photo_ids = [InputPhoto(id=p.id, access_hash=p.access_hash, file_reference=p.file_reference) 
                    for p in photos_to_delete]
        await self.client(DeletePhotosRequest(id=photo_ids))
        await utils.answer(message, self.strings["removed"].format(len(photo_ids)), parse_mode="HTML")

    @loader.command()
    async def avatarremall(self, message):
        """Удалить все аватарки - .AvatarREMALL"""
        photos = await self.client.get_profile_photos('me')
        if not photos:
            await utils.answer(message, self.strings["all_removed"], parse_mode="HTML")
            return

        photo_ids = [InputPhoto(id=p.id, access_hash=p.access_hash, file_reference=p.file_reference) 
                    for p in photos]
        await self.client(DeletePhotosRequest(id=photo_ids))
        await utils.answer(message, self.strings["all_removed"], parse_mode="HTML")
