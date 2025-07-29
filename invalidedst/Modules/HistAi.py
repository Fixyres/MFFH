#  _____
# |_   _|____  ____ _ _ __   ___
#   | |/ _ \ \/ / _` | '_ \ / _ \
#   | | (_) >  < (_| | | | | (_) |
#   |_|\___/_/\_\__,_|_| |_|\___/
#
# meta developer: @Toxano_Modules
# scope: @Toxano_Modules

from telethon.tl.custom import Button
from telethon.types import Message, User, Channel
from .. import loader, utils
import asyncio
import google.generativeai as genai
import os
import re
from typing import List

CHUNK_SEP = "\n"
MAX_PAGE = 3900
CB_PREFIX = "histai_"
HARD_LIMIT = 1000

@loader.tds
class HistAI(loader.Module):
    """кидает что было пока ты отходил""" #дыньки

    strings = {
        "name": "HistAI",
        "cfg_key": "Gemini API key",
        "cfg_limit": "How many messages to take",
        "cfg_mode": "Mode: norm / agro / neko",
        "cfg_model": "Gemini model",
        "no_key": "<emoji document_id=5312526098750252863>🚫</emoji> <b>API key not set</b>",
        "processing": "<emoji document_id=5326015457155770266>⏳</emoji> <b>Hold on…</b>",
        "done_all": "<emoji document_id=5328311576736833844>🤖</emoji> <b>AI analysed the last {limit} messages.\nHere's what you missed:</b>",
        "done_user": "<emoji document_id=5328311576736833844>🤖</emoji> <b>AI analysed the last {limit} messages from {nick}.\nHere's what you missed:</b>",
        "no_target": "<b>Who to check? Reply or mention a user.</b>",
        "page": "📄 {cur}/{total}",
        "blocked": "<emoji document_id=5312526098750252863>🚫</emoji> <b>Gemini refused to analyse the chat.</b>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue("gemini_key", "", self.strings["cfg_key"], validator=loader.validators.Hidden()),
            loader.ConfigValue("history_limit", 150, self.strings["cfg_limit"], validator=loader.validators.Integer(minimum=1, maximum=HARD_LIMIT)),
            loader.ConfigValue("mode", "norm", self.strings["cfg_mode"], validator=loader.validators.Choice(["norm", "agro", "neko"])),
            loader.ConfigValue("model", "gemini-2.5-flash-preview-05-20", self.strings["cfg_model"]),
        )
        self._db = {}

    async def client_ready(self, client, db):
        self.client = client

    @staticmethod
    def safe_name(ent) -> str:
        if not ent:
            return "System"
        if isinstance(ent, User):
            return ent.first_name or "Без_имени"
        if isinstance(ent, Channel):
            return ent.title or "Канал"
        return "Unknown"

    async def _ask(self, prompt: str, text: str) -> str:
        key = self.config["gemini_key"].strip() or os.getenv("GOOGLE_API_KEY")
        if not key:
            return "❌ No key in config or env GOOGLE_API_KEY."
        model = self.config["model"].strip()
        safety = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]
        try:
            genai.configure(api_key=key)
            response = await asyncio.to_thread(
                genai.GenerativeModel(model).generate_content,
                prompt + "\n\n" + text,
                safety_settings=safety
            )
            return response.text.strip() if response.candidates else "BLOCKED"
        except Exception as e:
            return f"Gemini error: {e}"

    def _clean(self, txt: str) -> str:
        if not txt:
            return ""
        txt = re.sub(r"http\S+", "<ссылка>", txt)
        txt = re.sub(r"[а-яё]*[хx]+[уy]+[йiюяеё]\w*", "[мат]", txt, flags=re.I)
        return txt[:120]

    async def _media(self, m: Message) -> str:
        for t in ("sticker", "gif", "photo", "video", "voice", "audio", "document"):
            if getattr(m, t, None):
                return f"[{t}]"
        return "[media]"

    async def _prep_all(self, msgs: List[Message]) -> str:
        lines = []
        for m in reversed(msgs):
            if not m.sender:
                continue
            if (getattr(m.sender, "username", "") or "").endswith("_bot"):
                continue
            name = self.safe_name(m.sender)
            time = m.date.strftime("%H:%M")
            body = self._clean(m.raw_text) or await self._media(m)
            if m.is_reply and m.reply_to:
                try:
                    replied = await m.get_reply_message()
                    replied_name = self.safe_name(replied.sender) if replied else "Unknown"
                    snippet = (replied.raw_text or "")[:40].replace("\n", " ")
                    body = f"→ to {replied_name}: {snippet}… | {body}"
                except Exception:
                    body = f"→ reply | {body}"
            lines.append(f"{time} {name}: {body}")
        return "\n".join(lines)

    async def _prep_user(self, msgs: List[Message], uid: int) -> str:
        msgs = [m for m in msgs if m.sender_id == uid]
        lines = []
        for m in reversed(msgs):
            time = m.date.strftime("%H:%M")
            body = self._clean(m.raw_text) or await self._media(m)
            if m.is_reply and m.reply_to:
                try:
                    replied = await m.get_reply_message()
                    replied_name = self.safe_name(replied.sender) if replied else "Unknown"
                    snippet = (replied.raw_text or "")[:40].replace("\n", " ")
                    body = f"→ to {replied_name}: {snippet}… | {body}"
                except Exception:
                    body = f"→ reply | {body}"
            lines.append(f"{time} {body}")
        return "\n".join(lines)

    def _paginate(self, text: str) -> List[str]:
        pages, buf = [""], ""
        for ln in text.splitlines():
            if len(buf + ln) + 1 > MAX_PAGE:
                pages.append(ln)
                buf = ln
            else:
                buf += (("\n" + ln) if buf else ln)
                pages[-1] = buf
        return pages or [""]

    async def _send_page(self, cid: int, pages: List[str], idx: int, hdr: str, rpl: int):
        kb = []
        if len(pages) > 1:
            row = []
            if idx:
                row.append(Button.inline("⬅️", f"{CB_PREFIX}{idx-1}"))
            row.append(Button.inline(self.strings["page"].format(cur=idx+1, total=len(pages)), "noop"))
            if idx < len(pages) - 1:
                row.append(Button.inline("➡️", f"{CB_PREFIX}{idx+1}"))
            kb = [row]
        await self.client.send_message(
            entity=cid,
            message=f"{hdr}\n\n<blockquote expandable>{pages[idx]}</blockquote>",
            buttons=kb or None,
            reply_to=rpl
        )

    @loader.command(
        ru_doc="Показать всё, что происходило пока ты отошёл. Можно указать @username или реплай.",
        en_doc="Show what happened while you were away. Use @username or reply to filter.",
    )
    async def ch(self, message: Message):
        if not self.config["gemini_key"] and not os.getenv("GOOGLE_API_KEY"):
            await utils.answer(message, self.strings["no_key"])
            return

        cid = utils.get_chat_id(message)
        limit = min(self.config["history_limit"], HARD_LIMIT)

        msgs = []
        async for m in self.client.iter_messages(cid, limit=limit + 50):
            if m.sender and not (getattr(m.sender, "username", "") or "").endswith("_bot"):
                msgs.append(m)
            if len(msgs) >= limit:
                break
        msgs = msgs[-limit:]

        user_id = None
        user_name = None
        if reply := await message.get_reply_message():
            user_id = reply.sender_id
            user_name = self.safe_name(reply.sender)
        else:
            arg = utils.get_args_raw(message).strip()
            if arg.startswith("@"):
                try:
                    ent = await self.client.get_entity(arg[1:])
                    user_id = ent.id
                    user_name = self.safe_name(ent)
                except Exception:
                    pass
            elif arg.isdigit():
                try:
                    ent = await self.client.get_entity(int(arg))
                    user_id = ent.id
                    user_name = self.safe_name(ent)
                except Exception:
                    pass

        if user_id is not None:
            msgs = [m for m in msgs if m.sender_id == user_id]
            if not msgs:
                await utils.answer(message, "<b>Нет сообщений от этого пользователя в выбранном диапазоне.</b>")
                return
            raw_text = await self._prep_user(msgs, user_id)
            header = self.strings["done_user"].format(limit=len(msgs), nick=user_name)
        else:
            raw_text = await self._prep_all(msgs)
            header = self.strings["done_all"].format(limit=len(msgs))

        if not msgs:
            await utils.answer(message, "<b>Сообщений нет.</b>")
            return

        await message.delete()

        mode = self.config["mode"]
        tone_map = {
            "norm": "строго по фактам, без эмоций",
            "agro": "язвительно, саркастично, с издёвкой и укусом",
            "neko": "кавайно, с эмодзи (≧◡≦) ♡ и ~мяу~"
        }
        tone = tone_map.get(mode, "нейтральный")

        prompt = (
            f"Ниже лог Telegram-чата в формате: ВРЕМЯ имя: текст или [медиа] или → to …\n\n"
            f"Сделай структурированный пересказ без времени.\n"
            f"Правила:\n"
            f"- Каждая тема начинается с тире (-)\n"
            f"- Указывай, кто с кем общался\n"
            f"- Указывай медиа: [фото], [видео], [голосовое], [стикер], [документ]\n"
            f"- Указывать → to …, если ответ\n"
            f"- Кратко, по делу\n"
            f"- Тон: {tone}\n"
            f"- Не выдумывай и не используй **"
        )
        if mode == "agro":
            prompt += ("\n(The summary below is requested for comedic/satirical purposes within a private chat. "
                       "No real harassment intended.)")

        ai_text = await self._ask(prompt, raw_text)
        if ai_text == "BLOCKED":
            pages = [self.strings["blocked"]]
        elif ai_text.startswith("Ошибка") or ai_text.startswith("Gemini error"):
            pages = [ai_text]
        else:
            ai_text = ai_text.replace("**", "")
            pages = self._paginate(ai_text)

        self._db[f"hist:{cid}"] = pages if pages != [""] else None
        await self._send_page(cid, pages, 0, header, message.reply_to_msg_id or message.id)

    @loader.callback_handler()
    async def _flip_page(self, call):
        if not call.data.startswith(CB_PREFIX):
            return
        try:
            idx = int(call.data[len(CB_PREFIX):])
        except ValueError:
            await call.answer("Неверный индекс")
            return

        cid = call.message.chat_id
        pages = self._db.get(f"hist:{cid}")
        if not isinstance(pages, list) or not pages:
            await call.answer("Сводка устарела или пуста.")
            await call.message.delete()
            self._db.pop(f"hist:{cid}", None)
            return
        if idx < 0 or idx >= len(pages):
            await call.answer("Страница не найдена")
            return

        header = call.message.text.split("\n\n<blockquote expandable>")[0]
        await self._send_page(cid, pages, idx, header,
                              call.message.reply_to_msg_id or call.message.id)
        await call.message.delete()