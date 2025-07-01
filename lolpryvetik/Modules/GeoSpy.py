# ©️ qq_shark & LoLpryvet, 2025
# 🌐 https://github.com/lolpryvetik/GeoSpy
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

# meta developer: @qq_shark, @LoLpryvet

from .. import loader, utils
from telethon.tl.types import MessageMediaGeo, MessageMediaGeoLive, MessageMediaVenue, InputMediaGeoLive, InputGeoPoint
from telethon.tl.functions.messages import SendMediaRequest, EditMessageRequest
from telethon import events
import asyncio
import logging
import random
import re

logger = logging.getLogger(__name__)


@loader.tds
class GeoSpyMod(loader.Module):
    """Модуль для пересылки, ретрансляции и подделки геопозиции в реальном времени"""

    strings = {
        "name": "GeoSpy",
        "no_reply": "❌ <b>Ответьте на сообщение с геопозицией</b>",
        "no_geo": "❌ <b>В сообщении нет геопозиции</b>",
        "no_chat_id": "❌ <b>Укажите ID чата для отправки</b>\n<code>.geospy [chat_id]</code>",
        "invalid_chat": "❌ <b>Неверный ID чата или нет доступа к чату</b>",
        "invalid_coords": "❌ <b>Неверные координаты. Формат:</b> <code>широта,долгота</code>\n<b>Пример:</b> <code>55.7558,37.6176</code>",
        "sent": "✅ <b>Геопозиция отправлена в чат</b> <code>{}</code>",
        "fake_sent": "✅ <b>Геопозиция отправлена в чат</b> <code>{}</code>\n📍 <b>Координаты:</b> <code>{}, {}</code>",
        "live_started": "🔴 <b>Запущена ретрансляция Live Location в чат</b> <code>{}</code>\n⏱ <b>Период обновления:</b> {} сек",
        "fake_live_started": "🔴 <b>Запущена Live Location в чат</b> <code>{}</code>\n📍 <b>Координаты:</b> <code>{}, {}</code>\n⏱ <b>Период обновления:</b> {} сек",
        "live_stopped": "⏹ <b>Ретрансляция Live Location остановлена</b>",
        "live_updated": "🔄 <b>Live Location обновлена</b> (попытка {})",
        "coords_updated": "📍 <b>Координаты обновлены на:</b> <code>{}, {}</code>",
        "error": "❌ <b>Ошибка при отправке:</b> <code>{}</code>",
        "already_tracking": "⚠️ <b>Уже отслеживается Live Location. Используйте</b> <code>.geostop</code> <b>для остановки</b>",
        "not_tracking": "⚠️ <b>Ретрансляция не активна</b>",
        "no_active_fake": "⚠️ <b>Нет активной трансляции для изменения координат</b>",
        "help": """
🌍 <b>GeoSpy - Модуль для пересылки, ретрансляции и подделки геопозиции</b>

<b>Команды:</b>
• <code>.geospy [chat_id] [period]</code> - Переслать/ретранслировать геопозицию
• <code>.fakegeo [chat_id] [lat,long] [period]</code> - Отправить геопозицию
• <code>.fakelive [chat_id] [lat,long] [period]</code> - Запустить Live Location
• <code>.geochange [lat,long]</code> - Изменить координаты активной трансляции
• <code>.geostop</code> - Остановить ретрансляцию Live Location
• <code>.geostatus</code> - Статус ретрансляции
• <code>.geospyhelp</code> - Показать справку

<b>Использование:</b>

<b>Обычная геопозиция:</b>
1. Ответьте на сообщение с геопозицией
2. <code>.geospy [ID_чата]</code>

<b>Отправка геопозиции:</b>
• <code>.fakegeo -1001234567890 55.7558,37.6176</code> - Отправить точку (Москва)

<b>Live Location (в реальном времени):</b>
1. Ответьте на Live Location
2. <code>.geospy [ID_чата] [период_в_секундах]</code>

<b>Live Location трансляция:</b>
• <code>.fakelive -1001234567890 55.7558,37.6176 30</code> - Трансляция каждые 30 сек
• <code>.geochange 40.7128,-74.0060</code> - Изменить координаты на Нью-Йорк

<b>Примеры координат:</b>
• Москва: <code>55.7558,37.6176</code>
• Нью-Йорк: <code>40.7128,-74.0060</code>
• Лондон: <code>51.5074,-0.1278</code>
• Токио: <code>35.6762,139.6503</code>
• Дубай: <code>25.2048,55.2708</code>

<b>Поддерживаемые типы:</b>
• Обычная геопозиция
• Live Location (с автообновлением)
• Venue (места/заведения)
""",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "default_update_period",
                20,
                "Период обновления Live Location по умолчанию (секунды)",
                validator=loader.validators.Integer(minimum=10)
            ),
            loader.ConfigValue(
                "max_update_period", 
                300,
                "Максимальный период обновления (секунды)",
                validator=loader.validators.Integer(minimum=60)
            )
        )
        self._tracking_tasks = {}
        self._fake_live_sessions = {}

    def _parse_coordinates(self, coord_string):
        try:
            coords = coord_string.replace(' ', '').split(',')
            if len(coords) != 2:
                return None, None
            
            lat = float(coords[0])
            long = float(coords[1])
            
            if not (-90 <= lat <= 90) or not (-180 <= long <= 180):
                return None, None
                
            return lat, long
        except (ValueError, IndexError):
            return None, None

    async def fakegeocmd(self, message):
        """Отправить геопозицию"""
        args = utils.get_args(message)
        
        if len(args) < 2:
            await utils.answer(message, "❌ <b>Использование:</b> <code>.fakegeo [chat_id] [lat,long]</code>\n<b>Пример:</b> <code>.fakegeo -1001234567890 55.7558,37.6176</code>")
            return

        chat_id = args[0]
        coord_string = args[1]
        
        lat, long = self._parse_coordinates(coord_string)
        if lat is None or long is None:
            await utils.answer(message, self.strings("invalid_coords"))
            return

        try:
            if chat_id.startswith('@'):
                chat = await message.client.get_entity(chat_id)
            else:
                try:
                    chat_id_int = int(chat_id)
                    chat = await message.client.get_entity(chat_id_int)
                except ValueError:
                    chat = await message.client.get_entity(chat_id)

            chat_info = getattr(chat, 'title', None) or getattr(chat, 'username', None) or str(chat.id)

            from telethon.tl.types import InputMediaGeoPoint
            geo_media = InputMediaGeoPoint(
                geo_point=InputGeoPoint(lat=lat, long=long)
            )
            
            result = await message.client(SendMediaRequest(
                peer=chat,
                media=geo_media,
                message="",
                random_id=random.randint(1, 2**63)
            ))
            
            await utils.answer(message, self.strings("fake_sent").format(chat_info, lat, long))
                
        except Exception as e:
            logger.exception("Error in fakegeo command")
            if "Could not find the input entity" in str(e):
                await utils.answer(message, self.strings("invalid_chat"))
            else:
                await utils.answer(message, self.strings("error").format(str(e)))

    async def fakelivecmd(self, message):
        """Запустить Live Location трансляцию"""
        args = utils.get_args(message)
        
        if len(args) < 2:
            await utils.answer(message, "❌ <b>Использование:</b> <code>.fakelive [chat_id] [lat,long] [period]</code>\n<b>Пример:</b> <code>.fakelive -1001234567890 55.7558,37.6176 30</code>")
            return

        chat_id = args[0]
        coord_string = args[1]
        update_period = int(args[2]) if len(args) > 2 else self.config["default_update_period"]
        
        lat, long = self._parse_coordinates(coord_string)
        if lat is None or long is None:
            await utils.answer(message, self.strings("invalid_coords"))
            return

        try:
            if chat_id.startswith('@'):
                chat = await message.client.get_entity(chat_id)
            else:
                try:
                    chat_id_int = int(chat_id)
                    chat = await message.client.get_entity(chat_id_int)
                except ValueError:
                    chat = await message.client.get_entity(chat_id)

            chat_info = getattr(chat, 'title', None) or getattr(chat, 'username', None) or str(chat.id)
            tracking_key = f"live_{chat.id}_{random.randint(1000, 9999)}"

            max_period = self.config["max_update_period"]
            if update_period > max_period:
                update_period = max_period
            elif update_period < 10:
                update_period = 10

            live_media = InputMediaGeoLive(
                geo_point=InputGeoPoint(lat=lat, long=long),
                period=3600,
            )
            
            result = await message.client(SendMediaRequest(
                peer=chat,
                media=live_media,
                message="",
                random_id=random.randint(1, 2**63)
            ))
            
            sent_message_id = None
            if hasattr(result, 'updates'):
                for update in result.updates:
                    if hasattr(update, 'message') and update.message:
                        sent_message_id = update.message.id
                        break
                    elif hasattr(update, 'id'):
                        sent_message_id = update.id
                        break
            
            if not sent_message_id:
                last_messages = await message.client.get_messages(chat, limit=1)
                if last_messages:
                    sent_message_id = last_messages[0].id
                else:
                    raise Exception("Could not determine sent message ID")
            
            await utils.answer(
                message, 
                self.strings("fake_live_started").format(chat_info, lat, long, update_period)
            )

            session = {
                'chat': chat,
                'message_id': sent_message_id,
                'current_lat': lat,
                'current_long': long,
                'update_period': update_period,
                'client': message.client
            }
            
            task = asyncio.create_task(
                self._live_maintainer(session, tracking_key)
            )
            
            self._fake_live_sessions[tracking_key] = session
            self._tracking_tasks[tracking_key] = {
                'task': task,
                'client': message.client,
                'type': 'live'
            }

        except Exception as e:
            logger.exception("Error in fakelive command")
            if "Could not find the input entity" in str(e):
                await utils.answer(message, self.strings("invalid_chat"))
            else:
                await utils.answer(message, self.strings("error").format(str(e)))

    async def geochangecmd(self, message):
        """Изменить координаты активной трансляции"""
        args = utils.get_args(message)
        
        if not args:
            await utils.answer(message, "❌ <b>Использование:</b> <code>.geochange [lat,long]</code>\n<b>Пример:</b> <code>.geochange 40.7128,-74.0060</code>")
            return

        coord_string = args[0]
        lat, long = self._parse_coordinates(coord_string)
        if lat is None or long is None:
            await utils.answer(message, self.strings("invalid_coords"))
            return

        active_sessions = [key for key, task_info in self._tracking_tasks.items() 
                          if isinstance(task_info, dict) and task_info.get('type') == 'live']
        
        if not active_sessions:
            await utils.answer(message, self.strings("no_active_fake"))
            return

        updated_count = 0
        for session_key in active_sessions:
            if session_key in self._fake_live_sessions:
                session = self._fake_live_sessions[session_key]
                session['current_lat'] = lat
                session['current_long'] = long
                updated_count += 1

        if updated_count > 0:
            await utils.answer(message, self.strings("coords_updated").format(lat, long))
        else:
            await utils.answer(message, self.strings("no_active_fake"))

    async def _live_maintainer(self, session, tracking_key):
        try:
            while tracking_key in self._tracking_tasks:
                await asyncio.sleep(session['update_period'])
                
                try:
                    new_live_media = InputMediaGeoLive(
                        geo_point=InputGeoPoint(
                            lat=session['current_lat'],
                            long=session['current_long']
                        ),
                        period=3600,
                    )
                    
                    await session['client'](EditMessageRequest(
                        peer=session['chat'],
                        id=session['message_id'],
                        media=new_live_media
                    ))
                    
                    logger.info(f"Live location updated to lat:{session['current_lat']:.6f}, long:{session['current_long']:.6f}")
                    
                except Exception as edit_error:
                    if "Content of the message was not modified" not in str(edit_error):
                        logger.warning(f"Could not edit live location: {edit_error}")
                        
                except Exception as e:
                    logger.exception(f"Error updating live location: {e}")
                        
        except asyncio.CancelledError:
            logger.info("Live location tracking cancelled")
        finally:
            if tracking_key in self._fake_live_sessions:
                del self._fake_live_sessions[tracking_key]
            if tracking_key in self._tracking_tasks:
                del self._tracking_tasks[tracking_key]
                logger.info(f"Stopped tracking {tracking_key}")

    async def geospycmd(self, message):
        """Переслать геопозицию или запустить ретрансляцию Live Location"""
        args = utils.get_args(message)
        
        if not args:
            await utils.answer(message, self.strings("no_chat_id"))
            return

        reply = await message.get_reply_message()
        if not reply:
            await utils.answer(message, self.strings("no_reply"))
            return

        if not reply.media or not isinstance(reply.media, (MessageMediaGeo, MessageMediaGeoLive, MessageMediaVenue)):
            await utils.answer(message, self.strings("no_geo"))
            return

        chat_id = args[0]
        update_period = int(args[1]) if len(args) > 1 else None

        try:
            if chat_id.startswith('@'):
                chat = await message.client.get_entity(chat_id)
            else:
                try:
                    chat_id_int = int(chat_id)
                    chat = await message.client.get_entity(chat_id_int)
                except ValueError:
                    chat = await message.client.get_entity(chat_id)

            geo_media = reply.media
            chat_info = getattr(chat, 'title', None) or getattr(chat, 'username', None) or str(chat.id)

            if isinstance(geo_media, MessageMediaGeoLive) and update_period:
                await self._start_live_tracking(message, reply, chat, update_period, chat_info)
            else:
                geo_point = geo_media.geo
                
                if isinstance(geo_media, MessageMediaGeoLive):
                    live_media = InputMediaGeoLive(
                        geo_point=InputGeoPoint(
                            lat=geo_point.lat,
                            long=geo_point.long,
                            accuracy_radius=getattr(geo_point, 'accuracy_radius', None)
                        ),
                        heading=getattr(geo_media, 'heading', None),
                        period=900,
                        proximity_notification_radius=getattr(geo_media, 'proximity_notification_radius', None)
                    )
                    
                    result = await message.client(SendMediaRequest(
                        peer=chat,
                        media=live_media,
                        message="",
                        random_id=random.randint(1, 2**63)
                    ))
                else:
                    geo_media_input = InputGeoPoint(
                        lat=geo_point.lat,
                        long=geo_point.long,
                        accuracy_radius=getattr(geo_point, 'accuracy_radius', None)
                    )
                    
                    from telethon.tl.types import InputMediaGeoPoint
                    result = await message.client(SendMediaRequest(
                        peer=chat,
                        media=InputMediaGeoPoint(geo_point=geo_media_input),
                        message="",
                        random_id=random.randint(1, 2**63)
                    ))
                    
                await utils.answer(message, self.strings("sent").format(chat_info))
                
        except Exception as e:
            logger.exception("Error in geospy command")
            if "Could not find the input entity" in str(e):
                await utils.answer(message, self.strings("invalid_chat"))
            else:
                await utils.answer(message, self.strings("error").format(str(e)))

    async def _start_live_tracking(self, message, source_message, target_chat, update_period, chat_info):
        max_period = self.config["max_update_period"]
        if update_period > max_period:
            update_period = max_period
        elif update_period < 10:
            update_period = 10

        tracking_key = f"{target_chat.id}_{source_message.id}"
        
        if tracking_key in self._tracking_tasks:
            await utils.answer(message, self.strings("already_tracking"))
            return

        try:
            geo_point = source_message.media.geo
            
            live_media = InputMediaGeoLive(
                geo_point=InputGeoPoint(
                    lat=geo_point.lat,
                    long=geo_point.long,
                    accuracy_radius=getattr(geo_point, 'accuracy_radius', None)
                ),
                heading=getattr(source_message.media, 'heading', None),
                period=3600,
                proximity_notification_radius=getattr(source_message.media, 'proximity_notification_radius', None)
            )
            
            result = await message.client(SendMediaRequest(
                peer=target_chat,
                media=live_media,
                message="",
                random_id=random.randint(1, 2**63)
            ))
            
            sent_message_id = None
            if hasattr(result, 'updates'):
                for update in result.updates:
                    if hasattr(update, 'message') and update.message:
                        sent_message_id = update.message.id
                        break
                    elif hasattr(update, 'id'):
                        sent_message_id = update.id
                        break
            
            if not sent_message_id:
                last_messages = await message.client.get_messages(target_chat, limit=1)
                if last_messages:
                    sent_message_id = last_messages[0].id
                else:
                    raise Exception("Could not determine sent message ID")
            
            await utils.answer(
                message, 
                self.strings("live_started").format(chat_info, update_period)
            )

            task = asyncio.create_task(
                self._live_location_updater(
                    message.client,
                    source_message, 
                    sent_message_id,
                    target_chat, 
                    update_period,
                    tracking_key
                )
            )
            self._tracking_tasks[tracking_key] = {
                'task': task,
                'client': message.client,
                'type': 'real_live'
            }

        except Exception as e:
            logger.exception("Error starting live tracking")
            await utils.answer(message, self.strings("error").format(str(e)))

    async def _live_location_updater(self, client, source_message, sent_message_id, target_chat, update_period, tracking_key):
        attempt = 0
        last_lat = None
        last_long = None
        
        try:
            while tracking_key in self._tracking_tasks:
                await asyncio.sleep(update_period)
                attempt += 1
                
                try:
                    updated_source = await client.get_messages(
                        source_message.peer_id, 
                        ids=source_message.id
                    )
                    
                    if updated_source and updated_source.media:
                        if isinstance(updated_source.media, MessageMediaGeoLive):
                            new_geo_point = updated_source.media.geo
                            current_lat = new_geo_point.lat
                            current_long = new_geo_point.long
                            
                            if last_lat is None or abs(current_lat - last_lat) > 0.000001 or abs(current_long - last_long) > 0.000001:
                                try:
                                    new_live_media = InputMediaGeoLive(
                                        geo_point=InputGeoPoint(
                                            lat=current_lat,
                                            long=current_long,
                                            accuracy_radius=getattr(new_geo_point, 'accuracy_radius', None)
                                        ),
                                        heading=getattr(updated_source.media, 'heading', None),
                                        period=3600,
                                        proximity_notification_radius=getattr(updated_source.media, 'proximity_notification_radius', None)
                                    )
                                    
                                    await client(EditMessageRequest(
                                        peer=target_chat,
                                        id=sent_message_id,
                                        media=new_live_media
                                    ))
                                    
                                    last_lat = current_lat
                                    last_long = current_long
                                    
                                    logger.info(f"Live location updated to lat:{current_lat:.6f}, long:{current_long:.6f} (attempt {attempt})")
                                    
                                except Exception as edit_error:
                                    if "Content of the message was not modified" in str(edit_error):
                                        logger.debug(f"Coordinates unchanged (attempt {attempt})")
                                    else:
                                        logger.warning(f"Could not edit live location (attempt {attempt}): {edit_error}")
                                    continue
                            else:
                                logger.debug(f"No coordinate change detected (attempt {attempt})")
                        else:
                            logger.info("Source live location ended")
                            break
                    else:
                        logger.warning("Source message not found or no media")
                        break
                        
                except Exception as e:
                    logger.exception(f"Error updating live location (attempt {attempt}): {e}")
                    if attempt > 30:
                        logger.error("Too many errors, stopping live location tracking")
                        break
                        
        except asyncio.CancelledError:
            logger.info("Live location tracking cancelled")
        finally:
            if tracking_key in self._tracking_tasks:
                del self._tracking_tasks[tracking_key]
                logger.info(f"Stopped tracking {tracking_key}")

    async def geostopcmd(self, message):
        """Остановить все активные ретрансляции Live Location"""
        if not self._tracking_tasks:
            await utils.answer(message, self.strings("not_tracking"))
            return
            
        for task_info in self._tracking_tasks.values():
            if isinstance(task_info, dict):
                task_info['task'].cancel()
            else:
                task_info.cancel()
            
        self._tracking_tasks.clear()
        self._fake_live_sessions.clear()
        await utils.answer(message, self.strings("live_stopped"))

    async def geostatuscmd(self, message):
        """Показать статус активных ретрансляций"""
        if not self._tracking_tasks:
            await utils.answer(message, "ℹ️ <b>Нет активных ретрансляций</b>")
            return
            
        status_text = f"📡 <b>Активных ретрансляций:</b> {len(self._tracking_tasks)}\n\n"
        for i, (key, task_info) in enumerate(self._tracking_tasks.items(), 1):
            task_type = "🔴 Реальная" if isinstance(task_info, dict) and task_info.get('type') == 'real_live' else "🟡 Трансляция"
            status_text += f"{i}. {task_type}: <code>{key}</code>\n"
            
        await utils.answer(message, status_text)

    async def geospyhelpcmd(self, message):
        """Показать справку по модулю GeoSpy"""
        await utils.answer(message, self.strings("help"))

    async def on_unload(self):
        """Остановить все задачи при выгрузке модуля"""
        for task_info in self._tracking_tasks.values():
            if isinstance(task_info, dict):
                task_info['task'].cancel()
            else:
                task_info.cancel()
        self._tracking_tasks.clear()
        self._fake_live_sessions.clear()
