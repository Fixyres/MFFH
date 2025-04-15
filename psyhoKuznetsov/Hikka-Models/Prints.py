__version__ = (1, 0, 0)
# meta developer: @psyhomodules

from .. import loader, utils
import asyncio
from telethon import functions, types

@loader.tds
class Prints(loader.Module):
    """⌨️ Модуль для статуса 'печатает...'"""
    
    strings = {
        "name": "Prints",
        "on": "✅ <b>Статус 'печатает...' включён в чате:</b> <code>{}</code>",
        "off": "✅ <b>Статус 'печатает...' выключён в чате:</b> <code>{}</code>",
        "already_on": "⚠️ <i>Статус уже включён в чате:</i> <code>{}</code>",
        "not_found": "⚠️ <i>Чат не найден в списке активных:</i> <code>{}</code>",
        "limit_reached": "🚫 <b>Достигнут лимит чатов (20)!</b>",
        "invalid_chat": "❌ <b>Неверный ID или username чата!</b>",
        "list": "📋 <b>Список активных чатов:</b>\n{}",
        "usage_on": "❓ <b>Использование:</b> <code>.printon [id/username]</code>",
        "usage_off": "❓ <b>Использование:</b> <code>.printoff [id/username]</code>",
        "usage_list": "❓ <b>Использование:</b> <code>.printlist</code>"
    }

    strings_ru = strings

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self._db_name = "Prints"
        self.active_chats = self.get("active_chats", [])
        self._tasks = {}

        for chat_id in self.active_chats:
            asyncio.ensure_future(self._keep_typing(chat_id))

    def get(self, key, default=None):
        return self.db.get(self._db_name, key, default)
    
    def set(self, key, value):
        self.db.set(self._db_name, key, value)


    async def printoncmd(self, message):
        """⌨️ Включить статус 'печатает...' в указанном чате"""
        args = utils.get_args_raw(message)
        
        if not args:
            return await utils.answer(message, self.strings["usage_on"])
        
        if len(self.active_chats) >= 20:
            return await utils.answer(message, self.strings["limit_reached"])
        
        try:
            try:
                chat_id = int(args)
                chat_entity = await self.client.get_entity(chat_id)
            except ValueError:
                chat_entity = await self.client.get_entity(args)
                chat_id = chat_entity.id
            
            if chat_id in self.active_chats:
                return await utils.answer(message, self.strings["already_on"].format(chat_id))
            
            self.active_chats.append(chat_id)
            self.set("active_chats", self.active_chats)
            
            asyncio.ensure_future(self._keep_typing(chat_id))
            await utils.answer(message, self.strings["on"].format(chat_id))
            
        except Exception:
            await utils.answer(message, self.strings["invalid_chat"])

    async def printoffcmd(self, message):
        """⌨️ Выключить статус 'печатает...' в указанном чате"""
        args = utils.get_args_raw(message)
        
        if not args:
            return await utils.answer(message, self.strings["usage_off"])
        
        try:
            try:
                chat_id = int(args)
                chat_entity = await self.client.get_entity(chat_id)
            except ValueError:
                chat_entity = await self.client.get_entity(args)
                chat_id = chat_entity.id
            
            if chat_id not in self.active_chats:
                return await utils.answer(message, self.strings["not_found"].format(chat_id))
            
            self.active_chats.remove(chat_id)
            self.set("active_chats", self.active_chats)
            
            if chat_id in self._tasks:
                self._tasks[chat_id].cancel()
                del self._tasks[chat_id]
            
            await utils.answer(message, self.strings["off"].format(chat_id))
            
        except Exception:
            await utils.answer(message, self.strings["invalid_chat"])

    async def printlistcmd(self, message):
        """📋 Показать список активных чатов"""
        if not self.active_chats:
            await utils.answer(message, "📋 <b>Нет активных чатов.</b>")
            return
        
        chat_list = "\n".join(f"💬 <code>{chat_id}</code>" for chat_id in self.active_chats)
        await utils.answer(message, self.strings["list"].format(chat_list))

    async def _keep_typing(self, chat_id):
        self._tasks[chat_id] = asyncio.current_task()
        
        try:
            while chat_id in self.active_chats:
                try:
                    await self.client(functions.messages.SetTypingRequest(
                        peer=chat_id,
                        action=types.SendMessageTypingAction()
                    ))
                except Exception:
                    await asyncio.sleep(1)
                
                await asyncio.sleep(5)
                
        except asyncio.CancelledError:
            pass
        except Exception:
            self.active_chats.remove(chat_id)
            self.set("active_chats", self.active_chats)
