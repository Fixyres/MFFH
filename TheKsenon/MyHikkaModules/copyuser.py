# ------------------------------------------------------------
# Module: CopyUser
# Description: One command, and you are already another.
# Author: @kmodules
# ------------------------------------------------------------
# Licensed under the GNU AGPLv3
# https:/www.gnu.org/licenses/agpl-3.0.html
# ------------------------------------------------------------
# Author: @MeKsenon
# Commands: .copyuser .backupme .restoreme
# scope: hikka_only
# meta banner: https://i.ibb.co/515XxY1/e3583b3c-434a-49fc-b532-cc70a3b5eccc.jpg
# meta developer: @kmodules
# ------------------------------------------------------------

from .. import loader, utils
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.account import UpdateProfileRequest, UpdateEmojiStatusRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest
from telethon.errors import UsernameNotOccupiedError, UsernameInvalidError, ImageProcessFailedError
from telethon import types, functions
import io
import requests
import os

__version__ = (1, 0, 9)

@loader.tds
class ProfileToolsModule(loader.Module):
    """Copy profile data from any user"""
    strings = {
        "name": "CopyUser",
        "user_not_found": "<emoji document_id=5210952531676504517>❌</emoji><b>Failed to find user!</b>",
        "specify_user": "<emoji document_id=5832251986635920010>➡️</emoji><b>Specify user (reply/@username/ID)!</b>",
        "profile_copied": "<emoji document_id=5397916757333654639>➕</emoji> <b>User profile copied!</b>",
        "username_not_found": "<emoji document_id=5240241223632954241>🚫</emoji> <b>User not found!</b>",
        "invalid_username": "<emoji document_id=5240241223632954241>🚫</emoji> <b>Invalid username/ID format.</b>",
        "backup_saved": "<emoji document_id=5294096239464295059>🔵</emoji> <b>Your current profile has been saved. You can restore it using</b> <code>restoreme</code>\n\n<b>⚙️ Current Avatar URL: {}</b>",
        "no_backup": "❌ <b>No backup found!</b>",
        "profile_restored": "<emoji document_id=5294096239464295059>🔵</emoji> <b>Your previous profile has been restored.</b>",
        "error": "😵 Error: {}"
    }

    strings_ru = {
        "name": "CopyUser",
        "user_not_found": "<emoji document_id=5210952531676504517>❌</emoji><b>Не удалось найти пользователя!</b>",
        "specify_user": "<emoji document_id=5832251986635920010>➡️</emoji><b>Укажите пользователя (reply/@username/ID)!</b>",
        "profile_copied": "<emoji document_id=5397916757333654639>➕</emoji> <b>Профиль пользователя скопирован!</b>",
        "username_not_found": "<emoji document_id=5240241223632954241>🚫</emoji> <b>Пользователь не найден!</b>", 
        "invalid_username": "<emoji document_id=5240241223632954241>🚫</emoji> <b>Неверный формат юзернейма/ID.</b>",
        "backup_saved": "<emoji document_id=5294096239464295059>🔵</emoji> <b>Ваш данный профиль сохранен. Вы можете вернуть его используя</b> <code>restoreme</code>\n\n<b>⚙️ URL данной Аватарки: {}</b>",
        "no_backup": "❌ <b>Резервная копия не найдена!</b>",
        "profile_restored": "<emoji document_id=5294096239464295059>🔵</emoji> <b>Ваш прошлый профиль возвращен.</b>",
        "error": "😵 Ошибка: {}"
    }

    def init(self):
        self.name = self.strings["name"]
        self._backup_data = None

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    async def upload_to_0x0(self, photo_bytes):
        try:
            files = {'file': ('photo.png', photo_bytes)}
            response = requests.post(
                'https://0x0.st',
                files=files,
                data={'secret': True}
            )
            return response.text.strip()
        except Exception as e:
            return f"Error: {str(e)}"

    @loader.command(ru_doc="Скопировать профиль пользователя (работает по reply/@username/ID)", en_doc="Copy user profile (works with reply/@username/ID)")
    async def copyuser(self, message):
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        
        try:
            if args:
                try:
                    if args.isdigit():
                        user = await message.client.get_entity(int(args))
                    else:
                        user = await message.client.get_entity(args)
                except ValueError:
                    await utils.answer(message, self.strings["user_not_found"])
                    return
            elif reply:
                user = await reply.get_sender()
            else:
                await utils.answer(message, self.strings["specify_user"])
                return

            full = await message.client(GetFullUserRequest(user.id))
            user_info = full.users[0]
            me = await message.client.get_me()
            
            if full.full_user.profile_photo:
                try:
                    photos = await message.client.get_profile_photos(user.id)
                    if photos:
                        await message.client(DeletePhotosRequest(
                            await message.client.get_profile_photos("me")
                        ))
                        
                        photo = await message.client.download_media(photos[0])
                        await message.client(UploadProfilePhotoRequest(
                            file=await message.client.upload_file(photo)
                        ))
                        os.remove(photo)
                except:
                    pass
            
            await message.client(UpdateProfileRequest(
                first_name=user_info.first_name if user_info.first_name is not None else "",
                last_name=user_info.last_name if user_info.last_name is not None else "",
                about=full.full_user.about[:70] if full.full_user.about is not None else "",
            ))

            if hasattr(user_info, 'emoji_status') and user_info.emoji_status and me.premium:
                try:
                    await message.client(
                        UpdateEmojiStatusRequest(
                            emoji_status=user_info.emoji_status
                        )
                    )
                except:
                    pass
            
            await utils.answer(message, self.strings["profile_copied"])
        except UsernameNotOccupiedError:
            await utils.answer(message, self.strings["username_not_found"])
        except UsernameInvalidError:
            await utils.answer(message, self.strings["invalid_username"])
        except Exception as e:
            await utils.answer(message, self.strings["error"].format(str(e)))

    @loader.command(ru_doc="Создать резервную копию вашего профиля", en_doc="Create backup of your profile")
    async def backupme(self, message):
        try:
            user = await self.client.get_me()
            full = await self.client(GetFullUserRequest(user.id))
            user_info = full.users[0]
            
            avatar_url = None
            photos = await self.client.get_profile_photos(user.id)
            if photos:
                photo = await self.client.download_media(photos[0], bytes)
                avatar_url = await self.upload_to_0x0(photo)

            emoji_status_id = None
            if hasattr(user_info, 'emoji_status') and user_info.emoji_status:
                emoji_status_id = user_info.emoji_status.document_id

            backup_data = {
                "first_name": user_info.first_name,
                "last_name": user_info.last_name,
                "about": full.full_user.about,
                "avatar_url": avatar_url,
                "emoji_status_id": emoji_status_id
            }
            
            self.db.set("BackupProfile", "backup_data", backup_data)
            
            await utils.answer(
                message,
                self.strings["backup_saved"].format(avatar_url)
            )

        except Exception as e:
            await utils.answer(message, self.strings["error"].format(str(e)))

    @loader.command(ru_doc="Восстановить профиль из резервной копии", en_doc="Restore profile from backup") 
    async def restoreme(self, message):
        try:
            backup_data = self.db.get("BackupProfile", "backup_data")
            me = await message.client.get_me()
            
            if not backup_data:
                await utils.answer(message, self.strings["no_backup"])
                return

            if backup_data.get("avatar_url"):
                try:
                    photos = await self.client.get_profile_photos('me')
                    await self.client(DeletePhotosRequest(photos))
                    
                    response = requests.get(backup_data["avatar_url"])
                    avatar_bytes = io.BytesIO(response.content)
                    
                    await self.client(UploadProfilePhotoRequest(
                        file=await self.client.upload_file(avatar_bytes)
                    ))
                except:
                    pass

            await self.client(UpdateProfileRequest(
                first_name=backup_data.get("first_name", ""),
                last_name=backup_data.get("last_name", "") or "",
                about=backup_data.get("about", "")
            ))

            if backup_data.get("emoji_status_id") and me.premium:
                try:
                    await self.client(
                        UpdateEmojiStatusRequest(
                            emoji_status=types.EmojiStatus(
                                document_id=backup_data["emoji_status_id"]
                            )
                        )
                    )
                except:
                    pass

            await utils.answer(message, self.strings["profile_restored"])

        except Exception as e:
            await utils.answer(message, self.strings["error"].format(str(e)))
