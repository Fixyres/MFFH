__version__ = (1, 0, 0)

#            © Copyright 2025
#           https://t.me/HikkTutor 
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
#┏┓━┏┓━━┏┓━━┏┓━━┏━━━━┓━━━━━┏┓━━━━━━━━━━━━
#┃┃━┃┃━━┃┃━━┃┃━━┃┏┓┏┓┃━━━━┏┛┗┓━━━━━━━━━━━
#┃┗━┛┃┏┓┃┃┏┓┃┃┏┓┗┛┃┃┗┛┏┓┏┓┗┓┏┛┏━━┓┏━┓━━━━
#┃┏━┓┃┣┫┃┗┛┛┃┗┛┛━━┃┃━━┃┃┃┃━┃┃━┃┏┓┃┃┏┛━━━━
#┃┃━┃┃┃┃┃┏┓┓┃┏┓┓━┏┛┗┓━┃┗┛┃━┃┗┓┃┗┛┃┃┃━━━━━
#┗┛━┗┛┗┛┗┛┗┛┗┛┗┛━┗━━┛━┗━━┛━┗━┛┗━━┛┗┛━━━━━
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# load from: t.me:HikkTutor 
# meta developer:@HikkTutor 
# author: @AmdFx6100, vsakoe
# name: ASCIIArt


from .. import loader, utils
from PIL import Image
import os
import art
import pyfiglet
from telethon.tl.types import Message
from ..inline.types import InlineCall

@loader.tds
class ASCIIArt(loader.Module):
    """Модуль для создания ASCII артов из фото, стикеров и текста"""

    strings = {"name": "ASCIIArt"}

    async def asciicmd(self, message):
        """<реплай на фото или текст> [количество] [" * " для арта из точек] - создать ASCII арт"""
        self.reply = await message.get_reply_message()
        self.message = message
        if not self.reply:
            await message.edit("❌ Используйте команду ответом на фото или текст.")
            return

        args = utils.get_args(message)
        
        if args:
            try:
                width = int(float(args[0]))
                if width < 50:
                    width = 50
                elif width > 1000:
                    width = 1000
                self.width = width if width % 2 == 0 else width - 1
            except ValueError:
                self.width = 100 
        else:
            self.width = 100 
        self.use_dots = '*' in utils.get_args_raw(message) 

        if self.reply.text and self.reply.media:
            self.form = await self.inline.form(
                message=message,
                text="Выберите что конвертировать:",
                reply_markup=[
                    [
                        {
                            "text": "Текст",
                            "callback": self.text_callback
                        },
                        {
                            "text": "Фото",
                            "callback": self.image_callback
                        }
                    ]
                ]
            )
            return
        temp_file = "ascii.txt"
        if self.reply.text:
            await self.process_text(message, self.reply, temp_file)
        elif self.reply.media:
            await self.process_image(message, self.reply, temp_file)
        else:
            await message.edit("❌ Используйте команду ответом на фото или текст")

    async def text_callback(self, call: InlineCall):
        temp_file = "ascii.txt"
        text = self.translit(self.reply.text)
        ascii = pyfiglet.figlet_format(text, font="slant")
        with open(temp_file, "w", encoding="utf-8") as file:
            file.write(ascii)
        await self._client.send_file(self.reply.chat_id, temp_file, reply_to=self.reply.id)
        os.remove(temp_file)
        await call.delete()
        if call.message:
            await call.message.delete()

    async def image_callback(self, call: InlineCall):
        temp_file = "ascii.txt"
        photo = await self._client.download_media(self.reply.media)
        if not photo:
            await call.edit("❌ Не удалось сохранить фото")
            return
        try:
            chars = self.get_char_set()
            ascii = self.image_to_ascii(photo, chars, self.width)
            os.remove(photo)
            with open(temp_file, "w", encoding="utf-8") as file:
                file.write(ascii)
            await self._client.send_file(self.reply.chat_id, temp_file, reply_to=self.reply.id)
            os.remove(temp_file)
            await call.delete()
            if call.message:
                await call.message.delete() 
        except Exception as e:
            await call.edit(f"❌ Ошибка: {e}")

    async def process_text(self, message, reply, temp_file):
        await message.edit("🖌 Создание ASCII арта из текста...")
        text = self.translit(reply.text)
        ascii = pyfiglet.figlet_format(text, font="slant")
        with open(temp_file, "w", encoding="utf-8") as file:
            file.write(ascii)
        await message.client.send_file(reply.chat_id, temp_file, reply_to=reply.id)
        os.remove(temp_file)
        await message.delete()

    async def process_image(self, message, reply, temp_file):
        await message.edit("🖼 Скачивание фото...")
        photo = await message.client.download_media(reply.media)
        if not photo:
            await message.edit("❌ Не удалось сохранить фото")
            return
        await message.edit("🖌 Создание ASCII арта...")
        try:
            chars = self.get_char_set()
            ascii = self.image_to_ascii(photo, chars, self.width)
            os.remove(photo)
            with open(temp_file, "w", encoding="utf-8") as file:
                file.write(ascii)
            await message.client.send_file(reply.chat_id, temp_file, reply_to=reply.id)
            os.remove(temp_file)
            await message.delete()
        except Exception as e:
            await message.edit(f"❌ Ошибка: {e}")

    def get_char_set(self):
        """Возвращает набор символов в зависимости от выбранного стиля."""
        if self.use_dots:
            return "⣿⡿⣾⣽⣻⣹⣸⣷⣶⣧⣇⣆⣄⣃⣂⣁⡀⠿⠾⠽⠻⠹⠸⠷⠶⠧⠇⠆⠄⠃⠂⠁⠛⠙⠚⠋⠉⠒⠐⠈"
        else:
            return "#/\|()1{}[]?-_+~<>i!lI;:,\^`'.@"

    def image_to_ascii(self, image_path, chars, width=100):
        image = Image.open(image_path)
        aspect_ratio = image.height / image.width
        new_height = int(aspect_ratio * width * 0.55)
        image = image.resize((width, new_height))
        image = image.convert("L")
        char_length = len(chars)
        pixels = image.getdata()
        ascii_str = "".join([chars[min(int(pixel * char_length / 256), char_length - 1)] for pixel in pixels])
        ascii_lines = [ascii_str[i:i + width] for i in range(0, len(ascii_str), width)]
        return "\n".join(ascii_lines)

    def translit(self, text):
        ru_en = {
            'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
            'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
            'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
            'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
            'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
            'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'E',
            'Ж': 'Zh', 'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M',
            'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U',
            'Ф': 'F', 'Х': 'H', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Sch',
            'Ъ': '', 'Ы': 'Y', 'Ь': '', 'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya'
        }
        for ru, en in ru_en.items():
            text = text.replace(ru, en)
        return text