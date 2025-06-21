
#  This file is part of SenkoGuardianModules
#  Copyright (c) 2025 Senko
#  This software is released under the MIT License.
#  https://opensource.org/licenses/MIT

__version__ = (5, 8, 0) #Новые улучшения!

# meta developer: @SenkoGuardianModules


#  .------. .------. .------. .------. .------. .------.
#  |S.--. | |E.--. | |N.--. | |M.--. | |O.--. | |D.--. |
#  | :/\: | | :/\: | | :(): | | :/\: | | :/\: | | :/\: |
#  | :\/: | | :\/: | | ()() | | :\/: | | :\/: | | :\/: |
#  | '--'S| | '--'E| | '--'N| | '--'M| | '--'O| | '--'D|
#  `------' `------' `------' `------' `------' `------'


import asyncio
import json
from datetime import datetime, timedelta
from telethon.utils import get_display_name
import logging
import random
import re

from typing import Optional, Tuple
from telethon import errors, utils as telethon_utils
from telethon.tl import types as tl_types
from telethon.utils import get_peer_id as telethon_get_peer_id

from .. import loader, utils

logger = logging.getLogger(__name__)

class SpecificWarningFilter(logging.Filter):
    def filter(self, record):
        if record.name == 'hikkatl.hikkatl.client.users' and \
           'PersistentTimestampOutdatedError' in record.getMessage() and \
           'GetChannelDifferenceRequest' in record.getMessage():
            return False
        return True

