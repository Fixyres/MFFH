# ░██████╗░██████╗░██╗░░░░░███╗░░░███╗███████╗██████╗░██████╗░
# ██╔════╝██╔═══██╗██║░░░░░████╗░████║██╔════╝██╔══██╗██╔══██╗
# ╚█████╗░██║██╗██║██║░░░░░██╔████╔██║█████╗░░██████╔╝██████╔╝
# ░╚═══██╗╚██████╔╝██║░░░░░██║╚██╔╝██║██╔══╝░░██╔══██╗██╔══██╗
# ██████╔╝░╚═██╔═╝░███████╗██║░╚═╝░██║███████╗██║░░██║██║░░██║
# ╚═════╝░░░░╚═╝░░░╚══════╝╚═╝░░░░░╚═╝╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝
# ---------------------------------------------------------------------------------------------
# Name: AnimatedProfile
# Description: Модуль для анимации вашего профиля (имя, био)
# Author: sqlmerr
# Commands:
# .animatedname (.aname) | .animatedbio (.abio) | .stopanimatedname (.stopaname) | .stopanimatedbio (.stopabio)
# ---------------------------------------------------------------------------------------------

# meta icon: https://github.com/sqlmerr/hikka_mods/blob/main/assets/icons/animatedprofile.png?raw=true
# meta developer: @sqlmerr_m
# only hikka

import asyncio

from hikkatl.tl.types import Message

from hikkatl import functions
import logging

from .. import loader, utils


logger = logging.getLogger(__name__)


@loader.tds
class AnimatedProfile(loader.Module):
    """Module for your profile animation (name, bio) look in the config"""

    strings = {
        "name": "AnimatedProfile",
        "name_delay": "Time between frames of name animation",
        "animated_name_frames": "Name animation frames",
        "not_name_frames": "<emoji document_id=5447644880824181073>⚠️</emoji> See the config! In the animated_name_frames parameter, put your animation frames by name",
        "name_is_enabled": "<emoji document_id=5447644880824181073>⚠️</emoji> Name animation is already enabled, use <code>.astopname</code> to turn it off.",
        "name_is_disabled": "<emoji document_id=5447644880824181073>⚠️</emoji> Name animation is already turned off.",
        "name_turned_off": "<emoji document_id=5447644880824181073>⚠️</emoji> Name animation is disabled.",
        "bio_status": "Is the bio animation enabled or not",
        "bio_delay": "Time between frames of bio animation",
        "animated_bio_frames": "Bio animation frames",
        "not_bio_frames": "<emoji document_id=5447644880824181073>⚠️</emoji> See the config! In the animated_bio_frames parameter, put your animation frames bio",
        "bio_is_enabled": "<emoji document_id=5447644880824181073>⚠️</emoji> Bio animation is already enabled, use <code>.astopname</code> to turn it off.",
        "bio_is_disabled": "<emoji document_id=5447644880824181073>⚠️</emoji> Bio animation is already turned off.",
        "bio_turned_off": "<emoji document_id=5447644880824181073>⚠️</emoji> Bio animation is disabled.",
    }
    strings_ru = {
        "name_delay": "Время между кадрами анимации имени",
        "animated_name_frames": "Кадры анимации имени",
        "not_name_frames": "<emoji document_id=5447644880824181073>⚠️</emoji> Смотрите конфиг! В параметре animated_name_frames, поставьте ваши кадры анимации имени",
        "name_is_enabled": "<emoji document_id=5447644880824181073>⚠️</emoji> Анимация имени уже включена, используйте <code>.stopaname</code>, чтобы выключить.",
        "name_is_disabled": "<emoji document_id=5447644880824181073>⚠️</emoji> Анимация имени уже выключена.",
        "name_turned_off": "<emoji document_id=5447644880824181073>⚠️</emoji> Анимация имени выключена.",
        "bio_status": "Включена ли анимация био или нет",
        "bio_delay": "Время между кадрами анимации био",
        "animated_bio_frames": "Кадры анимации био",
        "not_bio_frames": "<emoji document_id=5447644880824181073>⚠️</emoji> Смотрите конфиг! В параметре animated_bio_frames, поставьте ваши кадры анимации био",
        "bio_is_enabled": "<emoji document_id=5447644880824181073>⚠️</emoji> Анимация био уже включена, используйте <code>.stopabio</code>, чтобы выключить.",
        "bio_is_disabled": "<emoji document_id=5447644880824181073>⚠️</emoji> Анимация био уже выключена.",
        "bio_turned_off": "<emoji document_id=5447644880824181073>⚠️</emoji> Анимация био выключена.",
        "_cls_doc": "Модуль для анимации вашего профиля (имя, био) смотрите конфиг"
    }

    def __init__(self):
        self.aname = False
        self.abio = False
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "animated_name_frames",
                [],
                lambda: self.strings("animated_name_frames"),
                validator=loader.validators.Series(
                    loader.validators.Union(loader.validators.String())
                ),
            ),
            loader.ConfigValue(
                "name_delay",
                1.0,
                lambda: self.strings("name_delay"),
                validator=loader.validators.Float(),
            ),
            loader.ConfigValue(
                "animated_bio_frames",
                [],
                lambda: self.strings("animated_bio_frames"),
                validator=loader.validators.Series(
                    loader.validators.Union(loader.validators.String())
                ),
            ),
            loader.ConfigValue(
                "bio_delay",
                2.0,
                lambda: self.strings("bio_delay"),
                validator=loader.validators.Float(),
            ),
        )

    @loader.command(alias="aname", ru_doc="""(aname) Включить анимацию имени""")
    async def animatedname(self, message: Message):
        """(aname) Turn on name animation"""
        if not self.config["animated_name_frames"]:
            return await utils.answer(message, self.strings("not_name_frames"))
        if self.aname is False:
            self.aname = True
            await message.delete()
            while self.aname:
                for n in self.config["animated_name_frames"]:
                    await asyncio.sleep(self.config["name_delay"])
                    await self.client(
                        functions.account.UpdateProfileRequest(first_name=n)
                    )
        else:
            return await utils.answer(message, self.strings("name_is_enabled"))

    @loader.command(alias="abio", ru_doc="""(abio) Включить анимацию био""")
    async def animatedbio(self, message: Message):
        """(abio) Turn on bio animation"""
        if not self.config["animated_bio_frames"]:
            return await utils.answer(message, self.strings("not_bio_frames"))
        if self.abio is False:
            self.abio = True
            await message.delete()
            while self.abio:
                for n in self.config["animated_bio_frames"]:
                    await asyncio.sleep(self.config["bio_delay"])
                    await self.client(functions.account.UpdateProfileRequest(about=n))
        else:
            return await utils.answer(message, self.strings("bio_is_enabled"))

    @loader.command(
        alias="stopaname", ru_doc="""(stopaname) Выключить анимацию имени"""
    )
    async def stopanimatedname(self, message: Message):
        """(stopaname) Turn off name animation"""
        if self.aname is False:
            return await utils.answer(message, self.strings("name_is_disabled"))
        await utils.answer(message, self.strings("name_turned_off"))
        self.aname = False

    @loader.command(alias="stopabio", ru_doc="""(stopabio) Выключить анимацию био""")
    async def stopanimatedbio(self, message: Message):
        """(stopabio) Turn off bio animation"""
        if self.abio is False:
            return await utils.answer(message, self.strings("bio_is_disabled"))
        await utils.answer(message, self.strings("bio_turned_off"))
        self.abio = False
