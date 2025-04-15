__version__ = (1, 0, 0)
# meta developer: @psyhomodules

from .. import loader, utils
from telethon.tl.types import PeerUser, Channel
import asyncio
import random
from telethon.errors import FloodWaitError
from telethon import functions, types
import logging

@loader.tds
class MentionInAllChatsMod(loader.Module):
    """Модуль для упоминания пользовалей во всех общих чатах"""
    strings = {
        "name": "MentionChat",
        "started": "<b>🚀 Поиск общих групп запущен...</b>",
        "sending": "<b>📲 Отправляю упоминания в {} общих группах</b>",
        "done": "<b>✨ Упоминания отправлены в {} групп успешно!</b>",
        "no_user": "<b>❌ Укажи ID, username или ответь на сообщение</b>",
        "no_common_chats": "<b>😔 Нет общих групп с этим пользователем</b>",
        "flood_wait": "<b>⏳ FloodWait: ждем {} секунд</b>",
        "progress": "<b>📊 Прогресс: {}/{} групп</b>"
    }

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.emojis = ["✅", "🔥", "💥", "⚡", "💫", "🌟", "💯", "🔆", "💪", "👍", "🎯", "🚀", "⭐", "💢", "💦", "💣"]


    async def get_common_chats(self, user_id):
        try:
            common = await self.client(functions.messages.GetCommonChatsRequest(
                user_id=user_id,
                max_id=0,
                limit=100
            ))
            return [chat for chat in common.chats if not isinstance(chat, Channel) or not chat.broadcast]
        except Exception as e:
            logging.error(f"Error getting common chats: {e}")
            return await self.get_common_chats_manual(user_id)
    
    async def get_common_chats_manual(self, user_id):
        common_chats = []
        async for dialog in self.client.iter_dialogs():
            if dialog.is_group and not dialog.is_channel:
                try:
                    participants = await self.client.get_participants(dialog, limit=1)
                    full_chat = await self.client(functions.messages.GetFullChatRequest(chat_id=dialog.id))
                    for participant in full_chat.users:
                        if participant.id == user_id:
                            common_chats.append(dialog.entity)
                            break
                except Exception:
                    continue
        return common_chats

    def get_random_emoji_mention(self, user_id):
        emoji = random.choice(self.emojis)
        return f'<a href="tg://user?id={user_id}">{emoji}</a>'

    @loader.command()
    async def mn(self, message):
        """Упомянуть пользователя во всех общих группах - .mn [ID/reply/username] [текст]"""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        
        status_msg = await utils.answer(message, self.strings["started"])
        if isinstance(status_msg, list):
            status_msg = status_msg[0]
            
        user_id = None
        if reply and reply.from_id:
            if isinstance(reply.from_id, PeerUser):
                user_id = reply.from_id.user_id
            else:
                await utils.answer(status_msg, self.strings["no_user"])
                return
        elif args:
            parts = args.split(maxsplit=1)
            user_input = parts[0]
            
            try:
                if user_input.isdigit():
                    user_id = int(user_input)
                else:
                    user = await self.client.get_entity(user_input)
                    user_id = user.id
            except Exception:
                await utils.answer(status_msg, self.strings["no_user"])
                return
        else:
            await utils.answer(status_msg, self.strings["no_user"])
            return
            
        text = args.split(maxsplit=1)[1] if len(args.split()) > 1 else ""
        
        if text:
            if not (text.startswith("<b>") and text.endswith("</b>")):
                text = f"<b>{text}</b>"
        
        common_chats = await self.get_common_chats(user_id)
        
        if not common_chats:
            await utils.answer(status_msg, self.strings["no_common_chats"])
            return
        
        await utils.answer(status_msg, self.strings["sending"].format(len(common_chats)))
        
        success_count = 0
        total_common = len(common_chats)
        
        for i, chat in enumerate(common_chats):
            try:
                emoji_mention = self.get_random_emoji_mention(user_id)
                
                if reply and i == 0: 
 
                    mention_text = f"{emoji_mention} {text}"
                    await self.client.send_message(
                        chat, 
                        mention_text, 
                        parse_mode="HTML", 
                        reply_to=await self._get_reply_in_chat(chat.id, reply)
                    )
                else:
                    mention_text = f"{emoji_mention} {text}"
                    await self.client.send_message(chat, mention_text, parse_mode="HTML")
                
                success_count += 1
                
                if (i + 1) % 10 == 0 or i == len(common_chats) - 1:
                    await utils.answer(
                        status_msg, 
                        self.strings["progress"].format(success_count, total_common)
                    )
                

                await asyncio.sleep(0.5)
                
            except FloodWaitError as e:
                wait_time = e.seconds
                await utils.answer(
                    status_msg, 
                    self.strings["flood_wait"].format(wait_time)
                )
                await asyncio.sleep(wait_time)
                
                try:
                    emoji_mention = self.get_random_emoji_mention(user_id)
                    mention_text = f"{emoji_mention} {text}"
                    await self.client.send_message(chat, mention_text, parse_mode="HTML")
                    success_count += 1
                except Exception:
                    pass
                    
            except Exception as e:
                logging.error(f"Error sending to chat {chat.id}: {str(e)}")
                pass
            
        await utils.answer(status_msg, self.strings["done"].format(success_count))
    
    async def _get_reply_in_chat(self, chat_id, reply_msg):
        try:
            if hasattr(reply_msg, 'message') and reply_msg.message:
                async for msg in self.client.iter_messages(
                    chat_id, 
                    limit=100, 
                    search=reply_msg.message
                ):
                    if msg.message == reply_msg.message:
                        return msg.id
            return None
        except Exception:
            return None
