
# meta developer: @mwmodules & @Zeen17i & @mwoffice
# meta desc: TempChat - Private conversations with auto-deletion after chat ends or timer expires.
# by @mwmodules
# 🔒 Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# meta link: .dlm http://mwmodules.ftp.sh/tempchat.py


#Author: @Zeen17i & @mwoffice
__version__ = (1, 4, 1)

from .. import loader, utils
from telethon import events, types, functions, errors
import asyncio
import datetime
import time
import logging
import re
from typing import Union

logger = logging.getLogger(__name__)

@loader.tds
class TempChatsMod(loader.Module):
    """Модуль для создания и управления временными чатами
    Разработчики: @Zeen17i и @mwoffice"""
    
    strings = {
        "name": "TempChatsPlus",
        "chat_created": "🕒 <b>Временный чат создан</b>\n\n<b>Название:</b> {}\n<b>Время жизни:</b> {} минут\n<b>Участник добавлен:</b> {}\n\n⚠️ <i>Чат будет автоматически удален через указанное время</i>",
        "chat_deleted": "🗑 <b>Временный чат удален</b>",
        "no_args": "❌ <b>Формат:</b> <code>.tempchat название время_в_минутах @username</code>",
        "invalid_time": "❌ <b>Неверное время. Укажите от 1 до 10080 минут (7 дней)</b>",
        "no_user": "❌ <b>Не удалось найти пользователя</b>",
        "adding_user": "👤 <b>Добавление участника...</b>",
        "cant_add_user": "❌ <b>Не удалось добавить {}</b>",
        "chat_info": "📊 <b>Информация о чате:</b>\n\n<b>Название:</b> {}\n<b>Создан:</b> {}\n<b>Осталось:</b> {}\n<b>Создатель:</b> {}\n<b>Участников:</b> {}",
        "no_chat": "❌ <b>Это не временный чат</b>",
        "extended": "⏰ <b>Время жизни чата продлено на {} минут</b>",
        "not_admin": "❌ <b>Требуются права администратора</b>",
        "processing": "⏳ <b>Обработка...</b>",
        "warning_5min": "⚠️ <b>Внимание! Чат будет удален через 5 минут!</b>",
        "warning_1min": "⚠️ <b>Внимание! Чат будет удален через 1 минуту!</b>",
        "chat_cleaned": "🧹 <b>Чат очищен</b>",
        "user_kicked": "👞 <b>Пользователь исключен из чата</b>",
        "user_added": "✅ <b>Пользователь добавлен в чат</b>",
        "no_user_specified": "❌ <b>Укажите пользователя</b>",
        "chat_renamed": "✏️ <b>Чат переименован</b>",
        "no_name": "❌ <b>Укажите новое название</b>",
        "chat_frozen": "❄️ <b>Чат заморожен на {} минут</b>",
        "chat_unfrozen": "♨️ <b>Чат разморожен</b>",
        "chat_locked": "🔒 <b>Чат закрыт</b>",
        "chat_unlocked": "🔓 <b>Чат открыт</b>",
        "chat_archived": "📥 <b>Чат добавлен в архив</b>",
        "chat_unarchived": "📤 <b>Чат удален из архива</b>"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            "default_time", 60,
            "Время жизни чата по умолчанию (минуты)",
            "auto_delete", True,
            "Автоматически удалять служебные сообщения",
            "notify_deletion", True, 
            "Уведомлять об удалении чата",
            "clean_interval", 12,
            "Интервал очистки неактивных чатов (часы)",
            "max_participants", 50,
            "Максимальное количество участников"
        )
        self.temp_chats = {}
        self.tasks = {}
        self.warning_tasks = {}
        self.frozen_chats = {}
        self._cleanup_task = None

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.temp_chats = self.db.get(__name__, "temp_chats", {})
        self.frozen_chats = self.db.get(__name__, "frozen_chats", {})
        
        for chat_id, data in self.temp_chats.items():
            if time.time() < data["delete_time"]:
                self._schedule_deletion(chat_id)
            else:
                await self._delete_chat(chat_id)
        
        self._cleanup_task = asyncio.create_task(self._periodic_cleanup())

    async def _periodic_cleanup(self):
        while True:
            try:
                for chat_id in list(self.temp_chats.keys()):
                    if time.time() > self.temp_chats[chat_id]["delete_time"]:
                        await self._delete_chat(chat_id)
                        
                await asyncio.sleep(self.config["clean_interval"] * 3600)
            except Exception as e:
                logger.error(f"Cleanup error: {e}")
                await asyncio.sleep(3600)

    def _schedule_deletion(self, chat_id: str):
        if chat_id in self.tasks:
            self.tasks[chat_id].cancel()
        if chat_id in self.warning_tasks:
            self.warning_tasks[chat_id].cancel()
            
        self.tasks[chat_id] = asyncio.create_task(self._delete_chat_task(chat_id))
        self.warning_tasks[chat_id] = asyncio.create_task(self._warning_task(chat_id))

    async def _warning_task(self, chat_id):
        try:
            data = self.temp_chats[chat_id]
            remaining = data["delete_time"] - time.time()
            
            if remaining > 300:  
                await asyncio.sleep(remaining - 300)
                await self.client.send_message(int(chat_id), 
                    self.strings["warning_5min"])
                
            if remaining > 60:  
                await asyncio.sleep(240)  
                await self.client.send_message(int(chat_id),
                    self.strings["warning_1min"])
        except Exception as e:
            logger.error(f"Warning task error: {e}")

    async def _delete_chat_task(self, chat_id):
        try:
            data = self.temp_chats[chat_id]
            await asyncio.sleep(data["delete_time"] - time.time())
            await self._delete_chat(chat_id)
        except Exception as e:
            logger.error(f"Delete task error: {e}")

    async def _delete_chat(self, chat_id):
        try:
            if self.config["notify_deletion"]:
                try:
                    await self.client.send_message(int(chat_id), self.strings["chat_deleted"])
                except:
                    pass
            
            await self.client(functions.channels.DeleteChannelRequest(int(chat_id)))
        except:
            pass
            
        if chat_id in self.temp_chats:
            del self.temp_chats[chat_id]
            self.db.set(__name__, "temp_chats", self.temp_chats)
        
        if chat_id in self.tasks:
            del self.tasks[chat_id]
            
        if chat_id in self.warning_tasks:
            del self.warning_tasks[chat_id]

    async def _get_entity(self, user_str: str):
        try:
            if ',' in user_str:
                users = []
                for user in user_str.split(','):
                    user = user.strip()
                    if user.startswith('@'):
                        entity = await self.client.get_entity(user)
                        users.append(entity)
                return users[0] if users else None
            else:
                user = user_str.strip()
                if user.startswith('@'):
                    return await self.client.get_entity(user)
            return None
        except Exception as e:
            logger.error(f"Get entity error: {e}")
            return None

    async def _get_chat_members(self, chat_id: int) -> int:
        try:
            participants = await self.client.get_participants(chat_id, limit=0)
            return participants.total
        except:
            return 0

    @loader.command(ru_doc="<название> <время_в_минутах> <@username> - создать временный чат")
    async def tempchat(self, message):
        """Create temporary chat with specified lifetime"""
        text = utils.get_args_raw(message)
        if not text:
            await utils.answer(message, self.strings["no_args"])
            return
            
        username = text.split()[-1]
        if not username.startswith("@"):
            await utils.answer(message, self.strings["no_user"])
            return
            
        try:
            lifetime = int(text.split()[-2])
            if not 1 <= lifetime <= 10080:
                raise ValueError
        except:
            await utils.answer(message, self.strings["invalid_time"])
            return
            
        chat_title = " ".join(text.split()[:-2])
        if not chat_title:
            await utils.answer(message, self.strings["no_args"])
            return

        status = await utils.answer(message, self.strings["processing"])
        
        user_to_add = await self._get_entity(username)
        if not user_to_add:
            await utils.answer(status, self.strings["no_user"])
            return

        try:
            result = await self.client(functions.channels.CreateChannelRequest(
                title=chat_title,
                about=f"Временный чат • Удаление через {lifetime} минут",
                megagroup=True
            ))
            
            chat = result.chats[0]
            chat_id = str(chat.id)
            
            try:
                await self.client(functions.channels.InviteToChannelRequest(
                    channel=chat.id,
                    users=[user_to_add]
                ))
                user_added = True
            except:
                user_added = False
            
            delete_time = time.time() + (lifetime * 60)
            self.temp_chats[chat_id] = {
                "title": chat_title,
                "created": time.time(),
                "delete_time": delete_time,
                "creator": message.sender_id,
                "members": [user_to_add.id]
            }
            
            self.db.set(__name__, "temp_chats", self.temp_chats)
            self._schedule_deletion(chat_id)
            
            await self.client.send_message(
                chat.id,
                self.strings["chat_created"].format(
                    chat_title,
                    lifetime,
                    "✅" if user_added else "❌"
                )
            )
            
            await utils.answer(status, f"✅ <b>Чат создан:</b> t.me/c/{chat.id}/1")
                
        except Exception as e:
            await utils.answer(status, f"❌ <b>Ошибка:</b> {str(e)}")

    @loader.command(ru_doc="Показать информацию о временном чате")
    async def tempinfo(self, message):
        """Show information about temporary chat"""
        chat_id = str(utils.get_chat_id(message))
        
        if chat_id not in self.temp_chats:
            await utils.answer(message, self.strings["no_chat"])
            return
            
        data = self.temp_chats[chat_id]
        remaining = data["delete_time"] - time.time()
        
        if remaining <= 0:
            await self._delete_chat(chat_id)
            return
            
        members_count = await self._get_chat_members(int(chat_id))
        
        created = datetime.datetime.fromtimestamp(data["created"]).strftime("%d.%m.%Y %H:%M")
        remaining_str = str(datetime.timedelta(seconds=int(remaining)))
        
        creator = await self.client.get_entity(data["creator"])
        creator_name = f"{creator.first_name} (@{creator.username})" if creator.username else creator.first_name
        
        await utils.answer(
            message,
            self.strings["chat_info"].format(
                data["title"],
                created,
                remaining_str,
                creator_name,
                members_count
            )
        )

    @loader.command(ru_doc="<минуты> - продлить время жизни чата")
    async def tempextend(self, message):
        """Extend chat lifetime for specified minutes"""
        chat_id = str(utils.get_chat_id(message))
        
        if chat_id not in self.temp_chats:
            await utils.answer(message, self.strings["no_chat"])
            return
            
        try:
            minutes = int(utils.get_args_raw(message))
            if not 1 <= minutes <= 10080:
                raise ValueError
        except:
            await utils.answer(message, self.strings["invalid_time"])
            return
            
        data = self.temp_chats[chat_id]
        
        if message.sender_id != data["creator"]:
            admin = await self.client.get_permissions(message.chat_id, message.sender_id)
            if not admin.is_admin:
                await utils.answer(message, self.strings["not_admin"])
                return
        
        data["delete_time"] += minutes * 60
        self.db.set(__name__, "temp_chats", self.temp_chats)
        
        if chat_id in self.tasks:
            self.tasks[chat_id].cancel()
        self.tasks[chat_id] = asyncio.create_task(self._delete_chat_task(chat_id))
        
        if chat_id in self.warning_tasks:
            self.warning_tasks[chat_id].cancel()
        self.warning_tasks[chat_id] = asyncio.create_task(self._warning_task(chat_id))
        
        await utils.answer(message, self.strings["extended"].format(minutes))

    @loader.command(ru_doc="Закрыть чат (только админы могут писать)")
    async def templock(self, message):
        """Lock chat (only admins can write)"""
        chat_id = str(utils.get_chat_id(message))
        
        if chat_id not in self.temp_chats:
            await utils.answer(message, self.strings["no_chat"])
            return
            
        try:
            await self.client(functions.messages.EditChatDefaultBannedRightsRequest(
                peer=int(chat_id),
                banned_rights=types.ChatBannedRights(
                    until_date=None,
                    send_messages=True
                )
            ))
            await utils.answer(message, self.strings["chat_locked"])
        except:
            await utils.answer(message, self.strings["not_admin"])

    @loader.command(ru_doc="Открыть чат (все могут писать)")
    async def tempunlock(self, message):
        """Unlock chat (everyone can write)"""
        chat_id = str(utils.get_chat_id(message))
        
        if chat_id not in self.temp_chats:
            await utils.answer(message, self.strings["no_chat"])
            return
            
        try:
            await self.client(functions.messages.EditChatDefaultBannedRightsRequest(
                peer=int(chat_id),
                banned_rights=types.ChatBannedRights(
                    until_date=None,
                    send_messages=False
                )
            ))
            await utils.answer(message, self.strings["chat_unlocked"])
        except:
            await utils.answer(message, self.strings["not_admin"])

    @loader.command(ru_doc="Добавить чат в архив")
    async def temparchive(self, message):
        """Archive temporary chat"""
        chat_id = str(utils.get_chat_id(message))
        
        if chat_id not in self.temp_chats:
            await utils.answer(message, self.strings["no_chat"])
            return
            
        try:
            await message.client(functions.messages.EditChatFolderRequest(
                channel=int(chat_id),
                folder_id=1
            ))
            await utils.answer(message, self.strings["chat_archived"])
        except:
            pass

    @loader.command(ru_doc="Удалить чат из архива")
    async def tempunarchive(self, message):
        """Unarchive temporary chat"""
        chat_id = str(utils.get_chat_id(message))
        
        if chat_id not in self.temp_chats:
            await utils.answer(message, self.strings["no_chat"])
            return
            
        try:
            await message.client(functions.messages.EditChatFolderRequest(
                channel=int(chat_id),
                folder_id=0
            ))
            await utils.answer(message, self.strings["chat_unarchived"])
        except:
            pass

    async def watcher(self, message):
        chat_id = str(utils.get_chat_id(message))
        if chat_id not in self.temp_chats:
            return
            
        if chat_id in self.frozen_chats:
            if time.time() < self.frozen_chats[chat_id]:
                try:
                    await message.delete()
                except:
                    pass
                return
            else:
                del self.frozen_chats[chat_id]
                self.db.set(__name__, "frozen_chats", self.frozen_chats)
            
        if self.config["auto_delete"]:
            if (
                message.action or
                message.text in [
                    self.strings["chat_deleted"],
                    self.strings["adding_user"],
                    self.strings["warning_5min"],
                    self.strings["warning_1min"]
                ] or
                message.text.startswith("❌")
            ):
                await asyncio.sleep(5)
                try:
                    await message.delete()
                except:
                    pass