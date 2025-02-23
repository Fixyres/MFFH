"""

    █▀▀ ▄▀█ █▄▀ █▀▀ █▀ ▀█▀ █░█░█ █ ▀▄▀
    █▄▄ █▀█ █░█ ██▄ ▄█ ░█░ ▀▄▀▄▀ █ █░█

    Copyleft 2022 t.me/CakesTwix                                                            
    This program is free software; you can redistribute it and/or modify 

"""

__version__ = (2, 1, 1) # BETA

# requires: httpx pydantic
# meta pic: https://www.seekpng.com/png/full/824-8246338_yandere-sticker-yandere-simulator-ayano-bloody.png
# meta developer: @cakestwix_mods
# scope: inline
# scope: hikka_only
# scope: hikka_min 1.1.2

from .. import loader, utils
import httpx
import asyncio
import logging
import ast
import telethon
from aiogram.types import InputFile
from aiogram.utils.markdown import hlink
from pydantic import BaseModel, Field
from typing import Optional

logger = logging.getLogger(__name__)


def rating_string(rating_list: list) -> str:
    rating_str = ["s", "q", "e"]
    if sum(rating_list) == 2:
        return (
            "-rating:"
            + rating_str[[i for i, val in enumerate(rating_list) if not val][0]]
        )
    elif sum(rating_list) == 1:
        return f"rating:{rating_str[[i for i, val in enumerate(rating_list) if val][0]]}"

    else:
        return ""

# id: int                                | Айди
# tag: str = Field(alias='tag_string')   | Теги
# rating: str                            | Рейтинг
# author: str                            | Автор
# file_size: int                         | Размер без сжатия
# sample_file_size: int                  | Размер со средним сжатием
# file_url: str                          | Без сжатия
# preview_file_url: str                  | Сильное сжатие
# sample_url: Optional[str] = None       | Среднее сжатие
# source: Optional[str] = None           | Откуда арт

class BooruModel(BaseModel):
    id: int
    tag: str = Field(alias='tag_string_general')
    rating: str
    author: Optional[str] = None
    file_size: int
    sample_file_size: int = Field(alias='file_size')
    file_url: str
    preview_file_url: str = Field(alias='large_file_url')
    sample_url: Optional[str] = Field(alias='large_file_url')
    source: Optional[str] = None 


class MoebooruModel(BaseModel):
    id: int
    tag: str = Field(alias='tags')
    rating: str
    author: Optional[str] = None
    file_size: int
    sample_file_size: int
    file_url: str
    preview_file_url: str = Field(alias='preview_url')
    sample_url: Optional[str] = None
    source: Optional[str] = None


class Moebooru:
    domain = 'yande.re'
    get_url = f'https://{domain}' 
    post_url = '/post.json' 

    async def getLast(self, params):
        async with httpx.AsyncClient() as client:
            get = await client.get(self.get_url + self.post_url + params)
            result = get.json()
            return [MoebooruModel(**item) for item in result]

class Konachan_Net(Moebooru):
    domain = 'konachan.net'
    get_url = f'https://{domain}' 
    post_url = '/post.json'

class Lolibooru(Moebooru):
    domain = 'lolibooru.moe'
    get_url = f'https://{domain}'
    post_url = '/post.json'

# Very buggy :(
class Booru: 
    domain = 'danbooru.donmai.us'
    get_url = f'https://{domain}'
    post_url = '/posts.json'

    async def getLast(self, params):
        async with httpx.AsyncClient() as client:
            get = await client.get(self.get_url + self.post_url + params)
            result = get.json()
            list_art = []
            for item in result:
                try:
                    list_art.append(BooruModel(**item))
                except Exception as err:
                    logger.debug(str(err)) # Fck Booru
            return list_art

