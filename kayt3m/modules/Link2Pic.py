# Name: Link2Pic
# Description: Module for downloading images via link from any sources.
# Author: @nervousmods
# Commands:
# .l2p
# ---------------------------------------------------------------------------------
# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# ⚠️ All modules is not scam and absolutely safe.
# 👤 https://t.me/smlgwy
#-----------------------------------------------------------------------------------
# meta developer: @nervousmods, @hikka_mods
#scope: hikka_only 
#scope: hikka_min 1.6.0
#-----------------------------------------------------------------------------------

import logging
from hikka import loader, utils
import requests
import time

@loader.tds
class Link2Pic(loader.Module):
    """Module for downloading images via link from any sources"""
    strings={
        "name": "Link2Pic",
        "no_args": "Don't have any args!",
        "invalid": "Invalid args! Provide a valid image link",
        "download": "Downloading..",
    }

    strings_ru={
        "no_args": "Недостаточно аргументов!",
        "invalid": "Неверные аргументы! Укажи действующую ссылку на изображение",
        "download": "Скачиваю..",
    }

    @loader.command(ru_doc="-> скачать изображение по ссылке")
    async def l2pcmd(self, message):
        """-> to download image by url"""
        args=utils.get_args_raw(message)
        await utils.answer(message, self.strings("download"))
        time.sleep(1)
        await message.delete()
        response=requests.get(args)
        if response.status_code==200:
            with open('image.jpg', 'wb') as file:
                file.write(response.content)
                await utils.answer_file(message, "image.jpg")
        else:
            await utils.answer(message, self.strings('invalid'))
        
