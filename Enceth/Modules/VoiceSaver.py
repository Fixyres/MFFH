# meta developer: @Enceth

from .. import loader
from telethon.tl.types import Message
import os
import json

@loader.tds
class VoiceSaverMod(loader.Module):
    """Сохраняет и отправляет голосовые сообщения"""

    strings = {"name": "VoiceSaver"}

    def __init__(self):
        self.config_dir = os.path.join(os.path.expanduser("~"), ".voicesaver")
        os.makedirs(self.config_dir, exist_ok=True)
        self.json_path = os.path.join(self.config_dir, "voices.json")
        if not os.path.exists(self.json_path):
            with open(self.json_path, "w") as f:
                json.dump({}, f)

    def _load_db(self):
        with open(self.json_path, "r") as f:
            return json.load(f)

    def _save_db(self, db):
        with open(self.json_path, "w") as f:
            json.dump(db, f, indent=4)

    async def savevcmd(self, message: Message):
        """Сохраняет гс. Использование: .savev <имя> (в ответ на гс)"""
        args = message.raw_text.split(maxsplit=1)
        if len(args) < 2:
            await message.edit("Укажи имя для гс")
            return
        name = args[1].strip()
        reply = await message.get_reply_message()
        if not reply or not reply.voice:
            await message.edit("Ответь на голосовое сообщение")
            return
        path = os.path.join(self.config_dir, f"{name}.ogg")
        await reply.download_media(file=path)
        db = self._load_db()
        db[name] = path
        self._save_db(db)
        await message.edit(f"Гс `{name}` сохранено")

    async def delvcmd(self, message: Message):
        """Удаляет сохранённое гс. Использование: .delv <имя>"""
        args = message.raw_text.split(maxsplit=1)
        if len(args) < 2:
            await message.edit("Укажи имя для удаления")
            return
        name = args[1].strip()
        db = self._load_db()
        if name not in db:
            await message.edit("Такого гс нет")
            return
        os.remove(db[name])
        del db[name]
        self._save_db(db)
        await message.edit(f" Гс `{name}` удалено")

    async def listvcmd(self, message: Message):
        """Показывает список сохранённых гс"""
        db = self._load_db()
        if not db:
            await message.edit("Гс не найдено")
            return
        text = "🎵 Сохранённые гс:\n" + "\n".join(f"- {name}" for name in db)
        await message.edit(text)

    async def voicecmd(self, message: Message):
        """Отправляет сохранённое гс. Использование: .voice <имя>"""
        args = message.raw_text.split(maxsplit=1)
        if len(args) < 2:
            await message.edit("Укажи имя для воспроизведения")
            return
        name = args[1].strip()
        db = self._load_db()
        if name not in db:
            await message.edit("Такого гс нет")
            return
        await message.delete()
        reply = await message.get_reply_message()
        await message.client.send_file(
            message.to_id,
            db[name],
            voice_note=True,
            reply_to=reply.id if reply else None,
        )