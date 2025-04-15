__version__ = (1, 0, 0)
# meta developer: @psyhomodules

import os
import json
from asyncio import sleep
from telethon import functions, types
from telethon.tl.functions.account import UpdateProfileRequest, UpdateEmojiStatusRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.errors import FileReferenceExpiredError, FileIdInvalidError
from .. import loader, utils

@loader.tds
class CuMod(loader.Module):
    """Копирование профиля пользователя (аватар, имя, фамилия, био, эмодзи-статус)"""

    strings = {
        "name": "CopyUser",
        "no_user": "<b>❌ Укажите пользователя</b> (@username или реплай).",
        "saving_data": "<b>💾 Сохраняем данные...</b>",
        "cloning": "<b>🔄 Клонируем...</b>",
        "success": "<b>✅ Профиль скопирован!</b>",
        "restore_hint": "Восстановить профиль: <code>.restorecu</code>",
        "restoring": "<b>🔄 Восстанавливаем...</b>",
        "restore_success": "<b>✅ Профиль восстановлен!</b>",
        "no_backup": "<b>❌ Нет сохранённых данных.</b>",
        "profile_data": "<b>📋 Данные профиля:</b>\n{}",
        "photo_error": "<b>⚠️ Не удалось загрузить аватарку.</b>"
    }

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    async def cucmd(self, message):
        """.cu <s> <reply/@username>
        s - Скрытый режим
        Примеры: .cu s @user | .cu reply"""
        reply = await message.get_reply_message()
        user = None
        s = False
        args = utils.get_args_raw(message).split()
        for i in args:
            if i.lower() == "s":
                s = True
            else:
                try:
                    user = await message.client.get_entity(i)
                    break
                except Exception:
                    continue
        if user is None and reply is not None:
            user = reply.sender
        if user is None:
            await message.edit(self.strings["no_user"])
            return

        if s:
            await message.delete()
        else:
            await message.edit(self.strings["saving_data"])

        backup_data = await self._save_account_data(message.client)
        if not s:
            for stage in [
                "<b>🔄 Данные... [50%]</b> <code>█████</code>",
                "<b>🔄 Аватар... [80%]</b> <code>████████</code>"
            ]:
                await message.edit(stage)
                await sleep(0.15)

        avs = await message.client.get_profile_photos("me")
        if avs:
            await message.client(functions.photos.DeletePhotosRequest(avs))

        full = await message.client(GetFullUserRequest(user.id))
        user_info = full.users[0]

        about = full.full_user.about or ""
        profile_data = (
            f"<b>Имя:</b> {utils.escape_html(user_info.first_name or '')}\n"
            f"<b>Фамилия:</b> {utils.escape_html(user_info.last_name or '')}\n"
            f"<b>Био:</b> {utils.escape_html(about)}"
        )

        if full.full_user.profile_photo:
            try:
                photo_file = await message.client.download_profile_photo(user.id, file=bytes)
                if photo_file:
                    photo_path = "image.png"
                    with open(photo_path, "wb") as file:
                        file.write(photo_file)
                    file = await message.client.upload_file(photo_path)
                    await message.client(functions.photos.UploadProfilePhotoRequest(file=file))
                    if os.path.exists(photo_path):
                        os.remove(photo_path)
                else:
                    profile_data += f"\n{self.strings['photo_error']}"
            except (FileReferenceExpiredError, FileIdInvalidError, Exception):
                profile_data += f"\n{self.strings['photo_error']}"

        await message.client(
            UpdateProfileRequest(
                first_name=user_info.first_name or "",
                last_name=user_info.last_name or "",
                about=about[:70]
            )
        )

        if user_info.emoji_status:
            await message.client(
                UpdateEmojiStatusRequest(
                    emoji_status=types.EmojiStatus(document_id=user_info.emoji_status.document_id)
                )
            )

        if not s:
            await self.inline.form(
                message=message,
                text=(
                    f"{self.strings['success']}\n"
                    f"{self.strings['restore_hint']}\n"
                    f"{self.strings['profile_data'].format(profile_data)}"
                ),
                reply_markup=[
                    [{"text": "🔄 Восстановить", "callback": self._restore_callback}]
                ]
            )

    async def _save_account_data(self, client):
        full = await client(GetFullUserRequest("me"))
        user_info = full.users[0]
        about = full.full_user.about or ""
        backup_data = {
            "first_name": user_info.first_name or "",
            "last_name": user_info.last_name or "",
            "about": about,
            "emoji_status": user_info.emoji_status.document_id if user_info.emoji_status else None,
            "photo_path": None
        }

        if full.full_user.profile_photo:
            try:
                photo_file = await client.download_profile_photo("me", file=bytes)
                if photo_file:
                    photo_path = "vost.png"
                    with open(photo_path, "wb") as file:
                        file.write(photo_file)
                    backup_data["photo_path"] = photo_path
            except (FileReferenceExpiredError, FileIdInvalidError, Exception):
                pass

        try:
            with open("account.json", "w", encoding="utf-8") as f:
                json.dump(backup_data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass 

        return backup_data

    async def restorecucmd(self, message):
        """.restorecu - Восстановить профиль"""
        await message.edit(self.strings["restoring"])
        try:
            with open("account.json", "r", encoding="utf-8") as f:
                backup_data = json.load(f)

            client = message.client
            avs = await client.get_profile_photos("me")
            if avs:
                await client(functions.photos.DeletePhotosRequest(avs))

            await client(
                UpdateProfileRequest(
                    first_name=backup_data["first_name"],
                    last_name=backup_data["last_name"],
                    about=backup_data["about"]
                )
            )

            if backup_data["emoji_status"]:
                await client(
                    UpdateEmojiStatusRequest(
                        emoji_status=types.EmojiStatus(document_id=backup_data["emoji_status"])
                    )
                )

            if backup_data["photo_path"] and os.path.exists(backup_data["photo_path"]):
                file = await client.upload_file(backup_data["photo_path"])
                await client(functions.photos.UploadProfilePhotoRequest(file=file))
                os.remove(backup_data["photo_path"])

            await message.edit(self.strings["restore_success"])
            await sleep(2)
            await message.delete()

        except FileNotFoundError:
            await message.edit(self.strings["no_backup"])
            await sleep(2)
            await message.delete()
        except Exception as e:
            await message.edit(f"<b>❌ Ошибка восстановления: {str(e)}</b>")
            await sleep(2)
            await message.delete()

    async def _restore_callback(self, call):
        await call.edit(self.strings["restoring"])
        try:
            with open("account.json", "r", encoding="utf-8") as f:
                backup_data = json.load(f)

            client = self._client
            avs = await client.get_profile_photos("me")
            if avs:
                await client(functions.photos.DeletePhotosRequest(avs))

            await client(
                UpdateProfileRequest(
                    first_name=backup_data["first_name"],
                    last_name=backup_data["last_name"],
                    about=backup_data["about"]
                )
            )

            if backup_data["emoji_status"]:
                await client(
                    UpdateEmojiStatusRequest(
                        emoji_status=types.EmojiStatus(document_id=backup_data["emoji_status"])
                    )
                )

            # Восстанавливаем аватарку
            if backup_data["photo_path"] and os.path.exists(backup_data["photo_path"]):
                file = await client.upload_file(backup_data["photo_path"])
                await client(functions.photos.UploadProfilePhotoRequest(file=file))
                os.remove(backup_data["photo_path"])

            await call.edit(self.strings["restore_success"])

        except FileNotFoundError:
            await call.edit(self.strings["no_backup"])
        except Exception as e:
            await call.edit(f"<b>❌ Ошибка восстановления: {str(e)}</b>")
