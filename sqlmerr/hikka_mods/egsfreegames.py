"""
░██████╗░██████╗░██╗░░░░░███╗░░░███╗███████╗██████╗░██████╗░
██╔════╝██╔═══██╗██║░░░░░████╗░████║██╔════╝██╔══██╗██╔══██╗
╚█████╗░██║██╗██║██║░░░░░██╔████╔██║█████╗░░██████╔╝██████╔╝
░╚═══██╗╚██████╔╝██║░░░░░██║╚██╔╝██║██╔══╝░░██╔══██╗██╔══██╗
██████╔╝░╚═██╔═╝░███████╗██║░╚═╝░██║███████╗██║░░██║██║░░██║
╚═════╝░░░░╚═╝░░░╚══════╝╚═╝░░░░░╚═╝╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝
"""

# meta developer: @sqlmerr_m
# meta icon: https://github.com/sqlmerr/hikka_mods/blob/main/assets/icons/egsfreegames.png?raw=true
# meta banner: https://github.com/sqlmerr/hikka_mods/blob/main/assets/banners/egsfreegames.png?raw=true

import logging
from typing import Dict, List, Optional

import datetime
import aiohttp

from .. import utils, loader
from hikkatl.tl.patched import Message


@loader.tds
class EGSFreeGames(loader.Module):
    """Module for checking free games in Epic Games Store. Inline bot will send them every day in special chat"""

    strings = {
        "name": "EGSFreeGames",
        "game": (
            "-  <b>Game</b>: {title}\n"
            "    <i>Status</i>: {status}\n"
            "    <i>Promotion started at</i>: <code>{start}</code>\n"
            "    <i>Promotion will end at</i>: <code>{end}</code>\n"
            "    <i>Link</i>: {url}\n"
        ),
        "header": "<emoji document_id=5472282432436708545>🎮</emoji> <b>Free games in EGS:</b>",
        "header_bot": "🎮 <b>Today's free games in EGS:</b>",
        "footer": "<emoji document_id=6028435952299413210>ℹ️</emoji> <i>The </i><code>active</code><i> status means that the game can be picked up now.\nThe </i><code>upcoming</code><i> status means that the game can be picked up later</i>",
        "_region_cfg": "Free games check region",
        "_schedule_checking_cfg": "Will the bot automatically send the current free games to a special chat room",
    }
    strings_ru = {
        "game": (
            "-  <b>Игра</b>: {title}\n"
            "    <i>Статус</i>: {status}\n"
            "    <i>Акция началась</i>: <code>{start}</code>\n"
            "    <i>Акция закончится</i>: <code>{end}</code>\n"
            "    <i>Ссылка</i>: {url}\n"
        ),
        "header": "<emoji document_id=5472282432436708545>🎮</emoji> <b>Бесплатные игры в EGS:</b>",
        "header_bot": "🎮 <b>Сегодняшние бесплатные игры в EGS:</b>",
        "footer": "<emoji document_id=6028435952299413210>ℹ️</emoji> <i>Статус </i><code>active</code><i> означает, что игру можно забрать уже сейчас.\nСтатус </i><code>upcoming</code><i> означает, что игру можно будет забрать потом.</i>",
        "_region_cfg": "Регион проверки бесплатных игр",
        "_schedule_checking_cfg": "Будет ли бот автоматически отправлять в специальный чат текущие бесплатные игры",
        "_cls_doc": "Модуль для проверки бесплатных игр в Epic Games Store. Инлайн бот будет отправлять их каждый день в специальном чате",
    }

    async def client_ready(self):
        self.chat, _ = await utils.asset_channel(
            self._client,
            "EGS Free Games",
            "There will be free games from epic games every day",
            avatar="https://github.com/sqlmerr/hikka_mods/blob/main/assets/icons/egsfreegames_chat.png?raw=true",
            invite_bot=True,
            _folder="hikka",
        )

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "region",
                default="RU",
                doc=lambda: self.strings("_region_cfg"),
                validator=loader.validators.String(),
            ),
            loader.ConfigValue(
                "schedule_checking",
                default=True,
                doc=lambda: self.strings("_schedule_checking_cfg"),
                validator=loader.validators.Boolean(),
            ),
        )

    def create_game_info(self, game, offer, status, available_in_russia=None):
        price_info = {
            "discount": 0,
            "RUB": {"original": -1, "current": -1},
            "USD": {"original": -1, "current": -1},
        }

        if game.get("price"):
            total_price = game["price"].get("totalPrice", {})
            discount = offer["discountSetting"]["discountPercentage"]

            original_price = total_price.get("originalPrice", 0) / 100
            current_price = total_price.get("discountPrice", original_price) / 100

            currency = total_price.get("currencyCode", "USD")
            if currency in price_info:
                price_info[currency] = {
                    "original": original_price,
                    "current": current_price,
                }
                price_info["discount"] = discount

        slug = (
            game["productSlug"]
            if game["productSlug"]
            else game["catalogNs"]["mappings"][0]["pageSlug"]
        )
        url = "https://store.epicgames.com/ru/p/" + slug

        return {
            "title": game["title"],
            "publisher": game.get("seller", {}).get("name"),
            "status": status,
            "start_date": offer["startDate"],
            "end_date": offer["endDate"],
            "url": url,
            "image_url": game.get("keyImages", [{}])[0].get("url"),
            "price": price_info,
            "available_in_russia": available_in_russia,
        }

    def process_offers(
        self, game: Dict, offers: List, status: str, available_in_russia=None
    ):
        games_list = []
        if offers:
            for offer in offers[0].get("promotionalOffers", []):
                if offer["discountSetting"]["discountPercentage"] == 0:
                    games_list.append(
                        self.create_game_info(game, offer, status, available_in_russia)
                    )
        return games_list

    def get_normal_timestamp(self, date: str) -> str:
        dt = datetime.datetime.fromisoformat(date.replace("Z", "+00:00"))
        dt = dt.astimezone(datetime.timezone.utc)
        formatted_date = dt.strftime("%d.%m.%Y %H:%M (UTC)")
        return formatted_date

    async def get_free_games(self, region: str = "RU") -> Optional[List]:
        url = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions"
        params = {"locale": "en-US", "country": region, "allowCountries": region}
        try:
            async with aiohttp.ClientSession() as session:
                response = await session.get(url, params=params)
                response.raise_for_status()
                data = await response.json()

                games = []
                for game in data["data"]["Catalog"]["searchStore"]["elements"]:
                    if not game.get("promotions"):
                        continue

                    promotions = game["promotions"]

                    promo = promotions.get("promotionalOffers", [])
                    upcoming = promotions.get("upcomingPromotionalOffers", [])

                    games.extend(self.process_offers(game, promo, "active", None))
                    games.extend(self.process_offers(game, upcoming, "upcoming", None))
                return games
        except aiohttp.ClientResponseError as e:
            return

    def gen_text(self, games: List[Dict], bot: bool = False) -> str:
        header = self.strings("header") if not bot else self.strings("header_bot")
        text = "".join(
            [
                self.strings("game").format(
                    title=g["title"],
                    status=g["status"],
                    start=self.get_normal_timestamp(g["start_date"]),
                    end=self.get_normal_timestamp(g["end_date"]),
                    url=g["url"],
                )
                + "\n"
                for g in games
            ]
        )
        footer = self.strings("footer") if not bot else ""
        return f"{header}\n\n{text}{footer}"

    @loader.command(ru_doc="Получить бесплатные игры доступные в Epic Games Store")
    async def egsgames(self, message: Message):
        """Get free games links available in Epic Games Store"""

        games = await self.get_free_games(self.config["region"])
        text = self.gen_text(games)

        await utils.answer(message, text)

    @loader.loop(interval=86400, autostart=True)
    async def loop(self, *args, **kwargs):
        logging.error(self.chat.id)
        if not self.config["schedule_checking"]:
            return
        games = await self.get_free_games(self.config["region"])
        text = self.gen_text(games, bot=True)

        chat_id = utils.get_entity_id(self.chat)
        await self.inline.bot.send_message(chat_id=chat_id, text=text)
