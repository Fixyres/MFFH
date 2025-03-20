__version__ = (1, 0, 0)

# ███╗░░░███╗███████╗░█████╗░██████╗░░█████╗░░██╗░░░░░░░██╗░██████╗
# ████╗░████║██╔════╝██╔══██╗██╔══██╗██╔══██╗░██║░░██╗░░██║██╔════╝
# ██╔████╔██║█████╗░░███████║██║░░██║██║░░██║░╚██╗████╗██╔╝╚█████╗░
# ██║╚██╔╝██║██╔══╝░░██╔══██║██║░░██║██║░░██║░░████╔═████║░░╚═══██╗
# ██║░╚═╝░██║███████╗██║░░██║██████╔╝╚█████╔╝░░╚██╔╝░╚██╔╝░██████╔╝ 
# ╚═╝░░░░░╚═╝╚══════╝╚═╝░░╚═╝╚═════╝░░╚════╝░░░░╚═╝░░░╚═╝░░╚═════╝░
#                © Copyright 2025
#            ✈ https://t.me/mead0wssMods

# scope: hikka_only
# scope: hikka_min 1.3.3
# meta developer: @mead0wssMods
# meta banner: https://x0.at/Hu25.jpg


import requests
from telethon import events
from .. import loader, utils
from aiohttp import ClientSession
import json

@loader.tds
class MyFACEIT(loader.Module):
    """Модуль для получения информации о своем профиле FACEIT\nАвтор: @mead0ws_modules"""
    strings = {"name": "MyFACEIT"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "nickname",
                "",
                lambda: "Никнейм Faceit для получения информации",
                validator=loader.validators.String()
            ),
        )

    async def myfaceitcmd(self, event):
        """- Показать информацию об своем FACEIT профиле."""
        nickname = self.config["nickname"]

        if not nickname:
            await event.reply("❌ Никнейм Faceit не указан в .cfg!")
            return

        async with ClientSession() as session:
            async with session.get(f"https://api.faceit.com/users/v1/nicknames/{nickname}") as response:
                if response.status == 200:
                    payload = await response.json()
                    payload = payload.get("payload", {})

                    gender = payload.get("gender")
                    user_type = payload.get("user_type")
                    ID = payload.get("id")
                    country = payload.get("country")
                    region = payload.get("games", {}).get("cs2", {}).get("region")
                    elo = payload.get("games", {}).get("cs2", {}).get("faceit_elo")
                    faceit_lvl_c2 = payload.get("games", {}).get("cs2", {}).get("skill_level")
                    twitch_id = payload.get("streaming", {}).get("twitch_id")
                    steam_nickname = payload.get("platforms", {}).get("steam", {}).get("nickname")

                    if gender == "male":
                        gender = "Мужчина"
                    elif gender == "Female":
                        gender = "Женщина"
                    else:
                        gender = "*неуказано*"

                    if user_type == "user":
                        user_type = "Пользователь"
                    else:
                        user_type = "*неуказано*"

                    country_flags = {
                        "ru": "🇷🇺",
                        "eu": "🇪🇺",
                        "us": "🇺🇸",
                        "br": "🇧🇷",
                        "cn": "🇨🇳",
                        "kr": "🇰🇷",
                        "jp": "🇯🇵",
                        "au": "🇦🇺",
                        "ca": "🇨🇦",
                        "gb": "🇬🇧",
                        "de": "🇩🇪",
                        "fr": "🇫🇷",
                        "es": "🇪🇸",
                        "it": "🇮🇹",
                        "pl": "🇵🇱",
                        "tr": "🇹🇷",
                    }

                    country_flag = country_flags.get(country.lower(), "")
                    region_flag = country_flags.get(region.lower(), "")

                    await event.edit(f"<b>Информация об моем FACEIT профиле:\n\n🎮 Ник: {nickname}\n\n🚻 Пол: {gender}\n\n🔍 Тип: {user_type}\n\n🆔 Faceit ID: {ID}\n\n🌍 Страна: {country_flag}\n\n🌐 Регион: {region_flag}\n\n📊 Количество ELO: {elo}\n\n⭐️ Faceit LVL: {faceit_lvl_c2}\n\n📺 Twitch ID: {twitch_id}\n\n💻 Steam: {steam_nickname}</b>", parse_mode="html")
                else:
                    await event.reply("❌ Ошибка при запросе к FACEIT API")
