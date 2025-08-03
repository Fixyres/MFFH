#  This file is part of SenkoGuardianModules
#  Copyright (c) 2025 Senko
#  This software is released under the MIT License.
#  https://opensource.org/licenses/MIT

__version__ = (5, 0, 0) # асаламалейкум тем кто код смотрит от меня (кста для чего смотрите?) (я заебался, ошибок было дохуище)

# meta developer: @SenkoGuardianModules

#  .------. .------. .------. .------. .------. .------.
#  |S.--. | |E.--. | |N.--. | |M.--. | |O.--. | |D.--. |
#  | :/\: | | :/\: | | :(): | | :/\: | | :/\: | | :/\: |
#  | :\/: | | :\/: | | ()() | | :\/: | | :\/: | | :\/: |
#  | '--'S| | '--'E| | '--'N| | '--'M| | '--'O| | '--'D|
#  `------' `------' `------' `------' `------' `------'

import re
import os
import io
import random
import socket
import asyncio
import logging
import aiohttp
import tempfile
from markdown_it import MarkdownIt
import pytz
from telethon import types
from telethon.tl import types as tl_types
from telethon.tl.types import Message, DocumentAttributeFilename
from telethon.utils import get_display_name, get_peer_id
from telethon.errors.rpcerrorlist import MessageTooLongError, ChatAdminRequiredError
from telethon.errors.rpcerrorlist import UserNotParticipantError, ChannelPrivateError
import google.ai.generativelanguage as glm
import google.api_core.exceptions as google_exceptions
import google.generativeai as genai
from .. import loader, utils
from ..inline.types import InlineCall

# requires: google-generativeai google-api-core pytz markdown_it_py

logger = logging.getLogger(__name__)

DB_HISTORY_KEY = "gemini_conversations_v4"
DB_GAUTO_HISTORY_KEY = "gemini_gauto_conversations_v1"
DB_IMPERSONATION_KEY = "gemini_impersonation_chats"
GEMINI_TIMEOUT = 840
MAX_FFMPEG_SIZE = 90 * 1024 * 1024

