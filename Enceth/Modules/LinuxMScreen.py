# meta developer: @Enceth
import io
from PIL import Image, ImageDraw, ImageFilter

from .. import loader, utils


class ShadowEffectMod(loader.Module):
    """Спизженная хуйня у @mqone но она лучше"""
    strings = {"name": "LinuxMscreen"}

    async def lcmd(self, message):
        """вирусы (ответом на фото)"""
        reply = await message.get_reply_message()
        if not reply or not reply.media:
            await message.edit("<b>Ответьте на изображение!</b>")
            return

        image_bytes = io.BytesIO()
        await reply.download_media(image_bytes)
        image_bytes.seek(0)

        try:
            img = Image.open(image_bytes).convert("RGBA")
        except Exception:
            await message.edit("<b>Не удалось обработать изображение!</b>")
            return

        await message.edit("<b>Обработка...</b>")

        # Параметры
        blur_radius = 10  # Размытие для теней
        border_size = 30  # Отступ для тени
        shadow_color = (0, 0, 0, 150)  # Цвет тени с прозрачностью
        white_color = (255, 255, 255, 255)  # Белый цвет для фона

        shadow = Image.new("RGBA", (img.width + border_size * 2, img.height + border_size * 2), (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow)

        shadow_draw.rectangle(
            [border_size, border_size, shadow.width - border_size, shadow.height - border_size],
            fill=shadow_color
        )
        shadow = shadow.filter(ImageFilter.GaussianBlur(blur_radius))

        white_background = Image.new("RGBA", img.size, white_color)
        
        mask = Image.new("L", img.size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle(
            [(0, 0), (img.width, img.height)], radius=20, fill=255  
        )
        
        img.putalpha(mask)
        white_background.putalpha(mask)

        shadow.paste(white_background, (border_size, border_size), white_background)
        shadow.paste(img, (border_size, border_size), img)

        output = io.BytesIO()
        output.name = "shadow_effect_with_subtle_rounded_corners.png"
        shadow.save(output, "PNG")
        output.seek(0)

        await message.client.send_file(message.chat_id, output, caption="")
        await message.delete()
