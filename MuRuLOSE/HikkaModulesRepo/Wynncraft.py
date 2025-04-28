"""
    ███    ███ ██    ██ ██████  ██    ██ ██       ██████  ███████ ███████
    ████  ████ ██    ██ ██   ██ ██    ██ ██      ██    ██ ██      ██  
    ██ ████ ██ ██    ██ ██████  ██    ██ ██      ██    ██ ███████ █████
    ██  ██  ██ ██    ██ ██   ██ ██    ██ ██      ██    ██      ██ ██  
    ██      ██  ██████  ██   ██  ██████  ███████  ██████  ███████ ███████ 

    WynnCraft
"""

# scopes:
# requires: dataclasses-json

# 🔒 Licensed under the GNU AGPLv3

# meta banner: link
# meta desc: Wynncraft API Module
# meta developer: @BruhHikkaModules

from telethon.tl.types import Message
from .. import loader, utils
from ..inline.types import InlineCall

from dataclasses import dataclass
from dataclasses_json import dataclass_json

from typing import Optional, Dict, List, Union
import aiohttp
from aiohttp.web_exceptions import HTTPNotFound
import urllib.parse
import re

from datetime import datetime

@dataclass_json
@dataclass
class Guild:
    name: str
    prefix: str
    rank: str
    rankStars: str

@dataclass_json
@dataclass
class LegacyRankColour:
    main: str
    sub: str

@dataclass_json
@dataclass
class Pvp:
    kills: int
    deaths: int

@dataclass_json
@dataclass
class Dungeons:
    total: int
    list: Optional[Dict[str, int]] = None

@dataclass_json
@dataclass
class Raids:
    total: int
    list: Optional[Dict[str, int]] = None

@dataclass_json
@dataclass
class GlobalData:
    wars: int
    totalLevel: int
    killedMobs: int
    chestsFound: int
    completedQuests: int
    pvp: Pvp
    dungeons: Optional[Dungeons] = None
    raids: Optional[Raids] = None

@dataclass_json
@dataclass
class PlayerStats:
    username: str
    online: bool
    server: str
    activeCharacter: Optional[str]
    nickname: Optional[str]
    uuid: str
    rank: str
    rankBadge: Optional[str]
    legacyRankColour: Optional[LegacyRankColour]
    shortenedRank: Optional[str]
    supportRank: Optional[str]
    veteran: Optional[bool]
    firstJoin: str
    lastJoin: str
    playtime: float
    guild: Optional[Guild]
    globalData: GlobalData
    forumLink: Optional[int]
    ranking: Dict[str, int]
    previousRanking: Dict[str, int]
    publicProfile: bool
    characters: Optional[Dict[str, Dict]] = None

@dataclass_json
@dataclass
class GuildMember:
    uuid: str
    name: str
    rank: str
    contributed: int
    joined: str

@dataclass_json
@dataclass
class GuildBanner:
    base: str
    tier: int
    structure: str
    layers: List[Dict[str, str]]

@dataclass_json
@dataclass
class GuildStats:
    name: str
    prefix: str
    level: int
    xpPercent: int
    created: str
    territories: int
    banner: Optional[GuildBanner] = None
    wars: Optional[int] = None
    members: Optional[Union[Dict[str, Dict[str, Dict]], int]] = None
    xp: Optional[int] = None

class WynnCraftAPI:
    def __init__(self):
        self.v3_url = "https://api.wynncraft.com/v3"

    async def get_player_stats(self, identifier: str) -> PlayerStats:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.v3_url}/player/{identifier}?fullResult") as response:
                if response.status == 404:
                    raise HTTPNotFound
                if response.status == 300:
                    raise ValueError("Multiple players found, please use UUID")
                data = await response.json()
                if "globalData" in data:
                    global_data = data["globalData"]
                    for section in ["dungeons", "raids"]:
                        if section in global_data and global_data[section] and "list" not in global_data[section]:
                            global_data[section]["list"] = {
                                k: v for k, v in global_data[section].items()
                                if k != "total" and isinstance(v, int)
                            }
                            for k in list(global_data[section].keys()):
                                if k != "total" and k != "list":
                                    del global_data[section][k]
                return PlayerStats.from_dict(data.get("data", data))

    async def get_guild_stats(self, identifier: str) -> GuildStats:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.v3_url}/guild/{identifier}") as response:
                if response.status == 404:
                    raise HTTPNotFound
                if response.status == 300:
                    raise ValueError("Multiple guilds found, please use exact name or prefix")
                data = await response.json()
                return GuildStats.from_dict(data.get("data", data))

    async def get_leaderboard(self, type: str, result_limit: int = 100) -> Dict:
        async with aiohttp.ClientSession() as session:
            url = f"{self.v3_url}/leaderboards/{type}?resultLimit={result_limit}"
            async with session.get(url) as response:
                if response.status != 200:
                    raise HTTPNotFound
                return await response.json()

    async def get_leaderboard_types(self) -> List[str]:
        async with aiohttp.ClientSession() as session:
            url = f"{self.v3_url}/leaderboards/types"
            async with session.get(url) as response:
                if response.status != 200:
                    raise HTTPNotFound
                return await response.json()

    async def search(self, query: str) -> List[Dict]:
        encoded_query = urllib.parse.quote(query)
        async with aiohttp.ClientSession() as session:
            url = f"{self.v3_url}/search/{encoded_query}"
            async with session.get(url) as response:
                if response.status != 200:
                    raise HTTPNotFound
                data = await response.json()
                results = []
                for uuid, name in data.get("players", {}).items():
                    results.append({"type": "player", "uuid": uuid, "name": name})
                for guild_id, guild_data in data.get("guildsPrefix", {}).items():
                    results.append({"type": "guild", "name": guild_data["name"], "prefix": guild_data["prefix"]})
                return results

