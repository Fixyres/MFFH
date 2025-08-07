# ███████╗███╗░░░███╗██╗░░██╗░░░░░██╗
# ██╔════╝████╗░████║██║░░██║░░░░░██║
# █████╗░░██╔████╔██║███████║░░░░░██║
# ██╔══╝░░██║╚██╔╝██║██╔══██║██╗░░██║
# ██║░░░░░██║░╚═╝░██║██║░░██║╚█████╔╝
# ╚═╝░░░░░╚═╝░░░░░╚═╝╚═╝░░╚═╝░╚════╝░

# module ForwardHidden
# meta developer: @Hikimuro, @kf_ic3peak
# ver. 2.4.2
__version__ = (2, 4, 2) 

import logging
import os
import asyncio
import tempfile
import shutil
import uuid
import time
import gc
import random
import gzip
from collections import defaultdict
from functools import lru_cache
from telethon import errors
from telethon.tl.types import (
    Message,
    MessageMediaPhoto,
    MessageMediaDocument,
    MessageActionTopicCreate,
    DocumentAttributeFilename,
)
from telethon.tl.functions.channels import GetForumTopicsRequest

from .. import loader, utils

logger = logging.getLogger(__name__)

class AdaptiveDelayController:
    def __init__(self, base_delay=0.15):
        self.base_delay = base_delay
        self.current_delay = base_delay
        self.response_times = []
        self.flood_wait_count = 0
        self.last_flood_time = 0
    
    def record_response_time(self, response_time):
        self.response_times.append(response_time)
        if len(self.response_times) > 10:
            self.response_times.pop(0)
    
    def record_flood_wait(self):
        self.flood_wait_count += 1
        self.last_flood_time = time.time()
        self.current_delay = min(self.current_delay * 1.1, 0.8)
    
    def get_adaptive_delay(self):
        current_time = time.time()
        
        if self.last_flood_time > 0 and (current_time - self.last_flood_time) > 30:
            self.flood_wait_count = 0
            self.last_flood_time = 0
        
        if not self.response_times:
            return max(self.current_delay, 0.05)
            
        avg_time = sum(self.response_times) / len(self.response_times)
        
        if avg_time > 2.5 and self.flood_wait_count > 2:
            self.current_delay = min(self.current_delay * 1.05, 0.8)
        elif avg_time < 0.3 and self.flood_wait_count == 0:
            self.current_delay = max(self.current_delay * 0.95, 0.05)
        
        return max(self.current_delay, 0.05)
    
    async def wait(self):
        delay = self.get_adaptive_delay()
        jitter = random.uniform(0, delay * 0.05)
        final_delay = max(0.05, delay + jitter)
        await asyncio.sleep(final_delay)

