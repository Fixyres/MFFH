__version__ = (1, 1, 0)
# meta developer: @psyhomodules

from hikkatl.types import Message
from .. import loader, utils

@loader.tds
class AdvancedTextModule(loader.Module):
    strings = {"name": "AdvancedText"}

    def __init__(self):
        self.enabled_bold = False
        self.enabled_italic = False
        self.enabled_mono = False
        self.enabled_underline = False
        self.enabled_strikethrough = False
        self.enabled_center = False

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    async def edit_text(self, message: Message):
        text = message.text
        if not text:
            return

        if self.enabled_bold:
            text = f"<b>{text}</b>"
        if self.enabled_italic:
            text = f"<i>{text}</i>"
        if self.enabled_mono:
            text = f"<code>{text}</code>"
        if self.enabled_underline:
            text = f"<u>{text}</u>"
        if self.enabled_strikethrough:
            text = f"<s>{text}</s>"
        if self.enabled_center:
            text = f"<center>{text}</center>"

        await message.edit(text, parse_mode="HTML")

    def disable_all_styles(self):
        self.enabled_bold = False
        self.enabled_italic = False
        self.enabled_mono = False
        self.enabled_underline = False
        self.enabled_strikethrough = False
        self.enabled_center = False

    @loader.command()
    async def bold(self, message: Message):
        """Активирует жирный текст."""
        self.disable_all_styles()
        self.enabled_bold = not self.enabled_bold
        status = "включен" if self.enabled_bold else "выключен"
        await utils.answer(message, f"🪐 <b>Жирный текст</b> {status} ʕ·ᴥ·ʔ", parse_mode="HTML")

    @loader.command()
    async def italic(self, message: Message):
        """Активирует курсив."""
        self.disable_all_styles()
        self.enabled_italic = not self.enabled_italic
        status = "включен" if self.enabled_italic else "выключен"
        await utils.answer(message, f"🪐 <i>Курсив</i> {status} ʕ·ᴥ·ʔ", parse_mode="HTML")

    @loader.command()
    async def mono(self, message: Message):
        """Активирует моноширинный текст."""
        self.disable_all_styles()
        self.enabled_mono = not self.enabled_mono
        status = "включен" if self.enabled_mono else "выключен"
        await utils.answer(message, f"🪐 <code>Моноширинный текст</code> {status} ʕ·ᴥ·ʔ", parse_mode="HTML")

    @loader.command()
    async def underline(self, message: Message):
        """Активирует подчеркивание."""
        self.disable_all_styles()
        self.enabled_underline = not self.enabled_underline
        status = "включен" if self.enabled_underline else "выключен"
        await utils.answer(message, f"🪐 <u>Подчеркивание</u> {status} ʕ·ᴥ·ʔ", parse_mode="HTML")

    @loader.command()
    async def strikethrough(self, message: Message):
        """Активирует зачеркивание."""
        self.disable_all_styles()
        self.enabled_strikethrough = not self.enabled_strikethrough
        status = "включен" if self.enabled_strikethrough else "выключен"
        await utils.answer(message, f"🪐 <s>Зачеркивание</s> {status} ʕ·ᴥ·ʔ", parse_mode="HTML")

    @loader.command()
    async def off(self, message: Message):
        """Отключает все стили."""
        self.disable_all_styles()
        await utils.answer(message, "🪐 Все стили выключены ʕ·ᴥ·ʔ", parse_mode="HTML")

    @loader.command()
    async def on(self, message: Message):
        """Включает стиль по умолчанию (жирный текст)."""
        self.disable_all_styles()
        self.enabled_bold = True
        await utils.answer(message, "🪐 Стиль по умолчанию (жирный текст) включен ʕ·ᴥ·ʔ", parse_mode="HTML")

    @loader.watcher(out=True)
    async def watcher(self, message: Message):
        """Сразу редактируем сообщение в зависимости от активных опций."""
        if any([self.enabled_bold, self.enabled_italic, self.enabled_mono, self.enabled_underline, self.enabled_strikethrough, self.enabled_center]):
            await self.edit_text(message)
