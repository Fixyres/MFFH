# ███████╗███╗░░░███╗██╗░░██╗░░░░░██╗
# ██╔════╝████╗░████║██║░░██║░░░░░██║
# █████╗░░██╔████╔██║███████║░░░░░██║
# ██╔══╝░░██║╚██╔╝██║██╔══██║██╗░░██║
# ██║░░░░░██║░╚═╝░██║██║░░██║╚█████╔╝
# ╚═╝░░░░░╚═╝░░░░░╚═╝╚═╝░░╚═╝░╚════╝░

# module ForwardHidden
# meta developer: @Hikimuro, @kf_ic3peak
# ver. 2.2.1
__version__ = (2, 2, 1) 

import logging
import os
import asyncio
import tempfile
import shutil
import uuid
from telethon import errors
from telethon.tl.types import (
    Message,
    MessageMediaPhoto,
    MessageMediaDocument,
    MessageActionTopicCreate,
)
from telethon.tl.functions.channels import GetForumTopicsRequest

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class ForwardHiddenMod(loader.Module):
    """Forward messages from protected channels."""

    strings = {
        "name": "ForwardHidden",
        "help": (
            "❓ <b>Usage:</b>\n"
            "• <code>{prefix}fh {{chat_id}} {{count}}</code> — from main chat\n"
            "• <code>{prefix}fh {{chat_id}} {{topic_id}} {{count}}</code> — from specific topic\n"
            "• <code>{prefix}fh {{chat_id}} general {{count}}</code> — from General topic\n\n"
            "❓ <b>How to get chat_id:</b> use <code>{prefix}listch</code> or <code>{prefix}getid</code>\n"
            "❓ <b>How to get topic_id:</b> use <code>{prefix}listtopics {{chat_id}}</code>"
        ),
        "invalid_args": "❌ <b>Invalid arguments!</b>\n\n{help}",
        "invalid_count": "❌ <b>The count must be between 1 and 1000</b>",
        "chat_not_found": "❌ <b>Could not find chat</b>",
        "topic_not_found": "❌ <b>Could not find topic with ID:</b> <code>{}</code>",
        "no_messages": "❌ <b>No messages found for forwarding</b>",
        "processing": "⏳ <b>Processing messages...</b>",
        "processing_topic": "⏳ <b>Processing messages from topic...</b>",
        "success": "✅ <b>Done!</b> Processed: <code>{}</code> messages",
        "success_topic": "✅ <b>Done!</b> Processed: <code>{}</code> messages from topic <code>{}</code>",
        "error": "❌ <b>Error:</b> <code>{}</code>",
        "no_topics": "❌ <b>No topics found in this chat or it is not a supergroup</b>",
        "topics_list": (
            "📋 <b>Topics in chat {chat_name}:</b>\n\n"
            "🏠 <code>general</code> or <code>1</code> — General topic\n{topics}\n\n"
            "<b>💡 Example:</b>\n"
            "<code>{prefix}fh {chat_id} {topic_example} 5</code>"
        ),
        "no_chatid": "❌ <b>Please specify a chat ID:</b>\n<code>{prefix}listtopics -100123456789</code>",
        "no_chats_found": "❌ <b>No chats found</b>",
        "listch_title": "<b>📋 Available chats:</b>\n\n",
        "channels": "<b>📢 Channels:</b>\n",
        "groups": "<b>👥 Groups:</b>\n",
        "usage_example": (
            "<b>💡 Example:</b>\n<code>{prefix}fh {{chat_id}} 5</code>\n\n"
            "<i>🔒 — protected from forwarding</i>\n"
            "<i>🧵 — supports topics</i>"
        ),
        "getid": (
            "🆔 <b>This chat's ID:</b> <code>{chat_id}</code>\n"
            "📝 <b>Title:</b> {name}\n"
            "🧵 <b>Topics:</b> {forum_support}\n\n"
            "<b>💡 Quick copy:</b>\n<code>{prefix}fh {chat_id} 10</code>\n\n"
            "{topics_notice}"
        ),
        "getid_topics_notice": "<b>🔍 See topics:</b>\n<code>{prefix}listtopics {chat_id}</code>",
        "forum_true": "🧵 Supports topics",
        "forum_false": "❌ Regular chat"
    }

    strings_ru = {
        "_cls_doc": "Пересылка из защищённых каналов.",
        "help": (
            "❓ <b>Использование:</b>\n"
            "• <code>{prefix}fh {{chat_id}} {{количество}}</code> — из основного чата\n"
            "• <code>{prefix}fh {{chat_id}} {{topic_id}} {{количество}}</code> — из конкретного топика\n"
            "• <code>{prefix}fh {{chat_id}} general {{количество}}</code> — из General топика\n\n"
            "❓ <b>Чтобы узнать chat_id:</b> используй <code>{prefix}listch</code> или <code>{prefix}getid</code>\n"
            "❓ <b>Чтобы узнать topic_id:</b> используй <code>{prefix}listtopics {{chat_id}}</code>"
        ),
        "invalid_args": "❌ <b>Неверные аргументы!</b>\n\n{help}",
        "invalid_count": "❌ <b>Количество должно быть от 1 до 1000</b>",
        "chat_not_found": "❌ <b>Не удалось найти чат</b>",
        "topic_not_found": "❌ <b>Не удалось найти топик с ID:</b> <code>{}</code>",
        "no_messages": "❌ <b>Не найдено сообщений для пересылки</b>",
        "processing": "⏳ <b>Обрабатываю сообщения...</b>",
        "processing_topic": "⏳ <b>Обрабатываю сообщения из топика...</b>",
        "success": "✅ <b>Готово!</b> Обработано: <code>{}</code> сообщений",
        "success_topic": "✅ <b>Готово!</b> Обработано: <code>{}</code> сообщений из топика <code>{}</code>",
        "error": "❌ <b>Ошибка:</b> <code>{}</code>",
        "no_topics": "❌ <b>В этом чате нет топиков или это не супергруппа</b>",
        "topics_list": (
            "📋 <b>Список топиков в чате {chat_name}:</b>\n\n"
            "🏠 <code>general</code> или <code>1</code> — General топик\n{topics}\n\n"
            "<b>💡 Пример:</b>\n"
            "<code>{prefix}fh {chat_id} {topic_example} 5</code>"
        ),
        "no_chatid": "❌ <b>Укажите ID чата:</b>\n<code>{prefix}listtopics -100123456789</code>",
        "no_chats_found": "❌ <b>Чаты не найдены</b>",
        "listch_title": "<b>📋 Список доступных чатов:</b>\n\n",
        "channels": "<b>📢 Каналы:</b>\n",
        "groups": "<b>👥 Группы:</b>\n",
        "usage_example": (
            "<b>💡 Пример использования:</b>\n<code>{prefix}fh {{chat_id}} 5</code>\n\n"
            "<i>🔒 — защищён от пересылки</i>\n"
            "<i>🧵 — поддерживает топики</i>"
        ),
        "getid": (
            "🆔 <b>ID этого чата:</b> <code>{chat_id}</code>\n"
            "📝 <b>Название:</b> {name}\n"
            "🧵 <b>Топики:</b> {forum_support}\n\n"
            "<b>💡 Быстро скопировать:</b>\n<code>{prefix}fh {chat_id} 10</code>\n\n"
            "{topics_notice}"
        ),
        "getid_topics_notice": "<b>🔍 Для просмотра топиков:</b>\n<code>{prefix}listtopics {chat_id}</code>",
        "forum_true": "🧵 Поддерживает топики",
        "forum_false": "❌ Обычный чат"
    }

    strings_de = {
        "_cls_doc": "Weiterleitung aus geschützten Kanälen.",
        "help": (
            "❓ <b>Verwendung:</b>\n"
            "• <code>{prefix}fh {{chat_id}} {{anzahl}}</code> — aus dem Hauptchat\n"
            "• <code>{prefix}fh {{chat_id}} {{thema_id}} {{anzahl}}</code> — aus einem bestimmten Thema\n"
            "• <code>{prefix}fh {{chat_id}} general {{anzahl}}</code> — aus dem General-Thema\n\n"
            "❓ <b>Wie man chat_id erhält:</b> mit <code>{prefix}listch</code> oder <code>{prefix}getid</code>\n"
            "❓ <b>Wie man topic_id erhält:</b> mit <code>{prefix}listtopics {{chat_id}}</code>"
        ),
        "invalid_args": "❌ <b>Ungültige Argumente!</b>\n\n{help}",
        "invalid_count": "❌ <b>Die Anzahl muss zwischen 1 und 1000 liegen</b>",
        "chat_not_found": "❌ <b>Chat konnte nicht gefunden werden</b>",
        "topic_not_found": "❌ <b>Thema mit ID nicht gefunden:</b> <code>{}</code>",
        "no_messages": "❌ <b>Keine Nachrichten zum Weiterleiten gefunden</b>",
        "processing": "⏳ <b>Nachrichten werden verarbeitet…</b>",
        "processing_topic": "⏳ <b>Nachrichten aus Thema werden verarbeitet…</b>",
        "success": "✅ <b>Fertig!</b> Verarbeitet: <code>{}</code> Nachrichten",
        "success_topic": "✅ <b>Fertig!</b> Verarbeitet: <code>{}</code> Nachrichten aus Thema <code>{}</code>",
        "error": "❌ <b>Fehler:</b> <code>{}</code>",
        "no_topics": "❌ <b>Keine Themen in diesem Chat oder nicht Supergruppe</b>",
        "topics_list": (
            "📋 <b>Themen im Chat {chat_name}:</b>\n\n"
            "🏠 <code>general</code> oder <code>1</code> — General-Thema\n{topics}\n\n"
            "<b>💡 Beispiel:</b>\n"
            "<code>{prefix}fh {chat_id} {topic_example} 5</code>"
        ),
        "no_chatid": "❌ <b>Bitte gib eine Chat-ID an:</b>\n<code>{prefix}listtopics -100123456789</code>",
        "no_chats_found": "❌ <b>Keine Chats gefunden</b>",
        "listch_title": "<b>📋 Verfügbare Chats:</b>\n\n",
        "channels": "<b>📢 Kanäle:</b>\n",
        "groups": "<b>👥 Gruppen:</b>\n",
        "usage_example": (
            "<b>💡 Beispiel:</b>\n<code>{prefix}fh {{chat_id}} 5</code>\n\n"
            "<i>🔒 — geschützt vor Weiterleitung</i>\n"
            "<i>🧵 — unterstützt Themen</i>"
        ),
        "getid": (
            "🆔 <b>Diese Chat-ID:</b> <code>{chat_id}</code>\n"
            "📝 <b>Name:</b> {name}\n"
            "🧵 <b>Themen:</b> {forum_support}\n\n"
            "<b>💡 Schnell kopieren:</b>\n<code>{prefix}fh {chat_id} 10</code>\n\n"
            "{topics_notice}"
        ),
        "getid_topics_notice": "<b>🔍 Themen anzeigen:</b>\n<code>{prefix}listtopics {chat_id}</code>",
        "forum_true": "🧵 Unterstützt Themen",
        "forum_false": "❌ Regulärer Chat"
    }

    def get_prefix(self):
        return getattr(self, "get_prefix", lambda: ".")()

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    async def get_topic_info(self, chat, topic_id):
        try:
            if topic_id == 1:
                return "General"
            offset_id = 0
            while True:
                msgs = await self.client.get_messages(chat, limit=1000, offset_id=offset_id)
                if not msgs:
                    break
                for msg in msgs:
                    if msg.id == topic_id and hasattr(msg, "action") and isinstance(msg.action, MessageActionTopicCreate):
                        return msg.action.title
                offset_id = msgs[-1].id
                await asyncio.sleep(0.05)
            return f"Topic #{topic_id}"
        except Exception:
            return f"Topic #{topic_id}"

    async def download_and_save(self, message, index, session_dir):
        saved_items = []
        try:
            if message.media:
                if isinstance(message.media, MessageMediaPhoto):
                    filename = f"photo_{uuid.uuid4().hex[:8]}.jpg"
                    filepath = os.path.join(session_dir, filename)
                    await self.client.download_media(message, file=filepath)
                    saved_items.append({"type": "photo", "path": filepath, "caption": getattr(message, "text", "")})
                elif isinstance(message.media, MessageMediaDocument):
                    doc = message.media.document
                    original_name = f"file_{uuid.uuid4().hex[:8]}"
                    for attr in doc.attributes:
                        if hasattr(attr, "file_name"):
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
                    saved_items.append({"type": "document", "path": filepath, "caption": getattr(message, "text", "")})
            elif message.text:
                saved_items.append({"type": "text", "text": message.text})
        except Exception as e:
            logger.error(f"Download error: {e}")
            if message.text:
                saved_items.append({"type": "text", "text": message.text})
        return saved_items

    async def send_saved_content(self, saved_items, target_chat, target_topic_id=None, progress_msg=None):
        
        semaphore = asyncio.Semaphore(3)
        sent_count = 0
        total = len(saved_items)
        lock = asyncio.Lock()
        last_progress_text = {"v": None}
        
        async def send_one(idx, item):
            nonlocal sent_count
            async with semaphore:
                try:
                    if item["type"] == "text":
                        await self.client.send_message(
                            target_chat,
                            item["text"],
                            reply_to=target_topic_id if target_topic_id and target_topic_id != 1 else None
                        )
                    elif item["type"] in ["photo", "document"]:
                        if os.path.exists(item["path"]):
                            await self.client.send_file(
                                target_chat,
                                item["path"],
                                caption=item["caption"],
                                reply_to=target_topic_id if target_topic_id and target_topic_id != 1 else None
                            )
                            os.remove(item["path"])
                    async with lock:
                        sent_count += 1
                        progress = f"📤 {sent_count} / {total}"
                        if progress_msg and (sent_count % 5 == 0 or sent_count == total):
                            if last_progress_text["v"] != progress:
                                await progress_msg.edit(progress)
                                last_progress_text["v"] = progress
                except errors.FloodWaitError as e:
                    logger.warning(f"FloodWait: sleeping {e.seconds} sec.")
                    await asyncio.sleep(e.seconds)
                    return await send_one(idx, item)
                except Exception as e:
                    logger.error(f"Send error: {e}")

        await asyncio.gather(*[send_one(i, item) for i, item in enumerate(saved_items, 1)])
        if progress_msg:
            final_progress = f"📤 {sent_count} / {total}"
            if last_progress_text["v"] != final_progress:
                await progress_msg.edit(final_progress)
        return sent_count

    @loader.command(
        ru_doc="Пересылка сообщений из канала или топика.",
        de_doc="Weiterleitung von Nachrichten aus Channel oder Thema.",
    )
    async def fh(self, message: Message):
        """Forward messages from a channel or topic."""
        args = utils.get_args_raw(message)
        prefix = self.get_prefix()
        help_text = self.strings("help").format(prefix=prefix)
        if not args:
            await utils.answer(message, self.strings("invalid_args").format(help=help_text))
            return
        try:
            parts = args.split()
            if len(parts) == 2:
                chat_id, count_str = parts
                topic_id = None
            elif len(parts) == 3:
                chat_id, topic_str, count_str = parts
                topic_id = 1 if topic_str.lower() == "general" else int(topic_str)
            else:
                await utils.answer(message, self.strings("invalid_args").format(help=help_text))
                return
            count = int(count_str)
            if count <= 0 or count > 1000:
                await utils.answer(message, self.strings("invalid_count"))
                return
            progress_msg = await utils.answer(
                message,
                self.strings("processing_topic") if topic_id else self.strings("processing"),
            )
            try:
                source_chat = await self.client.get_entity(
                    int(chat_id) if chat_id.lstrip("-").isdigit() else chat_id
                )
            except Exception as e:
                await utils.answer(progress_msg, self.strings("chat_not_found"))
                logger.error(f"Chat not found: {e}")
                return

            messages = []
            try:
                async for msg in self.client.iter_messages(
                    source_chat, limit=count, reply_to=topic_id if topic_id else None
                ):
                    if msg and (msg.text or msg.media):
                        messages.append(msg)
            except Exception as e:
                txt = self.strings("topic_not_found").format(topic_id) if topic_id else self.strings("chat_not_found")
                await utils.answer(progress_msg, txt)
                logger.error(f"Message fetch error: {e}")
                return

            if not messages:
                await utils.answer(progress_msg, self.strings("no_messages"))
                return

            messages.reverse()
            session_dir = tempfile.mkdtemp(prefix="fh_", suffix="_" + uuid.uuid4().hex[:6])
            all_saved_items = []
            for i, msg in enumerate(messages, 1):
                saved_items = await self.download_and_save(msg, i, session_dir)
                all_saved_items.extend(saved_items)
                await asyncio.sleep(0.1)

            sent_count = await self.send_saved_content(
                all_saved_items, message.chat_id, None, progress_msg
            )
            if topic_id:
                topic_name = await self.get_topic_info(source_chat, topic_id)
                await progress_msg.edit(self.strings("success_topic").format(sent_count, topic_name))
            else:
                await progress_msg.edit(self.strings("success").format(sent_count))
        except Exception as e:
            logger.error(f"FH general error: {e}")
            await utils.answer(message, self.strings("error").format(str(e)))
        finally:
            if 'session_dir' in locals() and os.path.exists(session_dir):
                shutil.rmtree(session_dir, ignore_errors=True)

    @loader.command(
        ru_doc="Показать все топики в чате.",
        de_doc="Alle Themen im Chat anzeigen.",
    )
    async def listtopics(self, message: Message):
        """Show all topics in a chat."""
        args = utils.get_args_raw(message)
        prefix = self.get_prefix()
        if not args:
            await utils.answer(message, self.strings("no_chatid").format(prefix=prefix))
            return
        try:
            chat_id = args.strip()
            chat = await self.client.get_entity(
                int(chat_id) if chat_id.lstrip("-").isdigit() else chat_id
            )
            chat_name = getattr(chat, "title", "Unknown")
            if not getattr(chat, "megagroup", False) or not getattr(chat, "forum", False):
                await utils.answer(message, self.strings("no_topics"))
                return
            result = await self.client(GetForumTopicsRequest(
                channel=chat, offset_date=None, offset_id=0, offset_topic=0, limit=100
            ))
            if not result.topics:
                await utils.answer(message, self.strings("no_topics"))
                return

            topics = []
            topic_example = 1
            for t in result.topics:
                if hasattr(t, "title"):
                    topics.append(f"📌 <code>{t.id}</code> — {t.title}")
                    topic_example = t.id

            topics_text = "\n".join(topics[:200])
            output = self.strings("topics_list").format(
                chat_name=chat_name,
                topics=topics_text,
                chat_id=chat_id,
                topic_example=topic_example,
                prefix=prefix
            )
            await utils.answer(message, output)
        except Exception as e:
            logger.error(f"listtopics error: {e}")
            await utils.answer(message, self.strings("error").format(str(e)))

    @loader.command(
        ru_doc="Показать все каналы и группы.",
        de_doc="Alle Kanäle und Gruppen anzeigen.",
    )
    async def listch(self, message: Message):
        """Show all channels and groups."""
        try:
            dialogs = await self.client.get_dialogs(limit=1000)
            result = self.strings("listch_title")
            channels = []
            groups = []
            for dialog in dialogs:
                entity = dialog.entity
                chat_id = entity.id
                protected = "🔒" if getattr(entity, "noforwards", False) else ""
                topics_mark = "🧵" if getattr(entity, "forum", False) else ""
                if getattr(entity, "broadcast", False):
                    channels.append(f"📢 <code>{chat_id}</code> — {entity.title} {protected}")
                elif getattr(entity, "megagroup", False):
                    groups.append(f"👥 <code>{chat_id}</code> — {entity.title} {protected}{topics_mark}")

            prefix = self.get_prefix()
            if channels:
                result += self.strings("channels") + "\n".join(channels[:200]) + "\n\n"
            if groups:
                result += self.strings("groups") + "\n".join(groups[:200]) + "\n\n"

            result += self.strings("usage_example").format(prefix=prefix)

            if result.strip() == self.strings("listch_title").strip():
                result = self.strings("no_chats_found")

            await utils.answer(message, f"<blockquote>{result}</blockquote>")
        except Exception as e:
            logger.error(f"listch error: {e}")
            await utils.answer(message, self.strings("error").format(e))

    @loader.command(
        ru_doc="Получить ID текущего чата.",
        de_doc="ID des aktuellen Chats anzeigen.",
    )
    async def getid(self, message: Message):
        """Get the ID of the current chat."""
        chat_id = message.chat_id
        prefix = self.get_prefix()
        try:
            chat = await self.client.get_entity(chat_id)
            name = getattr(chat, "title", None) or getattr(chat, "first_name", "Unknown")
            forum_support = self.strings("forum_true") if getattr(chat, "forum", False) else self.strings("forum_false")
            topics_notice = self.strings("getid_topics_notice").format(prefix=prefix, chat_id=chat_id) if getattr(chat, "forum", False) else ""
            result = self.strings("getid").format(
                chat_id=chat_id,
                name=name,
                forum_support=forum_support,
                prefix=prefix,
                topics_notice=topics_notice
            )
            await utils.answer(message, result)
        except Exception:
            await utils.answer(message, f"🆔 <b>ID чата:</b> <code>{chat_id}</code>")
