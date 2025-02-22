"""
888    d8P   .d8888b.  888    888     888b     d888  .d88888b.  8888888b.   .d8888b.  
888   d8P   d88P  Y88b 888    888     8888b   d8888 d88P" "Y88b 888  "Y88b d88P  Y88b 
888  d8P    Y88b.      888    888     88888b.d88888 888     888 888    888 Y88b.      
888d88K      "Y888b.   8888888888 d8b 888Y88888P888 888     888 888    888  "Y888b.   
8888888b        "Y88b. 888    888 Y8P 888 Y888P 888 888     888 888    888     "Y88b. 
888  Y88b         "888 888    888     888  Y8P  888 888     888 888    888       "888 
888   Y88b  Y88b  d88P 888    888 d8b 888   "   888 Y88b. .d88P 888  .d88P Y88b  d88P 
888    Y88b  "Y8888P"  888    888 Y8P 888       888  "Y88888P"  8888888P"   "Y8888P"
                                                                     
(C) 2025 t.me/kshmods
Licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
"""

# meta developer: @kshmods

from .. import loader, utils
import requests

@loader.tds
class Weather(loader.Module):
    strings_ru = {'name': 'Weather',
               'url': 'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru',
               'weather_info': """
<emoji document_id=5884330496619450755>☁️</emoji> Погода в городе {city}, {country}:
<emoji document_id=5199707727475007907>🌡️</emoji> Температура:{temperature}°C (ощущается как {feels_like}°C)
<emoji document_id=6050944866580435869>💧</emoji> Влажность: {humidity}%
<emoji document_id=5415843564280107382>🌀</emoji> Скорость ветра: {wind_speed} м/с
<emoji document_id=5417937876232983047>⛅️</emoji> Небо: {description}
               """,
                  'error': "<b>Ошибка:</b> {e}",
                  'api_error': "Город не найден: {city}\nОтвет API: {data}",
                  'invalid_args': '<emoji document_id=5019523782004441717>❌</emoji> <b>Укажите город.</b>'}

    strings = {'name': 'Weather',
               'url': 'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=en',
               'weather_info': """
<emoji document_id=5884330496619450755>☁️</emoji> Weather in {city}, {country}:
<emoji document_id=5199707727475007907>🌡️</emoji> Temperature:{temperature}°C (feels like {feels_like}°C)
<emoji document_id=6050944866580435869>💧</emoji> Humidity: {humidity}%
<emoji document_id=5415843564280107382>🌀</emoji> Wind speed: {wind_speed} m/s
<emoji document_id=5417937876232983047>⛅️</emoji> Sky: {description}
                   """,
               'error': "<b>Error:</b> {e}",
               'api_error': "City not found: {city}\API response: {data}",
               'invalid_args': '<emoji document_id=5019523782004441717>❌</emoji> <b>Specify the city.</b>'}

    async def client_ready(self, db, client):
        self.db = db
        self._client = client

    @loader.command(
        ru_doc="Посмотрите погоду в указанном городе.",
        en_doc="Check the weather in the specified city."
    )
    async def weather(self, message):
        """Check the weather in the specified city."""
        args = utils.get_args_raw(message).split()
        if len(args) < 1:
            await utils.answer(message, self.strings('invalid_args', message))
            return
        if isinstance(args, list):
            args = args[0]
        city = args
        api_key = "934e9392018dd900103f54e50b870c02"
        url = self.strings('url', message).format(api_key=api_key, city=city)
        try:
            response = requests.get(url)
            data = response.json()
            if data.get('cod') != 200:
                await utils.answer(message, self.strings('api_error', message).format(city=city, data=data))
                return

            country = data['sys']['country']
            weather_data = data["main"]
            temperature = weather_data["temp"]
            feels_like = weather_data["feels_like"]
            wind_data = data["wind"]["speed"]
            wind_speed = wind_data
            humidity = weather_data["humidity"]
            description = data["weather"][0]["description"].capitalize()
            await utils.answer(message, self.strings('weather_info', message).format(city=city.capitalize(), country=country, description=description, temperature=temperature,
                                                                            feels_like=feels_like, humidity=humidity,
                                                                            wind_speed=wind_speed))
        except Exception as e:
            await utils.answer(message, self.strings('error', message).format(e=e))