@loader.tds
class Gemini(loader.Module):
    """Модуль для работы с Google Gemini AI.(стабильная память и поддержка video/image/audio)"""
    strings = {
        "name": "Gemini",
        "cfg_api_key_doc": "API ключ для Google Gemini AI.",
        "cfg_model_name_doc": "Модель Gemini.",
        "cfg_buttons_doc": "Включить интерактивные кнопки.",
        "cfg_system_instruction_doc": "Системная инструкция (промпт) для Gemini.",
        "cfg_max_history_length_doc": "Макс. кол-во пар 'вопрос-ответ' в памяти (0 - без лимита).",
        "cfg_timezone_doc": "Ваш часовой пояс. Список: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones",
        "cfg_proxy_doc": "Прокси для обхода блокировок. Формат: http://user:pass@host:port",
        "cfg_impersonation_prompt_doc": "Промпт для режима авто-ответа. {my_name} и {chat_history} будут заменены.",
        "cfg_impersonation_history_limit_doc": "Сколько последних сообщений из чата отправлять в качестве контекста для авто-ответа.",
        "cfg_impersonation_reply_chance_doc": "Вероятность ответа в режиме gauto (от 0.0 до 1.0). 0.2 = 20% шанс.",
        "no_api_key": '❗️ <b>Api ключ не настроен.</b>\nПолучить Api ключ можно <a href="https://aistudio.google.com/app/apikey">здесь</a>.\n <b>Поставить ключ сюда:</b> <code>.cfg gemini api_key</code>',
        "no_prompt_or_media": "⚠️ <i>Нужен текст или ответ на медиа/файл.</i>",
        "processing": "<emoji document_id=5386367538735104399>⌛️</emoji> <b>Обработка...</b>",
        "api_error": "❗️ <b>Ошибка API Google Gemini:</b>\n<code>{}</code>",
        "api_timeout": f"❗️ <b>Таймаут ответа от Gemini API ({GEMINI_TIMEOUT} сек).</b>",
        "blocked_error": "🚫 <b>Запрос/ответ заблокирован.</b>\n<code>{}</code>",
        "generic_error": "❗️ <b>Ошибка:</b>\n<code>{}</code>",
        "question_prefix": "💬 <b>Запрос:</b>",
        "response_prefix": "<emoji document_id=5325547803936572038>✨</emoji> <b>Gemini:</b>",
        "unsupported_media_type": "⚠️ <b>Формат медиа ({}) не поддерживается.</b>",
        "memory_status": "🧠 [{}/{}]",
        "memory_status_unlimited": "🧠 [{}/∞]",
        "memory_cleared": "🧹 <b>Память диалога очищена.</b>",
        "memory_cleared_gauto": "🧹 <b>Память gauto в этом чате очищена.</b>",
        "no_memory_to_clear": "ℹ️ <b>В этом чате нет истории.</b>",
        "no_gauto_memory_to_clear": "ℹ️ <b>В этом чате нет истории gauto.</b>",
        "memory_chats_title": "🧠 <b>Чаты с историей ({}):</b>",
        "memory_chat_line": "  • {} (<code>{}</code>)",
        "no_memory_found": "ℹ️ Память Gemini пуста.",
        "media_reply_placeholder": "[ответ на медиа]",
        "btn_clear": "🧹 Очистить",
        "btn_regenerate": "🔄 Другой ответ",
        "no_last_request": "Последний запрос не найден для повторной генерации.",
        "memory_fully_cleared": "🧹 <b>Вся память Gemini полностью очищена (затронуто {} чатов).</b>",
        "gauto_memory_fully_cleared": "🧹 <b>Вся память gauto полностью очищена (затронуто {} чатов).</b>",
        "no_memory_to_fully_clear": "ℹ️ <b>Память Gemini и так пуста.</b>",
        "no_gauto_memory_to_fully_clear": "ℹ️ <b>Память gauto и так пуста.</b>",
        "response_too_long": "Ответ Gemini был слишком длинным и отправлен в виде файла.",
        "gclear_usage": "ℹ️ <b>Использование:</b> <code>.gclear [auto]</code>",
        "gres_usage": "ℹ️ <b>Использование:</b> <code>.gres [auto]</code>",
        "auto_mode_on": "🎭 <b>Режим авто-ответа включен в этом чате.</b>\nЯ буду отвечать на сообщения с вероятностью {}%.",
        "auto_mode_off": "🎭 <b>Режим авто-ответа выключен в этом чате.</b>",
        "auto_mode_chats_title": "🎭 <b>Чаты с активным авто-ответом ({}):</b>",
        "no_auto_mode_chats": "ℹ️ Нет чатов с включенным режимом авто-ответа.",
        "auto_mode_usage": "ℹ️ <b>Использование:</b> <code>.gauto on/off</code>",
        "gch_usage": "ℹ️ <b>Использование:</b>\n<code>.gch <кол-во> <вопрос></code>\n<code>.gch <id чата> <кол-во> <вопрос></code>",
        "gch_processing": "<emoji document_id=5386367538735104399>⌛️</emoji> <b>Анализирую {} сообщений...</b>",
        "gch_result_caption": "Анализ последних {} сообщений",
        "gch_result_caption_from_chat": "Анализ последних {} сообщений из чата <b>{}</b>",
        "gch_invalid_args": "❗️ <b>Неверные аргументы.</b>\n{}",
        "gch_chat_error": "❗️ <b>Ошибка доступа к чату</b> <code>{}</code>: <i>{}</i>",
    }
    TEXT_MIME_TYPES = {
        "text/plain", "text/markdown", "text/html", "text/css", "text/csv",
        "application/json", "application/xml", "application/x-python", "text/x-python",
        "application/javascript", "application/x-sh",
    }
    def __init__(self):
        self.config=loader.ModuleConfig(
            loader.ConfigValue("api_key", "", self.strings["cfg_api_key_doc"], validator=loader.validators.Hidden()),
            loader.ConfigValue("model_name", "gemini-2.5-flash", self.strings["cfg_model_name_doc"]),
            loader.ConfigValue("interactive_buttons", True, self.strings["cfg_buttons_doc"], validator=loader.validators.Boolean()),
            loader.ConfigValue("system_instruction", "", self.strings["cfg_system_instruction_doc"], validator=loader.validators.String()),
            loader.ConfigValue("max_history_length", 800, self.strings["cfg_max_history_length_doc"], validator=loader.validators.Integer(minimum=0)),
            loader.ConfigValue("timezone", "Europe/Moscow", self.strings["cfg_timezone_doc"]),
            loader.ConfigValue("proxy", "", self.strings["cfg_proxy_doc"]),
            loader.ConfigValue(
                "impersonation_prompt",
                (
                    "Ты — это я, пользователь Telegram по имени {my_name}. Твоя задача — отвечать в чате от моего имени, основываясь на последних сообщениях. "
                    "Веди себя естественно, как обычный человек, а не как ассистент. Не признавайся, что ты — ИИ, даже если тебя спросят напрямую. "
                    "Твоя личность: [Здесь опишите свой характер: остроумный, серьезный, саркастичный, дружелюбный и т.д.].\n"
                    "Правила:\n"
                    "- Отвечай кратко и по делу. Не пиши длинные эссе.\n"
                    "- Используй неформальный язык, можешь использовать сленг, если это уместно.\n"
                    "- Не отвечай на каждое сообщение. Игнорируй простые сообщения типа 'ок', 'ага', 'спс'.\n"
                    "- Если кто-то отправляет медиа (стикер, фото), отреагируй на него, как бы это сделал человек (например: 'лол', 'ору', 'жиза', 'красиво').\n"
                    "- Не используй префиксы и кавычки. Просто пиши текст ответа.\n\n"
                    "Вот история чата для контекста. Последнее сообщение — то, на которое нужно отреагировать. Ответь на него.\n\n"
                    "ИСТОРИЯ ЧАТА:\n{chat_history}\n\n{my_name}:"
                ),
                self.strings["cfg_impersonation_prompt_doc"],
                validator=loader.validators.String(),
            ),
            loader.ConfigValue("impersonation_history_limit", 80, self.strings["cfg_impersonation_history_limit_doc"], validator=loader.validators.Integer(minimum=5, maximum=100)),
            loader.ConfigValue("impersonation_reply_chance", 0.25, self.strings["cfg_impersonation_reply_chance_doc"], validator=loader.validators.Float(minimum=0.0, maximum=1.0)),
        )
        self.conversations={}
        self.gauto_conversations={}
        self.last_requests={}
        self.impersonation_chats=set()
        self._lock=asyncio.Lock()
        self.memory_disabled_chats=set()

    @loader.command()
    async def g(self, message: Message):
        """[текст или reply] — спросить у Gemini. Может анализировать ссылки."""
        clean_args=utils.get_args_raw(message)
        reply=await message.get_reply_message()
        use_url_context=False
        text_to_check=clean_args
        if reply and reply.text: text_to_check+=" " + reply.text
        if re.search(r'https?://\S+', text_to_check): use_url_context=True
        status_msg=await utils.answer(message, self.strings["processing"])
        parts, warnings=await self._prepare_parts(message, custom_text=clean_args)
        if warnings and status_msg:
            warning_text="\n".join(warnings)
            try: await status_msg.edit(f"{status_msg.text}\n\n{warning_text}")
            except MessageTooLongError: await message.reply(warning_text)
        if not parts:
            err_msg=self.strings["no_prompt_or_media"]
            if status_msg: await utils.answer(status_msg, err_msg)
            return
        await self._send_to_gemini(message=message, parts=parts, status_msg=status_msg, use_url_context=use_url_context, display_prompt=clean_args or None)

    @loader.command()
    async def gch(self, message: Message):
        """<[id чата]> <кол-во> <вопрос> - Проанализировать историю чата."""
        args=utils.get_args_raw(message).split(maxsplit=2)
        target_chat_id, count_str, user_prompt=None, None, None
        if len(args) == 2:
            target_chat_id=utils.get_chat_id(message)
            count_str, user_prompt=args[0], args[1]
        elif len(args) == 3:
            try:
                target_chat_id=int(args[0])
                count_str, user_prompt=args[1], args[2]
            except ValueError:
                return await utils.answer(message, self.strings["gch_invalid_args"].format("ID чата должен быть числом."))
        else:
            return await utils.answer(message, self.strings["gch_usage"])
        try:
            count=int(count_str)
            if count<=0 or count > 20000: raise ValueError
        except ValueError:
            return await utils.answer(message, self.strings["gch_invalid_args"].format(f"Количество сообщений должно быть числом от 1 до 20000. Вы ввели: <code>{utils.escape_html(count_str)}</code>"))
        status_msg=await utils.answer(message, self.strings["gch_processing"].format(count))
        try:
            entity=await self.client.get_entity(target_chat_id)
            chat_name=utils.escape_html(get_display_name(entity))
            chat_log=await self._get_recent_chat_text(target_chat_id, count=count, skip_last=False)
        except (ValueError, TypeError, ChatAdminRequiredError, UserNotParticipantError, ChannelPrivateError) as e:
            return await utils.answer(status_msg, self.strings["gch_chat_error"].format(target_chat_id, e.__class__.__name__))
        except Exception as e:
            return await utils.answer(status_msg, self.strings["gch_chat_error"].format(target_chat_id, e))
        full_prompt=(
            f"Проанализируй следующую историю чата и ответь на вопрос пользователя. "
            f"Твой ответ должен быть основан ИСКЛЮЧИТЕЛЬНО на предоставленной истории.\n\n"
            f"ВОПРОС ПОЛЬЗОВАТЕЛЯ: \"{user_prompt}\"\n\n"
            f"ИСТОРИЯ ЧАТА:\n---\n{chat_log}\n---"
        )
        try:
            if not self.config["api_key"]:
                await utils.answer(status_msg, self.strings['no_api_key']); return
            genai.configure(api_key=self.config["api_key"])
            model=genai.GenerativeModel(self.config["model_name"], safety_settings=self.safety_settings)
            response=await asyncio.wait_for(model.generate_content_async(full_prompt), timeout=GEMINI_TIMEOUT)
            result_text=response.text
            header = self.strings["gch_result_caption_from_chat"].format(count, chat_name) if target_chat_id != utils.get_chat_id(message) else self.strings["gch_result_caption"].format(count)
            question_html=f"<blockquote expandable>{utils.escape_html(user_prompt)}</blockquote>"
            response_html=self._markdown_to_html(result_text)
            formatted_body=self._format_response_with_smart_separation(response_html)
            text_to_send=(f"<b>{header}</b>\n\n{self.strings['question_prefix']}\n{question_html}\n\n{self.strings['response_prefix']}\n{formatted_body}")
            if len(text_to_send) > 4096:
                file_content=(f"Вопрос: {user_prompt}\n\n════════════════════\n\nОтвет Gemini на анализ чата '{chat_name}':\n{result_text}")
                file=io.BytesIO(file_content.encode("utf-8"))
                file.name=f"analysis_{target_chat_id}.txt"
                await status_msg.delete()
                await message.reply(file=file, caption=f"📝 {header}")
            else:
                await utils.answer(status_msg, text_to_send)
        except Exception as e:
            await utils.answer(status_msg, self._handle_error(e))

    @loader.command()
    async def gauto(self, message: Message):
        """<on/off> — Включить/выключить режим авто-ответа в чате."""
        args=utils.get_args_raw(message)
        chat_id=utils.get_chat_id(message)
        if args=="on":
            self.impersonation_chats.add(chat_id)
            self.db.set(self.strings["name"], DB_IMPERSONATION_KEY, list(self.impersonation_chats))
            await utils.answer(message, self.strings["auto_mode_on"].format(int(self.config["impersonation_reply_chance"]*100)))
        elif args=="off":
            self.impersonation_chats.discard(chat_id)
            self.db.set(self.strings["name"], DB_IMPERSONATION_KEY, list(self.impersonation_chats))
            await utils.answer(message, self.strings["auto_mode_off"])
        else:
            await utils.answer(message, self.strings["auto_mode_usage"])

    @loader.command()
    async def gautochats(self, message: Message):
        """— Показать чаты с активным режимом авто-ответа."""
        if not self.impersonation_chats:
            await utils.answer(message, self.strings["no_auto_mode_chats"])
            return
        out=[self.strings["auto_mode_chats_title"].format(len(self.impersonation_chats))]
        for chat_id in self.impersonation_chats:
            try:
                entity=await self.client.get_entity(chat_id)
                name=utils.escape_html(get_display_name(entity))
                out.append(self.strings["memory_chat_line"].format(name, chat_id))
            except Exception:
                out.append(self.strings["memory_chat_line"].format("Неизвестный чат", chat_id))
        await utils.answer(message, "\n".join(out))

    @loader.command()
    async def gclear(self, message: Message):
        """[auto] — очистить память в чате. auto для памяти gauto."""
        args=utils.get_args_raw(message)
        chat_id=utils.get_chat_id(message)
        if args=="auto":
            if str(chat_id) in self.gauto_conversations:
                self._clear_history(chat_id, gauto=True)
                await utils.answer(message, self.strings["memory_cleared_gauto"])
            else:
                await utils.answer(message, self.strings["no_gauto_memory_to_clear"])
        elif not args:
            if str(chat_id) in self.conversations:
                self._clear_history(chat_id, gauto=False)
                await utils.answer(message, self.strings["memory_cleared"])
            else:
                await utils.answer(message, self.strings["no_memory_to_clear"])
        else:
            await utils.answer(message, self.strings["gclear_usage"])

    @loader.command()
    async def gmemdel(self, message: Message):
        """[N] — удалить последние N пар сообщений из памяти."""
        args=utils.get_args_raw(message)
        try: n=int(args) if args else 1
        except Exception: n=1
        chat_id=utils.get_chat_id(message)
        hist=self._get_structured_history(chat_id)
        elements_to_remove=n*2
        if n > 0 and len(hist) >= elements_to_remove:
            hist=hist[:-elements_to_remove]
            self.conversations[str(chat_id)]=hist
            self._save_history_sync()
            await utils.answer(message, f"🧹 Удалено последних <b>{n}</b> пар сообщений из памяти.")
        else:
            await utils.answer(message, "Недостаточно истории для удаления.")

    @loader.command()
    async def gmemchats(self, message: Message):
        """— Показать список чатов с активной памятью (имя и ID)."""
        if not self.conversations:
            await utils.answer(message, self.strings["no_memory_found"]); return
        out=[self.strings["memory_chats_title"].format(len(self.conversations))]
        shown=set()
        for chat_id_str in list(self.conversations.keys()):
            if not chat_id_str or not str(chat_id_str).isdigit():
                del self.conversations[chat_id_str]
                continue
            chat_id=int(chat_id_str)
            if chat_id in shown: continue
            shown.add(chat_id)
            try:
                entity=await self.client.get_entity(chat_id)
                name=get_display_name(entity)
            except Exception: name=f"Unknown ({chat_id})"
            out.append(self.strings["memory_chat_line"].format(name, chat_id))
        self._save_history_sync()
        if len(out)==1:
            await utils.answer(message, self.strings["no_memory_found"]); return
        await utils.answer(message, "\n".join(out))

    @loader.command()
    async def gmemexport(self, message: Message):
        """[auto] — экспортировать историю чата. auto для истории gauto."""
        args=utils.get_args_raw(message)
        gauto_mode=args=="auto"
        chat_id=utils.get_chat_id(message)
        hist=self._get_structured_history(chat_id, gauto=gauto_mode)
        if not hist: return await utils.answer(message, "История для экспорта пуста.")
        user_ids={e.get("user_id") for e in hist if e.get("role")=="user" and e.get("user_id")}
        user_names={None: None}
        for uid in user_ids:
            if not uid: continue
            try:
                entity=await self.client.get_entity(uid)
                user_names[uid]=get_display_name(entity)
            except Exception: user_names[uid]=f"Deleted Account ({uid})"
        import json
        def make_serializable(entry):
            entry=dict(entry)
            user_id=entry.get("user_id")
            if user_id: entry["user_name"]=user_names.get(user_id)
            if hasattr(user_id, "user_id"): entry["user_id"]=user_id.user_id
            elif isinstance(user_id, (int, str)): entry["user_id"]=user_id
            elif user_id is not None: entry["user_id"]=str(user_id)
            else: entry["user_id"]=None
            if "message_id" in entry and entry["message_id"] is not None:
                try: entry["message_id"]=int(entry["message_id"])
                except (ValueError, TypeError): entry["message_id"]=None
            return entry
        serializable_hist=[make_serializable(e) for e in hist]
        data=json.dumps(serializable_hist, ensure_ascii=False, indent=2)
        file_suffix="gauto_history" if gauto_mode else "history"
        file=io.BytesIO(data.encode("utf-8"))
        file.name=f"gemini_{file_suffix}_{chat_id}.json"
        caption="Экспорт истории gauto Gemini" if gauto_mode else "Экспорт памяти Gemini"
        await self.client.send_file(message.chat_id, file, caption=caption)

    @loader.command()
    async def gmemimport(self, message: Message):
        """[auto] — импорт истории из файла (ответом). auto для gauto."""
        reply=await message.get_reply_message()
        if not reply or not reply.document: return await utils.answer(message, "Ответьте на json-файл с памятью.")
        args=utils.get_args_raw(message)
        gauto_mode=args=="auto"
        file=io.BytesIO()
        await self.client.download_media(reply, file)
        file.seek(0)
        MAX_IMPORT_SIZE=6 * 1024 * 1024
        if file.getbuffer().nbytes > MAX_IMPORT_SIZE: return await utils.answer(message, f"Файл слишком большой (>{MAX_IMPORT_SIZE // (1024*1024)} МБ).")
        import json
        try:
            hist=json.load(file)
            if not isinstance(hist, list): raise ValueError("Файл не содержит список истории.")
            new_hist=[]
            for e in hist:
                if not isinstance(e, dict) or "role" not in e or "content" not in e: raise ValueError("Некорректная структура памяти.")
                entry={"role": e["role"], "type": e.get("type", "text"), "content": e["content"], "date": e.get("date")}
                if e["role"]=="user":
                    entry["user_id"]=e.get("user_id")
                    entry["message_id"]=e.get("message_id")
                new_hist.append(entry)
            chat_id=utils.get_chat_id(message)
            conversations=self.gauto_conversations if gauto_mode else self.conversations
            conversations[str(chat_id)]=new_hist
            self._save_history_sync(gauto=gauto_mode)
            await utils.answer(message, "Память успешно импортирована.")
        except Exception as e:
            await utils.answer(message, f"Ошибка импорта: {e}")

    @loader.command()
    async def gmemfind(self, message: Message):
        """[слово] — Поиск по истории текущего чата по ключевому слову или фразе."""
        args=utils.get_args_raw(message)
        if not args: return await utils.answer(message, "Укажите слово для поиска.")
        chat_id=utils.get_chat_id(message)
        hist=self._get_structured_history(chat_id)
        found=[f"{e['role']}: {e.get('content','')[:200]}" for e in hist if args.lower() in str(e.get("content", "")).lower()]
        if not found: await utils.answer(message, "Ничего не найдено.")
        else: await utils.answer(message, "\n\n".join(found[:10]))

    @loader.command()
    async def gmemoff(self, message: Message):
        """— Отключить память в этом чате"""
        chat_id=utils.get_chat_id(message)
        self.memory_disabled_chats.add(str(chat_id))
        await utils.answer(message, "Память в этом чате отключена.")

    @loader.command()
    async def gmemon(self, message: Message):
        """— Включить память в этом чате"""
        chat_id=utils.get_chat_id(message)
        self.memory_disabled_chats.discard(str(chat_id))
        await utils.answer(message, "Память в этом чате включена.")

    @loader.command()
    async def gmemshow(self, message: Message):
        """[auto] — Показать память чата (до 20 последних запросов). auto для gauto."""
        args=utils.get_args_raw(message)
        gauto_mode=args=="auto"
        chat_id=utils.get_chat_id(message)
        hist=self._get_structured_history(chat_id, gauto=gauto_mode)
        if not hist: return await utils.answer(message, "Память пуста.")
        out=[]
        for e in hist[-40:]:
            role=e.get('role')
            content=utils.escape_html(str(e.get('content',''))[:300])
            if role=='user': out.append(f"{content}")
            elif role=='model': out.append(f"<b>Gemini:</b> {content}")
        text="<blockquote expandable='true'>" + "\n".join(out) + "</blockquote>"
        await utils.answer(message, text)

    @loader.command()
    async def gmodel(self, message: Message):
        """[model или пусто] — Узнать/сменить модель"""
        args=utils.get_args_raw(message)
        if not args: await utils.answer(message, f"Текущая модель: <code>{self.config['model_name']}</code>"); return
        args_str=str(args).strip()
        self.config["model_name"]=args_str
        await utils.answer(message, f"Модель Gemini установлена: <code>{args_str}</code>")

    @loader.command()
    async def gres(self, message: Message):
        """[auto] — Очистить ВСЮ память. auto для всей памяти gauto."""
        args=utils.get_args_raw(message)
        if args=="auto":
            if not self.gauto_conversations: return await utils.answer(message, self.strings["no_gauto_memory_to_fully_clear"])
            num_chats=len(self.gauto_conversations)
            self.gauto_conversations.clear()
            self._save_history_sync(gauto=True)
            await utils.answer(message, self.strings["gauto_memory_fully_cleared"].format(num_chats))
        elif not args:
            if not self.conversations: return await utils.answer(message, self.strings["no_memory_to_fully_clear"])
            num_chats=len(self.conversations)
            self.conversations.clear()
            self._save_history_sync(gauto=False)
            await utils.answer(message, self.strings["memory_fully_cleared"].format(num_chats))
        else:
            await utils.answer(message, self.strings["gres_usage"])
    def _configure_proxy(self):
        for var in ["http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY"]: os.environ.pop(var, None)
        if self.config["proxy"]:
            os.environ["http_proxy"]=self.config["proxy"]
            os.environ["https_proxy"]=self.config["proxy"]

    async def client_ready(self, client, db):
        self.client=client
        self.db=db
        self.me=await client.get_me()
        self.conversations=self._load_history_from_db(DB_HISTORY_KEY)
        self.gauto_conversations=self._load_history_from_db(DB_GAUTO_HISTORY_KEY)
        self.impersonation_chats=set(self.db.get(self.strings["name"], DB_IMPERSONATION_KEY, []))
        self.safety_settings=[{"category": c, "threshold": "BLOCK_NONE"} for c in ["HARM_CATEGORY_HARASSMENT", "HARM_CATEGORY_HATE_SPEECH", "HARM_CATEGORY_SEXUALLY_EXPLICIT", "HARM_CATEGORY_DANGEROUS_CONTENT"]]
        self._configure_proxy()
        if not self.config["api_key"]: logger.warning("Gemini: API ключ не настроен!")

    @loader.watcher(only_incoming=True, ignore_edited=True)
    async def watcher(self, message: Message):
        if not isinstance(message, types.Message) or not hasattr(message, 'chat_id'): return
        chat_id=utils.get_chat_id(message)
        if chat_id not in self.impersonation_chats: return
        if message.out or (message.from_id and message.from_id.user_id==self.me.id) or (message.text and message.text.startswith(self.get_prefix())): return
        sender=await message.get_sender()
        if not sender or sender.bot: return
        if random.random() > self.config["impersonation_reply_chance"]: return
        parts, warnings=await self._prepare_parts(message)
        if warnings: logger.warning(f"Gauto watcher warnings: {warnings}")
        if not parts: return
        response_text=await self._send_to_gemini(message=message, parts=parts, impersonation_mode=True)
        if response_text and response_text.strip():
            await asyncio.sleep(random.uniform(1.0, 2.5))
            await message.reply(response_text.strip())
    def _load_history_from_db(self, db_key: str) -> dict:
        raw_conversations=self.db.get(self.strings["name"], db_key, {})
        if not isinstance(raw_conversations, dict):
            logger.warning(f"Gemini: БД для ключа '{db_key}' повреждена, сбрасываю.")
            raw_conversations={}; self.db.set(self.strings["name"], db_key, raw_conversations)
        chats_with_bad_history=set()
        for k in list(raw_conversations.keys()):
            v=raw_conversations[k]
            if not isinstance(v, list):
                chats_with_bad_history.add(k)
                raw_conversations[k]=[]
            else:
                filtered, bad_found=[], False
                for e in v:
                    if isinstance(e, dict) and "role" in e and "content" in e: filtered.append(e)
                    else: bad_found=True
                if bad_found: chats_with_bad_history.add(k)
                raw_conversations[k]=filtered
        if chats_with_bad_history: logger.warning(f"Gemini ({db_key}): Некорректная структура памяти в {len(chats_with_bad_history)} чатах. Некорректные записи пропущены.")
        return raw_conversations
    def _save_history_sync(self, gauto: bool=False):
        if getattr(self, "_db_broken", False): return
        conversations_to_save, db_key=(self.gauto_conversations, DB_GAUTO_HISTORY_KEY) if gauto else (self.conversations, DB_HISTORY_KEY)
        try: self.db.set(self.strings["name"], db_key, conversations_to_save)
        except Exception as e:
            logger.error(f"Ошибка сохранения истории Gemini (gauto={gauto}): {e}")
            self._db_broken=True
    def _get_structured_history(self, chat_id: int, gauto: bool=False) -> list:
        conversations=self.gauto_conversations if gauto else self.conversations
        hist=conversations.get(str(chat_id), [])
        if not isinstance(hist, list):
            logger.warning(f"Память для чата {chat_id} (gauto={gauto}) повреждена, сбрасываю.")
            hist=[]
            conversations[str(chat_id)]=hist
            self._save_history_sync(gauto)
        return hist
    def _update_history(self, chat_id: int, user_parts: list, model_response: str, regeneration: bool=False, message: Message=None, gauto: bool=False):
        if not self._is_memory_enabled(str(chat_id)): return
        history=self._get_structured_history(chat_id, gauto)
        now=int(asyncio.get_event_loop().time())
        user_id=get_peer_id(getattr(message, "from_id", None)) if message else self.me.id
        message_id=getattr(message, "id", None)
        user_text=" ".join([p.text for p in user_parts if hasattr(p, 'text') and p.text]) or "[ответ на медиа]"
        if regeneration:
            for i in range(len(history) - 1, -1, -1):
                if history[i].get("role")=="model":
                    history[i].update({"content": model_response, "date": now}); break
        else:
            history.extend([{"role": "user", "type": "text", "content": user_text, "date": now, "user_id": user_id, "message_id": message_id}, {"role": "model", "type": "text", "content": model_response, "date": now}])
        max_len=self.config["max_history_length"]
        if max_len > 0 and len(history) > max_len*2: history=history[-(max_len*2):]
        conversations=self.gauto_conversations if gauto else self.conversations
        conversations[str(chat_id)]=history
        self._save_history_sync(gauto)
    def _clear_history(self, chat_id: int, gauto: bool=False):
        conversations=self.gauto_conversations if gauto else self.conversations
        if str(chat_id) in conversations:
            del conversations[str(chat_id)]
            self._save_history_sync(gauto)
    def _handle_error(self, e: Exception) -> str:
        logger.exception("Gemini execution error")
        if isinstance(e, asyncio.TimeoutError): return self.strings["api_timeout"]
        if isinstance(e, google_exceptions.GoogleAPIError):
            msg=str(e)
            if "quota" in msg.lower() or "exceeded" in msg.lower():
                model_name_match=re.search(r'key: "model"\s+value: "([^"]+)"', msg)
                model_name=model_name_match.group(1) if model_name_match else self.config['model_name']
                return 
            (
            f"❗️ <b>Превышен лимит Google Gemini API для модели <code>{utils.escape_html(model_name)}</code>.",
            "</b>\n\nЧаще всего это происходит на бесплатном тарифе. Вы можете:\n ",
            "• Подождать, пока лимит сбросится (обычно раз в сутки).\n ",
            "• Проверить свой тарифный план в <a href='https://aistudio.google.com/app/billing'>Google AI Studio</a>.\n ",
            "• Узнать больше о лимитах <a href='https://ai.google.dev/gemini-api/docs/rate-limits'>здесь</a>.\n\n",
            "<b>Детали ошибки:</b>\n<code>{utils.escape_html(msg)}</code>"
            )
        
            if "500 An internal error has occurred" in msg: return 
            (
            "❗️ <b>Ошибка 500 от Google API.</b>\n"
            "Это значит, что формат медиа (файл или еще что то) который ты отправил, не поддерживается.\n"
            "Такое случается, по такой причине:\n  "
            "• Если формат файла в принципе не поддерживается Gemini/Гуглом.\n  "
            "• Временный сбой на серверах Google. Попробуйте повторить запрос позже."
            )
        
            if "User location is not supported for the API use" in msg or "location is not supported" in msg: return (
            "❗️ <b>В данном регионе Gemini API не доступен.</b>\n",
            "Скачайте VPN (для пк/тел) или поставьте прокси (платный/бесплатный).\n",
            "Или воспользуйтесь инструкцией <a href=\"https://t.me/SenkoGuardianModules/23\">вот тут</a>\n",
            "А для тех у кого UserLand инструкция <a href=\"https://t.me/SenkoGuardianModules/35\">тут</a>\n"
            )
        
            if "API key not valid" in msg: return self.strings["no_api_key"]
            if "blocked" in msg.lower(): return self.strings["blocked_error"].format(utils.escape_html(msg))
            return self.strings["api_error"].format(utils.escape_html(msg))
        if isinstance(e, (OSError, aiohttp.ClientError, socket.timeout)): return "❗️ <b>Сетевая ошибка:</b>\n<code>{}</code>".format(utils.escape_html(str(e)))
        msg=str(e)
        if "No API_KEY or ADC found" in msg or "GOOGLE_API_KEY environment variable" in msg or "genai.configure(api_key" in msg: return
        (
        "❗️ <b>API ключ не найден.</b>\n "
        "Получить ключ можно тут: <a href=\"https://aistudio.google.com/apikey\">https://aistudio.google.com/apikey</a>\n "
        "<b>Поставить API ключ сюда</b>: <code>.cfg gemini api_key</code>"
        )
        return self.strings["generic_error"].format(utils.escape_html(str(e)))

    async def _prepare_parts(self, message: Message, custom_text: str=None):
        final_parts, warnings=[], []
        prompt_text_chunks=[]
        user_args=custom_text if custom_text is not None else utils.get_args_raw(message)
        reply=await message.get_reply_message()
        if reply and reply.text:
            try:
                reply_sender=await reply.get_sender()
                reply_author_name=get_display_name(reply_sender) if reply_sender else "Unknown"
                prompt_text_chunks.append(f"{reply_author_name}: {reply.text}")
            except Exception: prompt_text_chunks.append(f"Ответ на: {reply.text}")
        try:
            current_sender=await message.get_sender()
            current_user_name=get_display_name(current_sender) if current_sender else "User"
            prompt_text_chunks.append(f"{current_user_name}: {user_args or ''}")
        except Exception: prompt_text_chunks.append(f"Запрос: {user_args or ''}")
        media_source=message if message.media or message.sticker else reply
        has_media=bool(media_source and (media_source.media or media_source.sticker))
        if has_media:
            MAX_IMAGE_SIZE=48 * 1024 * 1024
            if media_source.sticker and hasattr(media_source.sticker, 'mime_type') and media_source.sticker.mime_type=='application/x-tgsticker':
                alt_text=next((attr.alt for attr in media_source.sticker.attributes if isinstance(attr, types.DocumentAttributeSticker)), "?")
                prompt_text_chunks.append(f"[Отправлен анимированный стикер: {alt_text}]")
            else:
                media=media_source.media
                mime_type, filename="application/octet-stream", "file"
                if media_source.photo: mime_type="image/jpeg"
                elif hasattr(media_source, "document") and media_source.document:
                    mime_type=getattr(media_source.document, "mime_type", mime_type)
                    doc_attr=next((attr for attr in media_source.document.attributes if isinstance(attr, DocumentAttributeFilename)), None)
                    if doc_attr: filename=doc_attr.file_name
                if mime_type.startswith("image/"):
                    try:
                        byte_io=io.BytesIO()
                        await self.client.download_media(media, byte_io)
                        if byte_io.tell() < MAX_IMAGE_SIZE:
                            byte_io.seek(0)
                            final_parts.append(glm.Part(inline_data=glm.Blob(mime_type=mime_type, data=byte_io.getvalue())))
                        else: warnings.append(f"⚠️ Изображение '{filename}' слишком большое (> {MAX_IMAGE_SIZE // 1024 // 1024} МБ).")
                    except Exception as e: warnings.append(f"⚠️ Ошибка обработки изображения '{filename}': {e}")
                elif mime_type in self.TEXT_MIME_TYPES or filename.split('.')[-1] in ('txt', 'py', 'js', 'json', 'md', 'html', 'css', 'sh'):
                    try:
                        MAX_TEXT_SIZE=1 * 1024 * 1024
                        if hasattr(media_source, "document") and media_source.document and media_source.document.size > MAX_TEXT_SIZE: warnings.append(f"⚠️ Текстовый файл '{filename}' слишком большой (> {MAX_TEXT_SIZE // 1024 // 1024} МБ).")
                        else:
                            byte_io=io.BytesIO()
                            await self.client.download_media(media, byte_io)
                            byte_io.seek(0)
                            file_content=byte_io.read().decode('utf-8')
                            prompt_text_chunks.insert(0, f"[Содержимое файла '{filename}']: \n```\n{file_content}\n```")
                    except UnicodeDecodeError: warnings.append(f"⚠️ Не удалось прочитать файл '{filename}' как текст (ошибка кодировки).")
                    except Exception as e: warnings.append(f"⚠️ Ошибка чтения файла '{filename}': {e}")
                elif mime_type.startswith(("video/", "audio/")):
                    input_path, output_path=None, None
                    try:
                        with tempfile.NamedTemporaryFile(suffix=f".{filename.split('.')[-1]}", delete=False) as temp_in: input_path=temp_in.name
                        await self.client.download_media(media, input_path)
                        if os.path.getsize(input_path) > MAX_FFMPEG_SIZE:
                            warnings.append(f"⚠️ Медиафайл '{filename}' слишком большой для конвертации (> {MAX_FFMPEG_SIZE // 1024 // 1024} МБ)."); raise StopIteration
                        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_out: output_path=temp_out.name
                        ffmpeg_cmd=["ffmpeg", "-y", "-i", input_path, "-c:v", "libx264", "-c:a", "aac", "-pix_fmt", "yuv420p", "-movflags", "+faststart", output_path]
                        process=await asyncio.create_subprocess_exec(*ffmpeg_cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
                        _, stderr=await process.communicate()
                        if process.returncode !=0:
                            stderr_str=stderr.decode()
                            if "Invalid data found when processing input" in stderr_str: warnings.append(f"⚠️ Файл '{filename}' не является валидным медиафайлом и не может быть обработан.")
                            else: warnings.append(f"⚠️ <b>Ошибка FFmpeg:</b>\nНе удалось конвертировать '{filename}'. Детали:\n<code>{utils.escape_html(stderr_str)}</code>")
                            raise StopIteration
                        with open(output_path, "rb") as f: converted_bytes=f.read()
                        final_parts.append(glm.Part(inline_data=glm.Blob(mime_type="video/mp4", data=converted_bytes)))
                    except StopIteration: pass
                    except Exception as e: warnings.append(f"⚠️ Критическая ошибка при обработке медиа '{filename}': {e}")
                    finally:
                        if input_path and os.path.exists(input_path): os.remove(input_path)
                        if output_path and os.path.exists(output_path): os.remove(output_path)
        if not user_args and has_media and not final_parts and not any("[Содержимое файла" in chunk for chunk in prompt_text_chunks): prompt_text_chunks.append(self.strings["media_reply_placeholder"])
        full_prompt_text="\n".join(chunk for chunk in prompt_text_chunks if chunk and chunk.strip()).strip()
        if full_prompt_text: final_parts.insert(0, glm.Part(text=full_prompt_text))
        return final_parts, warnings
    def _markdown_to_html(self, text: str) -> str:
        def heading_replacer(match): level=len(match.group(1)); title=match.group(2).strip(); indent="   " * (level - 1); return f"{indent}<b>{title}</b>"
        text=re.sub(r"^(#+)\s+(.*)", heading_replacer, text, flags=re.MULTILINE)
        def list_replacer(match): indent=match.group(1); return f"{indent}• "
        text=re.sub(r"^([ \t]*)[-*+]\s+", list_replacer, text, flags=re.MULTILINE)
        md=MarkdownIt("commonmark", {"html": True, "linkify": True}); md.enable("strikethrough"); md.disable("hr"); md.disable("heading"); md.disable("list")
        html_text=md.render(text)
        def format_code(match):
            lang=utils.escape_html(match.group(1).strip()); code=utils.escape_html(match.group(2).strip())
            return f'<pre><code class="language-{lang}">{code}</code></pre>' if lang else f'<pre><code>{code}</code></pre>'
        html_text=re.sub(r"```(.*?)\n([\s\S]+?)\n```", format_code, html_text)
        html_text=re.sub(r"<p>(<pre>[\s\S]*?</pre>)</p>", r"\1", html_text, flags=re.DOTALL)
        html_text=html_text.replace("<p>", "").replace("</p>", "\n").strip()
        return html_text
    def _format_response_with_smart_separation(self, text: str) -> str:
        pattern=r"(<pre.*?>[\s\S]*?</pre>)"; parts=re.split(pattern, text, flags=re.DOTALL); result_parts=[]
        for i, part in enumerate(parts):
            if not part or part.isspace(): continue
            if i % 2==1: result_parts.append(part.strip())
            else:
                stripped_part=part.strip()
                if stripped_part: result_parts.append(f'<blockquote expandable="true">{stripped_part}</blockquote>')
        return "\n".join(result_parts)
    def _get_inline_buttons(self, chat_id, base_message_id): return [[{"text": self.strings["btn_clear"], "callback": self._clear_callback, "args": (chat_id,)}, {"text": self.strings["btn_regenerate"], "callback": self._regenerate_callback, "args": (base_message_id, chat_id)}]]

    async def _safe_del_msg(self, msg, delay=1):
        await asyncio.sleep(delay)
        try: await self.client.delete_messages(msg.chat_id, msg.id)
        except Exception as e: logger.warning(f"Ошибка удаления сообщения: {e}")

    async def _clear_callback(self, call: InlineCall, chat_id: int):
        self._clear_history(chat_id, gauto=False)
        await call.edit(self.strings["memory_cleared"], reply_markup=None)

    async def _send_to_gemini(self, message, parts: list, regeneration: bool=False, call: InlineCall=None, status_msg=None, chat_id_override: int=None, impersonation_mode: bool=False, use_url_context: bool=False, display_prompt: str=None):
        msg_obj=None
        if regeneration:
            chat_id=chat_id_override; base_message_id=message
            try: msg_obj=await self.client.get_messages(chat_id, ids=base_message_id)
            except Exception: msg_obj=None
        else:
            chat_id=utils.get_chat_id(message); base_message_id=message.id; msg_obj=message
        try:
            if not self.config["api_key"]:
                if not impersonation_mode and status_msg: await utils.answer(status_msg, self.strings['no_api_key'])
                return None if impersonation_mode else ""
            genai.configure(api_key=self.config["api_key"]); tools_list=[]
            if use_url_context:
                try: tools_list.append(genai.types.Tool(url_context=genai.types.UrlContext()))
                except AttributeError: logger.error("Инструмент UrlContext не поддерживается вашей версией библиотеки.")
            system_instruction_to_use=None; api_history_content=[]
            if impersonation_mode:
                my_name=get_display_name(self.me); chat_history_text=await self._get_recent_chat_text(chat_id); system_instruction_to_use=self.config["impersonation_prompt"].format(my_name=my_name, chat_history=chat_history_text)
                raw_history=self._get_structured_history(chat_id, gauto=True); api_history_content=[glm.Content(role=e["role"], parts=[glm.Part(text=e['content'])]) for e in raw_history]
            else:
                system_instruction_val=self.config["system_instruction"]; system_instruction_to_use=(system_instruction_val.strip() if isinstance(system_instruction_val, str) else "") or None
                raw_history=self._get_structured_history(chat_id, gauto=False)
                if regeneration: raw_history=raw_history[:-2]
                api_history_content=[glm.Content(role=e["role"], parts=[glm.Part(text=e['content'])]) for e in raw_history]
            model=genai.GenerativeModel(self.config["model_name"],safety_settings=self.safety_settings,system_instruction=system_instruction_to_use)
            full_request_content=list(api_history_content)
            if not impersonation_mode:
                from datetime import datetime
                try: user_timezone=pytz.timezone(self.config["timezone"])
                except pytz.UnknownTimeZoneError: user_timezone=pytz.utc
                now=datetime.now(user_timezone); time_str=now.strftime("%Y-%m-%d %H:%M:%S %Z"); time_note=f"[System note: Current time is {time_str}]"
                text_part_found=False
                for p in parts:
                    if hasattr(p, 'text'): p.text=f"{time_note}\n\n{p.text}"; text_part_found=True; break
                if not text_part_found: parts.insert(0, glm.Part(text=time_note))
            if regeneration:
                current_turn_parts,request_text_for_display=self.last_requests.get(f"{chat_id}:{base_message_id}", (parts, "[регенерация]"))
            else:
                current_turn_parts=parts; request_text_for_display=display_prompt or (self.strings["media_reply_placeholder"] if any("inline_data" in str(p) for p in parts) else ""); self.last_requests[f"{chat_id}:{base_message_id}"]=(current_turn_parts, request_text_for_display)
            if current_turn_parts: full_request_content.append(glm.Content(role="user", parts=current_turn_parts))
            if not full_request_content and not system_instruction_to_use:
                if not impersonation_mode and status_msg: await utils.answer(status_msg, self.strings["no_prompt_or_media"])
                return None if impersonation_mode else ""
            response=await asyncio.wait_for(model.generate_content_async(full_request_content,tools=tools_list or None),timeout=GEMINI_TIMEOUT)
            result_text,was_successful="",False
            try:
                if response.prompt_feedback.block_reason: result_text=f"🚫 <b>Запрос был заблокирован Google.</b>\nПричина: <code>{response.prompt_feedback.block_reason.name}</code>."
            except AttributeError: pass
            if not result_text:
                try:
                    result_text=response.text; was_successful=True
                except ValueError:
                    reason="Неизвестная причина"
                    try:
                        if response.candidates: reason=response.candidates[0].finish_reason.name
                    except(IndexError, AttributeError): pass
                    result_text=f"❗️ Gemini не смог сгенерировать ответ.\nПричина завершения: <code>{reason}</code>."
            if was_successful and self._is_memory_enabled(str(chat_id)): self._update_history(chat_id, current_turn_parts, result_text, regeneration, msg_obj, gauto=impersonation_mode)
            if impersonation_mode: return result_text if was_successful else None
            text_from_file_present=any(p.text.startswith("[Содержимое файла") for p in parts if hasattr(p, 'text'))
            binary_file_present=any("inline_data" in str(p) for p in parts)
            file_processed=text_from_file_present or binary_file_present
            hist_len_pairs=len(self._get_structured_history(chat_id, gauto=False)) // 2; limit=self.config["max_history_length"]; mem_indicator=self.strings["memory_status_unlimited"].format(hist_len_pairs) if limit <= 0 else self.strings["memory_status"].format(hist_len_pairs, limit)
            tool_indicator=""; 
            if use_url_context: tool_indicator+="🔗 "
            if file_processed: tool_indicator+="📎 "
            question_html=f"<blockquote>{utils.escape_html(request_text_for_display[:200])}</blockquote>"; response_html=self._markdown_to_html(result_text); formatted_body=self._format_response_with_smart_separation(response_html)
            header=f"{tool_indicator.strip()}\n{mem_indicator}\n\n{self.strings['question_prefix']}\n{question_html}\n\n{self.strings['response_prefix']}\n"; text_to_send=f"{header}{formatted_body}"
            buttons=self._get_inline_buttons(chat_id, base_message_id) if self.config["interactive_buttons"] else None
            if len(text_to_send) > 4096:
                file_content=(f"Вопрос: {display_prompt}\n\n════════════════════\n\nОтвет Gemini:\n{result_text}")
                file=io.BytesIO(file_content.encode("utf-8")); file.name="Gemini_response.txt"
                if call:
                    await call.answer("Ответ слишком длинный, отправляю файлом...", show_alert=False); await self.client.send_file(call.chat_id, file, caption=self.strings["response_too_long"], reply_to=call.message_id); await call.edit(f"✅ {self.strings['response_too_long']}", reply_markup=None)
                elif status_msg:
                    await status_msg.delete(); await self.client.send_file(chat_id, file, caption=self.strings["response_too_long"], reply_to=base_message_id)
            else:
                if call: await call.edit(text_to_send, reply_markup=buttons)
                elif status_msg: await utils.answer(status_msg, text_to_send, reply_markup=buttons)
        except Exception as e:
            error_text=self._handle_error(e)
            if impersonation_mode: logger.error(f"Gemini auto-reply error: {error_text}")
            elif call: await call.edit(error_text, reply_markup=None)
            elif status_msg: await utils.answer(status_msg, error_text)
        return None if impersonation_mode else ""

    async def _regenerate_callback(self, call: InlineCall, original_message_id: int, chat_id: int):
        key=f"{chat_id}:{original_message_id}"; last_request_tuple=self.last_requests.get(key)
        if not last_request_tuple: return await call.answer(self.strings["no_last_request"], show_alert=True)
        last_parts, display_prompt=last_request_tuple; use_url_context=bool(re.search(r'https?://\S+', display_prompt))
        await self._send_to_gemini(message=original_message_id, parts=last_parts, regeneration=True, call=call, chat_id_override=chat_id, use_url_context=use_url_context, display_prompt=display_prompt)

    async def _get_recent_chat_text(self, chat_id: int, count: int=None, skip_last: bool=False) -> str:
        history_limit=count or self.config["impersonation_history_limit"]; fetch_limit=history_limit + 1 if skip_last else history_limit; chat_history_lines=[]
        try:
            messages=await self.client.get_messages(chat_id, limit=fetch_limit)
            if skip_last and messages: messages=messages[1:]
            for msg in messages:
                if not msg.text and not msg.sticker and not msg.photo and not (msg.media and not hasattr(msg.media, "webpage")): continue
                sender=await msg.get_sender(); sender_name=get_display_name(sender) if sender else "Unknown"; text_content=msg.text or ""
                if msg.sticker and hasattr(msg.sticker, 'attributes'):
                    alt_text=next((attr.alt for attr in msg.sticker.attributes if isinstance(attr, types.DocumentAttributeSticker)), None)
                    text_content+=f" [Стикер: {alt_text or '?'}]"
                elif msg.photo: text_content+=" [Фото]"
                elif msg.document and not hasattr(msg.media, "webpage"): text_content+=" [Файл]"
                if text_content.strip(): chat_history_lines.append(f"{sender_name}: {text_content.strip()}")
        except Exception as e:
            logger.warning(f"Не удалось получить историю для авто-ответа: {e}")
        return "\n".join(reversed(chat_history_lines))

    def _is_memory_enabled(self, chat_id: str) -> bool: return chat_id not in self.memory_disabled_chats
    def _disable_memory(self, chat_id: int): self.memory_disabled_chats.add(str(chat_id))
    def _enable_memory(self, chat_id: int): self.memory_disabled_chats.discard(str(chat_id))
# A
# :^
# не ну тут беспредел какой то
# ну более менее написал
# и на последнее
# кто прочитал тот гей)
