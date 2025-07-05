# ©️ LoLpryvet, 2025
# 🌐 https://github.com/lolpryvetik/Modules/ChatSi
# Licensed under GNU AGPL v3.0
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
# meta developer: @LoLpryvet


import asyncio
from telethon.tl.functions.messages import GetCommonChatsRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.errors import UserPrivacyRestrictedError, FloodWaitError

from .. import loader, utils


@loader.tds
class ChatSiMod(loader.Module):
    """Модуль для поиска участников с общими чатами"""

    strings = {"name": "ChatSi"}

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    async def chatsicmd(self, message):
        """Найти участников с общими чатами. Использование: .chatsi <число> [ссылка на чат] [s - в избранное]"""
        args = utils.get_args_raw(message).split()
        
        if not args:
            await message.edit(
                "<b>❌ Использование:</b> <code>.chatsi <число> [ссылка на чат] [s]</code>\n"
                "<b>💡 Примеры:</b>\n"
                "<code>.chatsi 3</code> - найти в текущем чате участников с 3+ общими чатами\n"
                "<code>.chatsi 5 @chatname</code> - найти в указанном чате\n"
                "<code>.chatsi 2 s</code> - отправить отчет в избранное\n"
                "<code>.chatsi 3 @chat s</code> - найти в чате и отправить в избранное"
            )
            return
        
        try:
            min_common = int(args[0])
            if min_common < 1:
                await message.edit("<b>❌ Число должно быть больше 0!</b>")
                return
        except ValueError:
            await message.edit("<b>❌ Первый аргумент должен быть числом!</b>")
            return
        
        send_to_saved = 's' in args
        
        target_chat = None
        chat_specified = False
        
        for arg in args[1:]:
            if arg != 's':
                chat_specified = True
                try:
                    target_chat = await message.client.get_entity(arg)
                    break
                except Exception as e:
                    await message.edit(
                        f"<b>❌ Не удалось найти чат:</b> <code>{arg}</code>\n"
                        f"<b>🔧 Проверьте правильность ссылки или ID</b>"
                    )
                    return
        
        if not chat_specified:
            if message.is_private:
                await message.edit("<b>❌ Это не групповой чат! Укажите ссылку на чат.</b>")
                return
            target_chat = await message.client.get_entity(message.chat_id)
        
        chat_name = getattr(target_chat, 'title', f'чат {target_chat.id}')
        await message.edit(f"<b>🔍 Ищем в \"{chat_name}\" участников с {min_common}+ общими чатами...</b>")
        
        try:
            participants = await message.client.get_participants(target_chat)
            target_chat_id = target_chat.id
            
            me = await message.client.get_me()
            
            valid_users = [p for p in participants if not p.bot and not p.deleted and p.id != me.id]
            total_participants = len(valid_users)
            
            result_users = []
            processed = 0
            batch_size = 20
            
            semaphore = asyncio.Semaphore(10)
            
            user_cache = {}
            
            async def process_user_fast(user):
                nonlocal processed
                async with semaphore:
                    try:
                        common_chats = await message.client(
                            GetCommonChatsRequest(user_id=user.id, max_id=0, limit=50)
                        )
                        
                        common_count = sum(1 for chat in common_chats.chats if chat.id != target_chat_id)
                        
                        processed += 1
                        
                        if common_count >= min_common:
                            common_chat_names = []
                            for chat in common_chats.chats:
                                if chat.id != target_chat_id:
                                    chat_name_item = getattr(chat, 'title', f'Чат {chat.id}')
                                    if getattr(chat, 'username', None):
                                        common_chat_names.append(f"{chat_name_item} (@{chat.username})")
                                    else:
                                        common_chat_names.append(chat_name_item)
                            
                            return {
                                'user': user,
                                'common_count': common_count,
                                'common_chats': common_chat_names
                            }
                        return None
                        
                    except (UserPrivacyRestrictedError, Exception):
                        processed += 1
                        return None
            
            for i in range(0, total_participants, batch_size):
                batch = valid_users[i:i + batch_size]
                
                if i % (batch_size * 2) == 0:
                    await message.edit(
                        f"<b>🚀 Турбо-анализ участников...</b>\n"
                        f"<b>📊 Прогресс: {min(i + batch_size, total_participants)}/{total_participants}</b>\n"
                        f"<b>✅ Найдено: {len(result_users)} пользователей</b>"
                    )
                
                tasks = [process_user_fast(user) for user in batch]
                try:
                    batch_results = await asyncio.wait_for(
                        asyncio.gather(*tasks, return_exceptions=True), 
                        timeout=30
                    )
                    
                    for result in batch_results:
                        if result is not None and not isinstance(result, Exception):
                            result_users.append(result)
                            
                except asyncio.TimeoutError:
                    processed += len(batch)
                    continue
                
                if len(batch_results) == 0:
                    await asyncio.sleep(0.5)
                else:
                    await asyncio.sleep(0.05)
            
            if not result_users:
                result_text = (
                    f"<b>❌ В чате \"{chat_name}\" не найдено участников с {min_common}+ общими чатами</b>\n"
                    f"<b>📊 Проанализировано: {processed} участников</b>\n"
                    f"<b>⚡ Время анализа значительно сокращено благодаря параллельной обработке!</b>"
                )
            else:
                result_users.sort(key=lambda x: x['common_count'], reverse=True)
                
                result_text = f"<b>👥 Участники чата \"{chat_name}\" с {min_common}+ общими чатами:</b>\n\n"
                
                for i, item in enumerate(result_users, 1):
                    user = item['user']
                    count = item['common_count']
                    common_chats_list = item['common_chats']
                    
                    name = user.first_name or "Без имени"
                    if user.last_name:
                        name += f" {user.last_name}"
                    
                    chats_preview = ", ".join(common_chats_list[:3])
                    if len(common_chats_list) > 3:
                        chats_preview += f" и еще {len(common_chats_list) - 3}"
                    
                    result_text += f"{i}. <a href='tg://user?id={user.id}'>{name}</a> — {count} общих чатов\n"
                    result_text += f"   <i>Чаты: {chats_preview}</i>\n\n"
                
                result_text += f"<b>📊 Всего найдено: {len(result_users)} из {processed} участников</b>\n"
                result_text += f"<b>⚡ Турбо-анализ завершен! Максимальная скорость достигнута!</b>"
            
            target_chat_for_send = "me" if send_to_saved else message.chat_id
            
            if len(result_text) > 4096:
                status_msg = "📄 Результат большой, отправляю файл в избранное..." if send_to_saved else "📄 Результат слишком большой, сохраняю в файл..."
                await message.edit(status_msg)
                
                filename = f"common_chats_{target_chat.id}.txt"
                with open(filename, "w", encoding="utf-8") as f:
                    clean_text = result_text.replace("<b>", "").replace("</b>", "")
                    clean_text = clean_text.replace("<i>", "").replace("</i>", "")
                    clean_text = clean_text.replace("<a href='tg://user?id=", "")
                    clean_text = clean_text.replace("'>", " (ID: ").replace("</a>", ")")
                    
                    if result_users:
                        clean_text += "\n\n=== ПОЛНЫЕ СПИСКИ ОБЩИХ ЧАТОВ ===\n\n"
                        for item in result_users:
                            user = item['user']
                            common_chats_list = item['common_chats']
                            name = user.first_name or "Без имени"
                            if user.last_name:
                                name += f" {user.last_name}"
                            
                            clean_text += f"=== {name} (ID: {user.id}) ===\n"
                            for j, chat_name in enumerate(common_chats_list, 1):
                                clean_text += f"{j}. {chat_name}\n"
                            clean_text += "\n"
                    
                    f.write(clean_text)
                
                caption = f"<b>🔍 Результат поиска участников с {min_common}+ общими чатами</b>"
                
                await message.client.send_file(
                    target_chat_for_send,
                    filename,
                    caption=caption,
                    reply_to=message.id if not send_to_saved else None
                )
                
                try:
                    import os
                    os.remove(filename)
                except:
                    pass
                
                if send_to_saved:
                    await message.edit("<b>✅ Отчет отправлен в избранное!</b>")
                else:
                    await message.delete()
            else:
                if send_to_saved:
                    await message.client.send_message("me", result_text)
                    await message.edit("<b>✅ Отчет отправлен в избранное!</b>")
                else:
                    await message.edit(result_text)
                
        except Exception as e:
            await message.edit(
                f"<b>❌ Произошла ошибка:</b>\n"
                f"<code>{str(e)}</code>\n\n"
                f"<b>💡 Попробуйте еще раз через некоторое время</b>"
            )

    async def chatsinkcmd(self, message):
        """Найти общие чаты с конкретным пользователем. Использование: .chatsink <@user или реплай> [s - в избранное]"""
        args = utils.get_args_raw(message).split()
        reply = await message.get_reply_message()
        
        send_to_saved = 's' in args
        if send_to_saved:
            args = [arg for arg in args if arg != 's']
        
        user_arg = args[0] if args else None
        
        if not user_arg and not reply:
            await message.edit(
                "<b>❌ Использование:</b> <code>.chatsink <@user> [s]</code> или ответьте на сообщение\n"
                "<b>💡 Примеры:</b>\n"
                "<code>.chatsink @username</code>\n"
                "<code>.chatsink 123456789 s</code> - отправить в избранное\n"
                "Или ответьте на сообщение пользователя"
            )
            return
        
        await message.edit("<b>🔍 Ищем общие чаты...</b>")
        
        try:
            if user_arg:
                if user_arg.isdigit():
                    user = await message.client.get_entity(int(user_arg))
                else:
                    user = await message.client.get_entity(user_arg)
            else:
                user = await message.client.get_entity(reply.sender_id)
                
            user_full = await message.client(GetFullUserRequest(user.id))
            common_chats = await message.client(
                GetCommonChatsRequest(user_id=user.id, max_id=0, limit=100)
            )
            
            if not common_chats.chats:
                user_name = user.first_name or "Пользователь"
                result_text = f"<b>❌ Общих чатов с {user_name} не найдено</b>"
            else:
                user_name = user.first_name or "Пользователь"
                if user.last_name:
                    user_name += f" {user.last_name}"
                    
                result_text = f"<b>👥 Общие чаты с <a href='tg://user?id={user.id}'>{user_name}</a>:</b>\n\n"
                
                for i, chat in enumerate(common_chats.chats, 1):
                    chat_name = getattr(chat, 'title', f'Чат {chat.id}')
                    
                    if getattr(chat, 'username', None):
                        result_text += f"{i}. <a href='tg://resolve?domain={chat.username}'>{chat_name}</a> (@{chat.username})\n"
                    else:
                        result_text += f"{i}. {chat_name} (ID: {chat.id})\n"
                
                result_text += f"\n<b>📊 Всего общих чатов: {len(common_chats.chats)}</b>"
            
            if send_to_saved:
                await message.client.send_message("me", result_text)
                await message.edit("<b>✅ Список общих чатов отправлен в избранное!</b>")
            else:
                await message.edit(result_text)
            
        except Exception as e:
            await message.edit(
                f"<b>❌ Ошибка при поиске общих чатов:</b>\n"
                f"<code>{str(e)}</code>\n\n"
                f"<b>💡 Возможные причины:</b>\n"
                f"• Пользователь не найден\n"
                f"• Настройки приватности пользователя\n"
                f"• Вы не состоите в общих чатах"
            )

    async def chatsinfocmd(self, message):
        """Подробная информация об общих чатах с участником. Использование: .chatsinfo <@user или реплай> [s - в избранное]"""
        args = utils.get_args_raw(message).split()
        reply = await message.get_reply_message()
        
        send_to_saved = 's' in args
        if send_to_saved:
            args = [arg for arg in args if arg != 's']
        
        user_arg = args[0] if args else None
        
        if not user_arg and not reply:
            await message.edit(
                "<b>❌ Использование:</b> <code>.chatsinfo <@user> [s]</code> или ответьте на сообщение\n"
                "<b>💡 Показывает подробный список всех общих чатов с пользователем</b>\n"
                "<b>📁 Добавьте 's' для отправки в избранное</b>"
            )
            return
        
        await message.edit("<b>🔍 Получаем подробную информацию об общих чатах...</b>")
        
        try:
            if user_arg:
                if user_arg.isdigit():
                    user = await message.client.get_entity(int(user_arg))
                else:
                    user = await message.client.get_entity(user_arg)
            else:
                user = await message.client.get_entity(reply.sender_id)
                
            user_full = await message.client(GetFullUserRequest(user.id))
            common_chats = await message.client(
                GetCommonChatsRequest(user_id=user.id, max_id=0, limit=100)
            )
            
            if not common_chats.chats:
                user_name = user.first_name or "Пользователь"
                result_text = f"<b>❌ Общих чатов с {user_name} не найдено</b>"
            else:
                user_name = user.first_name or "Пользователь"
                if user.last_name:
                    user_name += f" {user.last_name}"
                    
                result_text = f"<b>👥 Подробная информация об общих чатах с <a href='tg://user?id={user.id}'>{user_name}</a>:</b>\n\n"
                
                for i, chat in enumerate(common_chats.chats, 1):
                    chat_name = getattr(chat, 'title', f'Чат {chat.id}')
                    
                    chat_info = f"{i}. <b>{chat_name}</b>\n"
                    
                    if getattr(chat, 'username', None):
                        chat_info += f"   📎 Username: @{chat.username}\n"
                    
                    chat_info += f"   🆔 ID: <code>{chat.id}</code>\n"
                    
                    if hasattr(chat, 'megagroup') and chat.megagroup:
                        chat_type = "Супергруппа"
                    elif hasattr(chat, 'broadcast') and chat.broadcast:
                        chat_type = "Канал"
                    elif hasattr(chat, 'channel'):
                        chat_type = "Группа/Канал"
                    else:
                        chat_type = "Чат"
                    
                    chat_info += f"   📋 Тип: {chat_type}\n"
                    
                    if hasattr(chat, 'participants_count'):
                        chat_info += f"   👥 Участников: {chat.participants_count}\n"
                    
                    result_text += chat_info + "\n"
                
                result_text += f"<b>📊 Всего общих чатов: {len(common_chats.chats)}</b>"
            
            if len(result_text) > 4096:
                status_msg = "📄 Информация большая, отправляю файл в избранное..." if send_to_saved else "📄 Информация слишком большая, сохраняю в файл..."
                await message.edit(status_msg)
                
                filename = f"detailed_chats_{user.id}.txt"
                with open(filename, "w", encoding="utf-8") as f:
                    clean_text = result_text.replace("<b>", "").replace("</b>", "")
                    clean_text = clean_text.replace("<code>", "").replace("</code>", "")
                    clean_text = clean_text.replace("<a href='tg://user?id=", "")
                    clean_text = clean_text.replace("'>", " (ID: ").replace("</a>", ")")
                    f.write(clean_text)
                
                target_chat_for_send = "me" if send_to_saved else message.chat_id
                caption = f"<b>📋 Подробная информация об общих чатах с {user_name}</b>"
                
                await message.client.send_file(
                    target_chat_for_send,
                    filename,
                    caption=caption,
                    reply_to=message.id if not send_to_saved else None
                )
                
                try:
                    import os
                    os.remove(filename)
                except:
                    pass
                
                if send_to_saved:
                    await message.edit("<b>✅ Подробная информация отправлена в избранное!</b>")
                else:
                    await message.delete()
            else:
                if send_to_saved:
                    await message.client.send_message("me", result_text)
                    await message.edit("<b>✅ Подробная информация отправлена в избранное!</b>")
                else:
                    await message.edit(result_text)
            
        except Exception as e:
            await message.edit(
                f"<b>❌ Ошибка при получении информации:</b>\n"
                f"<code>{str(e)}</code>\n\n"
                f"<b>💡 Возможные причины:</b>\n"
                f"• Пользователь не найден\n"
                f"• Настройки приватности пользователя\n"
                f"• Вы не состоите в общих чатах"
            )