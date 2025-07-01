# meta developer: @xdesai
# requires: requests

from .. import loader, utils
import requests


@loader.tds
class Weather(loader.Module):
    strings_ru = {
        "url": "http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru",
        "weather_info": """<emoji document_id=5884330496619450755>☁️</emoji> <b>Погода в городе {city}, {country}:</b>
<emoji document_id=5199707727475007907>🌡️</emoji> <b>Температура: {temperature}°C (ощущается как {feels_like}°C)</b>
<emoji document_id=6050944866580435869>💧</emoji> <b>Влажность: {humidity}%</b>
<emoji document_id=5415843564280107382>🌀</emoji> <b>Скорость ветра: {wind_speed} м/с</b>
<emoji document_id=5417937876232983047>⛅️</emoji> <b>Небо: {description}</b>""",
        "error": "<b>Ошибка:</b> <code>{e}</code>",
        "api_error": "<b>Город не найден: {city}\nОтвет API:</b> <code></code>",
        "invalid_args": "<emoji document_id=5019523782004441717>❌</emoji> <b>Укажите город.</b>",
    }

    strings_jp = {
        "url": "http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ja",
        "weather_info": """<emoji document_id=5884330496619450755>☁️</emoji> <b>{city}（{country}）の天気:</b>
<emoji document_id=5199707727475007907>🌡️</emoji> <b>気温: {temperature}℃（体感温度: {feels_like}℃）</b>
<emoji document_id=6050944866580435869>💧</emoji> <b>湿度: {humidity}%</b>
<emoji document_id=5415843564280107382>🌀</emoji> <b>風速: {wind_speed} m/s</b>
<emoji document_id=5417937876232983047>⛅️</emoji> <b>空模様: {description}</b>""",
        "error": "<b>エラー:</b> <code>{e}</code>",
        "api_error": "<b>都市が見つかりませんでした: {city}\nAPIの応答:</b> <code>{data}</code>",
        "invalid_args": "<emoji document_id=5019523782004441717>❌</emoji> <b>都市名を指定してください。</b>",
    }

    strings = {
        "name": "Weather",
        "url": "http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=en",
        "weather_info": """<emoji document_id=5884330496619450755>☁️</emoji> <b>Weather in {city}, {country}:</b>
<emoji document_id=5199707727475007907>🌡️</emoji> <b>Temperature: {temperature}°C (feels like {feels_like}°C)</b>
<emoji document_id=6050944866580435869>💧</emoji> <b>Humidity: {humidity}%</b>
<emoji document_id=5415843564280107382>🌀</emoji> <b>Wind speed: {wind_speed} m/s</b>
<emoji document_id=5417937876232983047>⛅️</emoji> <b>Sky: {description}</b>""",
        "error": "<b>Error:</b> <code>{e}</code>",
        "api_error": "<b>City not found: {city}\nAPI response:</b> <code>{data}</code>",
        "invalid_args": "<emoji document_id=5019523782004441717>❌</emoji> <b>Specify the city.</b>",
    }

    @loader.command(
        ru_doc="Посмотреть погоду в указанном городе",
        jp_doc="指定された都市の天気を確認してください",
    )
    async def weather(self, message):
        """Check the weather in the specified city"""
        args = utils.get_args_raw(message).split()
        if len(args) < 1:
            await utils.answer(message, self.strings("invalid_args", message))
            return
        if isinstance(args, list):
            args = args[0]
        city = args
        api_key = "934e9392018dd900103f54e50b870c02"
        url = self.strings("url", message).format(api_key=api_key, city=city)
        try:
            response = requests.get(url)
            data = response.json()
            if data.get("cod") != 200:
                await utils.answer(
                    message,
                    self.strings("api_error", message).format(city=city, data=data),
                )
                return

            country = data["sys"]["country"]
            weather_data = data["main"]
            temperature = weather_data["temp"]
            feels_like = weather_data["feels_like"]
            wind_data = data["wind"]["speed"]
            wind_speed = wind_data
            humidity = weather_data["humidity"]
            description = data["weather"][0]["description"].capitalize()
            await utils.answer(
                message,
                self.strings("weather_info", message).format(
                    city=city.capitalize(),
                    country=country,
                    description=description,
                    temperature=temperature,
                    feels_like=feels_like,
                    humidity=humidity,
                    wind_speed=wind_speed,
                ),
            )
        except Exception as e:
            await utils.answer(message, self.strings("error", message).format(e=e))
