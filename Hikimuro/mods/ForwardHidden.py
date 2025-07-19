# module ForwardHidden
# meta developer: @Hikimuro, @kf_ic3peak
# ver. 2.0.0

import logging
import os
import asyncio
import tempfile
import shutil
import uuid
from telethon import errors
from telethon.tl.types import Message, MessageMediaPhoto, MessageMediaDocument
from telethon.tl.types import DocumentAttributeFilename

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class ForwardHiddenMod(loader.Module):
    """Модуль для пересылки сообщений из каналов с обходом защиты"""

    strings = {
        "name": "ForwardHidden",
        "help": "❓ <b>Использование:</b> <code>.fh {chat_id} {количество}</code>\n❓ <b>Чтобы узнать chat_id:</b> используй <code>.listch</code> или <code>.getid</code>",
        "invalid_args": "❌ <b>Неверные аргументы!</b>\n\n{help}",
        "invalid_count": "❌ <b>Количество должно быть от 1 до 50</b>",
        "chat_not_found": "❌ <b>Не удалось найти чат</b>",
        "no_messages": "❌ <b>Не найдено сообщений для пересылки</b>",
        "processing": "⏳ <b>Обрабатываю сообщения...</b>",
        "success": "✅ <b>Готово!</b> Обработано: <code>{}</code> сообщений",
        "error": "❌ <b>Ошибка:</b> <code>{}</code>"
    }

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    async def download_and_save(self, message, index, session_dir):
        saved_items = []

        try:
            if message.media:
                if isinstance(message.media, MessageMediaPhoto):
                    filename = f"photo_{uuid.uuid4().hex[:8]}.jpg"
                    filepath = os.path.join(session_dir, filename)
                    await self.client.download_media(message, file=filepath)
                    saved_items.append({
                        'type': 'photo',
                        'path': filepath,
                        'caption': getattr(message, "text", "")
                    })
                elif isinstance(message.media, MessageMediaDocument):
                    doc = message.media.document
                    original_name = f"file_{uuid.uuid4().hex[:8]}"
                    for attr in doc.attributes:
                        if isinstance(attr, DocumentAttributeFilename):
                            name, ext = os.path.splitext(attr.file_name)
                            original_name = f"{name}_{uuid.uuid4().hex[:4]}{ext}"
                            break
                    else:
                        if doc.mime_type:
                            if "video" in doc.mime_type:
                                original_name += ".mp4"
                            elif "audio" in doc.mime_type:
                                original_name += ".mp3"
                            elif "image" in doc.mime_type:
                                original_name += ".jpg"
                            else:
                                original_name += ".bin"

                    filepath = os.path.join(session_dir, original_name)
                    await self.client.download_media(message, file=filepath)
                    saved_items.append({
                        'type': 'document',
                        'path': filepath,
                        'caption': getattr(message, "text", "")
                    })
            elif message.text:
                saved_items.append({'type': 'text', 'text': message.text})
        except Exception as e:
            logger.error(f"Ошибка скачивания: {e}")
            if message.text:
                saved_items.append({'type': 'text', 'text': message.text})
        return saved_items

    async def send_saved_content(self, saved_items, target_chat, progress_msg=None):
        sent_count = 0
        total = len(saved_items)

        for i, item in enumerate(saved_items, 1):
            try:
                if item['type'] == 'text':
                    await self.client.send_message(target_chat, item['text'])
                    sent_count += 1
                elif item['type'] in ['photo', 'document']:
                    if os.path.exists(item['path']):
                        await self.client.send_file(
                            target_chat,
                            item['path'],
                            caption=item['caption']
                        )
                        sent_count += 1
                        os.remove(item['path'])

                if progress_msg:
                    await progress_msg.edit(f"📤 Отправка {i} из {total}...")

                await asyncio.sleep(0.5)

            except errors.FloodWaitError as e:
                logger.warning(f"FloodWait: сплю {e.seconds} сек.")
                await asyncio.sleep(e.seconds)
            except Exception as e:
                logger.error(f"Ошибка отправки: {e}")
        return sent_count

    @loader.command()
    async def fh(self, message: Message):
        """<chat_id> <количество> — пересылка последних N сообщений из канала"""
        args = utils.get_args_raw(message)

        if not args:
            await utils.answer(message, self.strings["invalid_args"].format(help=self.strings["help"]))
            return

        try:
            parts = args.split()
            if len(parts) != 2:
                await utils.answer(message, self.strings["invalid_args"].format(help=self.strings["help"]))
                return

            chat_id = parts[0]
            try:
                count = int(parts[1])
            except ValueError:
                await utils.answer(message, self.strings["invalid_args"].format(help=self.strings["help"]))
                return

            if count <= 0 or count > 50:
                await utils.answer(message, self.strings["invalid_count"])
                return

            progress_msg = await utils.answer(message, self.strings["processing"])

            try:
                if chat_id.isdigit() or chat_id.startswith("-"):
                    source_chat = await self.client.get_entity(int(chat_id))
                else:
                    source_chat = await self.client.get_entity(chat_id)
            except Exception as e:
                await utils.answer(progress_msg, self.strings["chat_not_found"])
                logger.error(f"Чат не найден: {e}")
                return

            messages = []
            async for msg in self.client.iter_messages(source_chat, limit=count):
                if msg and (msg.text or msg.media):
                    messages.append(msg)


            session_dir = tempfile.mkdtemp(prefix="fh_", suffix="_" + uuid.uuid4().hex[:6])
            all_saved_items = []
            for i, msg in enumerate(messages, 1):
                saved_items = await self.download_and_save(msg, i, session_dir)
                all_saved_items.extend(saved_items)
                await asyncio.sleep(0.1)

            sent_count = await self.send_saved_content(all_saved_items, message.chat_id, progress_msg)

            await progress_msg.edit(self.strings["success"].format(sent_count))

        except Exception as e:
            logger.error(f"Общая ошибка fh: {e}")
            await utils.answer(message, self.strings["error"].format(str(e)))
        finally:
            if 'session_dir' in locals() and os.path.exists(session_dir):
                shutil.rmtree(session_dir, ignore_errors=True)

    @loader.command()
    async def listch(self, message: Message):
        """— показать список всех каналов и супергрупп, включая закрытые"""
        try:
            dialogs = await self.client.get_dialogs(limit=50)
            result = "<b>📋 Список доступных чатов:</b>\n\n"
            channels = []
            groups = []

            for dialog in dialogs:
                entity = dialog.entity
                chat_id = entity.id
                protected = "🔒" if getattr(entity, "noforwards", False) else ""
                if getattr(entity, "broadcast", False):
                    channels.append(f"📢 <code>{chat_id}</code> - {entity.title} {protected}")
                elif getattr(entity, "megagroup", False):
                    groups.append(f"👥 <code>{chat_id}</code> - {entity.title} {protected}")

            if channels:
                result += "<b>📢 Каналы:</b>\n" + "\n".join(channels[:20]) + "\n\n"
            if groups:
                result += "<b>👥 Группы:</b>\n" + "\n".join(groups[:15]) + "\n\n"

            result += f"<b>💡 Пример использования:</b>\n<code>.fh {chat_id} 5</code>\n\n"
            result += "<i>🔒 - защищенный от пересылки</i>"

            if result.strip() == "<b>📋 Список доступных чатов:</b>\n\n":
                result = "❌ <b>Чаты не найдены</b>"

            await utils.answer(message, result)
        except Exception as e:
            logger.error(f"Ошибка listch: {e}")
            await utils.answer(message, f"❌ <b>Не удалось получить chat_id:</b> <code>{e}</code>")

    @loader.command()
    async def getid(self, message: Message):
        """— получить ID текущего чата"""
        chat_id = message.chat_id
        try:
            chat = await self.client.get_entity(chat_id)
            chat_name = getattr(chat, "title", None) or getattr(chat, "first_name", "Неизвестно")
            result = f"🆔 <b>ID этого чата:</b> <code>{chat_id}</code>\n"
            result += f"📝 <b>Название:</b> {chat_name}\n\n"
            result += f"<b>💡 Для копирования используй:</b>\n<code>.fh {chat_id} 10</code>"
            await utils.answer(message, result)
        except Exception as e:
            await utils.answer(message, f"🆔 <b>ID чата:</b> <code>{chat_id}</code>")
