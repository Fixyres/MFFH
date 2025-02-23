# meta developer: @mwmodules
# meta desc: 🌤 Weather - Модуль для получения текущей погоды и прогноза в любом городе. Отображает температуру, ветер, влажность, давление и другие параметры. Имеет интерактивные кнопки для обновления данных, просмотра подробной информации и карты осадков.
# by @mwmodules
# 🔒 Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# meta link: .dlm http://mwmodules.ftp.sh/weather.py


from .. import loader, utils
import aiohttp
import datetime
from telethon.tl.types import Message

@loader.tds
class WeatherMod(loader.Module):
    """Модуль для получения погоды в любом городе мира"""
    strings = {
        "name": "Weather",
        "city_not_found": "🏙 Город не найден",
        "temp": "🌡 Температура",
        "feels": "🎭 Ощущается как", 
        "wind": "💨 Ветер",
        "humidity": "💧 Влажность",
        "pressure": "🎈 Давление",
        "clouds": "☁️ Облачность",
        "sunrise": "🌅 Рассвет",
        "sunset": "🌇 Закат",
        "current": "📍 Текущая погода в",
        "forecast": "📅 Прогноз на",
        "no_city": "🌍 Укажите город",
        "map_error": "❌ Не удалось загрузить карту"
    }

    def __init__(self):
        self.config = loader.ModuleConfig("token", "27f55366fdc2d2df4bdcdb6a2295251c", "API токен от OpenWeatherMap")

    async def client_ready(self, client, db):
        self._db = db
        self._client = client

    @loader.command()
    async def weathercmd(self, message):
        """<город> - Получить текущую погоду и прогноз на 5 дней
        Примеры:
        .weather Москва
        .weather Moscow 
        .weather New York"""
        if args := utils.get_args_raw(message):
            city = args
        else:
            return await utils.answer(message, self.strings["no_city"])

        weather = await self._get_weather(city)
        if not weather or weather.get("cod") != 200:
            return await utils.answer(message, self.strings["city_not_found"])

        forecast = await self._get_forecast(city)
        if not forecast:
            return await utils.answer(message, self.strings["city_not_found"])
        
        text = self._format_current(weather, city)
        text += "\n\n" + self._format_forecast(forecast)

        await self.inline.form(
            message=message,
            text=text,
            reply_markup=[
                [
                    {"text": "🔄 Обновить", "callback": self._update_weather, "args": (city,)},
                    {"text": "📊 Подробнее", "data": f"weather_details_{city}"}
                ],
                [{"text": "🗺 Карта осадков", "data": f"weather_map_{city}"}]
            ]
        )

    async def _get_weather(self, city):
        url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": self.config["token"],
            "units": "metric",
            "lang": "ru"
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                try:
                    return await response.json()
                except:
                    return None

    async def _get_forecast(self, city):
        url = "http://api.openweathermap.org/data/2.5/forecast"
        params = {
            "q": city,
            "appid": self.config["token"],
            "units": "metric",
            "lang": "ru"
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                try:
                    return await response.json()
                except:
                    return None

    def _format_current(self, data, city):
        return (
            f"{self.strings['current']} {city}:\n"
            f"{self.strings['temp']}: {round(data['main']['temp'])}°C\n"
            f"{self.strings['feels']}: {round(data['main']['feels_like'])}°C\n"
            f"{self.strings['wind']}: {data['wind']['speed']} м/с\n"
            f"{self.strings['humidity']}: {data['main']['humidity']}%\n"
            f"{self.strings['pressure']}: {round(data['main']['pressure'] * 0.750062)} мм.рт.ст\n"
            f"{self.strings['clouds']}: {data['clouds']['all']}%\n"
            f"Описание: {data['weather'][0]['description']}"
        )

    def _format_forecast(self, data):
        if not data or 'list' not in data:
            return ""
            
        text = f"{self.strings['forecast']} 5 дней:\n\n"
        current_date = None
        for item in data['list']:
            date = datetime.datetime.fromtimestamp(item['dt'])
            if current_date != date.date():
                current_date = date.date()
                text += (
                    f"{date.strftime('%d.%m')}:\n"
                    f"🌡 {round(item['main']['temp'])}°C | "
                    f"💨 {item['wind']['speed']} м/с | "
                    f"💧 {item['main']['humidity']}% | "
                    f"{item['weather'][0]['description']}\n\n"
                )
        return text

    async def _update_weather(self, call, city):
        """Обработчик кнопки обновления"""
        weather = await self._get_weather(city)
        if not weather or weather.get("cod") != 200:
            return await call.answer(self.strings["city_not_found"], show_alert=True)
            
        forecast = await self._get_forecast(city)
        if not forecast:
            return await call.answer(self.strings["city_not_found"], show_alert=True)
        
        text = self._format_current(weather, city)
        text += "\n\n" + self._format_forecast(forecast)
        
        await call.edit(
            text=text,
            reply_markup=[
                [
                    {"text": "🔄 Обновить", "callback": self._update_weather, "args": (city,)},
                    {"text": "📊 Подробнее", "data": f"weather_details_{city}"}
                ],
                [{"text": "🗺 Карта осадков", "data": f"weather_map_{city}"}]
            ]
        )

    @loader.callback_handler()
    async def weather_callback_handler(self, call):
        """Обработчик callback кнопок"""
        if call.data.startswith("weather_details_"):
            city = call.data.split("_")[2]
            weather = await self._get_weather(city)
            if not weather or weather.get("cod") != 200:
                return await call.answer(self.strings["city_not_found"], show_alert=True)
            
            text = (
                f"📍 Подробная информация о погоде в {city}:\n\n"
                f"🌡 Температура: {round(weather['main']['temp'])}°C\n"
                f"🎭 Ощущается как: {round(weather['main']['feels_like'])}°C\n"
                f"🌡 Минимальная: {round(weather['main']['temp_min'])}°C\n"
                f"🌡 Максимальная: {round(weather['main']['temp_max'])}°C\n"
                f"💨 Ветер: {weather['wind']['speed']} м/с\n"
                f"🧭 Направление: {weather['wind']['deg']}°\n"
                f"💧 Влажность: {weather['main']['humidity']}%\n"
                f"🎈 Давление: {round(weather['main']['pressure'] * 0.750062)} мм.рт.ст\n"
                f"☁️ Облачность: {weather['clouds']['all']}%\n"
                f"👁 Видимость: {round(weather.get('visibility', 0)/1000, 1)} км\n"
                f"🌅 Рассвет: {datetime.datetime.fromtimestamp(weather['sys']['sunrise']).strftime('%H:%M')}\n"
                f"🌇 Закат: {datetime.datetime.fromtimestamp(weather['sys']['sunset']).strftime('%H:%M')}\n"
                f"Описание: {weather['weather'][0]['description']}"
            )
            
            await call.edit(
                text=text,
                reply_markup=[[{"text": "« Назад", "callback": self._update_weather, "args": (city,)}]]
            )
            
        elif call.data.startswith("weather_map_"):
            city = call.data.split("_")[2]
            weather = await self._get_weather(city)
            if not weather or weather.get("cod") != 200:
                return await call.answer(self.strings["city_not_found"], show_alert=True)
                
            lat = weather['coord']['lat']
            lon = weather['coord']['lon']
            
            map_url = f"https://tile.openweathermap.org/map/precipitation_new/10/{lat}/{lon}.png?appid={self.config['token']}"
            
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(map_url) as response:
                        if response.status == 200:
                            map_data = await response.read()
                            await self._client.send_file(
                                call.message.chat.id,
                                map_data,
                                caption=f"🗺 Карта осадков для {city}"
                            )
                        else:
                            await call.answer(self.strings["map_error"], show_alert=True)
            except:
                await call.answer(self.strings["map_error"], show_alert=True)
