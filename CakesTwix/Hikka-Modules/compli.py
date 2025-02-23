"""

    █▀▀ ▄▀█ █▄▀ █▀▀ █▀ ▀█▀ █░█░█ █ ▀▄▀
    █▄▄ █▀█ █░█ ██▄ ▄█ ░█░ ▀▄▀▄▀ █ █░█

    Copyleft 2022 t.me/CakesTwix                                                            
    This program is free software; you can redistribute it and/or modify 

"""

__version__ = (1, 0, 1)

# meta pic: https://www.freeiconspng.com/uploads/facebook-circle-heart-love-png-4.png
# meta developer: @cakestwix_mods

import logging
import asyncio
from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class CompliMod(loader.Module):
    """Send a compliment to a person"""

    strings = {
        "name": "Compliments",
        "cfg_emoji":"Emoji at the end of the message",
        "compliments_women":"умная хорошая милая добрая лучшая заботливая",
        "compliments_man":"умный хороший милый добрый лучший заботливый",
    }

    strings_ru = {
        "cfg_emoji":"Эмодзи в конце сообщения",
        "compliments_women":"умная хорошая милая добрая лучшая заботливая",
        "compliments_man":"умный хороший милый добрый лучший заботливый"
    }

    def __init__(self):
        self.name = self.strings["name"]
        self.config = loader.ModuleConfig(
            "emoji",
            "✨",
            lambda: self.strings("cfg_emoji"),
        )

        self.gender = "women"
        self.better = "Самая"
        self.delay = 2

    @loader.unrestricted
    @loader.ratelimit
    async def complicmd(self, message):
        """
        Send a person compliments
        .compli [delay] [man/women]
        """
        if args :=  len(utils.get_args(message)) == 2 and utils.get_args(message):
            try:
                self.delay = int(args[0])
            except:
                pass
            
            if "man" in args[1]:
                    self.gender = args[1]
                    self.better = "Самый"

        elif args := utils.get_args(message):
            try:
                self.delay = int(args[0])
            except:
                if "man" in args[0]:
                    self.gender = args[0]
                    self.better = "Самый"
                
        for compl in self.strings["compliments_" + self.gender].split():
            message = await utils.answer(message, f"{self.better} {compl} {self.config['emoji']}")
            await asyncio.sleep(self.delay)

        
