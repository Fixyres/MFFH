__version__ = (1, 0, 0)

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
# meta banner: https://x0.at/GgLO.png

import requests
from .. import loader, utils
from telethon import events

@loader.tds
class AutomaticTranslator(loader.Module):
    """Модуль для автоматического перевода сообщений на язык. Создан ради забавы."""
    strings = {"name": "AutomaticTranslator"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "target_language",
                "",
                lambda: "Язык, на который будет производиться перевод (например, 'English').",
                validator=loader.validators.String()
            ),
            loader.ConfigValue(
                "enabled",
                True,
                lambda: "Включить или выключить автоматический перевод.",
                validator=loader.validators.Boolean()
            )
        )
        self.ignore_commands = ['off', 'on', 'cfg']

    async def translate_text(self, text, target_language):
        api_key = 'Bearer sk-l4HU4KwZt6bF8gOwwKCOMpfpIKvR9YhDHvTFIGJ6tJ5rPKXE'
        data = {
            "model": "deepseek-v3",
            "messages": [
                {"role": "user", "content": f"Please translate the following text to {target_language}, no extra text, just translation: {text}"}
            ]
        }

        response = requests.post("https://cablyai.com/v1/chat/completions", headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        }, json=data)

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return None

    @loader.command()
    async def oncmd(self, event):
        """Включить автоматический перевод."""
        self.config["enabled"] = True
        await event.edit("✅ Автоматический перевод включен.")

    @loader.command()
    async def offcmd(self, event):
        """Выключить автоматический перевод."""
        self.config["enabled"] = False
        await event.edit("❌ Автоматический перевод выключен.")

    @loader.watcher(out=True)
    async def message_watcher(self, message):
        if not self.config["enabled"]:
            return

        if message.raw_text.startswith(tuple(self.ignore_commands)):
            return

        target_language = self.config["target_language"]
        if not target_language:
            return

        translated_text = await self.translate_text(message.raw_text, target_language)

        if translated_text:
            await message.edit(translated_text)
        else:
            await message.edit("❌ Ошибка при переводе сообщения.")
# артемко лох
