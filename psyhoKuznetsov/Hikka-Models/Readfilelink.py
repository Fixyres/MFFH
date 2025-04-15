__version__ = (1, 0, 0)
# meta developer: @psyhomodules

import os
import aiohttp
import time
from datetime import datetime
from telethon.tl.types import Message
from .. import loader, utils
from urllib.parse import urlparse

@loader.tds
class ReadFilelinkMod(loader.Module):
    """Модуль для чтения содержимого файлов из реплая или по URL."""

    strings = {
        "name": "ReadFilelink",
        "no_reply": "❌ Ответь на файл для команды .rf.",
        "no_url": "❌ Укажи ссылку для команды .rl, например: .rl https://example.com/file.py",
        "read_error": "❌ Ошибка при чтении файла: {error}",
        "download_error": "❌ Ошибка при загрузке файла по ссылке: {error}",
        "loading": "⏳ Загружаю и обрабатываю данные...",
        "no_content": "❌ Файл пустой или не удалось извлечь содержимое."
    }

    strings_ru = {
        "no_reply": "❌ Ответь на файл для команды .rf.",
        "no_url": "❌ Укажи ссылку для команды .rl, например: .rl https://example.com/file.py",
        "read_error": "❌ Ошибка при чтении файла: {error}",
        "download_error": "❌ Ошибка при загрузке файла по ссылке: {error}",
        "loading": "⏳ Загружаю и обрабатываю данные...",
        "no_content": "❌ Файл пустой или не удалось извлечь содержимое."
    }

    def __init__(self):
        self.chunks = []
        self.file_info = {}
        self.file_content = ""
        self.file_path = ""
        self.source_url = None

    async def client_ready(self, client, db):
        self.client = client
        self.db = db


    async def rfcmd(self, message: Message):
        """Чтение файла из реплая: .rf"""
        reply = await message.get_reply_message()
        if not reply or not reply.file:
            await message.edit(self.strings["no_reply"])
            return

        await message.edit(self.strings["loading"])
        self.file_path = await reply.download_media()
        await self._process_file(message, source="reply")

    async def rlcmd(self, message: Message):
        """Чтение файла по ссылке: .rl <url>"""
        args = utils.get_args_raw(message)
        if not args:
            await message.edit(self.strings["no_url"])
            return

        await message.edit(self.strings["loading"])
        self.source_url = args.strip()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.source_url) as response:
                    if response.status != 200:
                        await message.edit(self.strings["download_error"].format(error=f"HTTP {response.status}"))
                        return
                    content = await response.text()
                    if not content:
                        await message.edit(self.strings["no_content"])
                        return
                    self.file_content = content
                    parsed_url = urlparse(self.source_url)
                    self.file_path = os.path.basename(parsed_url.path) or "downloaded_file"
                    await self._process_file(message, source="url")
        except Exception as e:
            await message.edit(self.strings["download_error"].format(error=str(e)))

    async def _process_file(self, message: Message, source: str):
        if source == "reply":
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    self.file_content = f.read()
            except Exception as e:
                await message.edit(self.strings["read_error"].format(error=str(e)))
                return

        if not self.file_content:
            await message.edit(self.strings["no_content"])
            return

        self.chunks = self._split_text(self.file_content, 1500)
        self.file_info = await self._collect_file_info(source)
        await self._show_page(message, 0)

    def _split_text(self, text, size):
        return [text[i:i + size] for i in range(0, len(text), size)]

    async def _collect_file_info(self, source: str) -> dict:
        file_size = os.path.getsize(self.file_path) if source == "reply" else len(self.file_content.encode("utf-8"))
        info = {
            "<b>Имя файла</b>": os.path.basename(self.file_path),
            "<b>Размер</b>": f"{file_size} байт",
            "<b>Источник</b>": "Реплай" if source == "reply" else f"URL: {utils.escape_html(self.source_url)}",
            "<b>Страниц</b>": len(self.chunks),
            "<b>Время обработки</b>": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "<b>Расширение</b>": os.path.splitext(self.file_path)[1] or "Не указано",
            "<b>Символов</b>": len(self.file_content)
        }
        return info

    async def _show_page(self, msg_or_call, index):
        total = len(self.chunks)
        index = max(0, min(index, total - 1))
        text = f"<b>📒 Страница {index + 1}/{total}</b>\n<pre>{utils.escape_html(self.chunks[index])}</pre>"
        buttons = [
            [
                {"text": "⬅️", "callback": self._page_cb, "args": (index - 1,)},
                {"text": "➡️", "callback": self._page_cb, "args": (index + 1,)}
            ],
            [
                {"text": "ℹ️ Инфа", "callback": self._info_cb, "args": (index,)}
            ]
        ]

        if isinstance(msg_or_call, Message):
            await self.inline.form(text=text, message=msg_or_call, reply_markup=buttons)
        elif hasattr(msg_or_call, "edit"):
            await msg_or_call.edit(text=text, reply_markup=buttons)

    async def _page_cb(self, call, index):
        await self._show_page(call, index)

    async def _info_cb(self, call, return_index):
        info_text = "\n".join([f"{k}: {utils.escape_html(str(v))}" for k, v in self.file_info.items()])
        await call.edit(
            text=f"<b>📄 Информация о файле:</b>\n{info_text}",
            reply_markup=[
                [{"text": "↩️ Назад", "callback": self._page_cb, "args": (return_index,)}]
            ]
        )
