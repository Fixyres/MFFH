from .. import loader, utils
import aiohttp

@loader.tds
class WeatherMod(loader.Module):
    """Модуль для просмотра погоды"""

    strings = {
        "name": "K:Weather",
        "no_city": "<emoji document_id=5465665476971471368>❌</emoji> <b>Укажите город</b>!",
        "error": "<emoji document_id=5465665476971471368>❌</emoji> <b>Ошибка получения погоды</b>.",
        "weather": "<emoji document_id=5431449001532594346>⚡️</emoji> <b>Погода в {}</b>\n\n"
        "<emoji document_id=5397575638146110953>🌎</emoji> <b>Состояние: {}</b>\n"
        "<emoji document_id=5420315771991497307>🔥</emoji> <b>Температура: {}°C</b>\n"
        "<emoji document_id=5427042798878610107>🌈</emoji> <b>Ветер: {} км/ч</b>\n"
        "<emoji document_id=5282833267551117457>🌨</emoji> <b>Влажность: {}%</b>"
    }

    async def weathercmd(self, message):
        """Использование: .weather <город>"""
        args = utils.get_args_raw(message)
        
        if not args:
            await utils.answer(message, self.strings["no_city"])
            return

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"https://wttr.in/{args}?format=j1&lang=ru") as response:
                    if response.status != 200:
                        await utils.answer(message, self.strings["error"])
                        return
                    
                    weather_data = await response.json()
                    current = weather_data["current_condition"][0]
                    
                    await utils.answer(
                        message,
                        self.strings["weather"].format(
                            args,
                            current["lang_ru"][0]["value"],
                            current["temp_C"],
                            current["windspeedKmph"],
                            current["humidity"]
                        )
                    )
            except Exception:
                await utils.answer(message, self.strings["error"])
              
