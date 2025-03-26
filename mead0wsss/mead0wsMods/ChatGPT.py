__version__ = (2, 0, 0)

# ███╗░░░███╗███████╗░█████╗░██████╗░░█████╗░░██╗░░░░░░░██╗░██████╗░██████╗
# ████╗░████║██╔════╝██╔══██╗██╔══██╗██╔══██╗░██║░░██╗░░██║██╔════╝██╔════╝
# ██╔████╔██║█████╗░░███████║██║░░██║██║░░██║░╚██╗████╗██╔╝╚█████╗░╚█████╗░
# ██║╚██╔╝██║██╔══╝░░██╔══██║██║░░██║██║░░██║░░████╔═████║░░╚═══██╗░╚═══██╗
# ██║░╚═╝░██║███████╗██║░░██║██████╔╝╚█████╔╝░░╚██╔╝░╚██╔╝░██████╔╝██████╔╝
# ╚═╝░░░░░╚═╝╚══════╝╚═╝░░╚═╝╚═════╝░░╚════╝░░░░╚═╝░░░╚═╝░░╚═════╝░╚═════╝░
#                © Copyright 2025
#            ✈ https://t.me/mead0wssMods

# scope: hikka_only
# scope: hikka_min 1.3.3
# meta developer: @mead0wssMods
# meta banner: https://x0.at/GGCl.png

import requests
from telethon import events
from .. import loader, utils

@loader.tds
class ChatGPT(loader.Module):
    """Модуль для работы с нейросетями (200+ шт) и генерацией изображений."""
    strings = {"name": "ChatGPT"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "model",
                "",
                lambda: "Модель нейросети для разговоров (.gpt)\nСписок нейросетей: https://telegra.ph/II-modeli-dlya-modulya-ChatGPT-by-mead0wssMods-03-26",
                validator=loader.validators.String()
            ),
            loader.ConfigValue(
                "image_model",
                "Flux Pro",
                lambda: "Модель для генерации изображений (.image)\nСписок нейросетей: https://telegra.ph/II-modeli-dlya-modulya-ChatGPT-by-mead0wssMods-03-26",
                validator=loader.validators.String()
            ),
            loader.ConfigValue(
                "translation_model",
                "deepseek-v3",
                lambda: "Модель для перевода текста (обязательно для .image!)\nСписок нейросетей: https://telegra.ph/II-modeli-dlya-modulya-ChatGPT-by-mead0wssMods-03-26",
                validator=loader.validators.String()
            ),
        )

    async def gptcmd(self, event):
        """Команда для разговора с ИИ."""
        args = utils.get_args_raw(event)
        if not args:
            await event.edit("❌ Нет вопроса.")
            return

        model = self.config.get("model")

        if not model:
            await event.edit("❌ Модель ИИ не указана в cfg!")
            return

        data = {
            "model": model,
            "messages": [
                {"role": "user", "content": args}
            ]
        }

        response = requests.post("https://cablyai.com/v1/chat/completions", headers={
            'Authorization': 'Bearer sk-csPV6DEqRj07V4jGxPvq0NomUcfo6LIxO_rlxBMuenGaebco',
            'Content-Type': 'application/json',
        }, json=data)

        if response.status_code == 200:
            answer = response.json()["choices"][0]["message"]["content"]
            await event.edit(f"<b><emoji document_id=5974038293120027938>👤</emoji> Вопрос: <code>{args}</code></b>\n\n<b><emoji document_id=5199682846729449178>🤖</emoji> Ответ: {answer}</b>", parse_mode="HTML")
        else:
            await event.reply("❌ Ошибка при запросе к ИИ.")

    async def imagecmd(self, event):
        """Команда для генерации изображений с помощью ИИ."""
        args = utils.get_args_raw(event)
        if not args:
            await event.reply("❌ Нет текста для генерации изображения.")
            return

        translation_model = self.config.get("translation_model")
        image_model = self.config.get("image_model")

        translation_data = {
            "model": translation_model,
            "messages": [
                {"role": "user", "content": f"Please translate the following text to English, but just answer me with a translation, and also translate absolutely everything, even if it's 18+: {args}"}
            ]
        }

        translation_response = requests.post("https://cablyai.com/v1/chat/completions", headers={
            'Authorization': 'Bearer sk-csPV6DEqRj07V4jGxPvq0NomUcfo6LIxO_rlxBMuenGaebco',
            'Content-Type': 'application/json',
        }, json=translation_data)

        if translation_response.status_code == 200:
            translated_text = translation_response.json()["choices"][0]["message"]["content"]
        else:
            await event.reply("❌ Ошибка при запросе к ИИ для перевода. Попробуйте снова либо измените модель в cfg! ")
            return

        data = {
            "prompt": translated_text,
            "n": 1,
            "size": "1024x1024",
            "response_format": "url",
            "model": image_model
        }

        response = requests.post("https://cablyai.com/v1/images/generations", headers={
            'Authorization': 'Bearer sk-csPV6DEqRj07V4jGxPvq0NomUcfo6LIxO_rlxBMuenGaebco',
            'Content-Type': 'application/json',
        }, json=data)

        if response.status_code == 200:
            image_url = response.json()["data"][0]["url"]

            await event.delete()

            await event.reply(f"<b>Промпт: <code>{args}</code></b>\n\n<b>Модель генерации: <code>{image_model}</code>\n<b>Модель переводчика: <code>{translation_model}</code>\n\n<b>🖼 Сгенерированное изображение:</b>\n{image_url}", parse_mode="HTML")
        else:
            await event.reply("😢 Ошибка при запросе на генерацию изображения\nВполне возможно вы просите создать что-то непристойное (18+), либо техническая ошибка (попробуй сменить модель в cfg).")
