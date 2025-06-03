#  _____                          
# |_   _|____  ____ _ _ __   ___  
#   | |/ _ \ \/ / _` | '_ \ / _ \ 
#   | | (_) >  < (_| | | | | (_) |
#   |_|\___/_/\_\__,_|_| |_|\___/ 
#                              
# meta banner: https://envs.sh/oJM.jpg
# meta developer: @Toxano_Modules

import asyncio
import logging
import datetime
from typing import Union
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import Message
from .. import loader, utils

logger = logging.getLogger(__name__)

TIMEZONE_OFFSETS = {
    "MSK": 3,      
    "UTC": 0,      
    "GMT": 0,      
    "CET": 1,      
    "EET": 2,      
    "AZT": 4,       
    "AMT": 4,      
    "GET": 4,      
    "TJT": 5,      
    "TMT": 5,      
    "UZT": 5,      
    "KGT": 6,      
    "BDT": 6,      
    "IST": 5.5,    
    "THA": 7,      
    "ICT": 7,      
    "CST": 8,      
    "HKT": 8,     
    "JST": 9,      
    "KST": 9,      
    "EST": -5,     
    "EDT": -4,     
    "CDT": -5,     
    "PDT": -7,     
    "PST": -8,     
    "AKST": -9,    
    "AEST": 10,    
    "NZST": 12     
}

FONT_STYLES_DESC = """
0. 12:34 -> 12:34 (обычный)
1. 12:34 -> 『12:34』
2. 12:34 -> ➊➋:➌➍
3. 12:34 -> ⓵⓶:⓷⓸
4. 12:34 -> ①②:③④
5. 12:34 -> 𝟙𝟚:𝟛𝟜 
6. 12:34 -> ¹²'³⁴
7. 12:34 -> ₁₂‚₃₄
8. 12:34 -> 1️⃣2️⃣:3️⃣4️⃣
"""

FONT_STYLES = {
    0: lambda x: x,
    1: lambda x: f"『{x}』",
    2: lambda x: x.translate(str.maketrans("0123456789", "⓿➊➋➌➍➎➏➐➑➒")),
    3: lambda x: x.translate(str.maketrans("0123456789", "⓪⓵⓶⓷⓸⓹⓺⓻⓼⓽")),
    4: lambda x: x.translate(str.maketrans("0123456789", "⓪①②③④⑤⑥⑦⑧⑨")),
    5: lambda x: x.translate(str.maketrans("0123456789", "𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡")),
    6: lambda x: x.translate(str.maketrans("0123456789:", "⁰¹²³⁴⁵⁶⁷⁸⁹'")),
    7: lambda x: x.translate(str.maketrans("0123456789:", "₀₁₂₃₄₅₆₇₈₉‚")),
    8: lambda x: "".join([i + "️⃣" if i.isdigit() else i for i in x])
}

