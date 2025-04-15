__version__ = (1, 0, 2)
# meta developer: @psyhomodules

import datetime
import aiohttp
import pytz
from .. import loader, utils
from telethon.tl.types import Message

class Time(loader.Module):
    """Узнать точное время страны/города"""
    strings = {
        "name": "Time",
        "invalid_args": "<b>❌ Неверные аргументы. Используйте .time [город/страна]</b>",
        "not_found": "<b>❌ Город или страна не найдена</b>",
        "time_result": "<b>⏱️ Точное время в {city}: {time}</b>",
        "api_error": "<b>❌ Ошибка API: {error}</b>",
        "timezone_info": "<b>🌍 Временная зона: {timezone}</b>",
        "loading": "<b>🔍 Ищу информацию о времени...</b>",
    }

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.location_cache = {}

    @loader.command("time", args="[город/страна]")
    async def time(self, message: Message):
        """[город/страна] - Узнать точное время в указанном месте"""
        args = utils.get_args_raw(message)
        
        if not args:
            await utils.answer(message, self.strings["invalid_args"])
            return
            
        loading_message = await utils.answer(message, self.strings["loading"])
        
        try:
            if args in self.location_cache:
                cached_data = self.location_cache[args]
                timezone_name = cached_data["timezone"]
                display_name = cached_data["display_name"]
            else:
                
                async with aiohttp.ClientSession() as session:
                    geo_url = f"https://nominatim.openstreetmap.org/search?q={args}&format=json&limit=1"
                    async with session.get(geo_url, 
                                          headers={"User-Agent": "HikkaWorldTimeModule/1.0"},
                                          timeout=5) as resp:
                        if resp.status != 200:
                            await utils.answer(message, self.strings["api_error"].format(error="Geocoding service unavailable"))
                            return
                        
                        geo_data = await resp.json()
                        if not geo_data:
                            await utils.answer(message, self.strings["not_found"])
                            return
                        
                        lat = float(geo_data[0]["lat"])
                        lon = float(geo_data[0]["lon"])
                        display_name = geo_data[0].get("display_name", "").split(",")[0]
                
                   
                    timezone_url = f"http://api.geonames.org/timezoneJSON?lat={lat}&lng={lon}&username=hikka_time_module"
                    async with session.get(timezone_url, timeout=5) as resp:
                        if resp.status != 200:
                            
                            timezone_name = self._approximate_timezone(lon)
                        else:
                            timezone_data = await resp.json()
                            timezone_name = timezone_data.get("timezoneId")
                            
                            if not timezone_name:
                                timezone_name = self._approximate_timezone(lon)
                
                self.location_cache[args] = {
                    "timezone": timezone_name,
                    "display_name": display_name
                }
            
            tz = pytz.timezone(timezone_name)
            current_time = datetime.datetime.now(tz)
            
            formatted_time = current_time.strftime("%H:%M:%S")
            formatted_date = current_time.strftime("%d.%m.%Y")
            
            await utils.answer(
                loading_message,
                f"{self.strings['time_result'].format(city=display_name, time=formatted_time)}\n"
                f"{self.strings['timezone_info'].format(timezone=timezone_name)}\n"
                f"<b>📅 {formatted_date}</b>"
            )
                    
        except aiohttp.ClientError as e:
            now = datetime.datetime.now()
            await utils.answer(
                loading_message,
                f"<b>⏱️ Ошибка сети. Время сервера: {now.strftime('%H:%M:%S')}</b>\n"
                f"<b>📅 {now.strftime('%d.%m.%Y')}</b>\n"
                f"<b>❌ Детали: {str(e)}</b>"
            )
        except Exception as e:
            now = datetime.datetime.now()
            await utils.answer(
                loading_message,
                f"<b>⏱️ Не удалось определить точное время. Время сервера: {now.strftime('%H:%M:%S')}</b>\n"
                f"<b>📅 {now.strftime('%d.%m.%Y')}</b>\n"
                f"<b>❌ Ошибка: {str(e)}</b>"
            )
    
    def _approximate_timezone(self, longitude):
        utc_offset = round(longitude / 15)
        if utc_offset > 0:
            return f"Etc/GMT-{utc_offset}"
        elif utc_offset < 0:
            return f"Etc/GMT+{abs(utc_offset)}"
        else:
            return "Etc/GMT"
