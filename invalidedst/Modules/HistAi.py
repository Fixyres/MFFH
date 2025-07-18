#  _____
# |_   _|____  ____ _ _ __   ___
#   | |/ _ \ \/ / _` | '_ \ / _ \
#   | | (_) >  < (_| | | | | (_) |
#   |_|\___/_/\_\__,_|_| |_|\___/
#
# meta developer: @Toxano_Modules
# scope: @Toxano_Modules

from telethon.tl.custom import Button
from telethon.types import Message
from .. import loader, utils
import asyncio
import google.generativeai as genai
from typing import List, Optional

CHUNK_SEP = "\n"
MAX_PAGE  = 3900
CB_PREFIX = "histai_"     

@loader.tds
class HistAI(loader.Module):
    """кидает что было пока ты отходил"""

    strings = {
        "name": "HistAI",
        "cfg_key": "Ключ Gemini",
        "cfg_limit": "Сколько сообщений брать",
        "cfg_mode": "Режим: agro / norm",
        "no_key": "<emoji document_id=5312526098750252863>🚫</emoji> <b>Ключ Gemini не задан</b>",
        "processing": "<emoji document_id=5326015457155770266>⏳</emoji> <b>Ща чекну…</b>",
        "done_all": "<emoji document_id=5328311576736833844>🤖</emoji> <b>AI проанализировал последние {limit} сообщений.\nВот что вы пропустили:</b>",
        "done_user": "<emoji document_id=5328311576736833844>🤖</emoji> <b>AI проанализировал последние {limit} сообщений от {nick}.\nВот что вы пропустили:</b>",
        "no_target": "<b>Кого чекать? Укажи @username или реплай.</b>",
        "page": "📄 {cur}/{total}",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue("gemini_key", "", self.strings["cfg_key"], validator=loader.validators.Hidden()),
            loader.ConfigValue("history_limit", 250, self.strings["cfg_limit"], validator=loader.validators.Integer(minimum=1, maximum=1000)),
            loader.ConfigValue("mode", "norm", self.strings["cfg_mode"], validator=loader.validators.Choice(["norm", "agro"])),
        )
        self._db = {}

    async def client_ready(self, client, db):
        self.client = client
        if self.config["gemini_key"]:
            genai.configure(api_key=self.config["gemini_key"])

    async def _ask(self, prompt: str, text: str) -> str:
        try:
            return (await asyncio.to_thread(
                genai.GenerativeModel("gemini-2.0-flash").generate_content,
                prompt + "\n\n" + text
            )).text.strip()
        except Exception as e:
            return f"Ошибка Gemini: {e}"

    def _prep_all(self, msgs: List[Message]) -> str:
        lines = []
        for msg in reversed(msgs):
            if msg.sender and str(getattr(msg.sender, "username", "") or "").endswith("_bot"):
                continue
            nick = str(getattr(msg.sender, "first_name", "") or str(getattr(msg.sender, "id", "Unknown")))
            content = self._content_repr(msg)
            lines.append(f"{nick}: {content}")
        return "\n".join(lines)

    def _prep_user(self, msgs: List[Message], user_id: int, user_name: str) -> str:
        lines = []
        for msg in reversed(msgs):
            if msg.sender_id != user_id:
                continue
            lines.append(self._content_repr(msg))
        return "\n".join(lines)

    def _content_repr(self, msg: Message) -> str:
        if msg.sticker:      return "[стикер]"
        if msg.gif:          return "[гиф]"
        if msg.photo:        return "[фото]"
        if msg.video:        return "[видео]"
        if msg.video_note:   return "[видео-кружок]"
        if msg.voice:        return "[голосовуха]"
        if msg.audio:        return "[аудио]"
        if msg.document:     return "[файл]"
        return (msg.raw_text or "").strip()

    def _paginate(self, text: str) -> List[str]:
        pages = []
        for line in text.splitlines():
            if not pages or len(pages[-1]) + len(line) + 1 > MAX_PAGE:
                pages.append(line)
            else:
                pages[-1] += "\n" + line
        return pages or [""]

    async def _send_page(self, chat_id: int, pages: List[str], idx: int, header: str, reply_to: int):
        kb = []
        if len(pages) > 1:
            row = []
            if idx > 0:
                row.append(Button.inline("⬅️", f"{CB_PREFIX}{idx-1}"))
            row.append(Button.inline(self.strings["page"].format(cur=idx+1, total=len(pages)), "noop"))
            if idx < len(pages) - 1:
                row.append(Button.inline("➡️", f"{CB_PREFIX}{idx+1}"))
            kb = [row]
        await self.client.send_message(
            entity=chat_id,
            message=f"{header}\n\n<blockquote expandable>{pages[idx]}</blockquote>",
            buttons=kb or None,
            reply_to=reply_to
        )

    @loader.command(
        ru_doc="Показать всё, что происходило пока ты отошёл. Можно указать @username или реплай.",
        en_doc="Show what happened while you were away. Use @username or reply to filter.",
    )
    async def ch(self, message: Message):
        """.ch (@username / reply) — конкретный юзер
        .ch — вся история"""
        if not self.config["gemini_key"]:
            await utils.answer(message, self.strings["no_key"])
            return

        chat_id = utils.get_chat_id(message)
        limit = self.config["history_limit"]
        msgs = [m async for m in self.client.iter_messages(chat_id, limit=limit)]
        if not msgs:
            await utils.answer(message, "<b>Сообщений нет.</b>")
            return

        await message.delete()
        user_id: Optional[int] = None
        user_name: str = ""
        reply = await message.get_reply_message()

        if reply and reply.sender:
            user_id = reply.sender_id
            user_name = reply.sender.first_name or str(reply.sender.id)
        else:
            args = utils.get_args_raw(message).strip()
            if args.startswith("@"):
                username = args[1:]
                try:
                    ent = await self.client.get_entity(username)
                    user_id = ent.id
                    user_name = ent.first_name or str(ent.id)
                except Exception:
                    user_id = None
            elif args.isdigit():
                user_id = int(args)
                try:
                    ent = await self.client.get_entity(user_id)
                    user_name = ent.first_name or str(ent.id)
                except Exception:
                    user_id = None

        if user_id is None:
            text = self._prep_all(msgs)
            header = self.strings["done_all"].format(limit=limit)
            prompt = (
                f"Сделай краткую, сжатую сводку, объединяя повторы и технические провалы в одну фразу.\n"
                f"Каждый пункт начинай с «- » и указывай только имя без @.\n"
                f"Учитывай текст, фото и файлы (кратко: [фото], [файл] и т.д.).\n"
                f"{'Можешь материться и быть язвительным.' if self.config['mode'] == 'agro' else 'Без мата.'}"
            )
            res = await self._ask(prompt, text)
            pages = self._paginate(res)
        else:
            text = self._prep_user(msgs, user_id, user_name)
            header = self.strings["done_user"].format(limit=limit, nick=user_name)
            prompt = (
                f"Сделай краткую, сжатую сводку сообщений пользователя, объединяя повторы.\n"
                f"Каждый пункт начинай с «- ».\n"
                f"Учитывай текст, фото и файлы (кратко: [фото], [файл] и т.д.).\n"
                f"{'Можешь материться и быть язвительным.' if self.config['mode'] == 'agro' else 'Без мата.'}"
            )
            res = await self._ask(prompt, text)
            pages = self._paginate(res)

        if pages and pages != [""]:
            self._db[f"hist:{chat_id}"] = pages
        else:
            self._db.pop(f"hist:{chat_id}", None)

        await self._send_page(chat_id, pages, 0, header, message.reply_to_msg_id or message.id)

    @loader.callback_handler()
    async def _flip_page(self, call):
        if not call.data.startswith(CB_PREFIX):
            return   # хуй

        try:
            idx = int(call.data[len(CB_PREFIX):])
        except ValueError:
            await call.answer("Неверный индекс")
            return

        chat_id = call.message.chat_id
        pages = self._db.get(f"hist:{chat_id}")

        if not isinstance(pages, list) or not pages:
            await call.answer("Сводка устарела или пуста.")
            await call.message.delete()
            self._db.pop(f"hist:{chat_id}", None)
            return

        if idx < 0 or idx >= len(pages):
            await call.answer("Страница не найдена")
            return

        header = call.message.text.split("\n\n<blockquote expandable>")[0]
        await self._send_page(chat_id, pages, idx, header,
                              call.message.reply_to_msg_id or call.message.id)
        await call.message.delete()