@loader.tds
class WynnCraft(loader.Module):
    """Wynncraft API Module"""
    
    async def client_ready(self, client, db):
        self.api = WynnCraftAPI()
        try:
            lb_types = await self.api.get_leaderboard_types()
            self.leaderboard_types = {t: t.replace("Level", "").replace("Completion", "").title() for t in lb_types}
        except Exception:
            self.leaderboard_types = {
                "guildLevel": "Guild Level",
                "guildTerritories": "Guild Territories",
                "guildWars": "Guild Wars",
                "alchemismLevel": "Alchemism",
                "miningLevel": "Mining",
                "woodcuttingLevel": "Woodcutting",
                "farmingLevel": "Farming",
                "fishingLevel": "Fishing",
                "armouringLevel": "Armouring",
                "tailoringLevel": "Tailoring",
                "weaponsmithingLevel": "Weaponsmithing",
                "woodworkingLevel": "Woodworking",
                "jewelingLevel": "Jeweling",
                "scribingLevel": "Scribing",
                "cookingLevel": "Cooking",
                "professionsGlobalLevel": "Professions Global",
                "combatGlobalLevel": "Combat Global",
                "totalGlobalLevel": "Total Global",
                "playerContent": "Player Content",
                "combatSoloLevel": "Combat Solo",
                "professionsSoloLevel": "Professions Solo",
                "totalSoloLevel": "Total Solo",
                "globalPlayerContent": "Global Player Content",
                "huntedContent": "Hunted Content",
                "grootslangCompletion": "Grootslang",
                "colossusCompletion": "Colossus",
                "orphionCompletion": "Orphion",
                "namelessCompletion": "Nameless",
                "warsCompletion": "Wars",
                "craftsmanContent": "Craftsman Content",
                "huicContent": "Huic Content",
                "ironmanContent": "Ironman Content",
                "ultimateIronmanContent": "Ultimate Ironman Content",
                "hardcoreLegacyLevel": "Hardcore Legacy",
                "hardcoreContent": "Hardcore Content",
                "huichContent": "Huich Content",
                "hicContent": "Hic Content",
                "hichContent": "Hich Content",
                "grootslangSrPlayers": "Grootslang Sr Players",
                "namelessSrPlayers": "Nameless Sr Players",
                "colossusSrGuilds": "Colossus Sr Guilds",
                "colossusSrPlayers": "Colossus Sr Players",
                "namelessSrGuilds": "Nameless Sr Guilds",
                "orphionSrPlayers": "Orphion Sr Players",
                "grootslangSrGuilds": "Grootslang Sr Guilds",
                "orphionSrGuilds": "Orphion Sr Guilds"
            }

    strings = {
        "name": "WynnCraft",
        "no_guild": "No guild",
        "offline": "Offline",
        "stats": (
            "<emoji document_id=5411535325535162690>👤</emoji> <b>Player Stats: {player}</b>\n"
            "\n<emoji document_id=5415992848753379520>🗄</emoji> <b>Server</b>: {server}"
            "\n<emoji document_id=5416042764863293485>⏳</emoji> <b>Playtime</b>: {playtime} hours"
            "\n<emoji document_id=5411547329968754408>👥</emoji> <b>Guild</b>: {guild}"
            "\n<emoji document_id=5413515838034561530>⭐</emoji> <b>Quests Completed</b>: {quests}"
            "\n<emoji document_id=5413347492496428200>💎</emoji> <b>Dungeons Completed</b>: {dungeons}"
            "\n<emoji document_id=5418376169055602355>📆</emoji> <b>First Joined</b>: {joindate}"
            "\n<emoji document_id=5418376169055602355>📆</emoji> <b>Last Joined</b>: {lastjoin}"
        ),
        "guild_stats": (
            "<emoji document_id=5411547329968754408>👥</emoji> <b>Guild Stats: {guild}</b>\n"
            "\n<emoji document_id=5415992848753379520>🏷</emoji> <b>Prefix</b>: {prefix}"
            "\n<emoji document_id=5413515838034561530>🎚️</emoji> <b>Level</b>: {level}"
            "\n<emoji document_id=5413515838034561530>📈</emoji> <b>XP Progress</b>: {xpPercent}%"
            "\n<emoji document_id=5413515838034561530>🌍</emoji> <b>Territories</b>: {territories}"
            "\n<emoji document_id=5413515838034561530>⚔️</emoji> <b>Wars</b>: {wars}"
            "\n<emoji document_id=5411547329968754408>👥</emoji> <b>Members</b>: {members}"
            "\n<emoji document_id=5418376169055602355>📆</emoji> <b>Created</b>: {created}"
        ),
        "guild_members": (
            "<emoji document_id=5411547329968754408>👥</emoji> <b>Guild Members: {guild}</b>\n"
            "\n{members_list}"
        ),
        "notfound": "<emoji document_id=5411402525146370107>⚠️</emoji> <b>Not found</b>",
        "extended_info_rankings": (
            "<emoji document_id=5411535325535162690>👤</emoji> <b>Rankings: {player}</b>\n"
            "\n<emoji document_id=5413515838034561530>🏆</emoji> <b>Rankings</b>:"
            "\n{ranking}"
        ),
        "extended_info_prev_rankings": (
            "<emoji document_id=5411535325535162690>👤</emoji> <b>Previous Rankings: {player}</b>\n"
            "\n<emoji document_id=5413515838034561530>📊</emoji> <b>Previous Rankings</b>:"
            "\n{prev_ranking}"
        ),
        "extended_info_global": (
            "<emoji document_id=5411535325535162690>👤</emoji> <b>Global Data: {player}</b>\n"
            "\n<emoji document_id=5413515838034561530>⚔️</emoji> <b>Wars</b>: {wars}"
            "\n<emoji document_id=5413515838034561530>🎚️</emoji> <b>Total Level</b>: {totalLevel}"
            "\n<emoji document_id=5413515838034561530>🧟</emoji> <b>Killed Mobs</b>: {killedMobs}"
            "\n<emoji document_id=5413515838034561530>📦</emoji> <b>Chests Found</b>: {chestsFound}"
            "\n<emoji document_id=5413515838034561530>📜</emoji> <b>Quests Completed</b>: {quests}"
        ),
        "extended_info_pvp": (
            "<emoji document_id=5411535325535162690>👤</emoji> <b>PvP: {player}</b>\n"
            "\n<emoji document_id=5413515838034561530>⚔️</emoji> <b>Kills</b>: {kills}"
            "\n<emoji document_id=5413515838034561530>💀</emoji> <b>Deaths</b>: {deaths}"
        ),
        "extended_info_dungeons": (
            "<emoji document_id=5411535325535162690>👤</emoji> <b>Dungeons: {player}</b>\n"
            "\n<emoji document_id=5413347492496428200>💎</emoji> <b>Total Dungeons</b>: {total}"
            "\n{dungeons_list}"
        ),
        "extended_info_raids": (
            "<emoji document_id=5411535325535162690>👤</emoji> <b>Raids: {player}</b>\n"
            "\n<emoji document_id=5413515838034561530>⚔️</emoji> <b>Total Raids</b>: {total}"
            "\n{raids_list}"
        ),
        "extended_info_characters": (
            "<emoji document_id=5411535325535162690>👤</emoji> <b>Characters: {player}</b>\n"
            "\n<emoji document_id=5413515838034561530>🎭</emoji> <b>Characters</b>:"
            "\n{characters_list}"
        ),
        "leaderboard": "<emoji document_id=5413515838034561530>⭐</emoji> <b>{title}</b>\n",
        "leaderboard_select": "<emoji document_id=5413515838034561530>🏆</emoji> <b>Choose Leaderboard</b>",
        "search_results": "<emoji document_id=5411535325535162690>🔍</emoji> <b>Search Results for '{query}'</b>\n",
        "no_results": "<emoji document_id=5411402525146370107>⚠️</emoji> <b>No results found</b>",
        "prev_page": "⬅️ Previous",
        "next_page": "Next ➡️",
        "btn_more": "More Info",
        "btn_back": "Back",
        "btn_rankings": "Rankings",
        "btn_prev_rankings": "Prev Rankings",
        "btn_global": "Global Data",
        "btn_pvp": "PvP",
        "btn_dungeons": "Dungeons",
        "btn_raids": "Raids",
        "btn_characters": "Characters",
        "btn_solo": "Solo",
        "btn_global": "Global",
        "btn_pvp_leaderboard": "PvP",
        "btn_guild": "Guilds",
        "btn_gamemodes": "Gamemodes",
        "btn_raids": "Raids",
        "error_player_notfound": "Player not found",
        "error_guild_notfound": "Guild not found",
        "error_leaderboard_failed": "Failed to load leaderboard",
        "error_no_results": "No results found",
        "error_multiple_choices": "Multiple players or guilds found, please use exact name or UUID"
    }

    strings_ru = {
        "no_guild": "Без гильдии",
        "offline": "Офлайн",
        "stats": (
            "<emoji document_id=5411535325535162690>👤</emoji> <b>Статистика игрока: {player}</b>\n"
            "\n<emoji document_id=5415992848753379520>🗄</emoji> <b>Сервер</b>: {server}"
            "\n<emoji document_id=5416042764863293485>⏳</emoji> <b>Время в игре</b>: {playtime} ч"
            "\n<emoji document_id=5411547329968754408>👥</emoji> <b>Гильдия</b>: {guild}"
            "\n<emoji document_id=5413515838034561530>⭐</emoji> <b>Выполнено квестов</b>: {quests}"
            "\n<emoji document_id=5413347492496428200>💎</emoji> <b>Пройдено подземелий</b>: {dungeons}"
            "\n<emoji document_id=5418376169055602355>📆</emoji> <b>Первый вход</b>: {joindate}"
            "\n<emoji document_id=5418376169055602355>📆</emoji> <b>Последний вход</b>: {lastjoin}"
        ),
        "guild_stats": (
            "<emoji document_id=5411547329968754408>👥</emoji> <b>Статистика гильдии: {guild}</b>\n"
            "\n<emoji document_id=5415992848753379520>🏷</emoji> <b>Префикс</b>: {prefix}"
            "\n<emoji document_id=5413515838034561530>🎚️</emoji> <b>Уровень</b>: {level}"
            "\n<emoji document_id=5413515838034561530>📈</emoji> <b>Прогресс опыта</b>: {xpPercent}%"
            "\n<emoji document_id=5413515838034561530>🌍</emoji> <b>Территории</b>: {territories}"
            "\n<emoji document_id=5413515838034561530>⚔️</emoji> <b>Войны</b>: {wars}"
            "\n<emoji document_id=5411547329968754408>👥</emoji> <b>Участники</b>: {members}"
            "\n<emoji document_id=5418376169055602355>📆</emoji> <b>Создана</b>: {created}"
        ),
        "guild_members": (
            "<emoji document_id=5411547329968754408>👥</emoji> <b>Участники гильдии: {guild}</b>\n"
            "\n{members_list}"
        ),
        "notfound": "<emoji document_id=5411402525146370107>⚠️</emoji> <b>Не найдено</b>",
        "extended_info_rankings": (
            "<emoji document_id=5411535325535162690>👤</emoji> <b>Рейтинги: {player}</b>\n"
            "\n<emoji document_id=5413515838034561530>🏆</emoji> <b>Рейтинги</b>:"
            "\n{ranking}"
        ),
        "extended_info_prev_rankings": (
            "<emoji document_id=5411535325535162690>👤</emoji> <b>Предыдущие рейтинги: {player}</b>\n"
            "\n<emoji document_id=5413515838034561530>📊</emoji> <b>Предыдущие рейтинги</b>:"
            "\n{prev_ranking}"
        ),
        "extended_info_global": (
            "<emoji document_id=5411535325535162690>👤</emoji> <b>Глобальные данные: {player}</b>\n"
            "\n<emoji document_id=5413515838034561530>⚔️</emoji> <b>Войны</b>: {wars}"
            "\n<emoji document_id=5413515838034561530>🎚️</emoji> <b>Общий уровень</b>: {totalLevel}"
            "\n<emoji document_id=5413515838034561530>🧟</emoji> <b>Убито мобов</b>: {killedMobs}"
            "\n<emoji document_id=5413515838034561530>📦</emoji> <b>Найдено сундуков</b>: {chestsFound}"
            "\n<emoji document_id=5413515838034561530>📜</emoji> <b>Выполнено квестов</b>: {quests}"
        ),
        "extended_info_pvp": (
            "<emoji document_id=5411535325535162690>👤</emoji> <b>PvP: {player}</b>\n"
            "\n<emoji document_id=5413515838034561530>⚔️</emoji> <b>Убийства</b>: {kills}"
            "\n<emoji document_id=5413515838034561530>💀</emoji> <b>Смерти</b>: {deaths}"
        ),
        "extended_info_dungeons": (
            "<emoji document_id=5411535325535162690>👤</emoji> <b>Подземелья: {player}</b>\n"
            "\n<emoji document_id=5413347492496428200>💎</emoji> <b>Всего подземелий</b>: {total}"
            "\n{dungeons_list}"
        ),
        "extended_info_raids": (
            "<emoji document_id=5411535325535162690>👤</emoji> <b>Рейды: {player}</b>\n"
            "\n<emoji document_id=5413515838034561530>⚔️</emoji> <b>Всего рейдов</b>: {total}"
            "\n{raids_list}"
        ),
        "extended_info_characters": (
            "<emoji document_id=5411535325535162690>👤</emoji> <b>Персонажи: {player}</b>\n"
            "\n<emoji document_id=5413515838034561530>🎭</emoji> <b>Персонажи</b>:"
            "\n{characters_list}"
        ),
        "leaderboard": "<emoji document_id=5413515838034561530>⭐</emoji> <b>{title}</b>\n",
        "leaderboard_select": "<emoji document_id=5413515838034561530>🏆</emoji> <b>Выберите лидерборд</b>",
        "search_results": "<emoji document_id=5411535325535162690>🔍</emoji> <b>Результаты поиска для '{query}'</b>\n",
        "no_results": "<emoji document_id=5411402525146370107>⚠️</emoji> <b>Результаты не найдены</b>",
        "prev_page": "⬅️ Назад",
        "next_page": "Вперёд ➡️",
        "btn_more": "Подробнее",
        "btn_back": "Назад",
        "btn_rankings": "Рейтинги",
        "btn_prev_rankings": "Пред. рейтинги",
        "btn_global": "Глобальные данные",
        "btn_pvp": "PvP",
        "btn_dungeons": "Подземелья",
        "btn_raids": "Рейды",
        "btn_characters": "Персонажи",
        "btn_solo": "Соло",
        "btn_global": "Глобальный",
        "btn_pvp_leaderboard": "PvP",
        "btn_guild": "Гильдии",
        "btn_gamemodes": "Игровые режимы",
        "btn_raids": "Рейды",
        "error_player_notfound": "Игрок не найден",
        "error_guild_notfound": "Гильдия не найдена",
        "error_leaderboard_failed": "Не удалось загрузить лидерборд",
        "error_no_results": "Результаты не найдены",
        "error_multiple_choices": "Найдено несколько игроков или гильдий, используйте точное название или UUID"
    }

    def format_ranking(self, ranking: Dict[str, int]) -> str:
        formatted = ""
        for key, value in ranking.items():
            human_key = self.leaderboard_types.get(key.lower(), None)
            if not human_key:
                key = key.lower()
                key = re.sub(r'level$', ' Level', key)
                key = re.sub(r'global', 'Global ', key)
                key = re.sub(r'solo', 'Solo ', key)
                key = re.sub(r'content', 'Content', key)
                human_key = ' '.join(word.capitalize() for word in key.split())
            formatted += f"  - {human_key}: {value}\n"
        return formatted or "  - None"

    def format_dungeons(self, dungeons: Optional[Dungeons]) -> str:
        if not dungeons or not dungeons.list:
            return "  - None"
        return "\n".join(f"  - {key}: {value}" for key, value in dungeons.list.items())

    def format_raids(self, raids: Optional[Raids]) -> str:
        if not raids or not raids.list:
            return "  - None"
        return "\n".join(f"  - {key}: {value}" for key, value in raids.list.items())

    def format_guild_members(self, members: Optional[Union[Dict[str, Dict[str, Dict]], int]]) -> str:
        if not members:
            return "  - None"
        if isinstance(members, int):
            return f"  - Total: {members}"
        if not members.get("total"):
            return "  - None"
        formatted = []
        for rank, players in members.items():
            if rank == "total":
                continue
            for name, data in players.items():
                joined = datetime.fromisoformat(data["joined"].replace('Z', '+00:00')).strftime('%d.%m.%Y')
                formatted.append(f"  - {name} ({rank.capitalize()}): Joined {joined}")
        return "\n".join(formatted[:10]) or "  - None"

    def format_characters(self, characters: Optional[Dict[str, Dict]]) -> str:
        if not characters:
            return "  - None"
        formatted = []
        for uuid, char_data in list(characters.items())[:5]:  # Limit to 5 characters
            char_type = char_data.get("type", "Unknown")
            level = char_data.get("level", 0)
            xp = char_data.get("xp", 0)
            xp_percent = char_data.get("xpPercent", 0)
            gamemodes = ", ".join(char_data.get("gamemode", [])) or "None"
            died = "Yes" if char_data.get("meta", {}).get("died", False) else "No"
            skills = char_data.get("skillPoints", {})
            professions = char_data.get("professions", {})
            dungeons = char_data.get("dungeons", {}).get("total", 0)
            raids = char_data.get("raids", {}).get("total", 0)
            formatted.append(
                f"  - {char_type} (Level {level})\n"
                f"    - XP: {xp} ({xp_percent}%)\n"
                f"    - Gamemodes: {gamemodes}\n"
                f"    - Died: {died}\n"
                f"    - Skills:\n"
                f"      - Strength: {skills.get('strength', 0)}\n"
                f"      - Dexterity: {skills.get('dexterity', 0)}\n"
                f"      - Intelligence: {skills.get('intelligence', 0)}\n"
                f"      - Defence: {skills.get('defence', 0)}\n"
                f"      - Agility: {skills.get('agility', 0)}\n"
                f"    - Professions:\n"
                f"      - Fishing: {professions.get('fishing', {}).get('level', 0)}\n"
                f"      - Mining: {professions.get('mining', {}).get('level', 0)}\n"
                f"      - Woodcutting: {professions.get('woodcutting', {}).get('level', 0)}\n"
                f"      - Farming: {professions.get('farming', {}).get('level', 0)}\n"
                f"    - Dungeons: {dungeons}\n"
                f"    - Raids: {raids}"
            )
        return "\n".join(formatted) or "  - None"

    def format_leaderboard_entry(self, entry: Dict, lb_type: str) -> str:
        if "Guild" in lb_type:
            return (
                f"{entry['num']}. <a href=\"https://wynncraft.com/stats/guild/{urllib.parse.quote(entry['name'])}\">{entry['prefix']} {entry['name']}</a>\n"
                f"  - Score: {entry.get('score', 'N/A')}\n"
                f"  - Members: {entry.get('members', 'N/A')}\n"
                f"  - Level: {entry.get('level', 'N/A')}\n"
            )
        elif lb_type == "warsCompletion":
            return (
                f"{entry['num']}. <a href=\"https://wynncraft.com/stats/player/{urllib.parse.quote(entry['name'])}\">{entry['name']}</a>\n"
                f"  - Score: {entry.get('score', 'N/A')}\n"
                f"  - Previous Rank: {entry.get('previousRanking', 'N/A')}\n"
            )
        elif lb_type in ["grootslangCompletion", "colossusCompletion", "orphionCompletion", "namelessCompletion"]:
            metadata = entry.get("metadata", {})
            return (
                f"{entry['num']}. <a href=\"https://wynncraft.com/stats/player/{urllib.parse.quote(entry['name'])}\">{entry['name']}</a>\n"
                f"  - Score: {entry.get('score', 'N/A')}\n"
                f"  - Completions: {metadata.get('completions', 'N/A')}\n"
                f"  - Gambits Used: {metadata.get('gambitsUsed', 'N/A')}\n"
            )
        else:
            metadata = entry.get("metadata", {})
            return (
                f"{entry['num']}. <a href=\"https://wynncraft.com/stats/player/{urllib.parse.quote(entry['name'])}\">{entry['name']}</a>\n"
                f"  - Score: {entry.get('score', 'N/A')}\n"
                f"  - XP: {metadata.get('xp', 'N/A')}\n"
                f"  - Previous Rank: {entry.get('previousRanking', 'N/A')}\n"
            )

    def get_extended_info_buttons(self, player_id: str, stats_text: str, current_category: str) -> List[Dict]:
        categories = ["rankings", "prev_rankings", "global", "pvp", "dungeons", "raids", "characters"]
        buttons = []
        for category in categories:
            text = f"🟢 {self.strings[f'btn_{category}']}" if category == current_category else self.strings[f"btn_{category}"]
            buttons.append({"text": text, "callback": self.show_extended_info, "args": (player_id, stats_text, category)})
        buttons.append({"text": self.strings["btn_back"], "callback": self.show_stats, "args": (stats_text, player_id)})
        return [
            buttons[0:2],  # Rankings, Prev Rankings
            buttons[2:4],  # Global, PvP
            buttons[4:6],  # Dungeons, Raids
            [buttons[6]],  # Characters
            [buttons[7]]   # Back
        ]

    def get_guild_info_buttons(self, guild_id: str, stats_text: str, current_category: str) -> List[Dict]:
        categories = ["members"]
        buttons = [
            {
                "text": f"🟢 {self.strings[f'btn_{category}']}" if category == current_category else self.strings[f"btn_{category}"],
                "callback": self.show_guild_extended_info,
                "args": (guild_id, stats_text, category)
            }
            for category in categories
        ]
        buttons.append({
            "text": self.strings["btn_back"],
            "callback": self.show_guild_stats,
            "args": (stats_text, guild_id)
        })
        return [buttons]

    async def show_extended_info(self, call: InlineCall, player_id: str, stats_text: str, category: str = "rankings"):
        try:
            stats = await self.api.get_player_stats(player_id)
            if category == "rankings":
                text = self.strings["extended_info_rankings"].format(
                    player=stats.username,
                    ranking=self.format_ranking(stats.ranking)
                )
            elif category == "prev_rankings":
                text = self.strings["extended_info_prev_rankings"].format(
                    player=stats.username,
                    prev_ranking=self.format_ranking(stats.previousRanking)
                )
            elif category == "global":
                text = self.strings["extended_info_global"].format(
                    player=stats.username,
                    wars=stats.globalData.wars,
                    totalLevel=stats.globalData.totalLevel,
                    killedMobs=stats.globalData.killedMobs,
                    chestsFound=stats.globalData.chestsFound,
                    quests=stats.globalData.completedQuests
                )
            elif category == "pvp":
                text = self.strings["extended_info_pvp"].format(
                    player=stats.username,
                    kills=stats.globalData.pvp.kills,
                    deaths=stats.globalData.pvp.deaths
                )
            elif category == "dungeons":
                text = self.strings["extended_info_dungeons"].format(
                    player=stats.username,
                    total=stats.globalData.dungeons.total if stats.globalData.dungeons else 0,
                    dungeons_list=self.format_dungeons(stats.globalData.dungeons)
                )
            elif category == "raids":
                text = self.strings["extended_info_raids"].format(
                    player=stats.username,
                    total=stats.globalData.raids.total if stats.globalData.raids else 0,
                    raids_list=self.format_raids(stats.globalData.raids)
                )
            elif category == "characters":
                text = self.strings["extended_info_characters"].format(
                    player=stats.username,
                    characters_list=self.format_characters(stats.characters)
                )
            await call.edit(
                text,
                reply_markup=self.get_extended_info_buttons(player_id, stats_text, category)
            )
        except HTTPNotFound:
            await call.answer(self.strings["error_player_notfound"], show_alert=True)
        except ValueError:
            await call.answer(self.strings["error_multiple_choices"], show_alert=True)

    async def show_stats(self, call: InlineCall, stats_text: str, player_id: str):
        await call.edit(
            stats_text,
            reply_markup=[
                [{"text": self.strings["btn_more"], "callback": self.show_extended_info, "args": (player_id, stats_text, "rankings")}]
            ]
        )

    async def show_guild_extended_info(self, call: InlineCall, guild_id: str, stats_text: str, category: str = "members"):
        try:
            stats = await self.api.get_guild_stats(guild_id)
            if category == "members":
                text = self.strings["guild_members"].format(
                    guild=stats.name,
                    members_list=self.format_guild_members(stats.members)
                )
            await call.edit(
                text,
                reply_markup=self.get_guild_info_buttons(guild_id, stats_text, category)
            )
        except HTTPNotFound:
            await call.answer(self.strings["error_guild_notfound"], show_alert=True)
        except ValueError:
            await call.answer(self.strings["error_multiple_choices"], show_alert=True)

    async def show_guild_stats(self, call: InlineCall, stats_text: str, guild_id: str):
        await call.edit(
            stats_text,
            reply_markup=[
                [{"text": self.strings["btn_members"], "callback": self.show_guild_extended_info, "args": (guild_id, stats_text, "members")}]
            ]
        )

    @loader.command()
    async def wstatscmd(self, message: Message):
        """[Username / uuid] - Player stats"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings["notfound"])
            return

        try:
            stats = await self.api.get_player_stats(args)
        except HTTPNotFound:
            await utils.answer(message, self.strings["notfound"])
            return
        except ValueError:
            await utils.answer(message, self.strings["error_multiple_choices"])
            return

        guild_text = f"{stats.guild.name} ({stats.guild.rank})" if stats.guild else self.strings["no_guild"]
        stats_text = self.strings["stats"].format(
            player=args,
            server=stats.server or self.strings["offline"],
            playtime=f"{stats.playtime:.2f}",
            guild=guild_text,
            quests=stats.globalData.completedQuests,
            dungeons=stats.globalData.dungeons.total if stats.globalData.dungeons else 0,
            joindate=datetime.fromisoformat(stats.firstJoin.replace("Z", "+00:00")).strftime("%d.%m.%Y"),
            lastjoin=datetime.fromisoformat(stats.lastJoin.replace("Z", "+00:00")).strftime("%d.%m.%Y %H:%M")
        )

        await self.inline.form(
            message=message,
            text=stats_text,
            reply_markup=[
                [{"text": self.strings["btn_more"], "callback": self.show_extended_info, "args": (args, stats_text, "rankings")}]
            ]
        )

    @loader.command()
    async def wguildcmd(self, message: Message):
        """[GuildName / Prefix] - Guild stats"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings["notfound"])
            return

        try:
            stats = await self.api.get_guild_stats(args)
        except HTTPNotFound:
            await utils.answer(message, self.strings["notfound"])
            return
        except ValueError:
            await utils.answer(message, self.strings["error_multiple_choices"])
            return

        members_count = stats.members if isinstance(stats.members, int) else stats.members.get("total", 0)
        stats_text = self.strings["guild_stats"].format(
            guild=stats.name,
            prefix=stats.prefix,
            level=stats.level,
            xpPercent=stats.xpPercent,
            territories=stats.territories,
            wars=stats.wars or 0,
            members=members_count,
            created=datetime.fromisoformat(stats.created.replace("Z", "+00:00")).strftime("%d.%m.%Y")
        )

        await self.inline.form(
            message=message,
            text=stats_text,
            reply_markup=[
                [{"text": self.strings["btn_members"], "callback": self.show_guild_extended_info, "args": (args, stats_text, "members")}]
            ]
        )

    @loader.command()
    async def wleaderboardcmd(self, message: Message):
        """Show Wynncraft leaderboards"""
        await self.inline.form(
            message=message,
            text=self.strings["leaderboard_select"],
            reply_markup=[
                [
                    {"text": self.strings["btn_solo"], "callback": self.show_leaderboard_menu, "args": ("solo",)},
                    {"text": self.strings["btn_global"], "callback": self.show_leaderboard_menu, "args": ("global",)},
                    {"text": self.strings["btn_pvp_leaderboard"], "callback": self.show_leaderboard, "args": ("warsCompletion",)},
                    {"text": self.strings["btn_guild"], "callback": self.show_leaderboard_menu, "args": ("guild",)},
                    {"text": self.strings["btn_gamemodes"], "callback": self.show_leaderboard_menu, "args": ("gamemodes",)},
                    {"text": self.strings["btn_raids"], "callback": self.show_leaderboard_menu, "args": ("raids",)}
                ]
            ]
        )

    @loader.command()
    async def wsearchcmd(self, message: Message):
        """[Query] - Search for players or guilds"""
        query = utils.get_args_raw(message)
        if not query:
            await utils.answer(message, self.strings["notfound"])
            return

        try:
            results = await self.api.search(query)
            if not results:
                await utils.answer(message, self.strings["no_results"])
                return

            await self.show_search_results(None, message, query, results, page=0)
        except HTTPNotFound:
            await utils.answer(message, self.strings["no_results"])

    async def show_leaderboard_menu(self, call: InlineCall, category: str):
        try:
            lb_types = await self.api.get_leaderboard_types()
            buttons = []
            if category == "solo":
                buttons = [
                    [
                        {"text": "Total", "callback": self.show_leaderboard, "args": ("totalSoloLevel",)},
                        {"text": "Combat", "callback": self.show_leaderboard, "args": ("combatSoloLevel",)}
                    ],
                    [
                        {"text": "Professions", "callback": self.show_leaderboard, "args": ("professionsSoloLevel",)},
                        {"text": "Mining", "callback": self.show_leaderboard, "args": ("miningLevel",)}
                    ],
                    [
                        {"text": "Woodcutting", "callback": self.show_leaderboard, "args": ("woodcuttingLevel",)},
                        {"text": "Farming", "callback": self.show_leaderboard, "args": ("farmingLevel",)}
                    ],
                    [
                        {"text": "Fishing", "callback": self.show_leaderboard, "args": ("fishingLevel",)},
                        {"text": "Armouring", "callback": self.show_leaderboard, "args": ("armouringLevel",)}
                    ],
                    [
                        {"text": "Tailoring", "callback": self.show_leaderboard, "args": ("tailoringLevel",)},
                        {"text": "Weaponsmithing", "callback": self.show_leaderboard, "args": ("weaponsmithingLevel",)}
                    ],
                    [
                        {"text": "Woodworking", "callback": self.show_leaderboard, "args": ("woodworkingLevel",)},
                        {"text": "Jeweling", "callback": self.show_leaderboard, "args": ("jewelingLevel",)}
                    ],
                    [
                        {"text": "Scribing", "callback": self.show_leaderboard, "args": ("scribingLevel",)},
                        {"text": "Cooking", "callback": self.show_leaderboard, "args": ("cookingLevel",)}
                    ],
                    [
                        {"text": "Alchemism", "callback": self.show_leaderboard, "args": ("alchemismLevel",)}
                    ]
                ]
            elif category == "global":
                buttons = [
                    [
                        {"text": "Total", "callback": self.show_leaderboard, "args": ("totalGlobalLevel",)},
                        {"text": "Combat", "callback": self.show_leaderboard, "args": ("combatGlobalLevel",)}
                    ],
                    [
                        {"text": "Professions", "callback": self.show_leaderboard, "args": ("professionsGlobalLevel",)},
                        {"text": "Player Content", "callback": self.show_leaderboard, "args": ("globalPlayerContent",)}
                    ]
                ]
            elif category == "guild":
                buttons = [
                    [
                        {"text": "Level", "callback": self.show_leaderboard, "args": ("guildLevel",)},
                        {"text": "Territories", "callback": self.show_leaderboard, "args": ("guildTerritories",)}
                    ],
                    [
                        {"text": "Wars", "callback": self.show_leaderboard, "args": ("guildWars",)},
                        {"text": "Colossus SR", "callback": self.show_leaderboard, "args": ("colossusSrGuilds",)}
                    ],
                    [
                        {"text": "Nameless SR", "callback": self.show_leaderboard, "args": ("namelessSrGuilds",)},
                        {"text": "Grootslang SR", "callback": self.show_leaderboard, "args": ("grootslangSrGuilds",)}
                    ],
                    [
                        {"text": "Orphion SR", "callback": self.show_leaderboard, "args": ("orphionSrGuilds",)}
                    ]
                ]
            elif category == "gamemodes":
                gamemode_types = [t for t in lb_types if "Content" in t and "Player" not in t]
                buttons = [
                    [
                        {"text": t.replace("Content", "").title(), "callback": self.show_leaderboard, "args": (t,)}
                        for t in gamemode_types[i:i+2]
                    ]
                    for i in range(0, len(gamemode_types), 2)
                ]
            elif category == "raids":
                raid_types = [t for t in lb_types if "Completion" in t or "SrPlayers" in t]
                buttons = [
                    [
                        {"text": t.replace("Completion", "").replace("SrPlayers", "SR").title(), "callback": self.show_leaderboard, "args": (t,)}
                        for t in raid_types[i:i+2]
                    ]
                    for i in range(0, len(raid_types), 2)
                ]
            buttons.append([{"text": self.strings["btn_back"], "callback": self.show_leaderboard_select}])
            await call.edit(
                self.strings["leaderboard_select"],
                reply_markup=buttons
            )
        except HTTPNotFound:
            await call.answer(self.strings["error_leaderboard_failed"], show_alert=True)

    async def show_leaderboard(self, call: InlineCall, leaderboard_type: str):
        try:
            leaderboard = await self.api.get_leaderboard(leaderboard_type)
            title = self.leaderboard_types.get(leaderboard_type, leaderboard_type.replace("/", " ").title())
            text = self.strings["leaderboard"].format(title=title)
            for pos, entry in list(leaderboard.items())[:10]:
                entry["num"] = pos
                text += self.format_leaderboard_entry(entry, leaderboard_type)
            await call.edit(
                text,
                reply_markup=[
                    [
                        {"text": self.strings["btn_solo"], "callback": self.show_leaderboard_menu, "args": ("solo",)},
                        {"text": self.strings["btn_global"], "callback": self.show_leaderboard_menu, "args": ("global",)},
                        {"text": self.strings["btn_pvp_leaderboard"], "callback": self.show_leaderboard, "args": ("warsCompletion",)},
                        {"text": self.strings["btn_guild"], "callback": self.show_leaderboard_menu, "args": ("guild",)},
                        {"text": self.strings["btn_gamemodes"], "callback": self.show_leaderboard_menu, "args": ("gamemodes",)},
                        {"text": self.strings["btn_raids"], "callback": self.show_leaderboard_menu, "args": ("raids",)}
                    ],
                    [{"text": self.strings["btn_back"], "callback": self.show_leaderboard_select}]
                ]
            )
        except HTTPNotFound:
            await call.answer(self.strings["error_leaderboard_failed"], show_alert=True)

    async def show_leaderboard_select(self, call: InlineCall):
        await call.edit(
            self.strings["leaderboard_select"],
            reply_markup=[
                [
                    {"text": self.strings["btn_solo"], "callback": self.show_leaderboard_menu, "args": ("solo",)},
                    {"text": self.strings["btn_global"], "callback": self.show_leaderboard_menu, "args": ("global",)},
                    {"text": self.strings["btn_pvp_leaderboard"], "callback": self.show_leaderboard, "args": ("warsCompletion",)},
                    {"text": self.strings["btn_guild"], "callback": self.show_leaderboard_menu, "args": ("guild",)},
                    {"text": self.strings["btn_gamemodes"], "callback": self.show_leaderboard_menu, "args": ("gamemodes",)},
                    {"text": self.strings["btn_raids"], "callback": self.show_leaderboard_menu, "args": ("raids",)}
                ]
            ]
        )

    async def show_search_results(self, call: Optional[InlineCall], message: Message, query: str, results: List[Dict], page: int):
        items_per_page = 5
        start = page * items_per_page
        end = start + items_per_page
        results_page = results[start:end]

        text = self.strings["search_results"].format(query=query)
        for result in results_page:
            if result["type"] == "player":
                text += (
                    f"<a href=\"https://wynncraft.com/stats/player/{urllib.parse.quote(result['name'])}\">{result['name']}</a> (Player)\n"
                    f"  - UUID: {result.get('uuid', 'N/A')}\n"
                )
            else:
                text += (
                    f"<a href=\"https://wynncraft.com/stats/guild/{urllib.parse.quote(result['name'])}\">{result['name']}</a> (Guild)\n"
                    f"  - Prefix: {result.get('prefix', 'N/A')}\n"
                )

        reply_markup = []
        row = []
        if page > 0:
            row.append({"text": self.strings["prev_page"], "callback": self.show_search_results, "args": (message, query, results, page - 1)})
        if end < len(results):
            row.append({"text": self.strings["next_page"], "callback": self.show_search_results, "args": (message, query, results, page + 1)})
        if row:
            reply_markup.append(row)
        reply_markup.append([{"text": self.strings["btn_back"], "callback": self.show_search_menu, "args": (query,)}])

        if call:
            await call.edit(
                text,
                reply_markup=reply_markup
            )
        else:
            await self.inline.form(
                message=message,
                text=text,
                reply_markup=reply_markup
            )

    async def show_search_menu(self, call: InlineCall, query: str):
        try:
            results = await self.api.search(query)
            if not results:
                await call.edit(self.strings["no_results"])
                return
            await self.show_search_results(call, call.message, query, results, page=0)
        except HTTPNotFound:
            await call.edit(self.strings["no_results"])