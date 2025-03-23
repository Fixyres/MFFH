__version__ = (1, 0, 0)

# ███╗░░░███╗███████╗░█████╗░██████╗░░█████╗░░██╗░░░░░░░██╗░██████╗░██████╗
# ████╗░████║██╔════╝██╔══██╗██╔══██╗██╔══██╗░██║░░██╗░░██║██╔════╝██╔════╝
# ██╔████╔██║█████╗░░███████║██║░░██║██║░░██║░╚██╗████╗██╔╝╚█████╗░╚█████╗░
# ██║╚██╔╝██║██╔══╝░░██╔══██║██║░░██║██║░░██║░░████╔═████║░░╚═══██╗░╚═══██╗
# ██║░╚═╝░██║███████╗██║░░██║██████╔╝╚█████╔╝░░╚██╔╝░╚██╔╝░██████╔╝██████╔╝
# ╚═╝░░░░░╚═╝╚══════╝╚═╝░░╚═╝╚═════╝░░╚════╝░░░░╚═╝░░░╚═╝░░╚═════╝░╚═════╝░
#                © Copyright 2025
#            ✈ https://t.me/mead0wssMods

# scope: hikka_only
# scope: hikka_min 1.3.3
# meta developer: @mead0wssMods
# meta banner: https://x0.at/B0ze.png

import aiohttp
import asyncio
from telethon import events
from .. import loader, utils

@loader.tds
class SteamProfile(loader.Module):
    """Модуль для получения информации о пользователях Steam."""
    strings = {"name": "Steam Profile"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "api_key",
                "",
                lambda: "Ваш API ключ Steam (https://steamcommunity.com/dev/apikey)",
                validator=loader.validators.Hidden(),
            ),
            loader.ConfigValue(
                "show_games",
                True,
                lambda: "Показ игр пользователя (True/False)",
                validator=loader.validators.Boolean(),
            ),
        )

    async def steamprofilecmd(self, event):
        """Получить информацию об пользователе Steam."""
        args = utils.get_args_raw(event)
        if not args:
            await event.edit("❌ Укажите никнейм Steam после команды.")
            return

        api_key = self.config.get("api_key")
        if not api_key:
            await event.edit("❌ API KEY неуказан в cfg! (https://steamcommunity.com/dev/apikey)")
            return

        persona_name = args.strip()
        await event.edit("⏱️ Получаю информацию...")
        await asyncio.sleep(5)

        steam_id = await self.get_steam_id(api_key, persona_name)
        if steam_id:
            player_info = await self.get_player_info(api_key, steam_id)
            owned_games = await self.get_owned_games(api_key, steam_id)

            if player_info is None or 'response' not in player_info or 'players' not in player_info['response']:
                await event.edit("❌ Ошибка: Не удалось получить информацию о пользователе.")
                return

            response_message = await self.send_profile_info(event, player_info, owned_games)
            await event.edit(response_message)
        else:
            await event.edit("❌ Ошибка: Никнейм не найден.")

    async def get_steam_id(self, api_key, persona_name):
        url = f"https://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={api_key}&vanityurl={persona_name}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    if data['response']['success'] == 1:
                        return data['response']['steamid']
        return None

    async def get_player_info(self, api_key, steam_id):
        url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids={steam_id}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
        return None

    async def get_owned_games(self, api_key, steam_id):
        url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={api_key}&steamid={steam_id}&include_appinfo=true&include_played_free_games=true"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
        return None

    async def send_profile_info(self, event, player_info, owned_games):
        if player_info is None or 'response' not in player_info or 'players' not in player_info['response']:
            return "❌ Нет информации о пользователе."

        player = player_info['response']['players'][0]
        response = f"<b>Информация о пользователе:</b>\n"
        response += f"👤 Ник: {player['personaname']}\n"
        response += f"🔗 URL: {player['profileurl']}\n"
        response += f"🧑 Настоящее имя: {player.get('realname', 'Не указано')}\n"
        response += f"🔒 Видимость профиля: {'Открытый' if player['communityvisibilitystate'] == 3 else 'Закрытый'}\n"
        response += f"💬 Статус: {'Онлайн' if player['personastate'] == 1 else 'Оффлайн'}\n"
        response += f"🌍 Страна: {player.get('loccountrycode', 'Не указано')}\n"
        response += f"🖼️ Аватарка: {player['avatarfull']}\n\n"
        
        if self.config.get("show_games") and owned_games and 'games' in owned_games['response']:
            response += "<b>Показ игр пользователя:</b>\n"
            for game in owned_games['response']['games']:
                hours_played = game['playtime_forever'] / 60
                response += f" - {game['name']} (Время игры: {hours_played:.2f} часов)\n"
        
        return response if response else "❌ Нет информации о пользователе."
