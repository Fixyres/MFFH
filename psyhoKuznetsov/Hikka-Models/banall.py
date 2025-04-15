__version__ = (1, 0, 0)
# meta developer: @psyhomodules

import logging
import asyncio
import time
from hikkatl.types import Message
from hikkatl.tl.functions.channels import GetParticipantsRequest, EditBannedRequest
from hikkatl.tl.types import (
    ChannelParticipantsSearch,
    ChatBannedRights,
    PeerChannel,
    ChannelParticipantAdmin,
    ChannelParticipantCreator,
    ChannelParticipantBanned,
    InputPeerChannel,
)
from hikkatl.errors import FloodWaitError
from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class BanAllModule(loader.Module):
    """Модуль для массового бана пользователей в канале, кроме админов и ботов."""
    
    strings = {
        "name": "BanAllModule",
        "no_channel_id": "<b>❌ Ошибка:</b> Укажите ID канала.",
        "getting_channel_error": "<b>❌ Ошибка:</b> Не удалось получить канал: <code>{}</code>",
        "no_admin_rights": "<b>❌ Ошибка:</b> У вас недостаточно прав администратора для бана пользователей.",
        "process_started": "<b>🚀 BanAll:</b> <i>Начинаю процесс бана пользователей...</i>",
        "process_complete": "<b>✅ BanAll завершен!</b>\n\n<b>📊 Статистика:</b>\n• Всего пользователей: <code>{}</code>\n• Забанено: <code>{}</code>\n• Пропущено (админы/боты): <code>{}</code>\n• Затраченное время: <code>{}</code>",
        "processing_status": "<b>⚙️ BanAll в процессе:</b>\n• Обработано пользователей: <code>{}</code>\n• Забанено: <code>{}</code>\n• Скорость: <code>{} пользователей/мин</code>",
        "general_error": "<b>❌ Произошла ошибка:</b> <code>{}</code>",
        "flood_wait": "<b>⚠️ Обнаружено флуд-ограничение.</b> Ожидание <code>{}</code> секунд...",
        "invalid_channel_id": "<b>❌ Ошибка:</b> ID канала должен быть числом."
    }

    def __init__(self):
        self.running = False

     async def client_ready(self, client, db):
        self.client = client
        self.db = db

    @loader.owner
    async def banallcmd(self, message: Message):
        """[ID канала/чата] - Бан всех пользователей в канале"""
        if self.running:
            await message.edit("<b>❌ Операция уже выполняется!</b> Дождитесь завершения.")
            return
            
        try:
            self.running = True
            start_time = time.time()
            
            args = utils.get_args_raw(message)
            if not args:
                await message.edit(self.strings["no_channel_id"])
                self.running = False
                return

            try:
                chat_id = int(args)
            except ValueError:
                await message.edit(self.strings["invalid_channel_id"])
                self.running = False
                return
            
            try:
                chat = await self.client.get_entity(PeerChannel(chat_id))
            except Exception as e:
                await message.edit(self.strings["getting_channel_error"].format(str(e)))
                self.running = False
                return

            try:
                admin_participants = await self.client(GetParticipantsRequest(
                    channel=InputPeerChannel(chat.id, chat.access_hash),
                    filter=None,
                    offset=0,
                    limit=100,
                    hash=0
                ))
                
                current_user_id = (await self.client.get_me()).id
                is_admin = False
                can_ban = False
                
                for participant in admin_participants.participants:
                    if hasattr(participant, 'user_id') and participant.user_id == current_user_id:
                        if isinstance(participant, ChannelParticipantAdmin):
                            is_admin = True
                            if hasattr(participant, 'admin_rights') and hasattr(participant.admin_rights, 'ban_users'):
                                can_ban = participant.admin_rights.ban_users
                        elif isinstance(participant, ChannelParticipantCreator):
                            is_admin = True
                            can_ban = True
                        break
                
                if not is_admin or not can_ban:
                    await message.edit(self.strings["no_admin_rights"])
                    self.running = False
                    return
            except Exception as e:
                logger.error(f"Ошибка: {str(e)}")
 
            banned_rights = ChatBannedRights(
                until_date=None,
                view_messages=True,
                send_messages=True,
                send_media=True,
                send_stickers=True,
                send_gifs=True,
                send_games=True,
                send_inline=True,
                embed_links=True,
            )

            await message.edit(self.strings["process_started"])

            offset = 0
            limit = 100 
            banned_count = 0
            total_users = 0
            status_update_counter = 0
            last_update_time = time.time()
            processed_since_last_update = 0


            while True:
                try:
                    participants = await self.client(GetParticipantsRequest(
                        channel=InputPeerChannel(chat.id, chat.access_hash),
                        filter=ChannelParticipantsSearch(""),
                        offset=offset,
                        limit=limit,
                        hash=0
                    ))
                    
                    if not participants.users:
                        break

                    batch_size = len(participants.users)
                    total_users += batch_size
                    processed_since_last_update += batch_size

                    participant_dict = {p.user_id: p for p in participants.participants}

                    for user in participants.users:
                        user_id = user.id
                        participant = participant_dict.get(user_id)

                        is_admin = isinstance(participant, (ChannelParticipantAdmin, ChannelParticipantCreator))
                        is_banned = isinstance(participant, ChannelParticipantBanned)

                        if not user.bot and not is_admin and not is_banned:
                            try:
                                await self.client(EditBannedRequest(
                                    channel=InputPeerChannel(chat.id, chat.access_hash),
                                    participant=user_id,
                                    banned_rights=banned_rights
                                ))
                                banned_count += 1
                                
                                
                                username = getattr(user, 'username', None)
                                username_str = f"@{username}" if username else "без юзернейма"
                                first_name = getattr(user, 'first_name', "")
                                last_name = getattr(user, 'last_name', "")
                                full_name = f"{first_name} {last_name}".strip()
                                
                                logger.info(f"Забанен пользователь {user_id} ({username_str}) - {full_name}")
                                
                                await asyncio.sleep(0.3)
                            except FloodWaitError as flood_error:
                                wait_time = flood_error.seconds
                                logger.warning(f"Обнаружено флуд-ограничение, ожидание {wait_time} секунд")
                                await message.edit(self.strings["flood_wait"].format(wait_time))
                                await asyncio.sleep(wait_time)
                            except Exception as ban_error:
                                logger.error(f"Ошибка при бане пользователя {user_id}: {str(ban_error)}")
                                continue
                        
                        status_update_counter += 1
                        if status_update_counter >= 20:
                            current_time = time.time()
                            time_diff = current_time - last_update_time
                            
                           
                            if time_diff > 0:
                                speed = int((processed_since_last_update / time_diff) * 60)
                            else:
                                speed = 0
                            
                            try:
                                await message.edit(self.strings["processing_status"].format(
                                    total_users, 
                                    banned_count,
                                    speed
                                ))
                                status_update_counter = 0
                                last_update_time = current_time
                                processed_since_last_update = 0
                            except Exception as edit_error:
                                logger.error(f"Ошибка при обновлении статуса: {str(edit_error)}")

                    offset += limit
                    
                    await asyncio.sleep(1.5)
                
                except FloodWaitError as flood_error:
                    wait_time = flood_error.seconds
                    logger.warning(f"Обнаружено флуд-ограничение, ожидание {wait_time} секунд")
                    await message.edit(self.strings["flood_wait"].format(wait_time))
                    await asyncio.sleep(wait_time)
                except Exception as e:
                    logger.error(f"Ошибка при получении участников: {str(e)}")
                    break

            elapsed_time = time.time() - start_time
            hours, remainder = divmod(int(elapsed_time), 3600)
            minutes, seconds = divmod(remainder, 60)
            time_str = f"{hours:02}:{minutes:02}:{seconds:02}"
            
            result_message = self.strings["process_complete"].format(
                total_users, banned_count, total_users - banned_count, time_str
            )
            
            await message.edit(result_message)

        except Exception as e:
            error_message = self.strings["general_error"].format(str(e))
            logger.error(error_message)
            await message.edit(error_message)
        finally:
            self.running = False
            
    @loader.owner
    async def banallstopcmd(self, message: Message):
        """Остановить текущую операцию бана"""
        if not self.running:
            await message.edit("<b>❌ Нет активной операции бана для остановки.</b>")
            return
            
        self.running = False
        await message.edit("<b>🛑 Операция бана остановлена пользователем.</b>")