@loader.tds
class MaillingChatGT99(loader.Module):
    """Модуль для массовой рассылки сообщений по чатам v5.8.0 (Поддерживает все типы сообщений (кроме цитат))"""
    strings = {
        "name": "MaillingChatGT99",
        "add_chat": "➕ Добавить текущий чат/тему. Используйте .add_chat или .add_chat <ID/Username/Ссылка> (Можно сразу несколько ссылкок в 1 комманду).",
        "remove_chat": "🗑️ Удалить чат/тему по номеру из списка. Используйте .remove_chat <номер>.",
        "list_chats": "📜 Показать список чатов/тем для рассылки.",
        "add_msg": "➕ Добавить сообщение (ответом).",
        "remove_msg": "➖ Удалить сообщение по номеру. Используйте .remove_msg <номер>.",
        "clear_msgs": "🗑️ Очистить список сообщений.",
        "list_msgs": "📜 Показать список сообщений для рассылки.",
        "set_seller": "⚙️ Установить ID чата/пользователя продавца для уведомлений. Используйте .set_seller <ID/Username/Ссылка/'me'>.",
        "mail_status": "📊 Показать статус рассылки.",
        "start_mail": "🚀 Запустить рассылку. Использование: .start_mail <время_сек> <интервал_цикла_от-до_сек>.",
        "stop_mail": "⏹️ Остановить рассылку.",
        "error_getting_entity": "⚠️ Не удалось получить информацию о чате/сущности: {}",
        "error_sending_message": "⚠️ Ошибка при отправке сообщения ({}) в чат {} ({}): {}",
        "notification_sent": "✅ Уведомление отправлено.",
        "invalid_arguments": "⚠️ Неверные аргументы.",
        "chats_empty": "⚠️ Сначала добавьте чаты.",
        "messages_empty": "⚠️ Сначала добавьте сообщения.",
        "already_running": "⚠️ Рассылка уже запущена.",
        "started_mailing": "✅ Рассылка начата.\n⏳ Общее время: {} сек.\n⏱️ Интервал между циклами: {}-{} сек.\n⏱️ Интервал между чатами: ~{}-{} сек\n⏱️ Интервал между сообщениями в чате: ~{}-{} сек",
        "stopped_mailing": "✅ Рассылка остановлена.",
        "not_running": "⚠️ Рассылка не активна.",
        "chat_added": "✅ Чат/тема '{}' добавлен в список рассылки.",
        "chat_already_added": "⚠️ Чат/тема '{}' уже в списке.",
        "chat_removed": "✅ #{} '{}' удален из списка рассылки.",
        "invalid_chat_selection": "⛔️ Неверный номер чата.",
        "chats_cleared": "✅ Все чаты удалены из списка.",
        "messages_cleared": "✅ Список сообщений очищен.",
        "no_chats": "📃 Список чатов пуст.",
        "no_messages": "✍️ Ответьте на сообщение, чтобы добавить его в список. Список сообщений пуст.",
        "message_added": "✅ Сообщение добавлено (Snippet: {}).",
        "message_removed": "✅ Сообщение №{} удалено (Snippet: {}).",
        "invalid_message_number": "✍️ Укажите корректный номер сообщения.",
        "seller_set": "✅ Установлен чат продавца.",
        "duration_invalid": "✍️ Использование: .start_mail <время_сек> <интервал_цикла_от-до_сек>. Укажите целое число для времени и интервал между циклами (например: 45-70).",
        "seller_notification": "Автоматическое уведомление: рассылка завершена",
        "mailing_complete": "✅ Рассылка завершена!",
        "safe_mode_enabled": "🟢 <b>Безопасный режим ВКЛЮЧЁН</b>\n• Только группы/каналы\n• Макс {} чатов/цикл\n• Интервал между чатами: ~{}-{} сек\n• Интервал между циклами: ~{}-{} сек\n• Интервал между сообщениями в чате: ~{}-{} сек",
        "safe_mode_disabled": "🔴 <b>Безопасный режим ВЫКЛЮЧЕН</b>",
        "mail_not_running": "⚠️ Рассылка не активна.",
        "no_permission": "️️️️️️️️️️️️⚠️ Нет прав на отправку в чат {} ({}), пропускаем.",
        "processing_entity": "⏳ Обработка сущности...",
        "failed_to_send_message": "⚠️ Не удалось отправить сообщение {} в чат {}. Причина: {}",
        "failed_perm_check": "⚠️ Не удалось проверить права в чатe {} ({}) из-за ошибки: {}. Пропускаем.",
        "permission_denied_skip": "🚫 Пропуск чата {} (ID: {}, Topic: {}) из-за отсутствия прав на отправку. Причина: {}",

        "cfg_safe_mode": "Включить безопасный режим (Отправка только по группам/каналам, больше задержка)",
        "cfg_max_chats_safe": "Максимальное кол-во чатов за цикл в безопасном режиме",
        "cfg_chats_interval": "Интервал между чатами (сек, от-до). Пример: 2,5",
        "cfg_safe_chats_interval": "Интервал между чатами в БЕЗОПАСНОМ режиме (сек, от-до). Пример: 10,20",
        "cfg_safe_cycle_interval": "Интервал между циклами в БЕЗОПАСНОМ режиме (сек, от-до). Пример: 180,300",
        "cfg_safe_message_interval": "Интервал между сообщениями в 1 чат в БЕЗОПАСНОМ режиме (сек, от-до). Пример: 5,10",
        "cfg_message_interval": "Интервал между сообщениями в 1 чат (сек, от-до). Пример: 1,3",
        "cfg_delete_replies_delay": "⏱️ Задержка автоудаления для ответов команд (сек, 0 - не удалять)",
        "cfg_randomize_messages": "Рандомизировать сообщения (1 случайное сообщение на чат за цикл)",
        "add_chat_summary_title": "<b>Результаты добавления чатов:</b>\n\n",
        "add_chat_success_header": "<b>Добавлено:</b>\n",
        "add_chat_already_exists_header": "<b>Уже существуют:</b>\n",
        "add_chat_errors_header": "<b>Ошибки:</b>\n",
        "no_valid_chats_provided": "⚠️ Не предоставлено валидных идентификаторов чатов или произошли ошибки при их обработке.",
    }
    PERMISSION_ERRORS = {
        "ChatForbiddenError", "UserBannedInChannelError", "ChatWriteForbiddenError",
        "ChatAdminRequiredError", "UserBlocked", "TopicClosedError",
        "TopicEditedError", "ForumTopicDeletedError",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue("safe_mode", False, lambda: self.strings("cfg_safe_mode"), validator=loader.validators.Boolean()),
            loader.ConfigValue("max_chats_safe", 10, lambda: self.strings("cfg_max_chats_safe"), validator=loader.validators.Integer(minimum=1)),
            loader.ConfigValue("chats_interval", "2,5", lambda: self.strings("cfg_chats_interval"), validator=loader.validators.String()),
            loader.ConfigValue("safe_chats_interval", "10,20", lambda: self.strings("cfg_safe_chats_interval"), validator=loader.validators.String()),
            loader.ConfigValue("safe_cycle_interval", "180,300", lambda: self.strings("cfg_safe_cycle_interval"), validator=loader.validators.String()),
            loader.ConfigValue("safe_message_interval", "5,10", lambda: self.strings("cfg_safe_message_interval"), validator=loader.validators.String()),
            loader.ConfigValue("message_interval", "1,3", lambda: self.strings("cfg_message_interval"), validator=loader.validators.String()),
            loader.ConfigValue("delete_replies_delay", 5, lambda: self.strings("cfg_delete_replies_delay"), validator=loader.validators.Integer(minimum=0)),
            loader.ConfigValue("randomize_messages", False, lambda: self.strings("cfg_randomize_messages"), validator=loader.validators.Boolean()),
        )
        self.chats = {}
        self.messages = []
        self.mail_task: Optional[asyncio.Task] = None
        self.seller_chat_id: Optional[int] = None
        self.total_messages_sent = 0
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.is_running = False
        self.lock = asyncio.Lock()
        self._current_cycle_start_time: Optional[datetime] = None
        self._processed_chats_in_cycle = 0
        
        try:
            h_logger = logging.getLogger('hikkatl.hikkatl.client.users')
            if not any(isinstance(f, SpecificWarningFilter) for f in h_logger.filters):
                h_logger.addFilter(SpecificWarningFilter())
        except Exception as e:
            logger.error(f"Failed to apply SpecificWarningFilter: {e}")


    def _validate_interval_tuple(self, value, default_tuple: Tuple[float, float]) -> Tuple[float, float]:
        parsed_value = None
        if isinstance(value, str):
            parts = value.split(',')
            if len(parts) == 2:
                try:
                    v_min_str = float(parts[0].strip())
                    v_max_str = float(parts[1].strip())
                    parsed_value = (v_min_str, v_max_str)
                except (ValueError, TypeError): pass
        elif isinstance(value, (list, tuple)) and len(value) == 2:
            parsed_value = value
        if parsed_value:
            try:
                v_min = float(parsed_value[0])
                v_max = float(parsed_value[1])
                if 0 <= v_min <= v_max: return (v_min, v_max)
            except (ValueError, TypeError): pass
        return (float(default_tuple[0]), float(default_tuple[1]))

    async def config_changed(self):
        logger.info(f"{self.strings['name']} configuration updated.")

    async def _load_state(self):
        stored_chats_raw = self._db.get(self.strings["name"], "chats", {})
        self.chats = {}
        if isinstance(stored_chats_raw, dict):
            for key_str, name_val in stored_chats_raw.items():
                try:
                    if isinstance(key_str, str) and key_str.startswith("("):
                        match = re.match(r"\((\-?\d+),\s*(\d+|\s*None)\)", key_str)
                        if match:
                            chat_id, topic_str = int(match.group(1)), match.group(2).strip()
                            self.chats[(chat_id, int(topic_str) if topic_str.lower() != 'none' else None)] = name_val
                        else: logger.warning(f"Не удалось разобрать ключ чата: '{key_str}'.")
                    elif isinstance(key_str, (str, int, float)):
                        self.chats[(int(key_str), None)] = f"Chat {int(key_str)} (old list format)"
                    else: logger.warning(f"Неизвестный формат ключа чата: '{key_str}'.")
                except (ValueError, TypeError) as e: logger.warning(f"Ошибка обработки ключа '{key_str}': {e}")
        elif isinstance(stored_chats_raw, list): 
            for chat_id_old in stored_chats_raw:
                try: self.chats[(int(chat_id_old), None)] = f"Chat {int(chat_id_old)} (very old list format)"
                except: pass
        async with self.lock: self._db.set(self.strings["name"], "chats", {str(k):v for k,v in self.chats.items()})
        
        self.messages = self._db.get(self.strings["name"], "messages", [])
        self.messages = [m for m in self.messages if isinstance(m,dict) and all(k in m for k in ["id","chat_id","snippet"])]
        async with self.lock: self._db.set(self.strings["name"], "messages", self.messages)
        
        raw_seller_id = self._db.get(self.strings["name"], "seller_chat_id", None)
        if raw_seller_id:
            try: self.seller_chat_id = int(raw_seller_id)
            except (ValueError, TypeError): 
                self.seller_chat_id = None
                self._db.set(self.strings["name"], "seller_chat_id", None)
        else:
            self.seller_chat_id = None


    async def client_ready(self, client, db):
        self.client = client
        self._db = db
        await self._load_state()
        
    async def _edit_or_reply_and_handle_deletion(self, message_event, text: str, delay: Optional[int] = None):
        if delay is None:
            delay = self.config["delete_replies_delay"]

        processed_message = None
        can_edit = message_event and hasattr(message_event, "edit") and callable(message_event.edit)
        
        try:
            if can_edit:
                try:
                    if getattr(message_event, "deleted", False):
                        logger.debug(f"Сообщение {message_event.id} было удалено перед попыткой редактирования.")
                        can_edit = False 
                    else:
                        processed_message = await message_event.edit(text, parse_mode='html')
                except errors.MessageNotModifiedError:
                    processed_message = message_event 
                    logger.debug("Сообщение не было изменено (текст совпадает).")
                except errors.MessageIdInvalidError: 
                    can_edit = False 
                    logger.debug("Исходное сообщение для редактирования не найдено/удалено (MessageIdInvalidError).")
                except errors.RPCError as e: 
                    can_edit = False
                    logger.warning(f"RPC ошибка при попытке ({type(e).__name__}) редактировать {getattr(message_event, 'id', 'N/A')}: {e}. Попытка отправить новое.")
            
            if not processed_message or not can_edit: 
                logger.debug(f"Редактирование не удалось или было невозможно (can_edit={can_edit}, processed_message={bool(processed_message)}). Отправка нового ответа.")
                chat_to_reply = None
                if message_event and hasattr(message_event, "chat_id") and message_event.chat_id is not None: chat_to_reply = message_event.chat_id
                elif message_event and hasattr(message_event, "chat") and message_event.chat is not None: chat_to_reply = utils.get_peer_id(message_event.chat)
                
                if chat_to_reply:
                    processed_message = await self.client.send_message(chat_to_reply, text, parse_mode='html')
                else:
                    logger.error("Не удалось определить чат для отправки ответа, сообщение не будет отправлено.")
                    return 
        
        except Exception as e_edit_reply_outer: 
            logger.error(f"Критическая ошибка на этапе редактирования/отправки сообщения: {e_edit_reply_outer}")
            try:
                await self.client.send_message(self.client.tg_id, f"Ошибка обработки ответа, текст:\n{utils.escape_html(text[:1000])}", parse_mode='html')
            except Exception as e_tgid:
                logger.error(f"Не удалось отправить сообщение об ошибке даже в избранное: {e_tgid}")
            return 
         
        if not processed_message: 
            logger.debug("Нет сообщения для обработки (например, отправка не удалась или некуда было отправлять).")
            return

        if delay <= 0:
            logger.debug(f"Сообщение {processed_message.id} не будет удалено (delay={delay}).")
            return

        await asyncio.sleep(delay)

        try:
            if hasattr(processed_message, 'delete') and not getattr(processed_message, 'deleted', False):
                await processed_message.delete()
                logger.debug(f"Сообщение {processed_message.id} удалено.")
            elif getattr(processed_message, 'deleted', False):
                logger.debug(f"Сообщение {processed_message.id} уже было удалено (до нашего sleep).")
        except errors.MessageDeleteForbiddenError:
            logger.warning(f"Нет прав на удаление сообщения {processed_message.id}.")
        except Exception as e_del:
            logger.warning(f"Произошла ошибка при удалении сообщения {processed_message.id}: {e_del}")


    async def _resolve_entity_and_get_id(self, identifier):
        try:
            resolved_identifier = identifier
            if isinstance(identifier, str):
                if identifier.startswith('c/'):
                    resolved_identifier = int(identifier.split('/')[1])
                    if resolved_identifier > 0:
                         resolved_identifier = int(f"-100{resolved_identifier}") 
                else:
                    try: resolved_identifier = int(identifier)
                    except ValueError: pass
            elif isinstance(identifier, (int, float)):
                resolved_identifier = int(identifier)
            
            entity = await self.client.get_entity(resolved_identifier)
            return telethon_utils.get_peer_id(entity), entity
        except Exception as e:
            logger.error(f"Ошибка получения сущности для '{identifier}': {e}")
            return None, None

    @loader.command(ru_doc="➕ Добавить текущий чат/тему. Используйте .add_chat или .add_chat <ID/Username/Ссылка> (Можно сразу несколько ссылкок в 1 комманду).")
    async def add_chat(self, message):
        args_raw = utils.get_args_raw(message).strip()
        reply = await message.get_reply_message()
        source_context = reply or message

        identifiers_to_process_spec = []

        if args_raw:
            for ident_str in args_raw.split():
                identifiers_to_process_spec.append({"input_identifier": ident_str, "is_context_based": False})
        elif source_context and source_context.chat_id:
            identifiers_to_process_spec.append({"input_identifier": str(source_context.chat_id), "is_context_based": True})
        else:
            await self._edit_or_reply_and_handle_deletion(message, self.strings["invalid_arguments"] + " Укажите ID/username/ссылку или ответьте на сообщение.", 5)
            return

        await self._edit_or_reply_and_handle_deletion(message, self.strings["processing_entity"], delay=0)

        added_chats_msgs = []
        already_added_msgs = []
        error_msgs = []

        async with self.lock:
            for item_spec in identifiers_to_process_spec:
                identifier_input_str = item_spec["input_identifier"]
                is_context_based_lookup = item_spec["is_context_based"]
                
                chat_identifier_for_resolution = identifier_input_str
                current_target_topic_id = None

                if not is_context_based_lookup:
                    link_pattern = re.compile(r"https://t\.me/(?:c/)?([\w\d_.-]+)/(\d+)")
                    match = link_pattern.match(identifier_input_str)
                    if match:
                        parsed_chat_part = match.group(1)
                        try:
                            parsed_message_id = int(match.group(2))
                            chat_identifier_for_resolution = parsed_chat_part
                            current_target_topic_id = parsed_message_id
                            logger.debug(f"Parsed link: chat_identifier='{chat_identifier_for_resolution}', potential_topic_id='{current_target_topic_id}'")
                        except ValueError:
                            logger.warning(f"Could not parse message ID from link segment: {match.group(2)} in {identifier_input_str}")
                            chat_identifier_for_resolution = identifier_input_str 
                            current_target_topic_id = None
                elif is_context_based_lookup:
                    chat_identifier_for_resolution = str(source_context.chat_id) 
                    if hasattr(source_context, 'is_topic_message') and source_context.is_topic_message:
                        if source_context.reply_to and \
                           getattr(source_context.reply_to, 'forum_topic', False) and \
                           getattr(source_context.reply_to, 'reply_to_top_id', None) is not None:
                            current_target_topic_id = source_context.reply_to.reply_to_top_id
                        elif getattr(source_context, 'reply_to_top_id', None) is not None:
                            current_target_topic_id = source_context.reply_to_top_id
                        elif isinstance(source_context, tl_types.MessageService) and \
                             isinstance(source_context.action, tl_types.MessageActionTopicCreate):
                            current_target_topic_id = source_context.id
                        elif source_context.id:
                             current_target_topic_id = source_context.id
                    logger.debug(f"Context-based lookup: chat_identifier='{chat_identifier_for_resolution}', potential_topic_id='{current_target_topic_id}'")


                chat_id_resolved, entity = await self._resolve_entity_and_get_id(chat_identifier_for_resolution)

                if not entity or not chat_id_resolved:
                    error_msgs.append(f"• {self.strings['error_getting_entity'].format(utils.escape_html(str(identifier_input_str)))}")
                    continue

                target_chat_id = chat_id_resolved
                is_forum = isinstance(entity, tl_types.Channel) and getattr(entity, 'forum', False)
                
                if current_target_topic_id and not is_forum:
                    logger.info(f"A topic ID ({current_target_topic_id}) was determined for chat '{utils.escape_html(get_display_name(entity))}', but it's not a forum. Topic ID will be ignored.")
                    current_target_topic_id = None 

                chat_key = (target_chat_id, current_target_topic_id)

                if chat_key in self.chats:
                    already_added_msgs.append(f"• {self.strings['chat_already_added'].format(utils.escape_html(self.chats[chat_key]))}")
                    continue
                
                chat_name_display = utils.escape_html(get_display_name(entity))
                if current_target_topic_id and is_forum:
                    try:
                        topic_info_msg_obj = None
                        _topic_messages = await self.client.get_messages(entity, ids=current_target_topic_id)
                        if _topic_messages: topic_info_msg_obj = _topic_messages[0]

                        if topic_info_msg_obj and isinstance(topic_info_msg_obj, tl_types.MessageService) and isinstance(topic_info_msg_obj.action, tl_types.MessageActionTopicCreate):
                            chat_name_display += f" | Topic: '{utils.escape_html(topic_info_msg_obj.action.title)}'"
                        elif topic_info_msg_obj and topic_info_msg_obj.is_topic_message and getattr(topic_info_msg_obj,'action', None) is None:
                            actual_topic_creation_msg_id = getattr(topic_info_msg_obj, 'reply_to_top_id', None)
                            if actual_topic_creation_msg_id:
                                _creation_msgs = await self.client.get_messages(entity, ids=actual_topic_creation_msg_id)
                                if _creation_msgs and isinstance(_creation_msgs[0], tl_types.MessageService) and isinstance(_creation_msgs[0].action, tl_types.MessageActionTopicCreate):
                                    chat_name_display += f" | Topic: '{utils.escape_html(_creation_msgs[0].action.title)}'"
                                else:
                                    chat_name_display += f" | Topic (msg {current_target_topic_id}): '{utils.escape_html(topic_info_msg_obj.text[:30])}{'...' if topic_info_msg_obj.text and len(topic_info_msg_obj.text) > 30 else ''}'"
                            else:
                                chat_name_display += f" | Topic (msg {current_target_topic_id}): '{utils.escape_html(topic_info_msg_obj.text[:30])}{'...' if topic_info_msg_obj.text and len(topic_info_msg_obj.text) > 30 else ''}'"
                        else:
                             chat_name_display += f" | Topic ID: {current_target_topic_id}"
                    except Exception as e_topic:
                        logger.warning(f"Ошибка получения инфо о теме {current_target_topic_id} в чате {target_chat_id} ({utils.escape_html(get_display_name(entity))}): {e_topic}")
                        chat_name_display += f" | Topic ID: {current_target_topic_id} (ошибка инфо)"
                
                self.chats[chat_key] = chat_name_display
                added_chats_msgs.append(f"• {self.strings['chat_added'].format(utils.escape_html(chat_name_display))}")

            if added_chats_msgs or already_added_msgs or error_msgs:
                self._db.set(self.strings["name"], "chats", {str(k): v for k, v in self.chats.items()})

        response_text = ""
        if added_chats_msgs or already_added_msgs or error_msgs:
            response_text = self.strings["add_chat_summary_title"]
            if added_chats_msgs:
                response_text += self.strings["add_chat_success_header"] + "\n".join(added_chats_msgs) + "\n\n"
            if already_added_msgs:
                response_text += self.strings["add_chat_already_exists_header"] + "\n".join(already_added_msgs) + "\n\n"
            if error_msgs:
                response_text += self.strings["add_chat_errors_header"] + "\n".join(error_msgs) + "\n"
        else:
            response_text = self.strings["no_valid_chats_provided"]
            
        await self._edit_or_reply_and_handle_deletion(message, response_text.strip())


    @loader.command(ru_doc="🗑️ Удалить чат/тему по номеру из списка. Используйте .remove_chat <номер>.")
    async def remove_chat(self, message):
        args = utils.get_args_raw(message)
        if not args or not args.isdigit():
            await self._edit_or_reply_and_handle_deletion(message, self.strings["invalid_chat_selection"], 5)
            return
        try:
            idx = int(args) - 1
            async with self.lock:
                chat_keys = sorted(list(self.chats.keys()), key=lambda x: (str(self.chats[x]), x[0], x[1] or -1))
                if 0 <= idx < len(chat_keys):
                    key_to_remove = chat_keys[idx]
                    removed_name = self.chats.pop(key_to_remove, "Неизвестный чат")
                    self._db.set(self.strings["name"], "chats", {str(k):v for k,v in self.chats.items()})
                    await self._edit_or_reply_and_handle_deletion(message, self.strings["chat_removed"].format(idx + 1, removed_name))
                else:
                    await self._edit_or_reply_and_handle_deletion(message, self.strings["invalid_chat_selection"])
        except Exception: 
            await self._edit_or_reply_and_handle_deletion(message, self.strings["invalid_chat_selection"] + " (ошибка индекса)", 5)

    @loader.command(ru_doc="🗑️ Очистить список чатов для рассылки.")
    async def clear_chats(self, message):
        async with self.lock: self.chats.clear(); self._db.set(self.strings["name"], "chats", {})
        await self._edit_or_reply_and_handle_deletion(message, self.strings["chats_cleared"])

    @loader.command(ru_doc="📜 Показать список чатов/тем для рассылки.")
    async def list_chats(self, message):
        async with self.lock: current_chats_copy = dict(self.chats)
        if not current_chats_copy:
            await self._edit_or_reply_and_handle_deletion(message, self.strings["no_chats"])
            return
        output = "<b>Список чатов для рассылки:</b>\n\n"
        sorted_chat_items = sorted(list(current_chats_copy.items()), key=lambda item: (str(item[1]), item[0][0], item[0][1] or -1))
        for i, ((cid, tid), name) in enumerate(sorted_chat_items):
            output += f"<b>{i+1}.</b> {utils.escape_html(name)} (<code>{cid}</code>{f' | Topic ID: <code>{tid}</code>' if tid is not None else ''})\n"
        await self._edit_or_reply_and_handle_deletion(message, output)

    @loader.command(ru_doc="➕ Добавить сообщение (ответом на другое сообщение).")
    async def add_msg(self, message):
        reply = await message.get_reply_message()
        if not reply:
            await self._edit_or_reply_and_handle_deletion(message, self.strings["no_messages"].split(". ")[0] + ".", 5)
            return
        
        snippet_text = reply.text
        if not snippet_text:
            if reply.photo: snippet_text = "[Фото]"
            elif reply.video: snippet_text = "[Видео]"
            else: snippet_text = "[Медиа/Сервисное]"
        snippet = (snippet_text[:100].replace("\n"," ") + "...") if len(snippet_text) > 100 else snippet_text.replace("\n"," ")
        source_chat_id = telethon_utils.get_peer_id(reply.peer_id)
        async with self.lock:
            self.messages.append({"id": reply.id, "chat_id": source_chat_id, "snippet": snippet})
            self._db.set(self.strings["name"], "messages", self.messages)
        await self._edit_or_reply_and_handle_deletion(message, self.strings["message_added"].format(utils.escape_html(snippet)))

    @loader.command(ru_doc="➖ Удалить сообщение по номеру из списка рассылки.")
    async def remove_msg(self, message):
        args = utils.get_args_raw(message)
        if not args or not args.isdigit():
            await self._edit_or_reply_and_handle_deletion(message, self.strings["invalid_message_number"], 5)
            return
        try:
            idx = int(args) - 1
            async with self.lock:
                if 0 <= idx < len(self.messages):
                    removed = self.messages.pop(idx)
                    self._db.set(self.strings["name"], "messages", self.messages)
                    await self._edit_or_reply_and_handle_deletion(message, self.strings["message_removed"].format(idx + 1, utils.escape_html(removed.get("snippet","N/A"))))
                else: await self._edit_or_reply_and_handle_deletion(message, self.strings["invalid_message_number"])
        except Exception: 
             await self._edit_or_reply_and_handle_deletion(message, self.strings["invalid_message_number"]+ " (ошибка индекса)", 5)

    @loader.command(ru_doc="🗑️ Очистить список сообщений для рассылки.")
    async def clear_msgs(self, message):
        async with self.lock: self.messages.clear(); self._db.set(self.strings["name"], "messages", [])
        await self._edit_or_reply_and_handle_deletion(message, self.strings["messages_cleared"])

    @loader.command(ru_doc="📜 Показать список сообщений для рассылки.")
    async def list_msgs(self, message):
        async with self.lock: current_messages_copy = list(self.messages)
        if not current_messages_copy:
            await self._edit_or_reply_and_handle_deletion(message, self.strings["no_messages"])
            return
        text = "<b>Список сообщений для рассылки:</b>\n\n"
        for i, msg_info in enumerate(current_messages_copy):
            preview = utils.escape_html(msg_info.get("snippet", "[N/A]"))
            text += f"<b>{i + 1}.</b> {preview} (ID: <code>{msg_info.get('id','N/A')}</code> из чата <code>{msg_info.get('chat_id','N/A')}</code>)\n"
        await self._edit_or_reply_and_handle_deletion(message, text)

    @loader.command(ru_doc="⚙️ Установить ID чата/пользователя продавца для уведомлений. Используйте .set_seller <ID/Username/Ссылка/'me'>.")
    async def set_seller(self, message):
        args = utils.get_args_raw(message).strip()
        if not args:
            await self._edit_or_reply_and_handle_deletion(message, "✍️ Укажите ID чата, username, ссылку или 'me'.", 5)
            return
        
        await self._edit_or_reply_and_handle_deletion(message, self.strings["processing_entity"], delay=0)
        
        identifier = args if args.lower() != 'me' else self.client.tg_id
        seller_id, entity = await self._resolve_entity_and_get_id(identifier)

        if not seller_id or not entity:
            await self._edit_or_reply_and_handle_deletion(message, self.strings["error_getting_entity"].format(f"'{args}'"), 5)
            return
        async with self.lock:
            self.seller_chat_id = seller_id
            self._db.set(self.strings["name"], "seller_chat_id", str(seller_id))
        name_display = utils.escape_html(get_display_name(entity))
        await self._edit_or_reply_and_handle_deletion(message, self.strings["seller_set"] + f": {name_display} (<code>{seller_id}</code>)")

    @loader.command(ru_doc="📊 Показать статус рассылки.")
    async def mail_status(self, message):
        await self._edit_or_reply_and_handle_deletion(message, "⏳ Запрос статуса...", delay=0)
        
        async with self.lock:
            is_running = self.is_running; s_time = self.start_time; e_time = self.end_time
            sent_count = self.total_messages_sent; chats_len = len(self.chats)
            safe_mode_cfg = self.config["safe_mode"]
            randomize_messages_cfg = self.config["randomize_messages"]
            task_active = (self.mail_task and not self.mail_task.done() and not self.mail_task.cancelled())
            cycle_s_time = self._current_cycle_start_time; processed_cycle = self._processed_chats_in_cycle
        
        status_text = ""
        if not is_running and not task_active: status_text = self.strings["mail_not_running"] + "\n"
        elif not is_running and task_active: status_text = "📊 <b>Статус рассылки:</b> ОСТАНОВКА ЗАВЕРШАЕТСЯ ⏹️\n"
        elif is_running and not task_active: status_text = "📊 <b>Статус рассылки:</b> ОЖИДАНИЕ ⏸️ (активен флаг, но задача не найдена?)\n"
        else: status_text = f"📊 <b>Статус рассылки:</b> АКТИВНА ✅\n"
        
        now = datetime.now()
        if is_running and s_time and e_time:
            def format_td(td_obj):
                s = int(td_obj.total_seconds()); h, r = divmod(s,3600); m,s = divmod(r,60); return f"{h:02}:{m:02}:{s:02}"
            status_text += f"⏳ <b>Прошло:</b> {format_td(now - s_time if now > s_time else timedelta(0))}\n"
            status_text += f"⏱️ <b>Осталось:</b> {format_td(e_time - now if e_time > now else timedelta(0))}\n"
            if cycle_s_time:
                status_text += f"🔄 <b>В цикле:</b> {format_td(now - cycle_s_time if now > cycle_s_time else timedelta(0))}, обработано чатов: {processed_cycle}\n"
        
        status_text += (f"✉️ <b>Отправлено сообщений (запуск):</b> {sent_count}\n"
                        f"🎯 <b>Всего чатов в списке:</b> {chats_len}\n"
                        f"🎲 <b>Рандом сообщений:</b> {'ВКЛ' if randomize_messages_cfg else 'ВЫКЛ'}\n"
                        f"💾 <b>Режим безопасности:</b> {'ВКЛ' if safe_mode_cfg else 'ВЫКЛ'}")
        
        delay_for_status = self.config["delete_replies_delay"]
        await self._edit_or_reply_and_handle_deletion(message, status_text, delay=delay_for_status if delay_for_status > 0 else 60)


    @loader.command(ru_doc="🚀 Запустить рассылку. Использование: .start_mail <время_сек> <интервал_цикла_от-до_сек>.")
    async def start_mail(self, message):
        args = utils.get_args(message)
        if len(args) != 2:
            await self._edit_or_reply_and_handle_deletion(message, self.strings["duration_invalid"], 5); return
        try:
            duration = int(args[0])
            interval_parts = args[1].split("-")
            if duration <= 0 or len(interval_parts) != 2: raise ValueError
            cycle_interval_input = (float(interval_parts[0]), float(interval_parts[1]))
            if not (0 <= cycle_interval_input[0] <= cycle_interval_input[1]): raise ValueError
        except ValueError:
            await self._edit_or_reply_and_handle_deletion(message, self.strings["duration_invalid"] + "\nПроверьте числа (время > 0) и формат интервала (например, 10-20).", 5); return
        
        current_message_for_status = message
        await self._edit_or_reply_and_handle_deletion(current_message_for_status, self.strings["processing_entity"], delay=0)

        async with self.lock:
            if not self.chats: await self._edit_or_reply_and_handle_deletion(current_message_for_status, self.strings["chats_empty"], 5); return
            if not self.messages: await self._edit_or_reply_and_handle_deletion(current_message_for_status, self.strings["messages_empty"], 5); return
            if self.is_running or (self.mail_task and not self.mail_task.done() and not self.mail_task.cancelled()):
                await self._edit_or_reply_and_handle_deletion(current_message_for_status, self.strings["already_running"], 5); return

            self.is_running = True; self.total_messages_sent = 0
            self.start_time = datetime.now()
            self.end_time = self.start_time + timedelta(seconds=duration)
            self._current_cycle_start_time = None; self._processed_chats_in_cycle = 0

            is_safe_cfg = self.config["safe_mode"]
            randomize_msg_cfg = self.config["randomize_messages"]
            
            short_int_disp = self._validate_interval_tuple(self.config["safe_chats_interval"] if is_safe_cfg else self.config["chats_interval"], (10,20) if is_safe_cfg else (2,5))
            msg_int_disp_val = (0,0) 
            if not randomize_msg_cfg: 
                msg_int_disp_val = self._validate_interval_tuple(self.config["safe_message_interval"] if is_safe_cfg else self.config["message_interval"], (5,10) if is_safe_cfg else (1,3))

            cycle_int_disp = self._validate_interval_tuple(self.config["safe_cycle_interval"],(180,300)) if is_safe_cfg else cycle_interval_input
            
            start_message_text_base = self.strings["started_mailing"].format(
                duration, 
                f"{cycle_int_disp[0]:.1f}", f"{cycle_int_disp[1]:.1f}",
                f"{short_int_disp[0]:.1f}", f"{short_int_disp[1]:.1f}",
                f"{msg_int_disp_val[0]:.1f}", f"{msg_int_disp_val[1]:.1f}"
            )
            if randomize_msg_cfg:
                 start_message_text_base = self.strings["started_mailing"].format(
                    duration, 
                    f"{cycle_int_disp[0]:.1f}", f"{cycle_int_disp[1]:.1f}",
                    f"{short_int_disp[0]:.1f}", f"{short_int_disp[1]:.1f}",
                    "N/A", "N/A" 
                )
                 start_message_text_base += f"\n🎲 <b>Рандомизация сообщений: ВКЛ</b> (1 сообщ./чат)"


            if is_safe_cfg:
                 start_message_text_base += "\n" + self.strings["safe_mode_enabled"].format(
                    self.config["max_chats_safe"],
                    f"{short_int_disp[0]:.1f}", f"{short_int_disp[1]:.1f}",
                    f"{cycle_int_disp[0]:.1f}", f"{cycle_int_disp[1]:.1f}",
                    f"{msg_int_disp_val[0]:.1f}" if not randomize_msg_cfg else "N/A", 
                    f"{msg_int_disp_val[1]:.1f}" if not randomize_msg_cfg else "N/A"
                ).split("\n")[0] 
            
            delay_for_start_msg = self.config["delete_replies_delay"]
            await self._edit_or_reply_and_handle_deletion(current_message_for_status, start_message_text_base, delay= delay_for_start_msg if delay_for_start_msg > 0 else 20)

            self.mail_task = asyncio.create_task(
                self._mail_loop(duration, cycle_int_disp, message), 
                name=f"{self.strings['name']}_MailLoopTask"
            )
            logger.info(f"Задача рассылки запущена: {self.mail_task.get_name()}")

    @loader.command(ru_doc="⏹️ Остановить рассылку.")
    async def stop_mail(self, message):
        current_message_for_status = message
        await self._edit_or_reply_and_handle_deletion(current_message_for_status, "⏳ Запрос остановки...", delay=0)
        
        task_to_cancel = None
        stopped_normally = False
        async with self.lock:
            if not self.is_running and not (self.mail_task and not self.mail_task.done() and not self.mail_task.cancelled()):
                await self._edit_or_reply_and_handle_deletion(current_message_for_status, self.strings["not_running"], 5); return
            
            self.is_running = False 
            if self.mail_task and not self.mail_task.done() and not self.mail_task.cancelled():
                task_to_cancel = self.mail_task
            else: 
                self.start_time = None; self.end_time = None; self._current_cycle_start_time = None
                self._processed_chats_in_cycle = 0; self.mail_task = None
                stopped_normally = True
        if task_to_cancel:
            task_to_cancel.cancel() 
            await self._edit_or_reply_and_handle_deletion(current_message_for_status, self.strings["stopped_mailing"] + "\n⏳ Ожидайте финального отчета...", delay=self.config["delete_replies_delay"] if self.config["delete_replies_delay"] > 0 else 10)
        elif stopped_normally:
             await self._edit_or_reply_and_handle_deletion(current_message_for_status, self.strings["stopped_mailing"] + " (Уже была остановлена или завершена)", delay=self.config["delete_replies_delay"] if self.config["delete_replies_delay"] > 0 else 10)
        else:
             await self._edit_or_reply_and_handle_deletion(current_message_for_status, self.strings["stopped_mailing"] + " (Состояние сброшено, активная задача не найдена)", delay=self.config["delete_replies_delay"] if self.config["delete_replies_delay"] > 0 else 10)


    async def _is_safe_chat(self, entity: tl_types.TypePeer) -> bool:
        if isinstance(entity, (tl_types.Chat, tl_types.Channel)):
             return telethon_utils.get_peer_id(entity) < -1000000000 
        return False

    async def _send_to_chat(self, target_chat_id: int, msg_info: dict, target_topic_id: Optional[int] = None) -> Tuple[bool, str]:
        original_chat_id = msg_info.get("chat_id")
        original_msg_id = msg_info.get("id")
        try:
            original_msg_list = await self.client.get_messages(original_chat_id, ids=[original_msg_id])
            original_msg = original_msg_list[0] if original_msg_list else None
            if not original_msg: return (False, f"Оригинальное сообщение {original_msg_id} в {original_chat_id} не найдено.")
        except Exception as e: return (False, f"Ошибка получения {original_msg_id} из {original_chat_id}: {type(e).__name__}")

        for attempt in range(5): 
            try:
                await self.client.send_message(entity=target_chat_id, message=original_msg, reply_to=target_topic_id)
                async with self.lock: self.total_messages_sent += 1 
                return (True, "OK")
            except errors.FloodWaitError as e_flood:
                if attempt < 4: 
                    logger.warning(f"FloodWait for {e_flood.seconds}s when sending to {target_chat_id}. Attempt {attempt+1}/5. Sleeping...")
                    await asyncio.sleep(e_flood.seconds + random.uniform(1,3)) 
                    continue
                return (False, f"FloodWait ({e_flood.seconds}s)")
            except errors.SlowModeWaitError as e_slow:
                logger.warning(f"SlowModeWait for {e_slow.seconds}s in {target_chat_id}. Sleeping...")
                await asyncio.sleep(e_slow.seconds + random.uniform(0.2,0.5))
                return(False, "SlowMode") 
            except errors.RPCError as e_rpc:
                 if type(e_rpc).__name__ in self.PERMISSION_ERRORS: return (False, type(e_rpc).__name__)
                 logger.warning(f"RPCError sending to {target_chat_id}: {type(e_rpc).__name__} - {e_rpc}. Attempt {attempt+1}/5.")
                 if attempt < 4: await asyncio.sleep(random.uniform(2,5)); continue 
                 return (False, f"RPCError: {type(e_rpc).__name__}")
            except Exception as e_unexp:
                 logger.error(f"Unexpected error sending to {target_chat_id}: {type(e_unexp).__name__} - {e_unexp}")
                 return (False, f"Unexpected: {type(e_unexp).__name__}")
        return (False, "Max retries reached") 


    async def _mail_loop(self, duration_seconds: int, cycle_interval_seconds_range: Tuple[float, float], initial_command_message_event):
        start_time_loop = datetime.now()
        end_time_loop = start_time_loop + timedelta(seconds=duration_seconds)
        
        final_status_for_user = self.strings["mailing_complete"]
        final_status_for_seller = self.strings["seller_notification"]
        async with self.lock: current_seller_id = self.seller_chat_id 

        try:
            while self.is_running and datetime.now() < end_time_loop:
                self._current_cycle_start_time = datetime.now(); self._processed_chats_in_cycle = 0
                
                async with self.lock: 
                    current_chats = list(self.chats.keys())
                    current_messages_list = list(self.messages) 
                    is_safe_mode = self.config["safe_mode"]
                    randomize_messages_cfg = self.config["randomize_messages"]
                    max_c_per_cycle = self.config["max_chats_safe"] 
                    short_interval = self._validate_interval_tuple(self.config["safe_chats_interval"] if is_safe_mode else self.config["chats_interval"], (10,20) if is_safe_mode else (2,5))
                    message_interval_val = (0,0) 
                    if not randomize_messages_cfg:
                        message_interval_val = self._validate_interval_tuple(self.config["safe_message_interval"] if is_safe_mode else self.config["message_interval"], (5,10) if is_safe_mode else (1,3))
                
                if not current_chats or not current_messages_list:
                    async with self.lock: self.is_running = False 
                    reason_empty = "чатов" if not current_chats else "сообщений"
                    final_status_for_user = f"⚠️ Рассылка остановлена: список {reason_empty} пуст."
                    final_status_for_seller += f" (остановлено: список {reason_empty} пуст)"
                    break
                
                random.shuffle(current_chats)
                chats_for_this_cycle = current_chats[:min(max_c_per_cycle if is_safe_mode else len(current_chats), len(current_chats))]
                logger.info(f"Новый цикл ({datetime.now():%H:%M:%S}). Чатов к обработке: {len(chats_for_this_cycle)} (Safe: {is_safe_mode}, Max: {max_c_per_cycle if is_safe_mode else 'All'}, RandomMsg: {randomize_messages_cfg}).")

                for i, (chat_id_target, topic_id_target) in enumerate(chats_for_this_cycle):
                    if not self.is_running or datetime.now() >= end_time_loop: break
                    
                    async with self.lock: chat_display_name = self.chats.get((chat_id_target, topic_id_target), f"ID:{chat_id_target}")
                    try:
                        entity_obj = await self.client.get_entity(chat_id_target)
                        if is_safe_mode and not await self._is_safe_chat(entity_obj):
                            logger.info(f"[Safe Mode] Пропуск не-группы/канала: {chat_display_name}")
                            async with self.lock: self._processed_chats_in_cycle += 1
                            continue
                    except Exception as e_ent_loop:
                        logger.warning(f"Не удалось получить сущность для {chat_display_name}: {e_ent_loop}. Пропуск."); 
                        async with self.lock: self._processed_chats_in_cycle += 1
                        continue
                    
                    sent_count_this_chat = 0; permission_issue = False

                    if randomize_messages_cfg:
                        if not current_messages_list: 
                            logger.warning(f"Список сообщений пуст, хотя проверка пройдена. Пропуск чата {chat_display_name}.")
                            async with self.lock: self._processed_chats_in_cycle += 1
                            continue
                        
                        message_to_send = random.choice(current_messages_list)
                        success_send, reason_send = await self._send_to_chat(chat_id_target, message_to_send, topic_id_target)
                        if success_send: 
                            sent_count_this_chat += 1
                        else:
                            if reason_send in self.PERMISSION_ERRORS: 
                                permission_issue = True
                                logger.warning(f"Проблема с правами ({reason_send}) при отправке в {chat_display_name}. Пропуск чата.")
                            else: 
                                logger.warning(f"Ошибка отправки случайного сообщения в {chat_display_name} (ID {message_to_send['id']}): {reason_send}. Прерываю для этого чата.")
                    else: 
                        shuffled_messages_for_chat = random.sample(current_messages_list, len(current_messages_list))
                        for message_detail in shuffled_messages_for_chat:
                            if not self.is_running or datetime.now() >= end_time_loop: break
                            
                            success_send, reason_send = await self._send_to_chat(chat_id_target, message_detail, topic_id_target)
                            if success_send: sent_count_this_chat += 1
                            else:
                                if reason_send in self.PERMISSION_ERRORS: 
                                    permission_issue = True
                                    logger.warning(f"Проблема с правами ({reason_send}) при отправке в {chat_display_name}. Прерываю для чата.")
                                else:
                                    logger.warning(f"Ошибка отправки в {chat_display_name} (сообщ.ID {message_detail['id']}): {reason_send}. Прерываю для чата.")
                                break 
                            
                            if self.is_running and datetime.now() < end_time_loop and sent_count_this_chat < len(shuffled_messages_for_chat): 
                                await asyncio.sleep(random.uniform(message_interval_val[0], message_interval_val[1]))
                        if not self.is_running or datetime.now() >= end_time_loop: break 
                    
                    async with self.lock: 
                        if sent_count_this_chat > 0 or permission_issue: 
                            self._processed_chats_in_cycle += 1
                    
                    if permission_issue: 
                        logger.info(f"Проблема с правами для чата {chat_display_name}, возможно, переход к следующему циклу или длительная пауза.")

                    if not self.is_running or datetime.now() >= end_time_loop: break 
                    
                    if i < len(chats_for_this_cycle) - 1 and not permission_issue:
                         await asyncio.sleep(random.uniform(short_interval[0], short_interval[1]))
                
                if not self.is_running or datetime.now() >= end_time_loop: break 
                
                if len(chats_for_this_cycle) > 0 : 
                    time_for_cycle_wait = random.uniform(cycle_interval_seconds_range[0], cycle_interval_seconds_range[1])
                    remaining_total_time_s = (end_time_loop - datetime.now()).total_seconds()
                    
                    actual_cycle_wait = max(0.0, min(time_for_cycle_wait, remaining_total_time_s if remaining_total_time_s > 0 else 0))
                    
                    if actual_cycle_wait > 0: 
                        logger.info(f"Пауза между циклами: {actual_cycle_wait:.1f} сек.")
                        await asyncio.sleep(actual_cycle_wait)
                    elif remaining_total_time_s <=0 : 
                        logger.info("Время рассылки истекло во время расчета паузы между циклами.")
                        break 

            current_time = datetime.now()
            if current_time >= end_time_loop and (self.is_running or (await self.get_total_messages_sent_atomic()) > 0): 
                 final_status_for_user += " (по времени)"
                 final_status_for_seller += " (завершено по времени)"
            elif not self.is_running and "пуст" not in final_status_for_user and "отменено" not in final_status_for_user : 
                 final_status_for_user = self.strings["stopped_mailing"] + " (по команде)"
                 final_status_for_seller += " (остановлено по команде)"
        
        except asyncio.CancelledError:
            logger.info("Задача рассылки была отменена.")
            final_status_for_user = self.strings["stopped_mailing"] + " (отменено)"
            final_status_for_seller += " (отменено)"
        except Exception as e_loop:
            logger.exception("Критическая ошибка в главном цикле рассылки (_mail_loop):")
            final_status_for_user = f"❌ Критическая ошибка в рассылке: {type(e_loop).__name__}. Рассылка остановлена."
            final_status_for_seller = f"Уведомление: ❌ Критическая ошибка в рассылке: {type(e_loop).__name__} - {e_loop}"
        finally:
            logger.info("Завершение задачи рассылки...")
            total_messages_sent_this_run = await self.get_total_messages_sent_atomic()

            async with self.lock: 
                self.is_running = False
                self.mail_task = None
                self._current_cycle_start_time = None
                self._processed_chats_in_cycle = 0
                self.total_messages_sent = 0 
                self.start_time = None 
                self.end_time = None

            final_status_for_user_with_count = f"{final_status_for_user} (Всего отправлено: {total_messages_sent_this_run})"
            final_status_for_seller_with_count = f"{final_status_for_seller} (Всего отправлено: {total_messages_sent_this_run})"

            try:
                target_chat_for_final_status = self.client.tg_id 
                if initial_command_message_event and hasattr(initial_command_message_event, "chat_id"):
                    try:
                        await self.client.get_input_entity(initial_command_message_event.chat_id)
                        target_chat_for_final_status = initial_command_message_event.chat_id
                    except Exception: 
                        logger.warning(f"Не удалось использовать чат команды {initial_command_message_event.chat_id} для финального статуса, использую Saved Messages.")
                        target_chat_for_final_status = self.client.tg_id
                
                await self.client.send_message(target_chat_for_final_status, final_status_for_user_with_count, parse_mode='html')
                logger.info(f"Финальное сообщение пользователю отправлено в чат {target_chat_for_final_status}.")
            except Exception as e_final_user:
                logger.error(f"Не удалось отправить финальное сообщение пользователю: {e_final_user}")

            if current_seller_id: 
                try:
                    await self.client.send_message(current_seller_id, final_status_for_seller_with_count, parse_mode='html')
                    logger.info(f"Уведомление о завершении отправлено продавцу {current_seller_id}.")
                except Exception as e_final_seller:
                    logger.error(f"Не удалось отправить уведомление продавцу {current_seller_id}: {e_final_seller}")
            
            logger.info(self.strings["mailing_complete"].replace("✅","").strip() + " (финализация).")
            
    async def get_total_messages_sent_atomic(self) -> int:
        async with self.lock:
            return self.total_messages_sent