@loader.tds
class ImageBoardSenderMod(loader.Module):
    """Auto-posting art to your channels"""

    strings = {
        "cfg_channel": "Сhannel variable where the content will be posted",
        "cfg_tags": "Filtering art by tags",
        "name": "ImageBoardSender",
        "no_chennel": "Channel does not exist",
        "ok": "Everything is okay",
        "no_ok": "Everything not okay (maybe not admin rights)",
        "channel_status": "<b>Channel Status</b>:",
        "channel_username": "<b>Channel username</b>:",
        "channel_tags": "<b>Channel tags</b>:",
        "channel_no_tags": "no tags",
        "change_channel_username": "<b>Change the channel username</b>",
        "changed_successfully": "Successfully changed",
        "btn_menu_change_channel": "✍️ Change username channel",
        "btn_menu_change_tags": "✍️ Change tags",
        "btn_menu_change_input": "✍️ Enter new configuration value for this option",
        "btn_menu_update": "Update",
        "btn_menu_start": "Start",
        "btn_menu_stop": "Stop",
        "btn_menu_Safe": "Safe",
        "btn_menu_Questionable": "Questionable",
        "btn_menu_Explicit": "Explicit",
        "btn_menu_autostart_on": "✅ Autostart",
        "btn_menu_autostart_off": "❌ Autostart",
        "source": "<b>List of available sources. \nThe source used:</b> <code>{}</code>",
    }

    strings_ru = {
        "cfg_channel": "Переменная канала, где будет размещаться контент",
        "cfg_tags": "Фильтрация артов по тегам",
        "name": "ImageBoardSender",
        "no_chennel": "Канал не существует",
        "ok": "Все хорошо",
        "no_ok": "Все не окей (возможно нет прав админа)",
        "channel_status": "<b>Статус канала</b>:",
        "channel_username": "<b>Имя канала</b>:",
        "channel_tags": "<b>Теги канала</b>:",
        "channel_no_tags": "нет тегов",
        "change_channel_username": "<b>Изменить имя пользователя канала</b>",
        "changed_successfully": "Успешно изменено",
        "btn_menu_change_channel": "✍️ Изменить имя канал",
        "btn_menu_change_tags": "✍️ Изменить теги",
        "btn_menu_change_input": "✍️ Введите новое значение конфигурации для этой опции",
        "btn_menu_update": "Обновить",
        "btn_menu_start": "Start",
        "btn_menu_stop": "Stop",
        "btn_menu_Safe": "Безопасно",
        "btn_menu_Questionable": "Под вопросом",
        "btn_menu_Explicit": "Откровенное 18+",
        "btn_menu_autostart_on": "✅ Автостарт",
        "btn_menu_autostart_off": "❌ Автостарт",
        "source": "<b>Список доступных источников. \nИспользуемый источник:</b> <code>{}</code>",
    }

    rating = {"e": "Explicit 🔴", "q": "Questionable 🟡", "s": "Safe 🟢"}
    url = "https://yande.re/post.json"

    def __init__(self):
        self.config = loader.ModuleConfig(
            "CONFIG_CHANNEL",
            "@notset",
            lambda: self.strings("cfg_channel"),
            "CONFIG_TAGS",
            "",
            lambda: self.strings("cfg_tags"),
        )

        self.entity = None
        self.last_id = 0

        self.sources = {"Yandere": Moebooru(), "Konachan.net": Konachan_Net(), "LoliBooru": Lolibooru()}
        self.source_btn = [{"text": item, "callback": self.callback__change_source, "args": (item,)} for item in self.sources]

    # Check channel rights
    async def check_entity(self) -> bool:
        try:
            if not self.entity:
                self.entity = await self._client.get_entity(self.config["CONFIG_CHANNEL"])
                if not isinstance(self.entity, telethon.types.Channel):
                    self.entity = None
                    return False
        except ValueError:
            self.entity = None
            return False

        if self.entity.admin_rights is None:
            return False
        elif self.entity.admin_rights.post_messages:
            return True

    async def menu_keyboard(self) -> list:
        return [
            [
                {
                    "text": self.strings["btn_menu_change_channel"],
                    "input": self.strings["btn_menu_change_input"],
                    "handler": self.change_config,
                    "args": ("CONFIG_CHANNEL",),
                },
                {
                    "text": self.strings["btn_menu_change_tags"],
                    "input": self.strings["btn_menu_change_input"],
                    "handler": self.change_config,
                    "args": ("CONFIG_TAGS",),
                },
            ],
            [
                {
                    "text": f"[ {self.strings['btn_menu_Safe']} ]"
                    if self._db.get(self.strings["name"], "rating")[0]
                    else self.strings["btn_menu_Safe"],
                    "callback": self.set_rating,
                    "args": ("s"),
                },
                {
                    "text": f"[ {self.strings['btn_menu_Questionable']} ]"
                    if self._db.get(self.strings["name"], "rating")[1]
                    else self.strings["btn_menu_Questionable"],
                    "callback": self.set_rating,
                    "args": ("q"),
                },
                {
                    "text": f"[ {self.strings['btn_menu_Explicit']} ]"
                    if self._db.get(self.strings["name"], "rating")[2]
                    else self.strings["btn_menu_Explicit"],
                    "callback": self.set_rating,
                    "args": ("e"),
                },
            ]
            if await self.check_entity()
            else [],
            [
                {"text": self.strings["btn_menu_stop"], "callback": self.stop_posting}
                if self.loop__send_arts.status
                else {
                    "text": self.strings["btn_menu_start"],
                    "callback": self.start_posting,
                },
                {
                    "text": self.strings["btn_menu_autostart_on"]
                    if self._db.get(self.strings["name"], "autostart")
                    else self.strings["btn_menu_autostart_off"],
                    "callback": self.change_autostart,
                },
            ]
            if await self.check_entity()
            else [],
            [
                {
                    "text": self.strings["btn_menu_update"],
                    "callback": self.update_channel_status,
                }
            ],
        ]

    # Just async init
    async def _init(self) -> None:
        await self.check_entity()
        bot_info = await self.inline.bot.get_me()
        if self.config["CONFIG_CHANNEL"] == "@notset":
            return

        self.entity = await self._client.get_entity(self.config["CONFIG_CHANNEL"])

        try:
            channel_bot = await self._client.edit_admin(self.config["CONFIG_CHANNEL"],
                user=bot_info.username,
                change_info=False,
                post_messages=True,
                edit_messages=True,
                delete_messages=True,
                ban_users=False,
                invite_users=False,
                pin_messages=True,
                add_admins=False,)
            logger.debug(f"[{self.strings['name']}] Bot added")

            if self._db.get(self.strings["name"], "autostart"):
                self.loop__send_arts.start()
        except ValueError:
            channel_bot = None
            logger.warning(f"[{self.strings['name']}] Check channel username")


    async def client_ready(self, client, db) -> None:
        self._db = db
        self._client = client

        None if self._db.get(self.strings["name"], "source") else self._db.set(self.strings["name"], "source", "Yandere")
        None if self._db.get(self.strings["name"], "rating") else self._db.set(self.strings["name"], "rating", [False, False, False])
        None if self._db.get(self.strings["name"], "autostart") else self._db.set(self.strings["name"], "autostart", False)

        await self._init()


    async def on_unload(self) -> None:
        try:
            self.loop__send_arts.stop()
        except Exception:
            pass

    # Caption
    def string_builder(self, json):
        # Thanks to Фрося <3
        string = f"Tags : {'#' + str.join(' #', json.tag.split())}\n"
        string += f'©️ : {json.author or "No author"}\n'
        string += f'🔗 : {json.source or "No source"}\n'
        string += f"Rating : {self.rating[json.rating]}\n\n"
        string += ("🆔 : " + str(json.id)) 

        return string

    # Commands #

    async def channelmenucmd(self, message):
        """🗒 Simple Menu and status"""
        string = f"{self.strings['channel_status']} {self.strings['ok'] if await self.check_entity() else self.strings['no_ok']}\n"
        string += f"{self.strings['channel_username']} {self.config['CONFIG_CHANNEL'] if self.config['CONFIG_CHANNEL'] != '@notset' else self.strings['change_channel_username']}\n"
        string += f"{self.strings['channel_tags']} {self.config['CONFIG_TAGS'] if self.config['CONFIG_TAGS'] != '' else self.strings['channel_no_tags']}\n"

        await self.inline.form(
            text=string,
            message=message,
            reply_markup=await self.menu_keyboard(),
        )
    
    async def artsourcecmd(self, message):   
        """🧑‍🎤 Change the source of art"""  
        await self.inline.form(
            text=self.strings["source"].format(self._db.get(self.strings["name"], "source")),
            message=message,
            reply_markup=utils.chunks(self.source_btn, 2),
        )

    async def latestartcmd(self, message):   
        """⌚️ Sending the last art for now"""  
        params = (
            "?tags="
            + rating_string(self._db.get(self.strings["name"], "rating")) 
            + " "
            + self.config["CONFIG_TAGS"]
        )
        art_data = await self.sources[self._db.get(self.strings["name"], "source")].getLast(params)
        
        await self.inline.bot.send_photo(
            self.config['CONFIG_CHANNEL'],
            InputFile.from_url(art_data[0].sample_url),
            self.string_builder(art_data[0]),
            parse_mode="HTML",
            reply_markup=self.inline._generate_markup(
                [{"text": "Full", "url": art_data[0].file_url}]
            ),
        )

        await message.delete()

    async def randomartcmd(self, message):   
        """🎲 Sending a random art"""  
        params = (
            "?tags=order:random "
            + rating_string(self._db.get(self.strings["name"], "rating")) 
            + " "
            + self.config["CONFIG_TAGS"]
        )
        art_data = await self.sources[self._db.get(self.strings["name"], "source")].getLast(params)
        
        await self.inline.bot.send_photo(
            self.config['CONFIG_CHANNEL'],
            InputFile.from_url(art_data[0].sample_url),
            self.string_builder(art_data[0]),
            parse_mode="HTML",
            reply_markup=self.inline._generate_markup(
                [{"text": "Full", "url": art_data[0].file_url}]
            ),
        )

        await message.delete()

    # Inline callback handlers #

    # From Hikka https://github.com/hikariatama/Hikka/blob/d3144fcebdbc8ecbec7f3d299cc927bb1fea00b6/hikka/modules/hikka_config.py#L51-L80
    async def change_config(self, call, param, config_name) -> None:
        for module in self.allmodules.modules:
            if module.strings("name") == self.strings["name"]:
                module.config[config_name] = param

                if param:
                    try:
                        param = ast.literal_eval(param)
                    except (ValueError, SyntaxError):
                        pass

                    self._db.setdefault(module.__class__.__name__, {}).setdefault(
                        "__config__", {}
                    )[config_name] = param
                else:
                    try:
                        del self._db.setdefault(
                            module.__class__.__name__, {}
                        ).setdefault("__config__", {})[config_name]
                    except KeyError:
                        pass

                self.allmodules.send_config_one(module, self._db, skip_hook=True)
                self._db.save()

        await call.edit(
            text=self.strings["changed_successfully"],
            reply_markup=[
                {
                    "text": self.strings["btn_menu_update"],
                    "callback": self.update_channel_status,
                }
            ],
        )

    async def update_channel_status(self, call) -> None:
        string = f"{self.strings['channel_status']} {self.strings['ok'] if await self.check_entity() else self.strings['no_ok']}\n"
        string += f"{self.strings['channel_username']} {self.config['CONFIG_CHANNEL'] if self.config['CONFIG_CHANNEL'] != '@notset' else self.strings['change_channel_username']}\n"
        string += f"{self.strings['channel_tags']} {self.config['CONFIG_TAGS'] if self.config['CONFIG_TAGS'] != '' else self.strings['channel_no_tags']}\n"

        await call.edit(
            text=string,
            reply_markup=await self.menu_keyboard(),
        )

    async def set_rating(self, call, rating) -> None:
        list_rating = self._db.get(self.strings["name"], "rating")
        if rating == "s":
            list_rating[0] = not list_rating[0]
            self._db.set(self.strings["name"], "rating", list_rating)
        elif rating == "q":
            list_rating[1] = not list_rating[1]
            self._db.set(self.strings["name"], "rating", list_rating)
        elif rating == "e":
            list_rating[2] = not list_rating[2]
            self._db.set(self.strings["name"], "rating", list_rating)

        await self.update_channel_status(call)

    async def start_posting(self, call) -> None:
        if not self.loop__send_arts.status:
            self.loop__send_arts.start()
            await asyncio.sleep(0.5) # Otherwise the button does not update
            await self.update_channel_status(call)

    async def stop_posting(self, call) -> None:
        if self.loop__send_arts.status:
            self.loop__send_arts.stop()
            await self.update_channel_status(call)

    async def change_autostart(self, call) -> None:
        self._db.set(
            self.strings["name"],
            "autostart",
            not self._db.get(self.strings["name"], "autostart"),
        )
        await self.update_channel_status(call)

    async def callback__change_source(self, call, source):
        self._db.set(self.strings["name"], "source", source)
        self.last_id = 0
        await call.edit(text=self.strings["source"].format(self._db.get(self.strings["name"], "source")), reply_markup=utils.chunks(self.source_btn, 2))

    # General loop #

    @loader.loop(interval=60)
    async def loop__send_arts(self):
        """Auto-Posting"""
        params = (
            "?tags="
            + rating_string(self._db.get(self.strings["name"], "rating")) 
            + " "
            + self.config["CONFIG_TAGS"]
        )

        art_data = await self.sources[self._db.get(self.strings["name"], "source")].getLast(params)

        if art_data == []:
            logger.warning(f"[{self.strings['name']}] No arts, check tags")
            return
            
        if self.last_id == 0:
            self.last_id = art_data[0].id
            return

        for item in reversed(art_data):
            if item.id > self.last_id:
                try:

                    # await self._client.send_file(
                    #    self.entity,
                    #    item["sample_url"],
                    #    caption=self.string_builder(item),
                    # )

                    await self.inline.bot.send_photo(
                        self.config['CONFIG_CHANNEL'],
                        InputFile.from_url(item.sample_url),
                        self.string_builder(item),
                        parse_mode="HTML",
                        reply_markup=self.inline._generate_markup(
                            [{"text": "Full", "url": item.file_url}]
                        ),
                    )
                    # break # DEBUG

                except Exception as e:
                    logger.error(str(e))

                await asyncio.sleep(1)

        self.last_id = art_data[0].id
        await asyncio.sleep(5 * 60)
