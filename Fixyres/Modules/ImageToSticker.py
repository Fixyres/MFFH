from .. import loader, utils
from telethon import types
from PIL import Image
import io

@loader.tds
class ImageToStickerMod(loader.Module):
    """🖼️ Модуль для преобразования изображений в стикеры."""

    strings = {"name": "ImageToSticker"}

    @loader.command()
    async def sticker(self, message):
        """Преобразовать изображение в стикер. Ответьте на изображение и введите .sticker"""
        if not message.is_reply:
            await utils.answer(message, "❗ Пожалуйста, ответьте на сообщение с изображением.")
            return
        reply = await message.get_reply_message()
        if not reply.photo:
            await utils.answer(message, "❗ В ответе должно быть изображение.")
            return
        photo = reply.photo
        file = await self.client.download_media(photo)
        image = Image.open(file)
        with io.BytesIO() as output:
            image.save(output, format="WEBP")
            sticker_data = output.getvalue()
        sticker_file = io.BytesIO(sticker_data)
        sticker_file.name = "sticker.webp"
        await self.client.send_file(
            message.chat_id,
            file=sticker_file,
            force_document=False,
            reply_to=message.id,
        )
        await utils.answer(message, "✅ Стикер создан! 🎉")