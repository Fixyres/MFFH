#         ______     ___  ___          _       _      
#    ____ | ___ \    |  \/  |         | |     | |     
#   / __ \| |_/ /   _| .  . | ___   __| |_   _| | ___ 
#  / / _` |  __/ | | | |\/| |/ _ \ / _` | | | | |/ _ \
# | | (_| | |  | |_| | |  | | (_) | (_| | |_| | |  __/
#  \ \__,_\_|   \__, \_|  |_/\___/ \__,_|\__,_|_|\___|
#   \____/       __/ |                                
#               |___/                                  

# На модуль распространяется лицензия "GNU General Public License v3.0"
# https://github.com/all-licenses/GNU-General-Public-License-v3.0

# meta developer: @pymodule
# requires: opencv-python

import os, shutil, cv2
from PIL import Image, UnidentifiedImageError
from telethon.tl.functions.stickers import CreateStickerSetRequest
from telethon.tl.types import InputStickerSetItem, InputDocument
from telethon.errors.rpcerrorlist import PackShortNameOccupiedError
from .. import loader
from telethon.tl.functions.photos import GetUserPhotosRequest

import asyncio
import random
import string

try:
    resample = Image.Resampling.LANCZOS
except:
    resample = Image.LANCZOS

@loader.tds
class CreateAvatarsPack(loader.Module):
    """Creates a sticker pack from photos and video avatars of participants"""
    strings = {
        "name": "CreateAvatarsPack",
        "processing": "📥 I'm collecting avatars of participants...",
        "no_avatars": "❌ No members with avatars",
        "no_valid": "❌ Could not process any avatars",
        "done": "✅ The sticker pack is ready:\n👉 <a href='https://t.me/addstickers/{}'>Open</a>",
        "already": "⚠️ A sticker pack with this name already exists.",
    }

    strings_ru = {
        "processing": "📥 Собираю аватарки участников...",
        "no_avatars": "❌ Нет участников с аватарками",
        "no_valid": "❌ Не удалось обработать ни одну аватарку",
        "done": "✅ Стикерпак готов:\n👉 <a href='https://t.me/addstickers/{}'>Открыть</a>",
        "already": "⚠️ Стикерпак с таким именем уже существует",
    }

    @loader.command(doc="- Create a sticker pack from the avatars of users in the group", ru_doc="- Создать стикерпак из аватаров пользователей группы", only_groups=True)
    async def createavatars(self, message):
        """- Create a sticker pack from the avatars of users in the group"""
        chat = await message.get_chat()
        cid = abs(message.chat_id)
        await message.edit(self.strings["processing"])

        users = []
        async for u in self._client.iter_participants(chat.id):
            if u.photo:
                users.append(u)
                if len(users) >= 100:
                    break

        if not users:
            return await message.edit(self.strings["no_avatars"])

        tmp_dir = f"/tmp/avatars_{cid}"
        os.makedirs(tmp_dir, exist_ok=True)
        sticker_files = []

        for u in users:
            try:
                photos = await self._client(GetUserPhotosRequest(u.id, 0, 0, 1))
                if not photos.photos:
                    continue

                raw = await self._client.download_media(photos.photos[0])
                data = raw if isinstance(raw, (bytes, bytearray)) else open(raw, "rb").read()

                path_raw = os.path.join(tmp_dir, f"{u.id}_raw")
                with open(path_raw, "wb") as f:
                    f.write(data)

                if b"ftyp" in data[:32] or path_raw.endswith((".mp4", ".webm", ".mov")):
                    cap = cv2.VideoCapture(path_raw)
                    success, frame = cap.read()
                    cap.release()
                    if not success:
                        continue
                    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA))
                else:
                    try:
                        img = Image.open(path_raw).convert("RGBA")
                    except UnidentifiedImageError:
                        continue

                img.thumbnail((512, 512), resample)
                w, h = img.size
                final = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
                final.paste(img, ((512 - w)//2, (512 - h)//2))

                out = os.path.join(tmp_dir, f"{u.id}.webp")
                final.save(out, "WEBP")
                sticker_files.append(out)

            except:
                continue

        if not sticker_files:
            shutil.rmtree(tmp_dir, ignore_errors=True)
            return await message.edit(self.strings["no_valid"])

        tag = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
        short = f"f{cid}_{tag}_by_fcreateavatars"
        title = f"AvaPack {tag}"

        stickers = []
        for p in sticker_files:
            await asyncio.sleep(0.3)
            file = await self._client.upload_file(p)
            msg = await self._client.send_file("me", file, force_document=True)
            doc = msg.document
            await self._client.delete_messages("me", msg.id)
            stickers.append(InputStickerSetItem(
                document=InputDocument(doc.id, doc.access_hash, doc.file_reference),
                emoji="🖼️"
            ))

        try:
            await self._client(CreateStickerSetRequest(
                user_id="me",
                title=title,
                short_name=short,
                stickers=stickers
            ))
        except PackShortNameOccupiedError:
            shutil.rmtree(tmp_dir, ignore_errors=True)
            return await message.edit(self.strings["already"])
        except Exception as e:
            shutil.rmtree(tmp_dir, ignore_errors=True)
            return await message.edit(f"❌ Error: {e}")

        shutil.rmtree(tmp_dir, ignore_errors=True)
        await message.edit(self.strings["done"].format(short))