@loader.tds
class TimeInNick(loader.Module):
    """Показывает текущее время в никнейме и био с разными стилями шрифтов"""
    
    strings = {
        "name": "TimeInNick",
        "time_enabled": "⏰ Отображение времени в никнейме включено",
        "time_disabled": "⏰ Отображение времени в никнейме выключено",
        "bio_enabled": "⏰ Отображение времени в био включено", 
        "bio_disabled": "⏰ Отображение времени в био выключено",
        "invalid_delay": "⚠️ Неверный интервал обновления (должно быть 0-60 минут)",
        "cfg_timezone": "Часовой пояс",
        "cfg_update": "Интервал обновления (0-60 минут, 0 = мгновенное обновление)",
        "cfg_nick_format": "Формат никнейма. Доступные переменные: {nickname}, {time}",
        "cfg_bio_format": "Формат био. Доступные переменные: {bio}, {time}",
        "error_updating": "⚠️ Ошибка обновления: {}",
        "error_timezone": "⚠️ Неверный часовой пояс. Используйте один из: {}"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "TIMEZONE",
                "MSK",
                doc=lambda: self.strings("cfg_timezone"),
                validator=loader.validators.Choice(list(TIMEZONE_OFFSETS.keys()))
            ),
            loader.ConfigValue(
                "UPDATE_DELAY",
                1,
                doc=lambda: self.strings("cfg_update"),
                validator=loader.validators.Integer(minimum=0, maximum=60)
            ),
            loader.ConfigValue(
                "NICK_FORMAT",
                "{nickname} | {time}",
                doc=lambda: self.strings("cfg_nick_format"),
                validator=loader.validators.String()
            ),
            loader.ConfigValue(
                "BIO_FORMAT",
                "{bio} | {time}",
                doc=lambda: self.strings("cfg_bio_format"),
                validator=loader.validators.String()
            ),
            loader.ConfigValue(
                "FONT_STYLE",
                0,
                doc=FONT_STYLES_DESC,
                validator=loader.validators.Integer(minimum=0, maximum=8)
            )
        )
        self.nick_active = False
        self.bio_active = False
        self.original_nick = None
        self.original_bio = None
        self.nick_task = None
        self.bio_task = None

    async def client_ready(self, client, db):
        """Инициализация после загрузки модуля"""
        try:
            self.nick_active = self.get("nick_active", False)
            self.bio_active = self.get("bio_active", False)
            self.original_nick = self.get("original_nick", None)
            self.original_bio = self.get("original_bio", None)
            
            if self.nick_active and self.original_nick:
                self.nick_task = asyncio.create_task(self._update_nickname())
            
            if self.bio_active and self.original_bio:
                self.bio_task = asyncio.create_task(self._update_bio())
                
        except Exception as e:
            logger.exception(f"Error in client_ready: {e}")

    def get_formatted_time(self) -> str:
        """Получает текущее время с учетом часового пояса и стиля шрифта"""
        try:
            now = datetime.datetime.now(datetime.timezone.utc)
            
            timezone = self.config["TIMEZONE"].upper()
            if timezone not in TIMEZONE_OFFSETS:
                logger.error(f"Invalid timezone: {timezone}")
                timezone = "MSK"
                
            offset = TIMEZONE_OFFSETS[timezone]
            hour_offset = int(offset)
            minute_offset = int((offset - hour_offset) * 60)
            
            adjusted_time = now + datetime.timedelta(hours=hour_offset, minutes=minute_offset)
            time_str = adjusted_time.strftime("%H:%M")
            
            font_style = self.config.get("FONT_STYLE", 0)
            if font_style in FONT_STYLES:
                return FONT_STYLES[font_style](time_str)
            else:
                return time_str
                
        except Exception as e:
            logger.exception(f"Error formatting time: {e}")
            return datetime.datetime.now().strftime("%H:%M")

    async def _update_nickname(self):
        """Обновляет никнейм с текущим временем"""
        last_time = None
        
        while self.nick_active:
            try:
                current_time = self.get_formatted_time()
                
                if current_time != last_time and self.original_nick:
                    new_nick = self.config["NICK_FORMAT"].format(
                        nickname=self.original_nick,
                        time=current_time
                    )

                    await self._client(UpdateProfileRequest(
                        first_name=new_nick[:70]
                    ))
                    last_time = current_time
                    logger.debug(f"Updated nickname to: {new_nick}")

            except Exception as e:
                logger.exception(f"Error updating nickname: {e}")
                await asyncio.sleep(10)
                continue

            update_delay = max(self.config.get("UPDATE_DELAY", 1) * 60, 30)
            await asyncio.sleep(update_delay)

    async def _update_bio(self):
        """Обновляет био с текущим временем"""
        last_time = None
        
        while self.bio_active:
            try:
                current_time = self.get_formatted_time()
                
                if current_time != last_time:
                    new_bio = self.config["BIO_FORMAT"].format(
                        bio=self.original_bio or "",
                        time=current_time
                    )

                    await self._client(UpdateProfileRequest(
                        about=new_bio[:70]
                    ))
                    last_time = current_time
                    logger.debug(f"Updated bio to: {new_bio}")

            except Exception as e:
                logger.exception(f"Error updating bio: {e}")
                await asyncio.sleep(10)
                continue

            update_delay = max(self.config.get("UPDATE_DELAY", 1) * 60, 30)
            await asyncio.sleep(update_delay)

    @loader.command(
        ru_doc="Включить/выключить отображение времени в никнейме"
    )
    async def timenick(self, message: Message):
        """Включить/выключить отображение времени в никнейме"""
        try:
            if self.nick_active:

                self.nick_active = False
                if self.nick_task and not self.nick_task.done():
                    self.nick_task.cancel()
                    
                if self.original_nick:
                    await self._client(UpdateProfileRequest(
                        first_name=self.original_nick[:70]
                    ))
                
                self.set("nick_active", False)
                self.set("original_nick", None)
                self.original_nick = None
                
                await utils.answer(message, self.strings["time_disabled"])
                return

            me = await self._client.get_me()
            current_nick = me.first_name or "User"

            if "|" in current_nick:
                self.original_nick = current_nick.split("|")[0].strip()
            else:
                self.original_nick = current_nick
                
            self.nick_active = True
            self.set("nick_active", True)
            self.set("original_nick", self.original_nick)
            
            current_time = self.get_formatted_time()
            new_nick = self.config["NICK_FORMAT"].format(
                nickname=self.original_nick,
                time=current_time
            )
            await self._client(UpdateProfileRequest(
                first_name=new_nick[:70]
            ))
            
            self.nick_task = asyncio.create_task(self._update_nickname())
            
            await utils.answer(message, self.strings["time_enabled"])
            
        except Exception as e:
            self.nick_active = False
            logger.exception(f"Error in timenick command: {e}")
            await utils.answer(message, self.strings["error_updating"].format(str(e)))

    @loader.command(
        ru_doc="Включить/выключить отображение времени в био"
    ) 
    async def timebio(self, message: Message):
        """Включить/выключить отображение времени в био"""
        try:
            if self.bio_active:
                self.bio_active = False
                if self.bio_task and not self.bio_task.done():
                    self.bio_task.cancel()
                    
                if self.original_bio is not None:
                    await self._client(UpdateProfileRequest(
                        about=self.original_bio[:70] if self.original_bio else ""
                    ))

                self.set("bio_active", False)
                self.set("original_bio", None)
                self.original_bio = None

                await utils.answer(message, self.strings["bio_disabled"])
                return

            full_user = await self._client(GetFullUserRequest("me"))
            current_bio = full_user.full_user.about or ""
            
            if "|" in current_bio:
                self.original_bio = current_bio.split("|")[0].strip()
            else:
                self.original_bio = current_bio
                
            self.bio_active = True
            self.set("bio_active", True)
            self.set("original_bio", self.original_bio)


            current_time = self.get_formatted_time()
            new_bio = self.config["BIO_FORMAT"].format(
                bio=self.original_bio,
                time=current_time
            )
            await self._client(UpdateProfileRequest(
                about=new_bio[:70]
            ))

            self.bio_task = asyncio.create_task(self._update_bio())
            
            await utils.answer(message, self.strings["bio_enabled"])
            
        except Exception as e:
            self.bio_active = False
            logger.exception(f"Error in timebio command: {e}")
            await utils.answer(message, self.strings["error_updating"].format(str(e)))

    async def on_unload(self):
        """Вызывается при выгрузке модуля"""
        try:
            if self.nick_active:
                self.nick_active = False
                if self.nick_task and not self.nick_task.done():
                    self.nick_task.cancel()
                if self.original_nick:
                    await self._client(UpdateProfileRequest(
                        first_name=self.original_nick[:70]
                    ))

            if self.bio_active:
                self.bio_active = False
                if self.bio_task and not self.bio_task.done():
                    self.bio_task.cancel()
                if self.original_bio is not None:
                    await self._client(UpdateProfileRequest(
                        about=self.original_bio[:70] if self.original_bio else ""
                    ))

        except Exception as e:
            logger.exception(f"Error during unload: {e}")
        finally:
            self.set("nick_active", False)
            self.set("bio_active", False)