# Название: PMNotifier
# Описание: Уведомляет о новых личных сообщениях и сохраняет исчезающие фото/видео
# Команды: load, pmroff, pmignore, pmmedia
# meta developer: @kelovo
# scope: heroku_only
# version: 2.0.0

__version__ = (2, 0, 0)

from telethon.tl.types import Message, InputMediaUploadedPhoto, InputMediaUploadedDocument
import os
import asyncio
from aiogram.exceptions import TelegramForbiddenError
from collections import defaultdict

from .. import loader, utils

@loader.tds
class PMNotifierMod(loader.Module):
    """Уведомляет о новых личных сообщениях и сохраняет исчезающие фото/видео"""

    strings = {
        "name": "PMNotifier",
        "pm_notification": (
            "<b>✉️ Новое сообщение от <a href=\"tg://openmessage?user_id={}\">{}</a></b>\n"
            "<code>Текст:</code>\n<code>{}</code>"
        ),
        "media_notification": (
            "<b>✉️ Новое медиа от <a href=\"tg://openmessage?user_id={}\">{}</a></b>\n"
            "<code>Текст:</code>\n<code>{}</code>"
        ),
        "grouped_notification": (
            "<b>✉️ {} сообщений от <a href=\"tg://openmessage?user_id={}\">{}</a></b>\n"
            "<code>Текст:</code>\n<code>{}</code>"
        ),
        "no_media": "🚫 Медиа не найдено в ответном сообщении или не прикреплено.",
        "ttl_set": "✅ Исчезающее медиа отправлено с TTL {} секунд!",
        "invalid_ttl": "❌ Укажите корректное время жизни (1-60 секунд).",
        "media_not_supported": "❌ Этот тип медиа не поддерживается для исчезающих сообщений.",
        "chat_access_denied": "❌ Бот не может отправить сообщение в указанный чат. Убедитесь, что бот добавлен в чат или пользователь начал диалог с ботом.",
        "module_toggled": "✅ PMNotifier {}",
        "chat_ignored": "✅ Чат {} добавлен в игнор-лист",
        "chat_unignored": "✅ Чат {} удалён из игнор-листа",
        "media_toggled": "✅ Сохранение медиа {}",
        "ignore_list": "📝 Игнор-лист:\n{}",
        "no_ignored": "ℹ️ Игнор-лист пуст",
        "_cfg_doc_notification_chat_id": "ID чата, куда будут отправляться уведомления",
        "_cfg_doc_show_ttl_confirmation": "Показывать сообщение об успешной отправке исчезающего медиа",
        "_cfg_doc_auto_delete_media": "Автоматически удалять медиа после отправки",
        "_cfg_doc_message_delay": "Задержка перед объединением сообщений (секунд)",
        "_cfg_doc_message_group_count": "Количество сообщений для объединения",
    }

    strings_ru = strings

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "notification_chat_id",
                None,
                lambda: self.strings("_cfg_doc_notification_chat_id"),
                validator=loader.validators.Integer(),
            ),
            loader.ConfigValue(
                "show_ttl_confirmation",
                True,
                lambda: self.strings("_cfg_doc_show_ttl_confirmation"),
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "auto_delete_media",
                True,
                lambda: self.strings("_cfg_doc_auto_delete_media"),
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "message_delay",
                1.5,
                lambda: self.strings("_cfg_doc_message_delay"),
                validator=loader.validators.Float(minimum=0.5, maximum=10.0),
            ),
            loader.ConfigValue(
                "message_group_count",
                5,
                lambda: self.strings("_cfg_doc_message_group_count"),
                validator=loader.validators.Integer(minimum=2, maximum=20),
            )
        )
        self._enabled = True
        self._media_enabled = True
        self._ignore_list = set()
        self._message_buffer = defaultdict(list)
        self._message_timers = {}

    async def client_ready(self):
        pass

    async def _can_send_message(self, chat_id):
        try:
            await self.inline.bot.get_chat(chat_id)
            return True
        except TelegramForbiddenError:
            return False

    async def _flush_buffer(self, user_id):
        if user_id not in self._message_buffer or not self._message_buffer[user_id]:
            return

        messages = self._message_buffer[user_id]
        del self._message_buffer[user_id]
        del self._message_timers[user_id]

        if not messages:
            return

        sender = await self._client.get_entity(user_id)
        sender_name = utils.escape_html(sender.first_name or "Неизвестный")

        if len(messages) == 1:
            message_text = utils.escape_html(messages[0].raw_text or "Без текста")
            notification = self.strings("pm_notification").format(
                user_id, sender_name, message_text
            )
        else:
            message_text = "\n".join(
                f"{i+1}. {utils.escape_html(msg.raw_text or 'Без текста')}"
                for i, msg in enumerate(messages)
            )
            notification = self.strings("grouped_notification").format(
                len(messages), user_id, sender_name, message_text
            )

        if await self._can_send_message(self.config["notification_chat_id"]):
            await self.inline.bot.send_message(
                self.config["notification_chat_id"],
                text=notification,
                parse_mode="HTML",
            )

    async def _schedule_flush(self, user_id):
        if user_id in self._message_timers:
            self._message_timers[user_id].cancel()

        self._message_timers[user_id] = asyncio.create_task(
            self._flush_after_delay(user_id)
        )

    async def _flush_after_delay(self, user_id):
        await asyncio.sleep(self.config["message_delay"])
        await self._flush_buffer(user_id)

    async def watcher(self, message: Message):
        if (not self._enabled or
            not message.is_private or
            message.out or
            not self.config["notification_chat_id"] or
            message.sender_id in self._ignore_list):
            return

        if not message.media and self.config["message_group_count"] > 1:
            self._message_buffer[message.sender_id].append(message)

            if len(self._message_buffer[message.sender_id]) >= self.config["message_group_count"]:
                await self._flush_buffer(message.sender_id)
            else:
                await self._schedule_flush(message.sender_id)
            return

        if message.media and not self._media_enabled:
            self._message_buffer[message.sender_id].append(message)
            await self._schedule_flush(message.sender_id)
            return

        sender = await self._client.get_entity(message.sender_id)
        sender_name = utils.escape_html(sender.first_name or "Неизвестный")
        message_text = utils.escape_html(message.raw_text or "Без текста")

        if message.media and self._media_enabled:
            try:
                media_path = await message.download_media()
                if not media_path:
                    return

                if message.photo:
                    media = InputMediaUploadedPhoto(file=await self._client.upload_file(media_path))
                elif message.video:
                    media = InputMediaUploadedDocument(
                        file=await self._client.upload_file(media_path),
                        mime_type="video/mp4",
                        attributes=[message.media.document.attributes[-1]]
                    )
                else:
                    if self.config["auto_delete_media"] and os.path.exists(media_path):
                        os.remove(media_path)
                    return

                await self._client.send_message(
                    self.config["notification_chat_id"],
                    message=self.strings("media_notification").format(
                        sender.id,
                        sender_name,
                        message_text,
                    ),
                    file=media,
                    parse_mode="HTML",
                )

                if self.config["auto_delete_media"] and os.path.exists(media_path):
                    os.remove(media_path)
            except Exception as e:
                if await self._can_send_message(self.config["notification_chat_id"]):
                    await self.inline.bot.send_message(
                        self.config["notification_chat_id"],
                        text=self.strings("pm_notification").format(
                            sender.id,
                            sender_name,
                            f"{message_text}\n[Ошибка загрузки медиа: {str(e)}]"
                        ),
                        parse_mode="HTML",
                    )
        else:
            if await self._can_send_message(self.config["notification_chat_id"]):
                await self.inline.bot.send_message(
                    self.config["notification_chat_id"],
                    text=self.strings("pm_notification").format(
                        sender.id,
                        sender_name,
                        message_text,
                    ),
                    parse_mode="HTML",
                )

    @loader.command(ru_doc="Отправляет исчезающее фото/видео")
    async def load(self, message):
        """Отправляет исчезающее фото/видео. Ответьте на медиа или прикрепите файл. Пример: .load (ответ на сообщение)"""
        args = utils.get_args_raw(message)
        ttl = int(args) if args and args.isdigit() else 30

        await message.delete()

        if not await self._can_send_message(self.config["notification_chat_id"]):
            if await self._can_send_message(message.chat_id):
                await self.inline.bot.send_message(
                    message.chat_id,
                    text=self.strings("chat_access_denied"),
                    parse_mode="HTML"
                )
            return

        if not (1 <= ttl <= 60):
            if await self._can_send_message(message.chat_id):
                await self.inline.bot.send_message(
                    message.chat_id,
                    text=self.strings("invalid_ttl"),
                    parse_mode="HTML"
                )
            return

        reply = await message.get_reply_message()
        media_path = None

        if reply and reply.media:
            media_path = await reply.download_media()
        elif message.media:
            media_path = await message.download_media()

        if not media_path:
            if await self._can_send_message(message.chat_id):
                await self.inline.bot.send_message(
                    message.chat_id,
                    text=self.strings("no_media"),
                    parse_mode="HTML"
                )
            return

        try:
            is_photo = (message.photo or (reply and reply.photo))
            is_video = (message.video or (reply and reply.video))

            if not (is_photo or is_video):
                if await self._can_send_message(message.chat_id):
                    await self.inline.bot.send_message(
                        message.chat_id,
                        text=self.strings("media_not_supported"),
                        parse_mode="HTML"
                    )
                if self.config["auto_delete_media"] and os.path.exists(media_path):
                    os.remove(media_path)
                return

            if is_photo:
                media = InputMediaUploadedPhoto(
                    file=await self._client.upload_file(media_path),
                    ttl_seconds=ttl
                )
            else:
                media = InputMediaUploadedDocument(
                    file=await self._client.upload_file(media_path),
                    mime_type="video/mp4",
                    attributes=[message.media.document.attributes[-1] if message.video else reply.media.document.attributes[-1]],
                    ttl_seconds=ttl
                )

            await self._client.send_message(
                self.config["notification_chat_id"],
                file=media,
                parse_mode="HTML",
            )

            if self.config["auto_delete_media"] and os.path.exists(media_path):
                os.remove(media_path)

            if self.config["show_ttl_confirmation"] and await self._can_send_message(message.chat_id):
                await self.inline.bot.send_message(
                    message.chat_id,
                    text=self.strings("ttl_set").format(ttl),
                    parse_mode="HTML"
                )
        except TelegramForbiddenError:
            if await self._can_send_message(message.chat_id):
                await self.inline.bot.send_message(
                    message.chat_id,
                    text=self.strings("chat_access_denied"),
                    parse_mode="HTML"
                )
            if self.config["auto_delete_media"] and media_path and os.path.exists(media_path):
                os.remove(media_path)
        except Exception as e:
            if await self._can_send_message(message.chat_id):
                await self.inline.bot.send_message(
                    message.chat_id,
                    text=f"❌ Ошибка: {str(e)}",
                    parse_mode="HTML"
                )
            if self.config["auto_delete_media"] and media_path and os.path.exists(media_path):
                os.remove(media_path)

    @loader.command(ru_doc="Включить/выключить PMNotifier")
    async def pmnoff(self, message):
        """Включить/выключить PMNotifier"""
        self._enabled = not self._enabled
        status = "включен" if self._enabled else "выключен"
        await utils.answer(message, self.strings("module_toggled").format(status))

    @loader.command(ru_doc="Добавить/удалить чат из игнора")
    async def pmnignore(self, message):
        """Добавить/удалить чат из игнора. Ответьте на сообщение или укажите ID"""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()

        chat_id = None
        if reply:
            chat_id = reply.sender_id
        elif args and args.isdigit():
            chat_id = int(args)
        elif message.is_private:
            chat_id = message.sender_id

        if not chat_id:
            await utils.answer(message, "❌ Укажите ID чата или ответьте на сообщение")
            return

        if chat_id in self._ignore_list:
            self._ignore_list.remove(chat_id)
            await utils.answer(message, self.strings("chat_unignored").format(chat_id))
        else:
            self._ignore_list.add(chat_id)
            await utils.answer(message, self.strings("chat_ignored").format(chat_id))

    @loader.command(ru_doc="Включить/выключить сохранение медиа")
    async def pmnmedia(self, message):
        """Включить/выключить сохранение медиа"""
        self._media_enabled = not self._media_enabled
        status = "включено" if self._media_enabled else "выключено"
        await utils.answer(message, self.strings("media_toggled").format(status))

    @loader.command(ru_doc="Показать игнор-лист")
    async def pmlist(self, message):
        """Показать игнор-лист"""
        if not self._ignore_list:
            await utils.answer(message, self.strings("no_ignored"))
            return

        ignored_list = "\n".join(f"• <code>{chat_id}</code>" for chat_id in self._ignore_list)
        await utils.answer(message, self.strings("ignore_list").format(ignored_list))
