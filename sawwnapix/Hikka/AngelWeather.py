# meta developer: @angellmodules

import requests
from .. import loader, utils

@loader.tds
class AngelWeatherMod(loader.Module):
    """Показывает текущую погоду в указанном городе.🍃"""
    strings = {"name": "AngelWeather"}

    async def weathercmd(self, message):
        """.weather <город> - Показывает текущую погоду."""
        args = utils.get_args_raw(message)
        if not args:
            await message.edit("Укажите город!")
            return

        city = args
        api_key = "934e9392018dd900103f54e50b870c02"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru"

        try:
            response = requests.get(url)
            data = response.json()

            if data.get("cod") != 200:
                await message.edit(f"Город не найден: {city}\nОтвет API: {data}")
                return

            weather_data = data["main"]
            wind_data = data["wind"]
            description = data["weather"][0]["description"].capitalize()

            temperature = weather_data["temp"]
            feels_like = weather_data["feels_like"]
            humidity = weather_data["humidity"]
            wind_speed = wind_data["speed"]

            weather_info = (
                f"<emoji document_id=5402477260982731644>☀️</emoji> Погода в городе {city.capitalize()}:\n"
                f"<emoji document_id=5470049770997292425>🌡</emoji> Температура: {temperature}°C (ощущается как {feels_like}°C)\n"
                f"<emoji document_id=5393512611968995988>💧</emoji> Влажность: {humidity}%\n"
                f"<emoji document_id=5449885771420934013>🍃</emoji> Скорость ветра: {wind_speed} м/с\n"
                f"<emoji document_id=5287571024500498635>☁️</emoji> Небо: {description}"
            )
            await message.edit(weather_info)
        except Exception as e:
            await message.edit(f"Ошибка при получении данных: {e}")


















#made by @sawwnapix