@loader.tds
class ForwardHiddenMod(loader.Module):
    """Optimized forward messages from protected channels."""

    strings = {
        "name": "ForwardHidden",
        "help": (
            "❓ <b>Usage:</b>\n"
            "• <code>{prefix}fh {{chat_id}} {{count}}</code> — from main chat\n"
            "• <code>{prefix}fh {{chat_id}} {{topic_id}} {{count}}</code> — from specific topic\n"
            "• <code>{prefix}fh {{chat_id}} general {{count}}</code> — from General topic\n\n"
            "❓ <b>How to get chat_id:</b> use <code>{prefix}listch</code> or <code>{prefix}getid</code>\n"
            "❓ <b>How to get topic_id:</b> use <code>{prefix}listtopics {{chat_id}}</code>\n\n"
            "⚡ <b>OPTIMIZED:</b> Faster processing, gentle FloodWait protection, proper filenames"
        ),
        "invalid_args": "❌ <b>Invalid arguments!</b>\n\n{help}",
        "invalid_count": "❌ <b>Count must be a positive number</b>",
        "invalid_chat_id": "❌ <b>Invalid chat ID format</b>",
        "large_count_warning": "⚠️ <b>Large batch detected:</b> {count} messages\n⚡ Using optimized batch processing",
        "chat_not_found": "❌ <b>Could not find chat</b>",
        "topic_not_found": "❌ <b>Could not find topic with ID:</b> <code>{}</code>",
        "no_messages": "❌ <b>No messages found for forwarding</b>",
        "processing": "⚡ <b>Processing messages...</b>\n📊 Progress: 0/{} | 🚀 Speed: 0 msg/min\n⏱️ ETA: calculating...",
        "processing_topic": "⚡ <b>Processing messages from topic...</b>\n📊 Progress: 0/{} | 🚀 Speed: 0 msg/min\n⏱️ ETA: calculating...",
        "progress_update": "📤 <b>Sending messages...</b>\n📊 Progress: {}/{} | 🚀 Speed: {:.0f} msg/min\n⏱️ ETA: {} | 🛡️ FloodWait: {}",
        "success": (
            "✅ <b>Done!</b> Processed: <code>{}</code> messages\n\n"
            "📊 <b>Statistics:</b>\n"
            "✅ Text: {} messages\n"
            "📷 Photos: {} files\n"
            "📄 Documents: {} files\n"
            "💾 Buffered: {} files\n"
            "🛡️ FloodWait handled: {} times\n"
            "❌ Errors: {} messages\n"
            "⏱️ Time: {} | 🚀 Avg speed: {:.0f} msg/min"
        ),
        "success_topic": (
            "✅ <b>Done!</b> Processed: <code>{}</code> messages from topic <code>{}</code>\n\n"
            "📊 <b>Statistics:</b>\n"
            "✅ Text: {} messages\n"
            "📷 Photos: {} files\n"
            "📄 Documents: {} files\n"
            "💾 Buffered: {} files\n"
            "🛡️ FloodWait handled: {} times\n"
            "❌ Errors: {} messages\n"
            "⏱️ Time: {} | 🚀 Avg speed: {:.0f} msg/min"
        ),
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
        "_cls_doc": "Оптимизированная пересылка с мягкой защитой.",
        "help": (
            "❓ <b>Использование:</b>\n"
            "• <code>{prefix}fh {{chat_id}} {{количество}}</code> — из основного чата\n"
            "• <code>{prefix}fh {{chat_id}} {{topic_id}} {{количество}}</code> — из конкретного топика\n"
            "• <code>{prefix}fh {{chat_id}} general {{количество}}</code> — из General топика\n\n"
            "❓ <b>Чтобы узнать chat_id:</b> используй <code>{prefix}listch</code> или <code>{prefix}getid</code>\n"
            "❓ <b>Чтобы узнать topic_id:</b> используй <code>{prefix}listtopics {{chat_id}}</code>\n\n"
            "⚡ <b>ОПТИМИЗИРОВАНО:</b> Быстрая обработка, мягкая защита от FloodWait, правильные имена файлов"
        ),
        "invalid_args": "❌ <b>Неверные аргументы!</b>\n\n{help}",
        "invalid_count": "❌ <b>Количество должно быть положительным числом</b>",
        "invalid_chat_id": "❌ <b>Неверный формат ID чата</b>",
        "large_count_warning": "⚠️ <b>Обнаружен большой объем:</b> {count} сообщений\n⚡ Используется оптимизированная пакетная обработка",
        "chat_not_found": "❌ <b>Не удалось найти чат</b>",
        "topic_not_found": "❌ <b>Не удалось найти топик с ID:</b> <code>{}</code>",
        "no_messages": "❌ <b>Не найдено сообщений для пересылки</b>",
        "processing": "⚡ <b>Обрабатываю сообщения...</b>\n📊 Прогресс: 0/{} | 🚀 Скорость: 0 сообщ/мин\n⏱️ Осталось: вычисляется...",
        "processing_topic": "⚡ <b>Обрабатываю сообщения из топика...</b>\n📊 Прогресс: 0/{} | 🚀 Скорость: 0 сообщ/мин\n⏱️ Осталось: вычисляется...",
        "progress_update": "📤 <b>Отправляю сообщения...</b>\n📊 Прогресс: {}/{} | 🚀 Скорость: {:.0f} сообщ/мин\n⏱️ Осталось: {} | 🛡️ FloodWait: {}",
        "success": (
            "✅ <b>Готово!</b> Обработано: <code>{}</code> сообщений\n\n"
            "📊 <b>Статистика:</b>\n"
            "✅ Текст: {} сообщений\n"
            "📷 Фото: {} файлов\n"
            "📄 Документы: {} файлов\n"
            "💾 Буферизовано: {} файлов\n"
            "🛡️ FloodWait обработано: {} раз\n"
            "❌ Ошибки: {} сообщений\n"
            "⏱️ Время: {} | 🚀 Средняя скорость: {:.0f} сообщ/мин"
        ),
        "success_topic": (
            "✅ <b>Готово!</b> Обработано: <code>{}</code> сообщений из топика <code>{}</code>\n\n"
            "📊 <b>Статистика:</b>\n"
            "✅ Текст: {} сообщений\n"
            "📷 Фото: {} файлов\n"
            "📄 Документы: {} файлов\n"
            "💾 Буферизовано: {} файлов\n"
            "🛡️ FloodWait обработано: {} раз\n"
            "❌ Ошибки: {} сообщений\n"
            "⏱️ Время: {} | 🚀 Средняя скорость: {:.0f} сообщ/мин"
        ),
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

    def __init__(self):
        self.topic_cache = {}
        self.delay_controller = AdaptiveDelayController()
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "max_retries",
                3,
                lambda: "Maximum retry attempts for failed operations",
                validator=loader.validators.Integer(minimum=1, maximum=10)
            ),
            loader.ConfigValue(
                "memory_limit_mb", 
                150,
                lambda: "Memory limit in MB for temp files",
                validator=loader.validators.Integer(minimum=50, maximum=500)
            ),
            loader.ConfigValue(
                "base_delay",
                0.15,
                lambda: "Base delay between messages in seconds", 
                validator=loader.validators.Float(minimum=0.05, maximum=2.0)
            ),
            loader.ConfigValue(
                "download_concurrency",
                12,
                lambda: "Max concurrent downloads",
                validator=loader.validators.Integer(minimum=3, maximum=25)
            ),
            loader.ConfigValue(
                "send_concurrency",
                15,
                lambda: "Max concurrent sends",
                validator=loader.validators.Integer(minimum=5, maximum=30)
            ),
            loader.ConfigValue(
                "small_file_limit",
                8,
                lambda: "Files smaller than this (MB) will be buffered in memory",
                validator=loader.validators.Integer(minimum=1, maximum=20)
            ),
            loader.ConfigValue(
                "batch_size",
                75,
                lambda: "Batch size for processing messages",
                validator=loader.validators.Integer(minimum=10, maximum=200)
            )
        )

    def get_prefix(self):
        return getattr(self, "get_prefix", lambda: ".")()

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    def format_time(self, seconds):
        if seconds < 60:
            return f"{int(seconds)}с"
        elif seconds < 3600:
            return f"{int(seconds // 60)}м {int(seconds % 60)}с"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours}ч {minutes}м"

    def get_memory_usage_mb(self):
        try:
            import psutil
            process = psutil.Process(os.getpid())
            return process.memory_info().rss / 1024 / 1024
        except ImportError:
            return 0

    async def cleanup_memory(self, session_dir=None):
        memory_before = self.get_memory_usage_mb()
        
        if session_dir and os.path.exists(session_dir):
            try:
                shutil.rmtree(session_dir, ignore_errors=True)
            except Exception:
                pass
        
        gc.collect()
        
        memory_after = self.get_memory_usage_mb()
        freed_mb = max(0, memory_before - memory_after)
        
        if freed_mb > 1:
            logger.info(f"Memory cleanup: freed {freed_mb:.1f}MB")
            
        return freed_mb

    def validate_chat_id(self, chat_id):
        if not chat_id:
            return False
        
        chat_id = str(chat_id).strip()
        if not chat_id:
            return False
            
        if chat_id.startswith("-100") and chat_id[1:].isdigit():
            return True
        elif chat_id.startswith("-") and chat_id[1:].isdigit():
            return True
        elif chat_id.isdigit():
            return True
        elif chat_id.startswith("@") and len(chat_id) > 1:
            return True
            
        return False

    @lru_cache(maxsize=100)
    async def get_topic_info(self, chat_id, topic_id):
        cache_key = f"{chat_id}_{topic_id}"
        if cache_key in self.topic_cache:
            return self.topic_cache[cache_key]
            
        try:
            if topic_id == 1:
                result = "General"
            else:
                chat = await self.client.get_entity(chat_id)
                offset_id = 0
                result = f"Topic #{topic_id}"
                
                while True:
                    msgs = await self.client.get_messages(chat, limit=1000, offset_id=offset_id)
                    if not msgs:
                        break
                    for msg in msgs:
                        if msg and msg.id == topic_id and hasattr(msg, "action") and isinstance(msg.action, MessageActionTopicCreate):
                            result = msg.action.title
                            break
                    offset_id = msgs[-1].id
                    await asyncio.sleep(0.05)
                    
            self.topic_cache[cache_key] = result
            return result
        except Exception as e:
            logger.error(f"Topic info error: {e}")
            return f"Topic #{topic_id}"

    async def safe_iter_messages(self, chat, count, topic_id=None):
        messages = []
        batch_size = self.config["batch_size"]
        
        try:
            kwargs = {"limit": None}
            
            if topic_id is not None and topic_id != "":
                kwargs["reply_to"] = topic_id
                
            collected = 0
            batch = []
            
            async for msg in self.client.iter_messages(chat, **kwargs):
                if msg and (msg.text or msg.media):
                    batch.append(msg)
                    collected += 1
                    
                    if len(batch) >= batch_size:
                        messages.extend(batch)
                        batch = []
                        await asyncio.sleep(0.05)
                        
                    if collected >= count:
                        break
                        
            messages.extend(batch)
                        
        except Exception as e:
            logger.error(f"Safe iter messages error: {e}")
            
        return messages[:count]

    async def smart_download_with_retry(self, message, index, session_dir, stats, max_retries=None):
        if max_retries is None:
            max_retries = self.config["max_retries"]
            
        saved_items = []
        
        if not message:
            stats["errors"] += 1
            return saved_items
        
        for attempt in range(max_retries + 1):
            try:
                if message.media:
                    if isinstance(message.media, MessageMediaPhoto):
                        file_bytes = await self.client.download_media(message, bytes)
                        saved_items.append({
                            "type": "photo_buffer", 
                            "data": file_bytes, 
                            "caption": getattr(message, "text", "") or ""
                        })
                        stats["photos"] += 1
                        stats["buffered"] += 1
                        
                    elif isinstance(message.media, MessageMediaDocument):
                        doc = message.media.document
                        file_size = getattr(doc, 'size', 0)
                        small_file_limit = self.config["small_file_limit"] * 1024 * 1024
                        
                        original_name = None
                        original_extension = ""
                        
                        for attr in doc.attributes:
                            if hasattr(attr, "file_name") and attr.file_name:
                                original_name = attr.file_name
                                if '.' in original_name:
                                    original_extension = original_name[original_name.rfind('.'):]
                                break
                        
                        if not original_name:
                            base_name = f"file_{uuid.uuid4().hex[:8]}"
                            
                            if doc.mime_type:
                                mime_extensions = {
                                    "text/plain": ".txt",
                                    "text/python": ".py", 
                                    "application/x-python-code": ".py",
                                    "text/x-python": ".py",
                                    "application/x-sh": ".sh",
                                    "text/x-shellscript": ".sh",
                                    "application/zip": ".zip",
                                    "application/x-rar-compressed": ".rar",
                                    "application/x-7z-compressed": ".7z",
                                    "application/x-tar": ".tar",
                                    "application/gzip": ".gz",
                                    "application/pdf": ".pdf",
                                    "application/msword": ".doc",
                                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
                                    "application/vnd.ms-excel": ".xls",
                                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".xlsx",
                                    "application/json": ".json",
                                    "application/xml": ".xml",
                                    "text/xml": ".xml",
                                    "text/html": ".html",
                                    "text/css": ".css",
                                    "application/javascript": ".js",
                                    "text/javascript": ".js",
                                    "image/jpeg": ".jpg",
                                    "image/png": ".png",
                                    "image/gif": ".gif",
                                    "image/webp": ".webp",
                                    "image/svg+xml": ".svg",
                                    "video/mp4": ".mp4",
                                    "video/avi": ".avi",
                                    "video/mkv": ".mkv",
                                    "video/webm": ".webm",
                                    "audio/mpeg": ".mp3",
                                    "audio/wav": ".wav",
                                    "audio/ogg": ".ogg",
                                    "audio/flac": ".flac",
                                }
                                
                                extension = mime_extensions.get(doc.mime_type, "")
                                if not extension:
                                    if "/" in doc.mime_type:
                                        subtype = doc.mime_type.split("/")[1]
                                        if subtype and not subtype.startswith("x-"):
                                            extension = f".{subtype}"
                                        
                                original_name = base_name + extension
                            else:
                                original_name = base_name + ".bin"
                        
                        if file_size < small_file_limit:
                            file_bytes = await self.client.download_media(message, bytes)
                            
                            saved_items.append({
                                "type": "document_buffer",
                                "data": file_bytes,
                                "filename": original_name,
                                "caption": getattr(message, "text", "") or ""
                            })
                            stats["documents"] += 1
                            stats["buffered"] += 1
                        else:
                            name_parts = os.path.splitext(original_name)
                            if len(name_parts) == 2:
                                unique_name = f"{name_parts[0]}_{uuid.uuid4().hex[:4]}{name_parts[1]}"
                            else:
                                unique_name = f"{original_name}_{uuid.uuid4().hex[:4]}"
                            
                            filepath = os.path.join(session_dir, unique_name)
                            await self.client.download_media(message, file=filepath)
                            saved_items.append({
                                "type": "document", 
                                "path": filepath,
                                "filename": original_name,
                                "caption": getattr(message, "text", "") or ""
                            })
                            stats["documents"] += 1
                        
                elif message.text:
                    saved_items.append({"type": "text", "text": message.text})
                    stats["text"] += 1
                    
                return saved_items
                
            except Exception as e:
                error_msg = str(e)
                if attempt < max_retries:
                    logger.warning(f"Download attempt {attempt + 1}/{max_retries + 1} failed: {error_msg}")
                    delay = min(1.5 ** attempt + random.uniform(0, 0.5), 8)
                    await asyncio.sleep(delay)
                else:
                    logger.error(f"Download failed after {max_retries + 1} attempts: {error_msg}")
                    stats["errors"] += 1
                    
                    if message.text:
                        saved_items.append({"type": "text", "text": message.text})
                        stats["text"] += 1
                    else:
                        saved_items.append({"type": "text", "text": f"⚠️ Failed to download media: {error_msg}"})
                        stats["text"] += 1
                        
                    break
                    
        return saved_items

    async def optimized_send_content(self, saved_items, target_chat, target_topic_id=None, progress_msg=None, stats=None):
        send_semaphore = asyncio.Semaphore(self.config["send_concurrency"])
        sent_count = 0
        total = len(saved_items)
        lock = asyncio.Lock()
        start_time = time.time()
        last_update_time = 0
        flood_wait_count = 0

        async def update_progress(force=False):
            nonlocal last_update_time
            
            current_time = time.time()
            
            if not force and (current_time - last_update_time) < 0.8:
                return
                
            if not progress_msg:
                return
                
            elapsed = current_time - start_time
            
            if elapsed > 0 and sent_count > 0:
                speed = (sent_count / elapsed) * 60
                eta_seconds = (total - sent_count) / (sent_count / elapsed) if sent_count > 0 else 0
                eta_str = self.format_time(eta_seconds) if eta_seconds < 3600 else "∞"
            else:
                speed = 0
                eta_str = "вычисляется..."
                
            progress_text = self.strings("progress_update").format(
                sent_count, total, speed, eta_str, flood_wait_count
            )
            
            try:
                await progress_msg.edit(progress_text)
                last_update_time = current_time
            except Exception as e:
                logger.error(f"Failed to update progress: {e}")

        async def send_with_flood_protection(item):
            nonlocal sent_count, flood_wait_count
            
            async with send_semaphore:
                max_retries = self.config["max_retries"]
                
                for attempt in range(max_retries + 1):
                    start_send_time = time.time()
                    temp_file_path = None
                    
                    try:
                        reply_to_param = None
                        if target_topic_id and target_topic_id != 1:
                            reply_to_param = target_topic_id
                            
                        if item["type"] == "text":
                            await self.client.send_message(
                                target_chat,
                                item["text"],
                                reply_to=reply_to_param
                            )
                            
                        elif item["type"] == "photo_buffer":
                            temp_file_path = os.path.join(tempfile.gettempdir(), f"photo_{uuid.uuid4().hex[:8]}.jpg")
                            with open(temp_file_path, 'wb') as f:
                                f.write(item["data"])
                            
                            await self.client.send_file(
                                target_chat,
                                temp_file_path,
                                caption=item["caption"],
                                reply_to=reply_to_param
                            )
                            
                        elif item["type"] == "document_buffer":
                            filename = item.get("filename", "unnamed.bin")
                            temp_file_path = os.path.join(tempfile.gettempdir(), f"temp_{uuid.uuid4().hex[:8]}_{filename}")
                            
                            with open(temp_file_path, 'wb') as f:
                                f.write(item["data"])
                            
                            await self.client.send_file(
                                target_chat,
                                temp_file_path,
                                caption=item["caption"],
                                file_name=filename,
                                attributes=[DocumentAttributeFilename(file_name=filename)],
                                reply_to=reply_to_param
                            )
                            
                        elif item["type"] == "document":
                            if os.path.exists(item["path"]):
                                filename = item.get("filename")
                                send_params = {
                                    "entity": target_chat,
                                    "file": item["path"], 
                                    "caption": item.get("caption", ""),
                                    "reply_to": reply_to_param
                                }
                                
                                if filename:
                                    send_params["file_name"] = filename
                                    send_params["attributes"] = [DocumentAttributeFilename(file_name=filename)]
                                
                                await self.client.send_file(**send_params)
                                
                                try:
                                    os.remove(item["path"])
                                except Exception:
                                    pass
                                    
                        elif item["type"] == "photo":
                            if os.path.exists(item["path"]):
                                await self.client.send_file(
                                    target_chat,
                                    item["path"],
                                    caption=item.get("caption", ""),
                                    reply_to=reply_to_param
                                )
                                try:
                                    os.remove(item["path"])
                                except Exception:
                                    pass
                        
                        if temp_file_path and os.path.exists(temp_file_path):
                            try:
                                os.remove(temp_file_path)
                            except Exception:
                                pass
                        
                        response_time = time.time() - start_send_time
                        self.delay_controller.record_response_time(response_time)
                        
                        async with lock:
                            sent_count += 1
                            await update_progress()
                        
                        await self.delay_controller.wait()
                        break
                        
                    except errors.FloodWaitError as e:
                        if temp_file_path and os.path.exists(temp_file_path):
                            try:
                                os.remove(temp_file_path)
                            except Exception:
                                pass
                                
                        flood_wait_count += 1
                        self.delay_controller.record_flood_wait()
                        wait_time = min(e.seconds + random.uniform(0.5, 1.5), 60)
                        logger.warning(f"FloodWait: sleeping {wait_time:.1f} sec")
                        await asyncio.sleep(wait_time)
                        continue
                        
                    except Exception as e:
                        if temp_file_path and os.path.exists(temp_file_path):
                            try:
                                os.remove(temp_file_path)
                            except Exception:
                                pass
                                
                        if attempt < max_retries:
                            logger.warning(f"Send attempt {attempt + 1}/{max_retries + 1} failed: {e}")
                            delay = min(1.5 ** attempt + random.uniform(0, 0.3), 5)
                            await asyncio.sleep(delay)
                        else:
                            logger.error(f"Send failed after {max_retries + 1} attempts: {e}")
                            if stats:
                                stats["errors"] += 1
                            break

        if progress_msg:
            try:
                initial_text = self.strings("progress_update").format(0, total, 0, "вычисляется...", 0)
                await progress_msg.edit(initial_text)
            except Exception as e:
                logger.error(f"Failed to set initial progress: {e}")

        await asyncio.gather(*[send_with_flood_protection(item) for item in saved_items])
        
        if stats:
            stats["flood_wait_handled"] = flood_wait_count
            
        await update_progress(force=True)
        return sent_count

    @loader.command(
        ru_doc="Оптимизированная пересылка с мягкой защитой.",
        de_doc="Optimized message forwarding.",
    )
    async def fh(self, message: Message):
        """Optimized forward messages from a channel or topic."""
        args = utils.get_args_raw(message)
        prefix = self.get_prefix()
        help_text = self.strings("help").format(prefix=prefix)
        
        if not args:
            await utils.answer(message, self.strings("invalid_args").format(help=help_text))
            return
            
        try:
            parts = args.strip().split()
            if len(parts) == 2:
                chat_id_str, count_str = parts
                topic_id = None
            elif len(parts) == 3:
                chat_id_str, topic_str, count_str = parts
                try:
                    if topic_str.lower() == "general":
                        topic_id = 1
                    else:
                        topic_id = int(topic_str)
                        if topic_id <= 0:
                            await utils.answer(message, self.strings("invalid_args").format(help=help_text))
                            return
                except ValueError:
                    await utils.answer(message, self.strings("invalid_args").format(help=help_text))
                    return
            else:
                await utils.answer(message, self.strings("invalid_args").format(help=help_text))
                return

            if not self.validate_chat_id(chat_id_str):
                await utils.answer(message, self.strings("invalid_chat_id"))
                return
                
            try:
                count = int(count_str)
                if count <= 0:
                    await utils.answer(message, self.strings("invalid_count"))
                    return
            except ValueError:
                await utils.answer(message, self.strings("invalid_count"))
                return

            current_topic_id = None
            if hasattr(message, 'reply_to') and message.reply_to:
                current_topic_id = message.reply_to.reply_to_top_id or message.reply_to.reply_to_msg_id

            if count >= 100:
                warning_msg = await utils.answer(
                    message, 
                    self.strings("large_count_warning").format(count=count)
                )
                await asyncio.sleep(1)
            
            initial_msg_key = "processing_topic" if topic_id else "processing"
            progress_msg = await utils.answer(
                message,
                self.strings(initial_msg_key).format(count),
            )
            
            start_time = time.time()
            session_dir = None
            stats = defaultdict(int)
            
            try:
                if chat_id_str.lstrip("-").isdigit():
                    chat_id = int(chat_id_str)
                else:
                    chat_id = chat_id_str
                    
                source_chat = await self.client.get_entity(chat_id)
                
            except Exception as e:
                await utils.answer(progress_msg, self.strings("chat_not_found"))
                logger.error(f"Chat not found: {e}")
                return

            try:
                messages = await self.safe_iter_messages(source_chat, count, topic_id)
            except Exception as e:
                txt = self.strings("topic_not_found").format(topic_id) if topic_id else self.strings("chat_not_found")
                await utils.answer(progress_msg, txt)
                logger.error(f"Message fetch error: {e}")
                return

            if not messages:
                await utils.answer(progress_msg, self.strings("no_messages"))
                return

            messages.reverse()
            session_dir = tempfile.mkdtemp(prefix="fh_rel_", suffix="_" + uuid.uuid4().hex[:6])
            all_saved_items = []
            
            download_semaphore = asyncio.Semaphore(self.config["download_concurrency"])
            
            async def download_batch(batch):
                tasks = []
                for i, msg in enumerate(batch, 1):
                    async def download_one(message, idx):
                        async with download_semaphore:
                            return await self.smart_download_with_retry(message, idx, session_dir, stats)
                    tasks.append(download_one(msg, i))
                return await asyncio.gather(*tasks)
            
            batch_size = min(self.config["batch_size"], len(messages))
            for i in range(0, len(messages), batch_size):
                batch = messages[i:i + batch_size]
                batch_results = await download_batch(batch)
                
                for result in batch_results:
                    all_saved_items.extend(result)
                
                if i % (batch_size * 2) == 0:
                    await self.cleanup_memory()
                    
                await asyncio.sleep(0.02)

            sent_count = await self.optimized_send_content(
                all_saved_items, message.chat_id, current_topic_id, progress_msg, stats
            )

            end_time = time.time()
            total_time = self.format_time(end_time - start_time)
            avg_speed = (sent_count / (end_time - start_time)) * 60 if (end_time - start_time) > 0 else 0
            
            if topic_id:
                topic_name = await self.get_topic_info(chat_id, topic_id)
                final_msg = self.strings("success_topic").format(
                    sent_count, topic_name, stats["text"], stats["photos"], 
                    stats["documents"], stats.get("buffered", 0), stats.get("flood_wait_handled", 0),
                    stats["errors"], total_time, avg_speed
                )
            else:
                final_msg = self.strings("success").format(
                    sent_count, stats["text"], stats["photos"], 
                    stats["documents"], stats.get("buffered", 0), stats.get("flood_wait_handled", 0),
                    stats["errors"], total_time, avg_speed
                )
                
            await progress_msg.edit(final_msg)
                
        except Exception as e:
            logger.error(f"FH general error: {e}")
            await utils.answer(message, self.strings("error").format(str(e)))
        finally:
            if session_dir:
                freed_mb = await self.cleanup_memory(session_dir)
                if freed_mb > 5:
                    logger.info(f"Session cleanup: freed {freed_mb:.1f}MB")

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
            if not self.validate_chat_id(chat_id):
                await utils.answer(message, self.strings("invalid_chat_id"))
                return
                
            if chat_id.lstrip("-").isdigit():
                chat_id = int(chat_id)
                
            chat = await self.client.get_entity(chat_id)
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
                chat_id=args.strip(),
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
                if not entity:
                    continue
                    
                chat_id = entity.id
                title = getattr(entity, "title", "Unknown")
                protected = "🔒" if getattr(entity, "noforwards", False) else ""
                topics_mark = "🧵" if getattr(entity, "forum", False) else ""
                
                if getattr(entity, "broadcast", False):
                    channels.append(f"📢 <code>{chat_id}</code> — {title} {protected}")
                elif getattr(entity, "megagroup", False):
                    groups.append(f"👥 <code>{chat_id}</code> — {title} {protected}{topics_mark}")

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
