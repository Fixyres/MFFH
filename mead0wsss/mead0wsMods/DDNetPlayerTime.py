# -- version --
__version__ = (1, 0, 0)
# -- version --


# ███╗░░░███╗███████╗░█████╗░██████╗░░█████╗░░██╗░░░░░░░██╗░██████╗░██████╗
# ████╗░████║██╔════╝██╔══██╗██╔══██╗██╔══██╗░██║░░██╗░░██║██╔════╝██╔════╝
# ██╔████╔██║█████╗░░███████║██║░░██║██║░░██║░╚██╗████╗██╔╝╚█████╗░╚█████╗░
# ██║╚██╔╝██║██╔══╝░░██╔══██║██║░░██║██║░░██║░░████╔═████║░░╚═══██╗░╚═══██╗
# ██║░╚═╝░██║███████╗██║░░██║██████╔╝╚█████╔╝░░╚██╔╝░╚██╔╝░██████╔╝██████╔╝
# ╚═╝░░░░░╚═╝╚══════╝╚═╝░░╚═╝╚═════╝░░╚════╝░░░░╚═╝░░░╚═╝░░╚═════╝░╚═════╝░
#                © Copyright 2025
#            ✈ https://t.me/mead0wssMods


# meta developer: @mead0wssMods
# scope: heroku_only

import herokutl
from .. import loader, utils
import aiohttp

@loader.tds
class DDNetPlayerTime(loader.Module):
    """Получение статистики отыгранного времени игрока DDNet с ddstats.tw"""

    strings = {
        "name": "DDNetPT",
        "no_args": "<emoji document_id=5980953710157632545>❌</emoji><b> Укажите ник игрока!</b>",
        "api_error_or_player_not_found": "<emoji document_id=5980953710157632545>❌</emoji><b> Возможно данный игрок не найден либо ошибка на стороне API</b>",
    }

    async def client_ready(self, client, db):
        self.client = client

    @loader.command()
    async def ddpt(self, message):
        """<ник> | Получить статистику игрока"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings["no_args"])
            return

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://ddstats.tw/player/json?player={args}") as resp:
                    if resp.status != 200:
                        await utils.answer(message, self.strings["api_error_or_player_not_found"])
                        return
                    data = await resp.json()
                    response = ""
                    gametypes = data.get("most_played_gametypes", [])
                    if gametypes:
                        gametypes_str = []
                        for gt in gametypes:
                            hours = round(gt.get("seconds_played", 0) / 3600)
                            gametypes_str.append(f"{gt.get('key', '?')} - <code>{hours}ч</code>")
                        
                        response += f"<b><emoji document_id=6032693626394382504>👤</emoji> Игрок: <code>{args}</code>\n\n<emoji document_id=5908961403917570106>📌</emoji> Тип:\n<blockquote>" + "\n".join(gametypes_str) + "</blockquote>\n\n</b>"

                    # мапы
                    maps = data.get("most_played_maps", [])
                    if maps:
                        maps_str = []
                        for m in maps:
                            hours = round(m.get("seconds_played", 0) / 3600)
                            maps_str.append(f"{m.get('map_name', '?')} - <code>{hours}ч</code>")
                        
                        response += "<b><emoji document_id=5985479497586053461>🗺</emoji> Карта:\n<blockquote>" + "\n".join(maps_str) + "</blockquote>\n\n</b>"

                    # категории
                    categories = data.get("most_played_categories", [])
                    if categories:
                        categories_str = []
                        for cat in categories:
                            hours = round(cat.get("seconds_played", 0) / 3600)
                            categories_str.append(f"{cat.get('key', '?')} - <code>{hours}ч</code>")
                        
                        response += "<b><emoji document_id=5924720918826848520>📦</emoji> Категория:\n<blockquote>" + "\n".join(categories_str) + "</blockquote>\n\n</b>"

                    # время
                    general = data.get("general_activity", {})
                    if general:
                        total_hours = round(general.get("total_seconds_played", 0) / 3600)
                        avg_hours = round(general.get("average_seconds_played", 0) / 3600)
                        start_date = general.get("start_of_playtime", "?")
                        response += "<b><emoji document_id=5870729937215819584>⏰️</emoji> Время:\n<blockquote>"
                        response += f"Общее время игры - <code>{total_hours}ч</code>\n"
                        response += f"Дата начала игры - <code>{start_date}</code>\n"
                        response += f"Среднее время игры - <code>{avg_hours}ч</code>"
                        response += "</blockquote></b>"

                    await utils.answer(message, response)

        except Exception as e:
            await utils.answer(message, f"{self.strings['api_error_or_player_not_found']}: {str(e)}")

# ебеший-ленеивый говнокод
