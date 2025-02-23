"""

    █▀▀ ▄▀█ █▄▀ █▀▀ █▀ ▀█▀ █░█░█ █ ▀▄▀
    █▄▄ █▀█ █░█ ██▄ ▄█ ░█░ ▀▄▀▄▀ █ █░█

    Copyleft 2022 t.me/CakesTwix                                                     
    This program is free software; you can redistribute it and/or modify 

"""

__version__ = (1, 0, 1)

# requires: aiohttp
# scope: inline
# scope: geektg_only
# scope: geektg_min 3.1.15
# meta pic: https://image.winudf.com/v2/image/cnUucmFkaWF0aW9ueC5hbmlsaWJyaWEuYXBwX2ljb25fMTUyODYyNzQ2NV8wMjY/icon.png?w=&fakeurl=1
# meta developer: @cakestwix_mods

from .. import loader, main
from ..inline import GeekInlineQuery, rand
from aiogram.types import InlineQueryResultPhoto, CallbackQuery
import aiohttp
import logging
from requests import post
import datetime

logger = logging.getLogger(__name__)


@loader.tds
class AniLibriaMod(loader.Module):
    """A non-profit project for the dubbing and adaptation of foreign TV series, cartoons and anime"""

    strings = {
        "name": "AniLibria",
        "cfg_mail": "Your mail from anilibria.tv",
        "cfg_pass": "Your password from anilibria.tv",
        "announce": "<b>Анонс</b> :",
        "status": "<b>Статус</b> :",
        "type": "<b>Тип</b> :",
        "genres": "<b>Жанры</b> :",
        "favorite": "<b>Избранное &lt;3</b> :",  # &lt; == <
        "season": "<b>Сезон</b> :",
        "inline": "Взаимодействие с аниме {}",
    }

    link = "https://anilibria.tv"
    api = "https://api.anilibria.tv/v2/"
    getFavorites_api = (
        "https://api.anilibria.tv/v2/getFavorites?session={}&limit=999&filter=id"
    )

    weekdays = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"]

    def __init__(self):
        self.config = loader.ModuleConfig(
            "CONFIG_MAIL",
            None,
            lambda m: self.strings("cfg_mail", m),
            "CONFIG_PASS",
            None,
            lambda m: self.strings("cfg_pass", m),
        )

        # Try login and get cookies for some methods
        self.logined = False
        if (
            self.config["CONFIG_MAIL"] is not None
            and self.config["CONFIG_PASS"] is not None
        ):
            self.login = post(
                f"{self.link}/public/login.php",
                data={
                    "mail": self.config["CONFIG_MAIL"],
                    "passwd": self.config["CONFIG_PASS"],
                },
            )

            if self.login.cookies.values() != []:
                self.logined = True
                self.cookies = self.login.cookies.values()[0]

    async def client_ready(self, client, db) -> None:
        self._client = client

    @loader.unrestricted
    @loader.ratelimit
    async def arandomcmd(self, message) -> None:
        """Возвращает случайный тайтл из базы"""

        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.api}getRandomTitle") as get:
                anime_title = await get.json()
                await session.close()

        text = f"{anime_title['names']['ru']} | {anime_title['names']['en']} \n"
        text += f"{self.strings['status']} {anime_title['status']['string']}\n\n"
        text += f"{self.strings['type']} {anime_title['type']['full_string']}\n"
        text += f"{self.strings['season']} {anime_title['season']['string']} {anime_title['season']['year']}\n"
        text += f"{self.strings['genres']} {' '.join(anime_title['genres'])}\n\n"

        # text += f"<code>{anime_title['description']}</code>\n\n"
        text += f"{self.strings['favorite']} {anime_title['in_favorites']}"

        kb = [
            [
                {
                    "text": "Ссылка",
                    "url": f"https://anilibria.tv/release/{anime_title['code']}.html",
                }
            ]
        ]

        if self.logined:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.getFavorites_api.format(self.cookies)
                ) as get:
                    favorite_list = await get.json()
                await session.close()

            ids_favorite = [_id["id"] for _id in favorite_list]
            if anime_title["id"] in ids_favorite:
                kb.append(
                    [
                        {
                            "text": "Убрать из избранного",
                            "callback": self.inline__favorite,
                            "args": [anime_title["id"], "delFavorite"],
                        }
                    ]
                )
            else:
                kb.append(
                    [
                        {
                            "text": "Добавить в избранное",
                            "callback": self.inline__favorite,
                            "args": [anime_title["id"], "addFavorite"],
                        }
                    ]
                )

        kb.extend(
            [
                {
                    "text": f"{torrent['quality']['string']}",
                    "url": f"https://anilibria.tv/{torrent['url']}",
                }
            ]
            for torrent in anime_title["torrents"]["list"]
        )
        kb.append([{"text": "🚫 Закрыть", "callback": self.inline__close}])
        await message.client.send_file(
            message.chat_id,
            self.link + anime_title["posters"]["original"]["url"],
            caption=text,
        )
        await self.inline.form(
            self.strings["inline"].format(anime_title["names"]["ru"]),
            message=message,
            reply_markup=kb,
            always_allow=self._client.dispatcher.security._owner,
        )

    async def aschedulecmd(self, message) -> None:
        """
        Получить список последних обновлений тайтлов
        """

        selected_weekday = datetime.datetime.weekday(datetime.datetime.now())

        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.api}getSchedule") as get:
                schedule_list = await get.json()
                await session.close()

        kb = [[]]
        for day in schedule_list:
            kb[0].append(
                {
                    "text": f"[{self.weekdays[day['day']]}]"
                    if day["day"] == selected_weekday
                    else self.weekdays[day["day"]],  # With [] if current weekday
                    "callback": self.inline__update_schedule,
                    "args": [day["day"]],  # Number of the day
                }
            )
            if day["day"] == selected_weekday:
                text = "".join(
                    f"<b>{new_anime['names']['ru']}</b>\n" for new_anime in day["list"]
                )

        await self.inline.form(
            "Актуальное расписание Либрии\n" + text,
            message=message,
            reply_markup=kb,
            always_allow=self._client.dispatcher.security._owner,
        )

    async def asearch_inline_handler(self, query: GeekInlineQuery) -> None:
        """
        Возвращает список найденных по названию тайтлов
        """
        text = query.args

        if not text:
            return

        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.api + f"searchTitles?search={text}&limit=10"
            ) as get:
                search_list = await get.json()
                await session.close()

        inline_query = []
        for anime in search_list:
            text = f"{anime['names']['ru']} | {anime['names']['en']} \n"
            text += f"{self.strings['status']} {anime['status']['string']}\n\n"
            text += f"{self.strings['type']} {anime['type']['full_string']}\n"
            text += f"{self.strings['season']} {anime['season']['string']} {anime['season']['year']}\n"
            text += f"{self.strings['genres']} {' '.join(anime['genres'])}\n\n"

            # text += f"<code>{anime['description']}</code>\n\n"
            text += f"{self.strings['favorite']} {anime['in_favorites']}"

            inline_query.append(
                InlineQueryResultPhoto(
                    id=rand(20),
                    title=anime["names"]["ru"],
                    description=anime["type"]["full_string"],
                    caption=text,
                    thumb_url=f"{self.link}{anime['posters']['small']['url']}",  # noqa
                    photo_url=f"{self.link}{anime['posters']['original']['url']}",
                    parse_mode="html",
                )
            )
        await query.answer(
            inline_query,
            cache_time=0,
        )

    async def inline__close(self, call: CallbackQuery) -> None:
        await call.delete()

    async def inline__favorite(
        self, call: CallbackQuery, _id: int, method: str
    ) -> None:
        _id = str(_id)
        async with aiohttp.ClientSession() as session:
            # get anime by id for update buttons
            async with session.get(f"{self.api}getTitle?id={_id}") as get:
                anime_title = await get.json()

            kb = [
                [
                    {
                        "text": "Ссылка",
                        "url": f"https://anilibria.tv/release/{anime_title['code']}.html",
                    }
                ]
            ]

            if method == "addFavorite":
                async with session.put(
                    (self.api + f"{method}?session={self.cookies}&title_id={_id}")
                ) as get:
                    kb.append(
                        [
                            {
                                "text": "Убрать из избранного",
                                "callback": self.inline__favorite,
                                "args": [anime_title["id"], "delFavorite"],
                            }
                        ]
                    )
            else:  # delFavorite
                async with session.delete(
                    (self.api + f"{method}?session={self.cookies}&title_id={_id}")
                ) as get:
                    kb.append(
                        [
                            {
                                "text": "Добавить в избранное",
                                "callback": self.inline__favorite,
                                "args": [anime_title["id"], "addFavorite"],
                            }
                        ]
                    )
            kb.extend(
                [
                    {
                        "text": f"{torrent['quality']['string']}",
                        "url": f"https://anilibria.tv/{torrent['url']}",
                    }
                ]
                for torrent in anime_title["torrents"]["list"]
            )
            kb.append([{"text": "🚫 Закрыть", "callback": self.inline__close}])
            await session.close()

            await call.edit(
                text="Взаимодействие с аниме " + anime_title["names"]["ru"],
                reply_markup=kb,
            )

    async def inline__update_schedule(
        self, call: CallbackQuery, day_inline: int
    ) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.api}getSchedule") as get:
                schedule_list = await get.json()
                await session.close()

        kb = [[]]
        for day in schedule_list:
            kb[0].append(
                {
                    "text": f"[{self.weekdays[day['day']]}]"
                    if day["day"] == day_inline
                    else self.weekdays[day["day"]],  # With [] if current weekday
                    "callback": self.inline__update_schedule,
                    "args": [day["day"]],  # Number of the day
                }
            )
            if day["day"] == day_inline:
                text = "".join(
                    f"<b>{new_anime['names']['ru']}</b>\n" for new_anime in day["list"]
                )

        await call.edit(
            text="Актуальное расписание Либрии\n" + text,
            reply_markup=kb,
        )
