#  This file is part of SenkoGuardianModules
#  Copyright (c) 2025 Senko
#  This software is released under the MIT License.
#  https://opensource.org/licenses/MIT

# meta developer: @SenkoGuardianModules

import asyncio
import random
import re

from .. import loader, utils
from herokutl.tl.functions.payments import GetSavedStarGiftsRequest
from herokutl.tl.functions.channels import GetFullChannelRequest
from herokutl.tl.types import Message, StarGiftUnique, Channel
from herokutl.errors.rpcerrorlist import DocumentInvalidError, FloodWaitError, ChatAdminRequiredError
from telethon.utils import get_display_name

@loader.tds
class GiftFinderMod(loader.Module):
    """Парсер пользователей с NFT-подарками в чате."""
    strings = {
        "name": "GiftFinder",
        "not_a_chat": "🚫 <b>Не удалось найти указанный чат.</b>",
        "scanning": "<emoji document_id=5464429933543628237>⏳</emoji> <b>Сканирую участников...</b>",
        "scanning_supplement": "<emoji document_id=5464429933543628237>⏳</emoji> <b>Список участников неполон. Дополнительно сканирую сообщения...</b>",
        "scanning_messages_only": "<emoji document_id=5464429933543628237>⏳</emoji> <b>Участники скрыты. Сканирую только сообщения...</b>",
        "header": "<emoji document_id=5237868881267153432>🔖</emoji> Те у кого есть НФТ подарки:",
        "premium_star": "<emoji document_id=5274026806477857971>⭐️</emoji>",
        "flood_wait": "\n<emoji document_id=5212102117953384237>😖</emoji> Поймал FloodWait на {} секунд. Увеличиваю задержку и жду...",
        "scanning_safe": "⏳ <b>Сканирую участников...</b>",
        "scanning_supplement_safe": "⏳ <b>Список участников неполон. Дополнительно сканирую сообщения...</b>",
        "scanning_messages_only_safe": "⏳ <b>Участники скрыты. Сканирую только сообщения...</b>",
        "flood_wait_safe": "\n😖 Поймал FloodWait на {} секунд. Увеличиваю задержку и жду...",
        "no_users_found": "🚫 <b>В этом чате не найдено пользователей с NFT-подарками.</b>",
    }

    async def _safe_edit(self, msg: Message, text_premium: str, text_safe: str):
        try:
            await msg.edit(text_premium)
        except DocumentInvalidError:
            await msg.edit(text_safe)
        except Exception:
            pass

    async def giftscancmd(self, message: Message):
        """
        Ищет пользователей с NFT-подарками в чате.
        Использование: .giftscan [лимит] или .giftscan [ID чата] [лимит]
        """
        args = utils.get_args_raw(message)
        chat_arg = None
        msgs_limit = 3000
        if args:
            parts = args.split()
            first_arg = parts[0]
            if first_arg.lstrip('-').isdigit():
                chat_arg = int(first_arg)
                if len(parts) > 1 and parts[1].isdigit():
                    msgs_limit = int(parts[1])
            else:
                chat_arg = first_arg
                if len(parts) > 1 and parts[1].isdigit():
                    msgs_limit = int(parts[1])
        if not chat_arg and args and args.isdigit():
            msgs_limit = int(args)
        try:
            msg = await utils.answer(message, self.strings("scanning"))
        except DocumentInvalidError:
            msg = await utils.answer(message, self.strings("scanning_safe"))
        try:
            chat = await self.client.get_entity(chat_arg) if chat_arg is not None else await message.get_chat()
        except Exception:
            await self._safe_edit(msg, self.strings("not_a_chat"), self.strings("not_a_chat"))
            return
        user_ids = set()
        scan_messages_mode = False
        try:
            if isinstance(chat, Channel):
                full_chat = await self.client(GetFullChannelRequest(channel=chat))
                total_participants = full_chat.full_chat.participants_count
            else:
                total_participants = chat.participants_count
            participants = await self.client.get_participants(chat, limit=None)
            user_ids.update(user.id for user in participants)
            if len(participants) < total_participants:
                scan_messages_mode = True
                await self._safe_edit(msg, self.strings("scanning_supplement"), self.strings("scanning_supplement_safe"))
        except (ChatAdminRequiredError, AttributeError, TypeError, ValueError):
            scan_messages_mode = True
            await self._safe_edit(msg, self.strings("scanning_messages_only"), self.strings("scanning_messages_only_safe"))
        if scan_messages_mode:
            async for m in self.client.iter_messages(chat, limit=msgs_limit):
                if m.from_id and hasattr(m.from_id, 'user_id'):
                    user_ids.add(m.from_id.user_id)
        found_users = []
        base_delay_min, base_delay_max, flood_penalty = 0.5, 1.5, 0.0
        for user_id in user_ids:
            try:
                user = await self.client.get_entity(user_id)
                if user.bot or user.is_self: continue
            except Exception: continue
            await asyncio.sleep(random.uniform(base_delay_min + flood_penalty, base_delay_max + flood_penalty))
            while True:
                try:
                    all_gifts = await self.client(GetSavedStarGiftsRequest(peer=user, offset="", limit=100))
                    if gifts := [g for g in all_gifts.gifts if isinstance(g.gift, StarGiftUnique)]:
                        raw_name = get_display_name(user)
                        s_name = re.sub(r'[\u2066-\u2069\u200e\u200f\u202a-\u202e\u3164\u115f\u2800]', '', raw_name).strip()
                        link_text = f"@{user.username}" if not s_name and user.username else (f"User ID: {user.id}" if not s_name else utils.escape_html(s_name))
                        link = f'<a href="https://t.me/{user.username}">{link_text}</a>' if user.username else f'<a href="tg://user?id={user.id}">{link_text}</a>'
                        p_icon = self.strings('premium_star') if getattr(user, 'premium', False) else ""
                        found_users.append(f"• {p_icon} {link}  -  {len(gifts)}")
                    break
                except FloodWaitError as e:
                    current_text = (await self.client.get_messages(msg.chat_id, ids=msg.id)).text
                    premium_text = current_text + self.strings("flood_wait").format(e.seconds)
                    safe_text = current_text + self.strings("flood_wait_safe").format(e.seconds)
                    await self._safe_edit(msg, premium_text, safe_text)
                    flood_penalty += 0.2
                    await asyncio.sleep(e.seconds)
                    continue
                except Exception: break
        if not found_users:
            await self._safe_edit(msg, self.strings("no_users_found"), self.strings("no_users_found"))
            return
        user_list = "\n".join(found_users)
        response_text = f"{self.strings('header')}\n<blockquote expandable>{user_list}</blockquote>"
        safe_header = "🔖 " + self.strings("header").split("</emoji>")[1]
        safe_list = [line.replace(self.strings("premium_star"), "⭐️") for line in found_users]
        safe_user_list = '\n'.join(safe_list)
        response_text_safe = f"{safe_header}\n<blockquote expandable>{safe_user_list}</blockquote>"
        await self._safe_edit(msg, response_text, response_text_safe)
        # горе кодер
