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

from .. import loader, utils
import requests
import uuid
import os

@loader.tds
class QRGenMod(loader.Module):
    """Generate QR codes from text or links"""

    strings = {
        "name": "QRGen",
        "generating": "📡 Generating QR for:\n<code>{text}</code>",
        "no_text": "❗ Please provide text or a link to encode",
        "api_error": "🚫 Error while contacting QR API",
        "not_image": "⚠️ API did not return an image",
        "ok": "✅ QR code successfully generated",
        "error_with_details": "🚫 Error:\n<code>{error}</code>"
    }

    strings_ru = {
        "name": "QRGen",
        "generating": "📡 Генерация QR для:\n<code>{text}</code>",
        "no_text": "❗ Укажи текст или ссылку для кодирования",
        "api_error": "🚫 Ошибка при запросе к QR API",
        "not_image": "⚠️ API не вернул изображение",
        "ok": "✅ QR-код успешно сгенерирован",
        "error_with_details": "🚫 Ошибка:\n<code>{error}</code>"
    }

    @loader.command(doc="Generate a QR code from text or link", ru_doc="Сгенерировать QR-код из текста или ссылки")
    async def qr(self, message):
        """<text or URL> — generate QR code"""
        text = utils.get_args_raw(message)
        if not text:
            return await utils.answer(message, self.strings("no_text"))

        await utils.answer(message, self.strings("generating").format(text=text))

        try:
            params = {
                "data": text,
                "size": "512x512",
                "ecc": "M",
                "format": "png",
                "margin": 10
            }

            response = requests.get("https://api.qrserver.com/v1/create-qr-code/", params=params, stream=True, timeout=15)
            if response.status_code != 200:
                return await utils.answer(message, self.strings("api_error"))

            if not response.headers.get("Content-Type", "").startswith("image/"):
                return await utils.answer(message, self.strings("not_image"))

            temp_file = f"/tmp/qr_{uuid.uuid4()}.png"
            with open(temp_file, "wb") as f:
                for chunk in response.iter_content(8192):
                    f.write(chunk)

            await message.client.send_file(
                message.chat_id,
                temp_file,
                caption=self.strings("ok"),
                reply_to=message.id
            )
            os.remove(temp_file)

            await message.delete()

        except Exception as e:
            await utils.answer(message, self.strings("error_with_details").format(error=e))