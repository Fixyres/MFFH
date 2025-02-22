#meta developer: @thisLyomi & @AmekaMods

import os
import requests
from .. import loader

@loader.tds
class AmeChangeLoaderText(loader.Module):
    """Модуль для изменения текста загрузки хикки. Используйте осторожно!\nАккуратнее при использовании на Lavhost и подобных. Использовать крайне не рекомендуется. \nЕсли у вас форк, то, вероятно, все будет работать, но выдаст не критическую ошибку."""

    strings = {"name": "AmeChangeLoaderText"}

    async def chloadertextcmd(self, message):
        """{url} {text} - Задать текст загрузчика. Ссылка обязательна. Для пропуска строки используйте HTML."""
        args = message.raw_text.split(" ", 2)

        if len(args) < 3:
            await message.edit("<b>Используйте:</b> <code>.chloadertext {url} {text}</code>\n<b>Ссылка обязательна</b>")
            return

        url = args[1]
        text = args[2]

        if not url.startswith("https://"):
            await message.edit("<b>❌ Укажите ссылку, начинающуюся с 'https://'</b>")
            return

        try:
            main_file_path = os.path.join("hikka", "main.py")

            with open(main_file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()

            lines[784] = f'                "{url}",\n'
            lines[786] = f'                    "{text}"\n'

            with open(main_file_path, "w", encoding="utf-8") as file:
                file.writelines(lines)

            await message.edit("✅ <b>Успешно, перезагрузите бота.</b>")

        except Exception as e:
            await message.edit(f"❌ <b>Ошибка:</b><code> {e}</code>")

    async def updatefilecmd(self, message):
        """- Обязательно перед использованием используйте это."""
        try:
            main_file_path = os.path.join("hikka", "main.py")

            response = requests.get("https://github.com/amm1edev/EditAutoTxt/raw/main/main.py")

            if response.status_code != 200:
                await message.edit(f"❌ <b>Ошибка загрузки файла:</b> {response.status_code}")
                return

            with open(main_file_path, "w", encoding="utf-8") as file:
                file.write(response.text)

            await message.edit("✅ <b>Файл успешно обновлён, напишите </b><code>.restart -f</code>")

        except Exception as e:
            await message.edit(f"❌ <b>Ошибка:</b><code> {e}</code>")
