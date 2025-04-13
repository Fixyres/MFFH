# meta developer: @Goduser18
from .. import loader, utils
import qrcode
from io import BytesIO
from PIL import Image
from telethon.tl.functions.channels import JoinChannelRequest

@loader.tds
class QRCodeMod(loader.Module):
    """Создать QR-code"""
    
    strings = {"name": "QRCode"}

    async def client_ready(self, client, db):
        """Авто"""
        self.client = client
        try:
            await client(JoinChannelRequest("goduser18"))
        except Exception:
            pass
    async def qrcmd(self, message):
        """Создать QR-код. Используй: .qr <текст/ссылка>"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "❌ Укажи текст или ссылку.\nПример: <code>.qr @goduser18</code>")
            return

        await utils.answer(message, "🔄 Генерирую QR-код...")

        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(args)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)

            await message.client.send_file(
                message.chat_id,
                buffer,
                caption=f"📲 QR-код для: <code>{args}</code>",
                reply_to=message.id,
                silent=True,
            )
            await message.delete()

        except Exception as e:
            await utils.answer(message, f"❌ Ошибка: {e}")
            # сори за  авто подписку 