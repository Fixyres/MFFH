# meta developer: @kotcheat

import io
import aiohttp
from .. import loader, utils
from telethon import types


@loader.tds
class KOTimgbbMod(loader.Module):
    """Загружает изображения на imgbb.com ( by @kotcheat )"""
    strings = {
        "name": "KOTimgbb",
        "api_key_needed": (
            "🚫 <b>API ключ ImgBB не установлен!</b>\n"
            "1. Получите ключ на <a href='https://api.imgbb.com/'>api.imgbb.com</a>.\n"
            "2. Установите его командой:\n<code>{prefix}apikey ВАШ_КЛЮЧ</code>"
        ),
        "reply_needed": "❓ <b>Ответьте на сообщение с фото или документом-изображением.</b>",
        "processing": "⏳ <i>Загрузка изображения на imgbb.com...</i>",
        "downloading": "⏳ <i>Скачивание изображения...</i>",
        "upload_error": "❌ <b>Ошибка загрузки:</b>\n<code>{}</code>",
        "download_error": "❌ <b>Ошибка скачивания:</b>\n<code>{}</code>",
        "success": (
            "✅ <b>Изображение загружено:</b>\n"
            "🔗 Прямая ссылка: <code>{url}</code>\n"
            "🖼️ Страница просмотра: <code>{display_url}</code>"
        ),
        "invalid_response": "⚠️ <b>Некорректный ответ от API ImgBB.</b>\n<code>{}</code>",
        "api_key_set": "✅ <b>API ключ ImgBB успешно сохранен!</b>",
        "api_key_args": "🚫 <b>Не указан API ключ.</b> Используйте: <code>{prefix}apikey ВАШ_КЛЮЧ</code>",
    }

    @loader.owner
    @loader.command(alias="setibbkey")
    async def apikey(self, message: types.Message):
        """<ключ> - Установить API ключ для imgbb.com"""
        key = utils.get_args_raw(message)
        prefix = self.get_prefix()

        if not key:
            await utils.answer(message, self.strings("api_key_args").format(prefix=prefix))
            return

        self.db.set(__name__, "api_key", key)
        await utils.answer(message, self.strings("api_key_set"))

    @loader.command(alias="ibb")
    async def imgbb(self, message: types.Message):
        """[ответ на изображение] - Загрузить изображение на imgbb.com"""

        api_key = self.db.get(__name__, "api_key", None)

        if not api_key:
            prefix = self.get_prefix()
            await utils.answer(message, self.strings("api_key_needed").format(prefix=prefix))
            return

        reply = await message.get_reply_message()
        if not reply or not reply.media:
            await utils.answer(message, self.strings("reply_needed"))
            return

        media = reply.media
        is_photo = isinstance(media, types.MessageMediaPhoto)

        is_image_document = (
            isinstance(media, types.MessageMediaDocument)
            and hasattr(media, 'document')
            and hasattr(media.document, 'mime_type')
            and getattr(media.document, "mime_type", "").startswith("image/")
        )

        if not (is_photo or is_image_document):
             await utils.answer(message, self.strings("reply_needed"))
             return


        status_msg = await utils.answer(message, self.strings("downloading"))
        message_to_edit = status_msg if isinstance(status_msg, types.Message) else message

        image_bytes = io.BytesIO()
        try:
            await message.client.download_media(reply, file=image_bytes)
            image_bytes.seek(0)
            if image_bytes.getbuffer().nbytes == 0:
                raise ValueError("Downloaded file is empty.")
        except Exception as e:
            await utils.answer(message_to_edit, self.strings("download_error").format(utils.escape_html(str(e))))
            if not image_bytes.closed:
                image_bytes.close()
            return

        await utils.answer(message_to_edit, self.strings("processing"))

        data = aiohttp.FormData()
        data.add_field('key', api_key)

        filename = "image.png"
        mime_type = None
        if is_image_document:
            mime_type = getattr(reply.document, "mime_type", None)


        if mime_type:
             ext = mime_type.split('/')[-1]

             if ext in ["png", "jpg", "jpeg", "gif", "bmp", "tiff", "webp"]:
                 filename = f"image.{ext}"
             elif ext == "heic" or ext == "heif":
                 filename = f"image.{ext}"


        data.add_field('image', image_bytes, filename=filename)

        upload_url = "https://api.imgbb.com/1/upload"
        response_text = "No response"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(upload_url, data=data) as response:
                    response_text = await response.text()
                    response.raise_for_status()

                    result = await response.json(content_type=None)

                    if isinstance(result, dict) and result.get("success") and result.get("data"):
                        res_data = result["data"]
                        image_url = res_data.get("url")
                        display_url = res_data.get("display_url")
                        if image_url and display_url:
                            await utils.answer(message_to_edit, self.strings("success").format(
                                url=utils.escape_html(image_url),
                                display_url=utils.escape_html(display_url)
                            ))
                        else:
                             raise ValueError("Missing 'url' or 'display_url' in successful API response.")
                    else:
                        error_message = result.get("error", {}).get("message", "Unknown API error") if isinstance(result, dict) else "Invalid response structure"
                        await utils.answer(message_to_edit, self.strings("invalid_response").format(utils.escape_html(error_message)))

        except aiohttp.ClientResponseError as e:
            await utils.answer(message_to_edit, self.strings("upload_error").format(f"HTTP {e.status} {e.message}: {utils.escape_html(response_text[:500])}"))
        except aiohttp.ClientError as e:
            await utils.answer(message_to_edit, self.strings("upload_error").format(f"Network Error: {utils.escape_html(str(e))}"))
        except ValueError as e:
             await utils.answer(message_to_edit, self.strings("invalid_response").format(f"{utils.escape_html(str(e))} Response: {utils.escape_html(response_text[:500])}"))
        except Exception as e:
            await utils.answer(message_to_edit, self.strings("upload_error").format(f"Unexpected Error: {utils.escape_html(str(e))}"))
        finally:
            if not image_bytes.closed:
                 image_bytes.close()