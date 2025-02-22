# meta developer: @angellmodules
from .. import loader, utils
from PIL import Image
import io
import os

@loader.tds
class ASCIIArtMod(loader.Module):
    """Конвертация изображений в ASCII-арт"""
    strings = {"name": "ASCIIArt"}

    async def asciicmd(self, message):
        """<реплай на изображение>"""
        reply = await message.get_reply_message()
        if not reply or not (reply.photo or (reply.document and reply.file.mime_type.startswith("image/"))):
            await message.edit("<b>Пожалуйста, ответьте на изображение!</b>")
            return

        
        try:
            photo = await reply.download_media()
        except Exception as e:
            await message.edit(f"<b>Не удалось скачать изображение:</b> {e}")
            return

        await message.edit("<b>Конвертирую изображение в ASCII...</b>")

        try:
         
            ascii_art = self._convert_to_ascii(photo)

            
            file_path = "/tmp/ascii_art.txt"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(ascii_art)

           
            await message.client.send_file(
                message.chat_id,
                file_path,
                caption="",  
                force_document=True
            )

          
            os.remove(file_path)
            await message.delete()

        except Exception as e:
            await message.edit(f"<b>Ошибка при обработке:</b> {e}")

    def _convert_to_ascii(self, image_path):
        """Конвертация изображения в ASCII-арт"""
        chars = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]
        new_width = 100

       
        with Image.open(image_path) as img:
        
            img = img.convert("L")

            
            aspect_ratio = img.height / img.width
            new_height = int(aspect_ratio * new_width * 0.55)
            img = img.resize((new_width, new_height))

      
            pixels = img.getdata()
            ascii_str = "".join([chars[pixel // 25] for pixel in pixels])
            ascii_lines = [ascii_str[i:i + new_width] for i in range(0, len(ascii_str), new_width)]

            return "\n".join(ascii_lines)






#made by @sawwnapix
