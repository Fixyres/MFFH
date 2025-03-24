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
# meta banner: https://x0.at/yCcx.jpg

from telethon import events
from .. import loader, utils

@loader.tds
class AutoFormatting(loader.Module):
    """Модуль для автоматического форматирования вашего текста в чате."""
    strings = {"name": "AutoFormatting"}

    def __init__(self):
        self.styles = {
            "bold": False,
            "italic": False,
            "mono": False,
            "underline": False,
            "strikethrough": False,
            "center": False
        }

    async def format_message(self, message):
        content = message.text
        if not content:
            return

        for style, enabled in self.styles.items():
            if enabled:
                tags = {
                    "bold": "b",
                    "italic": "i",
                    "mono": "code",
                    "underline": "u",
                    "strikethrough": "s",
                    "center": "center"
                }
                content = f"<{tags[style]}>{content}</{tags[style]}>"

        await message.edit(content, parse_mode="HTML")

    def reset_styles(self):
        for style in self.styles:
            self.styles[style] = False

    @loader.command()
    async def bold(self, message):
        """Включает или отключает жирный текст."""
        self.styles["bold"] = not self.styles["bold"]
        status = "включен" if self.styles["bold"] else "выключен"
        await utils.answer(message, f"🪐 <b>Жирный текст</b> {status} ʕ·ᴥ·ʔ", parse_mode="HTML")

    @loader.command()
    async def italic(self, message):
        """Включает или отключает курсив."""
        self.styles["italic"] = not self.styles["italic"]
        status = "включен" if self.styles["italic"] else "выключен"
        await utils.answer(message, f"🪐 <i>Курсив</i> {status} ʕ·ᴥ·ʔ", parse_mode="HTML")

    @loader.command()
    async def mono(self, message):
        """Включает или отключает моноширинный текст."""
        self.styles["mono"] = not self.styles["mono"]
        status = "включен" if self.styles["mono"] else "выключен"
        await utils.answer(message, f"🪐 <code>Моноширинный текст</code> {status} ʕ·ᴥ·ʔ", parse_mode="HTML")

    @loader.command()
    async def underline(self, message):
        """Включает или отключает подчеркивание."""
        self.styles["underline"] = not self.styles["underline"]
        status = "включен" if self.styles["underline"] else "выключен"
        await utils.answer(message, f"🪐 <u>Подчеркивание</u> {status} ʕ·ᴥ·ʔ", parse_mode="HTML")

    @loader.command()
    async def strikethrough(self, message):
        """Включает или отключает зачеркивание."""
        self.styles["strikethrough"] = not self.styles["strikethrough"]
        status = "включен" if self.styles["strikethrough"] else "выключен"
        await utils.answer(message, f"🪐 <s>Зачеркивание</s> {status} ʕ·ᴥ·ʔ", parse_mode="HTML")

    @loader.command()
    async def off(self, message):
        """Отключает все стили."""
        self.reset_styles()
        await utils.answer(message, "🪐 Все стили выключены ʕ·ᴥ·ʔ", parse_mode="HTML")

    @loader.command()
    async def on(self, message):
        """Включает стиль по умолчанию (жирный текст)."""
        self.reset_styles()
        self.styles["bold"] = True
        await utils.answer(message, "🪐 Стиль по умолчанию (жирный текст) включен ʕ·ᴥ·ʔ", parse_mode="HTML")

    @loader.watcher(out=True)
    async def message_watcher(self, message):
        commands = ["bold", "italic", "mono", "underline", "strikethrough", "off", "on"]
        if message.text.split()[0] in commands:
            return

        if any(self.styles.values()):
            await self.format_message(message)
